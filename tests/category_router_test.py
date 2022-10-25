import unittest
from unittest.mock import Mock

from common.responses import NotFound
from data.models import Category, Topic
from routers import categories
from routers.categories import categories_router

mock_category_service = Mock(spec='services.category_service')
mock_topic_service = Mock(spec='services.topic_service')
categories_router.category_service = mock_category_service
categories_router.topic_service = mock_topic_service


def fake_category(id=1, name='Problems', description='Something', is_private=1, is_locked=1):
    mock_category = Mock(spec=Category)
    mock_category.id = id
    mock_category.name = name
    mock_category.description = description
    mock_category.is_private = is_private
    is_locked.is_locked = is_locked
    return mock_category


def fake_topic(id=1, title='Test_topic', replies_ids=list, views=12, category_id=1, user_id=1, is_locked=1):
    if replies_ids is None:
        replies_ids = [1, 2, 3]
    mock_topic = Mock(spec=Topic)
    mock_topic.id = id
    mock_topic.name = title
    mock_topic.replies_ids = replies_ids
    mock_topic.views = views
    mock_topic.category_id = category_id
    mock_topic.user_id = user_id
    mock_topic.is_locked = is_locked

    return mock_topic


class CategoryRouter_Should(unittest.TestCase):

    def setup(self) -> None:
        mock_category_service.reset_mock()
        mock_topic_service.reset_mock()

