from django.utils import timezone
from django.core.exceptions import ValidationError

from http import HTTPStatus



from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User


from ..models import Client
 

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
            #print("setUp: Run once for every test method to setup clean data.")
            pass

        
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def tearDown(self):
            # Clean up run after every test method.
            pass
 
   
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_user_is_not_client(self):
            dummy_user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='rock')
            with self.assertRaises(Client.DoesNotExist):
                Client.objects.get(user=dummy_user)

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_user_is_client(self):
            dummy_user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='rock')
            Client.objects.create(user=dummy_user)
            try:
               c1= Client.objects.get(user=dummy_user)

            except Exception as e:
                self.fail(msg=f"{dummy_user} is not a client")

            self.assertTrue(c1.active)

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_get_absolute_url(self):
            dummy_user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='rock')
            Client.objects.create(user=dummy_user)
            try:
               c1= Client.objects.get(user=dummy_user)

            except Exception as e:
                self.fail(msg=f"{dummy_user} is not a client")

            try:
               c1.get_absolute_url()
            except Exception as e:
                self.fail(msg=str(e))       

            # confirm that absolute URL is reachable
            #most testing under test_views
            response = self.client.get(c1.get_absolute_url())
            self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND) 