from fastapi import APIRouter, Header
from common.responses import BadRequest, Forbidden, InternalServerError, NoContent, NotFound, Success, Unauthorized
from common.auth import get_user_or_raise_401
from data.models import Category, CategoryBody, Reply, ReplyBody, Topic, TopicBody, TopicResponse
from services import topic_service
from services import reply_service
from services import user_service
from services import category_service

topics_router = APIRouter(prefix='/topics')


@topics_router.get('/') 
def get_topics(sort: str | None = None, attribute:str | None = None, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    
    if not user.is_admin():
        return Forbidden('Not authorized')
    
    topics = topic_service.all()

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_service.sort(topics, attribute = attribute, reverse=sort == 'desc')
    
    else:
        return topics


@topics_router.get('/{id}')
def get_topic_by_id(id:int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    topic = topic_service.get_by_id(id)
    if not topic:
        return NotFound('Topic does not exist.')
    
    category = category_service.get_by_id_with_users(topic.category_id)

    if not user_service.has_access_to_category(user, category):
        return Forbidden('You do not have access to this topic.')
    
    replies = reply_service.all_in_topic(topic.id)

    replies_responses = [reply_service.create_response_object(reply, user_service.get_user_name_by_id(reply.user_id)) for reply in replies]

    topic_service.update_views(topic.id)
    return topic_service.create_response_object(topic, category.name, replies_responses)


@topics_router.post('/', response_model=TopicResponse)
def create_topic(category_body: CategoryBody, topic: Topic, reply: Reply, x_token: str = Header()): 
    user = get_user_or_raise_401(x_token)

    category = category_service.get_by_id_with_users(category_body.id)
    if not category:
        return NotFound(f'Category with id {category_body.id} does not exist.')
    
    if category.private() and not user_service.has_access_to_category(user, category):
        return Forbidden('You do not have access to this category.')

    if category.private() and user_service.has_readonly_access_to_category(user, category):
        return Forbidden('You do not have write access to this category, only read. You cannot create new topics.')

    topic = topic_service.create(topic, user, category)

    reply = reply_service.create(reply, topic.id, user)

    topic.activity = reply.created_on

    replies = reply_service.all_in_topic(topic.id)

    replies_responses = [reply_service.create_response_object(reply, user_service.get_user_name_by_id(reply.user_id)) for reply in replies]

    return topic_service.create_response_object(topic, category.name, replies_responses)


@topics_router.post('/{id}', response_model=TopicResponse)
def create_reply(id: int, reply: Reply, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    topic = topic_service.get_by_id(id)
    if not topic:
        return NotFound('Topic does not exist.')

    category = category_service.get_by_id_with_users(topic.category_id)

    if category.private() and not user_service.has_access_to_category(user, category):
        return Forbidden('You do not have access to this topic.')

    if category.private() and user_service.has_readonly_access_to_category(user, category):
        return Forbidden('You do not have write access to this topic, only read.')

    if topic.locked():
        return Forbidden('Topic is locked. You cannot reply in it.')

    reply = reply_service.create(reply, id, user)

    topic.activity = reply.created_on

    topic_replies = topic_service.get_topic_replies(topic.id)
    
    replies_responses = [reply_service.create_response_object(reply, user_service.get_user_name_by_id(reply.user_id)) for reply in topic_replies]

    return topic_service.create_response_object(topic, category.name, replies_responses)

@topics_router.put('/{id}')
def lock_topic(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = topic_service.get_by_id(id)
    
    if not user.is_admin():
        return Forbidden('You do not have permission to lock topic')
    
    if topic.locked():
        return BadRequest('The topic is already locked!')
    
    if topic_service.lock(topic):
        return Success(f'Topic with ID {topic.id} was successfully locked!')


@topics_router.delete('/{id}')
def delete_topic(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = topic_service.get_by_id(id)
    if topic is None:
        return NotFound()

    if not user.is_admin():
        return Forbidden('You do not have permission to delete topics')

    topic_service.delete(topic)

    return Success(f'Topic with id {id} successfully deleted!')


@topics_router.put('/{id}/replies/{reply_id}')
def update_reply(id: int, reply_id: int, reply_body: ReplyBody, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = topic_service.get_by_id(id)

    category = category_service.get_by_id_with_users(topic.category_id)

    if category.private() and not user_service.has_access_to_category(user, category):
        return Forbidden('You do not have access to this topic.')

    reply = reply_service.get_by_id(reply_id)
    reply_author_name = user_service.get_user_name_by_id(reply.user_id)
    
    if reply_body.upvote or reply_body.downvote:
        if reply_body.upvote:
            upvote = reply_service.upvote(reply, user)
            if not upvote:
                return Forbidden('You already upvoted this reply.')
        
        else:
            downvote = reply_service.downvote(reply, user)
            if not downvote:
                return Forbidden('You already downvoted this reply.')
        response_object = reply_service.create_response_object(reply, reply_author_name)

    if reply_body.is_best:
        if not user_service.owns_topic(user, topic):
            return Forbidden('You do not own this topic.')
        
        else:
            if not reply_service.choose_best(reply_id, topic):
                return Forbidden('Topic already has best reply.')
            
            else:
                reply_service.choose_best(reply.id, topic)
                reply.is_best = 1
        response_object = reply_service.create_response_object(reply, reply_author_name)

    if reply_body.text:
        if not user_service.owns_reply(user, reply):
            return Forbidden('You cannot edit this reply.')
            
        reply_service.edit_reply_text(reply_body.text, reply)

        reply.text = reply_body.text

        response_object = reply_service.create_response_object(reply, user.user_name)

    return response_object


@topics_router.delete('/{topic_id}/replies/{reply_id}')
def delete_reply(topic_id: int, reply_id:int, reply_body: ReplyBody, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = topic_service.get_by_id(topic_id)
    reply = reply_service.get_by_id(reply_id)

    if not topic:
        return NotFound('Topic does not exist.')

    if not reply:
        return NotFound('Reply does not exist.')

    if not user_service.owns_topic(user, topic):
        return Forbidden('You do not have access to this topic.')

    if not user_service.owns_reply(user, reply) or not user.is_admin():
        return Forbidden('You cannot delete this reply.')

    reply_service.delete(reply)

    return Success(f'Reply with id {reply_id} successfully deleted!')