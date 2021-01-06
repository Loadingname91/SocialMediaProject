import re
from django.conf import settings
from rest_framework import serializers


def Email_domain_validator(email):
    """
    Checks whether the domain of the user's email is under the required domains.

    Input parameters : Email (string)

    Output parameters : Email or Validation Error

    """

    domain = re.search('@*?\.', email)
    if domain not in settings.EMAILS_ALLOWED:
        raise serializers.ValidationError("Invalid domain , please retry with common email providers like google")
    return email
