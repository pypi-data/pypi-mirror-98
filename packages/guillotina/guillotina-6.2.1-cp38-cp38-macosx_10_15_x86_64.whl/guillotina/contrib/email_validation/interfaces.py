from guillotina import schema
from zope.interface import Interface


class IValidationSettings(Interface):

    site_url = schema.Text(
        title="Public frontend site url",
        description="Full url without tailing /",
        missing_value="http://localhost:4200",
    )

    validation_template = schema.Text(
        title="Validation template",
        description="Template id or path to object",
        missing_value="validate.html",
    )

    validation_url = schema.Text(
        title="Validation frontend tail url",
        description="Tail url starting with /",
        missing_value="/@@validation",
    )

    site_mails_from = schema.Text(
        title="Site mails from", description="Orig email to send mails", missing_value="noreply@test.org"
    )
