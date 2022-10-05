from django.apps import apps
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.fields import Field


from inspect import ismethod




"""
If you do something with the database in AppConfig.ready(), 
then during test runs it runs against the production db as it happens before django knows it's testing.
I don't think there's any way to change this, but it should be documented.



https://docs.djangoproject.com/en/1.11/topics/testing/tools/#provided-test-case-classes
"""
 
from django.test.utils import override_settings    
@override_settings(   )
class TestModelMeta(TestCase):
        multi_db = True
        databases = {'default', 'pci'}
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
        @classmethod
        def setUpTestData(cls):
            pass      


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------        
        def setUp(self):
            self.app_name= self.__module__.split('.')[0]

        
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def tearDown(self):
            # Clean up run after every test method.
            pass
 
   
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_verbose_name_in_all_models(self):
         
            app_models = apps.get_app_config(self.app_name).get_models()
            for model in app_models:
                fields = model._meta.get_fields()
                for field in fields:
                    if isinstance(field,Field):
                        if field._verbose_name is None:
                            self.fail(msg=f"Verbose name not defined for {model.__name__}.{field.name}")

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_get_absolute_url_in_all_models(self):
         
            app_models = apps.get_app_config(self.app_name).get_models()
            for model in app_models:
                if not hasattr(model, 'get_absolute_url'):
                        self.fail(msg=f"get_absolute_url not defined for {model.__name__}")
