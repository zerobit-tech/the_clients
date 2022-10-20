 
import os
import binascii
from decimal import *
from random import choices

from django.db import models
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
            return True if client else False
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


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
    def _get_meta(self,key):
        try:
            return self.meta.get(key = str(key).upper())
        except ClientMeta.DoesNotExist:
            return None
    
    def _delete_meta(self,key):
        meta = self._get_meta(key)
        if meta:
            meta.delete()    


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
    def set_meta(self,key,value,description =None):
        if isinstance(value,int):
            self._set_int_meta(key,value)

        elif isinstance(value,float):
            self._set_decimal_meta(key,value)
            
        elif isinstance(value,Decimal):
            self._set_decimal_meta(key,float(value))


        elif isinstance(value,bool):
            self._set_boolean_meta(key,value)
        else:
            self._set_string_meta(key,str(value))


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
    def _set_string_meta(self,key,value,description =None):
        self._delete_meta(key)

        ClientMeta.objects.create(client=self, 
                    key =str(key).upper(),
                    string_value = value,
                    description = description,
                    )


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
    def _set_int_meta(self,key,value,description =None):
        self._delete_meta(key)

        int_value = int(value)


        ClientMeta.objects.create(client=self, 
                    key =str(key).upper(),
                    int_value = int_value,
                    description = description,
                    value_type= ClientMetaType.INTEGER
                    )
    
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
    def _set_decimal_meta(self,key,value,description =None):
        self._delete_meta(key)

        float_value = float(value)


        ClientMeta.objects.create(client=self, 
                    key =str(key).upper(),
                    decimal_value = float_value,
                    description = description,
                    value_type= ClientMetaType.DECIMAL
                    )
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
    def _set_boolean_meta(self,key,value,description =None):
        self._delete_meta(key)
        boolean_value = bool(value)
        ClientMeta.objects.create(client=self, 
                    key =str(key).upper(),
                    boolean_value = boolean_value,
                    description = description,
                    value_type= ClientMetaType.BOOLEAN
                    )


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
    def get_meta_value(self,key, default = None):
        meta = self._get_meta(key)
        return_value = None
        if meta:           
            if meta.value_type == str(ClientMetaType.DECIMAL):
                return_value= meta.decimal_value
            elif meta.value_type == str(ClientMetaType.BOOLEAN):
                return_value= meta.boolean_value                            
            elif meta.value_type == str(ClientMetaType.INTEGER):
                return_value= meta.int_value
            else:
                return_value= meta.string_value

        return default if return_value is None else return_value

#--------------------------------------------------------------
#
#--------------------------------------------------------------
class ClientMetaType(models.TextChoices):
        STRING = 'S', _('String')
        DECIMAL = 'D', _('Decimal')
        BOOLEAN = 'B', _('Boolean')
        INTEGER = 'I', _('Integer')

class ClientMeta(models.Model):
    client = models.ForeignKey(Client, on_delete = models.CASCADE,related_name="meta")
    key = models.CharField(max_length = 50)
    value_type = models.CharField(max_length = 1,choices=ClientMetaType.choices, default=ClientMetaType.STRING)
    description = models.TextField(null=True,blank = True)

    string_value = models.TextField(null=True,blank = True)
    decimal_value = models.DecimalField(max_digits=11, decimal_places=5,null=True,blank = True)
    boolean_value = models.BooleanField(null=True,blank = True)
    int_value = models.IntegerField(null=True,blank = True)

