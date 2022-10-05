from django.db import models
import binascii
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
 
import logging
logger = logging.getLogger('ilogger')
# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client', verbose_name=_("User"))
    active = models.BooleanField(default=True, verbose_name=_('Is client active?'), help_text="is this user active as a Client?")
    token = models.TextField(default="", blank=True, null=True)
    refresh_token = models.TextField(default="", blank=True, null=True)

    callback_url =   models.URLField( blank=True, null=True)
    callback_token = models.TextField(default="", blank=True, null=True)
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def __str__(self):
        return str(self.user)

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('the_clients:display', kwargs={'pk' : self.pk })
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    class Meta:
        ordering = ['user']

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def save(self, **kwargs):
        self.full_clean()
        if not self.token:
           self.get_new_drf_tokens() 
        super().save(**kwargs)

 

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------    
    def get_new_drf_tokens(self):
        token =  binascii.hexlify(os.urandom(40)).decode()
        self.token =str(token)

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------    
    @classmethod
    def is_client(cls, user):
        try:
            client = Client.objects.get(user=user)
            return True
        except Client.DoesNotExist:
            return False

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------    
    @staticmethod
    def get_client_by_token(token):
        try:
            return Client.objects.get(token=token)    
        except Client.DoesNotExist:
            return None