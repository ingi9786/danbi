import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

      
class NumericSpecialCharValidator:
    """
    Validate that the password is not entirely numeric.
    """

    def validate(self, password, user=None):
        regex = re.compile(r'(.*[a-z?=A-Z])(?=.*[0-9])(?=.*[\W\S_]).*')
        if re.match(regex, password) is None:
            raise ValidationError(
                _("It must contain at least one special and numeric character."),
                code="password_validate_error",
            )

    def get_help_text(self):
        return _("Password contain at least 'one special character' and 'one numeric character'!")