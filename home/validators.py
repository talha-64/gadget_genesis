import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def __init__(self, regex=None, message=None):
        self.regex = regex or r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        self.message = message or _(
            "Password must be at least 8 characters long and include at least one uppercase letter, one digit, and one special character."
        )

    def validate(self, password, user=None):
        if not re.match(self.regex, password):
            raise ValidationError(self.message, code='password_no_match')

    def get_help_text(self):
        return self.message