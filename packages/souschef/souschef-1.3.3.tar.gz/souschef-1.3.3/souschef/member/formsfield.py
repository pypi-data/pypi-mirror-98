import re
from django import forms
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from localflavor.ca.forms import CAPhoneNumberField


class CAPhoneNumberExtField(CAPhoneNumberField):
    """Canadian phone number form field."""
    phone_digits_re = re.compile(
            r'^(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4})$'
    )
    phone_digits_with_ext = re.compile(
            r'^(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4})#?(\d*)$'
        )

    default_error_messages = {
        'invalid':
        _('Phone numbers must be in XXX-XXX-XXXX # XXXXX format.'),
    }

    def clean(self, value):
        try:
            return super(CAPhoneNumberExtField, self).clean(value)
        except forms.ValidationError as error:
            value = re.sub('(\(|\)|\s+)', '', smart_text(value))
            m = self.phone_digits_with_ext.search(value)
            if m:
                return '%s-%s-%s #%s' % (m.group(1), m.group(2),
                                         m.group(3), m.group(4))
            raise error
