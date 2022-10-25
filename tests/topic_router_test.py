import unittest
from unittest.mock import Mock
from data.models import Topic, Reply
from routers import topics as topics_router
from common.responses import NotFound

mock_topic_service = Mock(spec='services.topic_service')
mock_reply_service = Mock(spec='services.reply_service')

topics_router.topic_service = mock_topic_service
topics_router.reply_service = mock_reply_service

# def fake_topic()