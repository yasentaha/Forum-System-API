import unittest
from unittest import TestCase
from data.models import Category
from routers.categories import CategoryResponseModel
from services import category_service

fake_categories = lambda q: [(1, 'Problems', 'Something', 1, 1),
                             (2, 'Solutions', 'Something', 0, 1),
                             (3, 'OthersSolutions', 'Something special', 1, 0)]
fake_empty_categories = lambda q: []
fake_new_category = Category(id=1,name='Problems', description='Something', is_private=1, is_locked=1)
fake_new_category_without_id = Category(name='Problems', description='Something', is_private=1, is_locked=1)


class CategoryService_Should(unittest.TestCase):

    def test_create_with_created_id(self):
        id = 1
        insert_data = lambda q, cat: id
        result = category_service.create(fake_new_category_without_id, insert_data)
        expected = fake_new_category
        self.assertEqual(expected, result)

    def test_all_function(self):
        result = list(category_service.all(fake_categories))
        self.assertEqual(3, len(result))

    def test_all_function_with_no_data(self):
        result = list(category_service.all(fake_empty_categories))
        self.assertEqual([], result)

    def test_get_category_by_id(self):
        id=1
        insert_data = lambda q, cat: id
        result = category_service.create(fake_new_category_without_id,insert_data)
        expected = fake_new_category
        self.assertEqual(expected, result)

    def test_exist_function_return_True_with_data(self):
        get_data = lambda q, id: [(1, 'Problems', 'neshto si',1, 1)]
        result = category_service.exists(1, get_data)
        self.assertEqual(True, result)

    def test_exist_function_returt_False_with_no_data(self):
        get_data = lambda q, id: []
        result = category_service.exists(1, get_data)
        self.assertEqual(False, result)
