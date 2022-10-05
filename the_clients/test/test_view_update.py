import datetime
from http import HTTPStatus

from django.urls import reverse
from django.contrib.auth.models import Group

from django.test import TestCase
from django.utils import timezone
from ..forms import ClientForm
from ..models import Client
from django.contrib.auth.models import User
from the_user.initial_groups import CUSTOMER_CARE_SUPERVISER, CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER,TECH_SUPPORT
from django.core.paginator import Page 

from the_system.settings import get_page_size
from django.forms.fields import BooleanField

from django.test.utils import override_settings    
@override_settings(   )
class TestView(TestCase):
    multi_db = True
    databases = {'default', 'pci'}
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
    @classmethod
    def setUpTestData(cls):
        Group.objects.get_or_create(name=CUSTOMER_CARE_SUPERVISER)      
        Group.objects.get_or_create(name=TECH_SUPPORT)      
        Group.objects.get_or_create(name=CUSTOMER_CARE_REP)  
        dummy_user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='rock')    
        Client.objects.create(user=dummy_user)
 


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------        
    def setUp(self):
        self.dummy_client= Client.objects.get(user__username="john")
        self.dummy_user = self.dummy_client.user
        self.url = reverse('the_clients:update',kwargs={'pk':self.dummy_client.id})

        
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def tearDown(self):
        # Clean up run after every test method.
        pass

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_absolute_url(self):
        self.assertEquals(self.url, self.dummy_client.get_absolute_url())
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_not_logged_in(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"/accounts/login/?next={self.url}", fetch_redirect_response=False)

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_not_in_group(self):
        """
            user is not in the required group

        """
        self.client.login(username='john', password='rock')
        response = self.client.get(self.url)
        # print(response)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN) # user is not in the group
 
        # self.assertTrue('is_paginated' in response.context)
        # self.assertTrue(response.context['is_paginated'] == True)
        # self.assertEqual(len(response.context['author_list']), 10)

        # self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')
        # self.assertTemplateUsed(response, 'catalog/bookinstance_list_borrowed_user.html')
        # self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal in past')


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_not_staff(self):
        """
            user is in the group but use is not STAFF
        """

        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)
        # for grp in self.dummy_user.groups.all():
        #     print(" >>>>. grp ", grp)

        self.client.login(username='john', password='rock')
        response = self.client.get(self.url)

        # print(response)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  

 


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_in_higher_weightage_group(self):
        """
            user is in the HIGHER weightage group AND is   STAFF
        """

        my_group = Group.objects.get(name=TECH_SUPPORT) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 

        self.client.login(username='john', password='rock')
        response = self.client.get(self.url)

        # print(response)
        self.assertEqual(response.status_code, HTTPStatus.OK)  

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_in_lower_weightage_group(self):
        """
            user is in the LOWER WEIGHTAGE group AND is   STAFF
        """

        my_group = Group.objects.get(name=CUSTOMER_CARE_REP) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 

        self.client.login(username='john', password='rock')
        response = self.client.get(self.url)

        # print(response)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  
 
 

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_get_update_client_form(self):
        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 

        self.client.login(username='john', password='rock')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK) 
        # for key in response.context.keys():
        #     print(key," > ",  response.context[key], " >> ", type(response.context[key]))
 


        self.assertTemplateUsed(response, 'the_clients/update.html')
        self.assertEqual( response.context['form'].__class__.__name__, 'ClientUpdateForm')
        self.assertEqual( response.context['client_to_update'].id, self.dummy_client.id)
        self.assertEquals( response.context['form']['active'].value(),self.dummy_client.active)
        with self.assertRaises(KeyError):
             response.context['form'].fields['user']

        
 

 
 
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_post_add_client_form_with_invalid_user(self):

        initial_client_count = Client.objects.count()
        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 
        initial_active = self.dummy_client.active
        data = {"user": 3}    # user values must be ignored as its not a form field
        self.client.login(username='john', password='rock')
        response = self.client.post(self.url, data=data, follow=True)

        self.assertRedirects(response, f"{reverse('the_clients:list')}", fetch_redirect_response=True)
        self.assertEqual(response.status_code, HTTPStatus.OK) 

        # print("================================")
        # for key in response.context.keys():
        #   print(key," > ",  response.context[key], " >> ", type(response.context[key]))      
        # print("================================")
 
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("updated successfully" in message.message)

        new_client_count = Client.objects.count()
        self.assertEqual(new_client_count, initial_client_count)
        self.assertEquals(initial_active,self.dummy_client.active)
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_post_add_client_form_with_invalid_user_status_change(self):

        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 
        data = {"user": 3, "active":False}    # user values must be ignored as its not a form field
        self.client.login(username='john', password='rock')
        response = self.client.post(self.url, data=data, follow=True)

        self.assertRedirects(response, f"{reverse('the_clients:list')}", fetch_redirect_response=True)
        self.assertEqual(response.status_code, HTTPStatus.OK) 

        # print("================================")
        # for key in response.context.keys():
        #   print(key," > ",  response.context[key], " >> ", type(response.context[key]))      
        # print("================================")
 
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("updated successfully" in message.message)
        new_client = Client.objects.get(user__username="john")
        self.assertFalse(new_client.active)

   