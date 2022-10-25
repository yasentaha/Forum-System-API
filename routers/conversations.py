from fastapi import APIRouter, Header
from common.responses import BadRequest, Forbidden, InternalServerError, NoContent, NotFound, Unauthorized
from common.auth import get_user_or_raise_401
from data.models import Conversation, ConversationResponse, Message, MessageResponse, User, ConversationsResponse, UserName
from services import conversation_service
from services import message_service
from services import user_service

conversations_router = APIRouter(prefix='/conversations')

@conversations_router.post('/', response_model=ConversationResponse)
def create_conversation(user_name:UserName, conversation: Conversation, message: Message, x_token: str = Header()): 
    to_user = user_service.find_by_username(user_name.user_name)
    if not to_user:
        return NotFound('User does not exist')
    
    from_user = get_user_or_raise_401(x_token)
    
    created_conversation = conversation_service.create(conversation)
    conversation_service.insert_user_to_conversation(to_user.id, created_conversation.id)

    created_message = message_service.create(message, created_conversation.id, from_user)
    conversation_service.insert_user_to_conversation(from_user.id, created_conversation.id)

    messages = message_service.all_messages_in_conversation(created_conversation.id)

    return conversation_service.create_response_object(
        created_conversation, 
        messages)

@conversations_router.get('/{id}')
def get_conversation_by_id(id:int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    
    conversation = conversation_service.get_by_id(id)
    if user.id not in conversation.user_ids:
        return Unauthorized('Not authorized')
    
    if not conversation:
        return NotFound('Conversation does not exist')
    
    messages = message_service.all_messages_in_conversation(conversation.id)

    return conversation_service.create_response_object(
        conversation, 
        messages)

@conversations_router.get('/')
def get_all_conversations_for_user(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    
    conversations = conversation_service.get_user_conversations(user)
    
    if not conversations:
        return NotFound('User has no conversations.')

    return conversations

@conversations_router.post('/{id}', response_model=MessageResponse)
def create_message(id: int, message: Message, x_token: str = Header()): 
    user = get_user_or_raise_401(x_token)

    conversation = conversation_service.get_by_id(id)
    if user.id not in conversation.user_ids:
        return Unauthorized('Not authorized')
    
    message = message_service.create(message, id, user)

    return message_service.create_response_object(message, user)