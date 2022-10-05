from django import forms

from django_otp.forms import OTPAuthenticationFormMixin
from .models import Client
import logging
logger = logging.getLogger('ilogger')

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["user", "active"]


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["active","token"]