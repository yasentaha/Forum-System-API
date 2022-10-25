import unittest
from unittest.mock import Mock, create_autospec, patch
from data.models import User
from services import user_service
from datetime import date

class UserService_Should(unittest.TestCase):

    #Find By Username
    def test_findByUsername_returns_singleUser_when_dataIsPresent(self):
        #Arrange:
        registered_on = date(2022,2,10)
        get_data_func = lambda q, user_name: [(1, 'yasen_taha', 'fhgjfghkfhdfhdskjhfsdhf', 'regular', registered_on, 'yasen@gmail.com')]
        expected = User(id=1, user_name='yasen_taha', password='fhgjfghkfhdfhdskjhfsdhf', role='regular', registered_on=registered_on, email='yasen@gmail.com')
        
        #Act:
        result = user_service.find_by_username(1, get_data_func)

        #Assert:
        self.assertEqual(expected, result)

    def test_findByUsername_returns_None_when_noDataIsPresent(self):
        #Arrange:
        get_data_func = lambda q, user_name: []
        expected = None
        
        #Act:
        result = user_service.find_by_username(1, get_data_func)

        #Assert:
        self.assertEqual(expected, result)

    #Valid Email
    def test_validEmail_returns_Email_when_valid(self):
        #Arrange:
        email = 'yasen@gmail.com'
        expected = email

        #Act:
        result = user_service.valid_email(email)

        #Assert:
        self.assertEqual(expected, result)

    def test_validEmail_returns_None_when_invalidEmailExtension(self):
        #Arrange:
        email = 'yasen@gmail'
        expected = None

        #Act:
        result = user_service.valid_email(email)

        #Assert:
        self.assertEqual(expected, result)

    def test_validEmail_returns_None_when_invalidEmail_NoAtMail(self):
        #Arrange:
        email = 'yasengmail.com'
        expected = None

        #Act:
        result = user_service.valid_email(email)

        #Assert:
        self.assertEqual(expected, result)

    #Create User
    def test_create_returns_userWithGeneratedId(self):
        raise NotImplementedError
        # generated_id = 2
        # insert_data_func = lambda q, user: generated_id
        # result = user_service.create('yasen_taha', 'fhgjfghkfhdfhdskjhfsdhf', 'yasen@gmail.com', insert_data_func)
        # expected = 
    

