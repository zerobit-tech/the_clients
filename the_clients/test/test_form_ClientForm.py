import datetime

from django.test import TestCase
from django.utils import timezone
from ..forms import ClientForm
from ..models import Client
from django.contrib.auth.models import User
from django.test.utils import override_settings    
@override_settings(   )
class TestClientForm(TestCase):
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
        self.dummy_user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='rock') 

        
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def tearDown(self):
        # Clean up run after every test method.
        pass

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_001(self):
        form = ClientForm()
        self.assertFalse(form.is_valid())

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_002(self):
        data={'user': "someuser", }
        form = ClientForm(data=data)
        self.assertFalse(form.is_valid())
         
        self.assertEqual(
            form.errors["user"], ["Select a valid choice. That choice is not one of the available choices."]
        )

        # self.assertTrue(form.fields["date"].disabled)
        # self.assertIn("due_date", form.fields)
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_003(self):
        data={'user': self.dummy_user, }
        form = ClientForm(data=data)
        self.assertTrue(form.is_valid())
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------         
    def test_004(self):
        data={'user': self.dummy_user, "active": False}
        form = ClientForm(data=data)
        self.assertTrue(form.is_valid())

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------         
    def test_005(self):
        data={'user': self.dummy_user, "active": False}
        form = ClientForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        try:
            client = Client.objects.get(user=self.dummy_user)
        except Client.DoesNotExist as e:
            self.fail(msg=str(e))

        self.assertFalse(client.active)
        
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------         
    def test_006(self):
        data={'user': self.dummy_user, "active": True}
        form = ClientForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        try:
            client = Client.objects.get(user=self.dummy_user)
        except Client.DoesNotExist as e:
            self.fail(msg=str(e))

        self.assertTrue(client.active)