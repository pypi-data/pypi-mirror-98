from django import forms
from django.utils.translation import gettext_lazy as _


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='File',
        label_suffix=':',
        help_text=_('PKCS7 file (e.g. eml, msg, p7m, txt)'),
        required=True,
    )
