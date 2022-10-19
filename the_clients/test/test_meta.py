from django.utils import timezone
from django.core.exceptions import ValidationError

from http import HTTPStatus



from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User


from ..models import Client
 
from decimal import *

"""
If you do something with the database in AppConfig.ready(), 
then during test runs it runs against the production db as it happens before django knows it's testing.
I don't think there's any way to change this, but it should be documented.



https://docs.djangoproject.com/en/1.11/topics/testing/tools/#provided-test-case-classes
"""
 
from django.test.utils import override_settings    
@override_settings(   )
class Test001(TestCase):
        multi_db = True
        databases = {'default', }
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
            dummy_user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='rock')
            self.client = Client.objects.create(user=dummy_user)
             

        
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def tearDown(self):
            # Clean up run after every test method.
            pass
 
   
 
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_string_meta(self):
            self.client.set_meta("test1","hello")
            value = self.client.get_meta_value("test1")
            self.assertEquals(value,"hello")
            self.assertTrue(isinstance(value,str))

 
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_int_meta(self):
            self.client.set_meta("test_int",12)
            value = self.client.get_meta_value("test_int")
            self.assertEquals(value,12)
            self.assertTrue(isinstance(value,int))


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_int_meta2(self):
            self.client.set_meta("test_int","12")
            value = self.client.get_meta_value("test_int")
            self.assertNotEquals(value,12)
            self.assertFalse(isinstance(value,int))    

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_float_meta(self):
            self.client.set_meta("test_float",12.23)
            value = self.client.get_meta_value("test_float")
            self.assertAlmostEquals(value,Decimal(12.23))
            self.assertTrue(isinstance(value,Decimal))


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_int_meta_with_default(self):
            
            value = self.client.get_meta_value("test_int", 13)
            self.assertEquals(value,13)
            self.assertTrue(isinstance(value,int))

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_int_meta_with_default2(self):
            self.client.set_meta("test_int",12)

            value = self.client.get_meta_value("test_int", 13)
            self.assertEquals(value,12)
            self.assertTrue(isinstance(value,int))