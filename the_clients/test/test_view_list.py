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
    databases = {'default', 'pci'}
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
        response = self.client.get(reverse('the_clients:list'))

        self.assertRedirects(response, f"/accounts/login/?next={reverse('the_clients:list')}", fetch_redirect_response=False)

        # self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_not_in_group(self):
        """
            user is not in the required group

        """
        self.client.login(username='john', password='rock')
        response = self.client.get(reverse('the_clients:list'))
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
        response = self.client.get(reverse('the_clients:list'))

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
        response = self.client.get(reverse('the_clients:list'))

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
        response = self.client.get(reverse('the_clients:list'))

        # print(response)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_in_group_and_staff_without_client_data(self):
        """
            user is in the group AND is STAFF
        """

        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()
      

        self.client.login(username='john', password='rock')
        response = self.client.get(reverse('the_clients:list'))

        self.assertEqual(response.status_code, HTTPStatus.OK) 
        # for key in response.context.keys():
        #     print(key," > ",  response.context[key], " >> ", type(response.context[key]))
        self.assertTrue('paginator' in response.context)
        self.assertTrue('clients' in response.context)
        self.assertTrue('page' in response.context)
        self.assertEqual(response.context['page'], 1)
        self.assertEqual(response.context['paginator'].paginator.per_page, get_page_size())
        self.assertEqual(response.context['clients'].paginator.per_page, get_page_size())
        # currently no client in db
        self.assertEqual(len(response.context['clients']), 0)


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    def test_user_is_in_group_and_staff_with_client_data(self):
        """
            user is in the group AND is STAFF
        """

        my_group = Group.objects.get(name=CUSTOMER_CARE_SUPERVISER) 
        my_group.user_set.add(self.dummy_user)

        self.dummy_user.is_staff = True
        self.dummy_user.save()

        # create one client in db
        Client.objects.create(user=self.dummy_user)

        self.client.login(username='john', password='rock')
        response = self.client.get(reverse('the_clients:list'))

        self.assertEqual(response.status_code, HTTPStatus.OK) 
        # for key in response.context.keys():
        #     print(key," > ",  response.context[key], " >> ", type(response.context[key]))
        self.assertTrue('paginator' in response.context)
        self.assertTrue('clients' in response.context)
        self.assertTrue('page' in response.context)
        self.assertEqual(response.context['page'], 1)
        self.assertEqual(response.context['paginator'].paginator.per_page, get_page_size())
        self.assertEqual(response.context['clients'].paginator.per_page, get_page_size())
        # currently 1 client in db
        self.assertEqual(len(response.context['clients']), 1)

        self.assertTrue(response.context['clients'].object_list)
        self.assertEqual(response.context['clients'].object_list[0].user.id,self.dummy_user.id )


        self.assertTemplateUsed(response, 'the_clients/list.html')