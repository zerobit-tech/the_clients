# from django.utils import timezone
# from django.core.exceptions import ValidationError
# from rest_framework.test import APIRequestFactory

# from django.urls import include, path, reverse
# from rest_framework import status
# from rest_framework.test import APITestCase,URLPatternsTestCase


# from django.test import TestCase, TransactionTestCase
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken,OutstandingToken


# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


# from ..models import Client
 

# """
# If you do something with the database in AppConfig.ready(), 
# then during test runs it runs against the production db as it happens before django knows it's testing.
# I don't think there's any way to change this, but it should be documented.



# https://docs.djangoproject.com/en/1.11/topics/testing/tools/#provided-test-case-classes

# https://www.django-rest-framework.org/api-guide/testing/

# https://docs.djangoproject.com/en/4.0/topics/testing/tools/#the-test-client
# """
 
# from django.test.utils import override_settings    
# @override_settings(   )
# class Test001(APITestCase,URLPatternsTestCase):
#         multi_db = True
#         databases = {'default', }

#         urlpatterns = [
#             path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#             path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#             path("api/", include('the_system.urls_api')),

#         ]
#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------   
#         @classmethod
#         def setUpTestData(cls):
#             pass      


#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------        
#         def setUp(self):
#             self.dummy_user = User.objects.create_user(username='john',
#                                             email='jlennon@beatles.com',
#                                             password='rock')             

        
#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------
#         def tearDown(self):
#             # Clean up run after every test method.
#             pass
 
            
#     #--------------------------------------------------------------
#     # HTTP GET NOT ALLOWED
#     #--------------------------------------------------------------
#         def test_http_get_not_allowed(self):
#             url = reverse('token_obtain_pair')


#             response = self.client.get(url,{"username": "john", "password": "rock"}, format='json')
#             self.assertGreaterEqual(response.status_code,400)

#     #--------------------------------------------------------------
#     # if user is not register as client, it should be able to get the token
#     #--------------------------------------------------------------
#         def test_user_can_not_get_api_token(self):
#             url = reverse('token_obtain_pair')

 
#             response = self.client.post(url,{"username": "john", "password": "rock"}, format='json')
#             with self.assertRaises(KeyError):
#                 response.data['access']

#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------
#         def test_client_wrong_password(self):
#             url = reverse('token_obtain_pair')

#             Client.objects.create(user=self.dummy_user)
#             response = self.client.post(url,{"username": "john", "password": "wrongpass"}, format='json')
#             self.assertEqual(response.status_code, 401)

#             #self.assertIn('no_active_account',response.data['detail'])
        
#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------
#         def test_client_can_get_api_token(self):
#             url = reverse('token_obtain_pair')

#             Client.objects.create(user=self.dummy_user)
#             response = self.client.post(url,{"username": "john", "password": "rock"}, format='json')
#             self.assertTrue(response.data['access'])
#             self.assertTrue(response.data['refresh'])

    
#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------
#         def test_auth_with_token(self):
#             url = reverse('token_obtain_pair')
#             Client.objects.create(user=self.dummy_user)
#             response = self.client.post(url,{"username": "john", "password": "rock"}, format='json')

#             access = response.data['access']
#             self.check_health(access=access)

                            
#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------
#         def test_auth_with_wrong_token(self):
#             url = reverse('token_obtain_pair')
#             Client.objects.create(user=self.dummy_user)
#             response = self.client.post(url,{"username": "john", "password": "rock"}, format='json')

#             access = response.data['access']+"dummy_Data"
#             health_url = reverse('the_system_api:health')
#             self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access)
#             health_response = self.client.get(health_url,format='json')
#             self.assertEqual(health_response.status_code, 401)         
#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------
#         def test_expired_token(self): 
#             pass               

#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------
#         def test_refresh_token(self): 
#             url = reverse('token_obtain_pair')
#             Client.objects.create(user=self.dummy_user)
#             response = self.client.post(url,{"username": "john", "password": "rock"}, format='json')
#             refresh = response.data['refresh']
#             self.assertTrue(response.data['refresh'])

#             refresh_url = reverse('token_refresh')
#             refresh_response = self.client.post(refresh_url,{"refresh": refresh}, format='json')
#             new_access = refresh_response.data['access']
#             self.check_health(access=new_access)

#             # print(" ++++++++++ checking black list++++++++++++++")
#             # for obj in OutstandingToken.objects.all():
#             #     print("=======OutstandingToken=++++++++++++++++++++",str(obj), obj.token)
#             # for obj in BlacklistedToken.objects.all():
#             #     print("========+BlacklistedToken+++++++++++++++++++",str(obj), obj.token)

#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------
#         def check_health(self,access):
#             health_url = reverse('the_system_api:health')
#             self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access)
#             health_response = self.client.get(health_url,format='json')
#             self.assertEqual(health_response.status_code, 200)
#             self.assertTrue(health_response.data["healthy"])
     

#     #--------------------------------------------------------------
#     #
#     #--------------------------------------------------------------
#         def test_blocked_token(self): 
#             pass    