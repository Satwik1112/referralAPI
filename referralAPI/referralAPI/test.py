from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, LoginHistory


class AccountTests(APITestCase):
    def test_create_account_new(self):
        """
        Ensure we can create a new user object.
        """
        url = '/user-registration/'
        data = {
            "name": "satwik",
            "password": "satwik",
            "email": "satyam@d.com",
            "referral_code": "xyz"
        }
        expected_data = {
            "token": "",
            "userID": "",
            "status": "Successfully generated data"
        }
        response = self.client.post(url, data)
        expected_data["token"] = response.data["token"]
        expected_data["userID"] = response.data["userID"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)


    def test_get_account(self):
        """
        Ensure exits users data only, given to authorised users.
        """
        url = '/users/'
        data = {
            "name": "satwik",
            "password": "satwik",
            "email": "satyam@d.com",
            "referral_code": "xyz"
        }
        expected_data = {
            'userID': '',
            'name': 'satwik',
            'email': 'satyam@d.com',
            'referrer_score': 1,
            'timestamp': ''
        }
        user_data = User(name=data["name"], email=data["email"], password="password",
                         referral_code=data["referral_code"], referral_score=1)
        user_data.save()
        user_auth_data = LoginHistory(user=user_data)
        user_auth_data.save()
        headers = {"token": user_auth_data.token}
        response = self.client.get(url, headers=headers)
        expected_data["userID"] = response.data.get("userID")
        expected_data["timestamp"] = response.data.get("timestamp")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_referral_account(self):
        """
        Ensure users data who has referral only, given to authorised users.
        """
        url = '/users-referral-data/'
        data = {
            "name": "satwik",
            "password": "satwik",
            "email": "satwik@d.com",
            "referral_code": "xyz"
        }
        data1 = {
            "name": "satyam",
            "password": "satyam",
            "email": "satyam@d.com",
        }
        expected_data = [{
            'userID': '',
            'name': 'satwik',
            'email': 'satwik@d.com',
            'referrer_score': 1,
            'timestamp': ''
        }]
        user_data = User(name=data["name"], email=data["email"], password="password",
                         referral_code=data["referral_code"], referral_score=1)
        user_data.save()
        user_data = User(name=data1["name"], email=data1["email"], password="password")
        user_data.save()
        user_auth_data = LoginHistory(user=user_data)
        user_auth_data.save()
        headers = {"token": user_auth_data.token}
        response = self.client.get(url, headers=headers)
        expected_data[0]["userID"] = response.data[0].get("userID")
        expected_data[0]["timestamp"] = response.data[0].get("timestamp")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
