from fnmatch import fnmatch
from guillotina import logger
from guillotina import profile
from guillotina._settings import app_settings
from guillotina.factory import make_app
from guillotina.utils import get_dotted_name
from guillotina.utils import resolve_dotted_name

import argparse
import asyncio
import cProfile
import json
import os
import signal
import sys
import yaml


try:
    import uvloop  # type: ignore

    uvloop.install()
except ImportError:
    pass

try:
    import line_profiler  # type: ignore

    HAS_LINE_PROFILER = True
except ImportError:
    HAS_LINE_PROFILER = False

try:
    import aiomonitor  # type: ignore

    HAS_AIOMONITOR = True
except ImportError:
    HAS_AIOMONITOR = False


MISSING_SETTINGS = {
    "databases": [{"db": {"storage": "DUMMY_FILE"}}],
    "jsapps": {"+admin": "guillotina:static/executioner"},
    "port": 8080,
    "root_user": {"password": "root"},
}


def get_settings(configuration, overrides=None):
    if configuration == "config.yaml" and not os.path.exists(configuration):
        # try config.json as well...
        configuration = "config.json"
    if os.path.exists(configuration):
        with open(configuration, "r") as config:
            if configuration.lower().endswith(".json"):
                try:
                    settings = json.load(config)
                except json.decoder.JSONDecodeError:
                    logger.warning("Could not parse json configuration {}".format(configuration))
                    raise
            else:
                # should be yaml then...
                settings = yaml.load(config, Loader=yaml.FullLoader)
        settings["__file__"] = configuration
    else:
        try:
            settings = json.loads(configuration)
        except json.decoder.JSONDecodeError:
            # try with yaml parser too..
            try:
                settings = yaml.load(configuration, Loader=yaml.FullLoader)
                # will also parse strings...
                if isinstance(settings, str):
                    settings = None
            except yaml.parser.ParserError:
                settings = None

    if settings is None or settings == configuration:
        if "logged" not in MISSING_SETTINGS:
            logger.warning(f"No configuration file found. Using default settings with DUMMY_FILE db.")
        MISSING_SETTINGS["logged"] = True
        settings = MISSING_SETTINGS.copy()

    for override in overrides or []:
        if "=" not in override:
            raise Exception(f"Invalid configuration {override}")
        name, _, value = override.partition("=")
        context = settings
        parts = name.split(".")
        for part in parts[:-1]:
            if part not in context:
                context[part] = {}
            context = context[part]
        context[parts[-1]] = value

    for env_name in os.environ.keys():
        orig_env_name = env_name
        env_name = env_name.lower()
        if not env_name.startswith("g_"):
            continue
        name = env_name[2:]
        value = os.environ[orig_env_name]
        if len(value) > 0 and value[0] in ("{", "["):
            value = json.loads(value)
        context = settings
        parts = name.split("__")
        for part in parts[:-1]:
            if part not in context:
                context[part] = {}
            context = context[part]
        context[parts[-1]] = value

    return settings


