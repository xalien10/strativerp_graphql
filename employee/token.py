from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from datetime import date


class ActivationToken(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp)
        )


Account_activation_token = ActivationToken()