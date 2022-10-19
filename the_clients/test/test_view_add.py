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


from django.test.utils import override_settings    
@override_settings(   )
class TestView(TestCase):
    multi_db = True
    databases = {'default', }
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
    @classmethod
    def setUpTestData(cls):
        Group.objects.get_or_create(name=CUSTOMER_CARE_SUPERVISER)      
        Group.objects.get_or_create(name=TECH_SUPPORT)      
        Group.objects.get_or_create(name=CUSTOMER_CARE_REP)      


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------        
    def setUp(self):
        self.dummy_user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='rock') 

        self.add_url = reverse('the_clients:add')

        
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def tearDown(self):
        # Clean up run after every test method.
        pass
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_not_logged_in(self):
        response = self.client.get(self.add_url)

        self.assertRedirects(response, f"/accounts/login/?next={self.add_url}", fetch_redirect_response=False)

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_not_in_group(self):
        """
            user is not in the required group

        """
        self.client.login(username='john', password='rock')
        response = self.client.get(self.add_url)
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
        response = self.client.get(self.add_url)

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
        response = self.client.get(self.add_url)

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
        response = self.client.get(self.add_url)

        # print(response)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  
 
 

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_get_add_client_form(self):
        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 

        self.client.login(username='john', password='rock')
        response = self.client.get(self.add_url)

        self.assertEqual(response.status_code, HTTPStatus.OK) 
        # for key in response.context.keys():
        #     print(key," > ",  response.context[key], " >> ", type(response.context[key]))
 


        self.assertTemplateUsed(response, 'the_clients/add.html')
        self.assertEqual( response.context['add_form'].__class__.__name__, 'ClientForm')
        self.assertTrue( response.context['add_form'].fields['user'])
        self.assertTrue( response.context['add_form'].fields['active'])
 

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_post_add_client_form_with_invalid_user(self):

        initial_client_count = Client.objects.count()
        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 

        data = {"user": 3}    
        self.client.login(username='john', password='rock')
        response = self.client.post(self.add_url, data=data)
        
 
        
        self.assertFalse( response.context['add_form'].is_valid())


        self.assertEqual(response.status_code, HTTPStatus.OK) 
        new_client_count = Client.objects.count()
        self.assertEqual(new_client_count, initial_client_count)

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_post_add_client_form_with_valid_user(self):

        initial_client_count = Client.objects.count()
        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 

        data = {"user": self.dummy_user.id}    
        
        self.client.login(username='john', password='rock')
        response = self.client.post(self.add_url, data=data)
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND) 
        self.assertRedirects(response, f"{reverse('the_clients:list')}", fetch_redirect_response=True)
        
        new_client_count = Client.objects.count()
        self.assertEqual(new_client_count, initial_client_count+1)

        # 2nd add with same user
        response_again = self.client.post(self.add_url, data=data)        
        self.assertFalse( response_again.context['add_form'].is_valid())
        new_client_count_2 = Client.objects.count()
        self.assertEqual(new_client_count_2, initial_client_count+1)

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_default_value(self):

        initial_client_count = Client.objects.count()
        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 

        data = {"user": self.dummy_user.id}    
        
        self.client.login(username='john', password='rock')
        response = self.client.post(self.add_url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND) 

        new_client=  Client.objects.get(user=self.dummy_user)
        self.assertFalse(new_client.active)

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_active_true(self):

        initial_client_count = Client.objects.count()
        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 

        data = {"user": self.dummy_user.id, "active":True}    
        
        self.client.login(username='john', password='rock')
        response = self.client.post(self.add_url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND) 

        new_client=  Client.objects.get(user=self.dummy_user)
        self.assertTrue(new_client.active)


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_active_false(self):

        initial_client_count = Client.objects.count()
        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
 

        data = {"user": self.dummy_user.id, "active":False}    
        
        self.client.login(username='john', password='rock')
        response = self.client.post(self.add_url, data=data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK) 

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("created successfully" in message.message)


        new_client=  Client.objects.get(user=self.dummy_user)
        self.assertFalse(new_client.active)