class Command(object):

    profiler = line_profiler = None
    description = ""
    hide = False
    loop = None

    def __init__(self, arguments=None):
        """
        Split out into parts that can be overridden
        """
        if arguments is None:
            self.parse_arguments()
        else:
            self.arguments = arguments

    def parse_arguments(self):
        parser = self.get_parser()
        self.arguments = parser.parse_known_args()[0]

    def run_command(self, settings=None, loop=None):
        if loop is not None:
            self.loop = loop
        if settings is None:
            settings = get_settings(self.arguments.configuration, self.arguments.override)
        if settings.get("loop_policy"):
            loop_policy = resolve_dotted_name(settings["loop_policy"])
            asyncio.set_event_loop_policy(loop_policy())

        app = self.make_app(settings)

        if self.arguments.line_profiler:
            if not HAS_LINE_PROFILER:
                sys.stderr.write(
                    "You must first install line_profiler for the --line-profiler option to work.\n"
                    "Use `pip install line_profiler` to install line_profiler.\n"
                )
                return 1
            self.line_profiler = line_profiler.LineProfiler()
            for func in profile.get_profilable_functions():
                if fnmatch(get_dotted_name(func), self.arguments.line_profiler_matcher or "*"):
                    self.line_profiler.add_function(func)
            self.line_profiler.enable_by_count()

        run_func = self.__run
        if self.arguments.monitor:
            if not HAS_AIOMONITOR:
                sys.stderr.write(
                    "You must install aiomonitor for the "
                    "--monitor option to work.\n"
                    "Use `pip install aiomonitor` to install aiomonitor.\n"
                )
                return 1
            run_func = self.__run_with_monitor

        if self.arguments.profile:
            self.profiler = cProfile.Profile()
            self.profiler.runcall(run_func, app, settings)
        else:
            run_func(app, settings)

    def __run_with_monitor(self, app, settings):
        loop = self.get_loop()
        with aiomonitor.start_monitor(loop=loop):
            self.__run(app, settings)

    def __run(self, app, settings):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(app.startup())
        if asyncio.iscoroutinefunction(self.run):
            # Blocking call which returns when finished
            loop.run_until_complete(self.run(self.arguments, settings, app))
        else:
            self.run(self.arguments, settings, app.app)
        loop.run_until_complete(self.cleanup(app))
        loop.close()

        if self.profiler is not None:
            if self.arguments.profile_output:
                self.profiler.dump_stats(self.arguments.profile_output)
            else:
                # dump to screen
                self.profiler.print_stats(-1)
        if self.line_profiler is not None:
            self.line_profiler.disable_by_count()
            if self.arguments.line_profiler_output:
                self.line_profiler.dump_stats(self.arguments.line_profiler_output)
            else:
                self.line_profiler.print_stats()

    async def cleanup(self, app):
        try:
            await app.shutdown()
        except Exception:
            logger.warning("Unhandled error cleanup tasks", exc_info=True)
        for task in asyncio.Task.all_tasks():
            if task.done():
                continue
            if "cleanup" in task._coro.__qualname__:
                continue
            try:
                logger.info(f"Waiting for {task._coro.__qualname__} to finish")
                try:
                    await asyncio.wait_for(asyncio.shield(task), 1)
                except asyncio.TimeoutError:
                    logger.warning(f"Timeout for {task._coro.__qualname__}")
            except (AttributeError, KeyError):
                pass

    def get_loop(self):
        if self.loop is None:
            try:
                self.loop = asyncio.get_event_loop()
            except RuntimeError:
                # attempt to recover by making new loop
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
        if self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        return self.loop

    def signal_handler(self, signal, frame):
        sys.exit(0)

    def make_app(self, settings):
        signal.signal(signal.SIGINT, self.signal_handler)
        loop = self.get_loop()
        return make_app(settings=settings, loop=loop)

    def get_parser(self):
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument("-c", "--configuration", default="config.yaml", help="Configuration file")
        parser.add_argument("--debug", dest="debug", action="store_true", help="Log verbose")
        parser.add_argument(
            "-m", "--monitor", action="store_true", dest="monitor", help="Monitor", default=False
        )
        parser.add_argument(
            "--profile", action="store_true", dest="profile", help="Profile execution", default=False
        )
        parser.add_argument(
            "--profile-output", help="Where to store the output of the profile data", default=None
        )
        parser.add_argument(
            "--line-profiler",
            action="store_true",
            dest="line_profiler",
            help="Line profiler execution",
            default=False,
        )
        parser.add_argument("--line-profiler-matcher", help="Line profiler execution", default=None)
        parser.add_argument(
            "--line-profiler-output", help="Where to store the output of the line profiler data", default=None
        )
        parser.add_argument("--override", action="append", help="Override configuration values")
        parser.set_defaults(debug=False)
        return parser

    def __repr__(self):
        """
        to prevent command line from printing object...
        """
        return ""


def load_commands(module_name, commands):
    module = resolve_dotted_name(module_name)
    if hasattr(module, "app_settings") and app_settings != module.app_settings:
        commands.update(module.app_settings.get("commands", {}))
        for dependency in module.app_settings.get("applications") or []:
            load_commands(dependency, commands)


def command_runner():
    parser = argparse.ArgumentParser(description="Guillotina command runner", add_help=False)
    parser.add_argument("command", nargs="?")
    parser.add_argument("-c", "--configuration", default="config.yaml", help="Configuration file")
    parser.add_argument("-h", "--help", action="store_true", dest="help", help="Help", default=False)

    arguments, _ = parser.parse_known_args()
    settings = get_settings(arguments.configuration)
    _commands = app_settings["commands"].copy()
    _commands.update(settings.get("commands", {}))
    for module_name in settings.get("applications", []):
        load_commands(module_name, _commands)

    if not arguments.command and arguments.help:
        # for other commands, pass through and allow those parsers to print help
        parser.print_help()
        return print(
            """
Available commands:
{}\n\n""".format(
                "\n  - ".join(c for c in _commands.keys())
            )
        )

    if not arguments.command:
        # default to serve command
        arguments.command = "serve"

    if arguments.command not in _commands:
        return print(
            """Invalid command "{}".

Available commands:
{}\n\n""".format(
                arguments.command, "\n  - ".join(c for c in _commands.keys())
            )
        )

    app_settings["_command"] = arguments.command
    Command = resolve_dotted_name(_commands[arguments.command])
    if Command is None:
        return print(
            "Could not resolve command {}:{}".format(arguments.command, _commands[arguments.command])
        )

    app_settings["__run_command__"] = arguments.command
    # finally, run it...
    command = Command()
    command.run_command()
