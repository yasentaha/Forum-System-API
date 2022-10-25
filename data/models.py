from datetime import date, datetime
from pydantic import BaseModel, constr

class Category(BaseModel):
    id: int | None
    name: str
    description: str | None
    is_private: int
    is_locked: int | None
    users_ids: list[int] = []

    def locked(self):
        return self.is_locked == 1
    
    def private(self):
        return self.is_private == 1

class Topic(BaseModel):
    id: int | None
    title: str
    replies_ids: list[int] = []
    views: int | None
    category_id: int | None
    user_id: int | None 
    activity: datetime | None
    is_locked: int | None
    
    def locked(self):
        return self.is_locked == 1

    @classmethod
    def from_query_result(cls, id, title, views=None, activity=None, is_locked=None, user_id=None, category_id=None, replies_ids=[]):
        return cls(
            id=id,
            title=title,
            views=views,
            activity=activity,
            is_locked=is_locked,
            user_id=user_id,
            category_id=category_id,
            replies_ids=replies_ids)

class Reply(BaseModel):
    id: int | None
    text: str  
    created_on: datetime | None
    topic_id: int | None
    user_id: int | None
    is_best: int | None 

    @classmethod
    def from_query_result(cls, id, text, created_on, is_best, topic_id, user_id):
        return cls(
            id=id,
            text=text,
            created_on=created_on,
            is_best=is_best,
            topic_id=topic_id,
            user_id=user_id)

class Conversation(BaseModel):
    id: int | None
    subject: str
    user_ids: list[int] = []
    message_ids: list[int] = []

    @classmethod
    def from_query_result(cls, id, subject, user_ids = [], message_ids = []):
        return cls(
            id=id,
            subject = subject,
            user_ids=user_ids,
            message_ids = message_ids)


class Message(BaseModel):
    id: int | None
    text: str
    created_on: datetime | None
    conversation_id: int | None
    user_id: int | None

    @classmethod
    def from_query_result(cls, id, text, created_on, conversation_id, user_id):
        return cls(
            id = id,
            text = text,
            user_id = user_id,
            created_on = created_on,
            conversation_id = conversation_id
            )


class User(BaseModel):
    id: int | None
    user_name: str
    password: str
    role: str
    registered_on: date
    email: str
 
    def is_admin(self):
        return self.role == Role.ADMIN

    @classmethod
    def from_query_result(cls, id, user_name, password, role, registered_on, email):
        return cls(
            id=id,
            user_name=user_name,
            password=password,
            role=role,
            registered_on=registered_on,
            email=email)

class Role:
    REGULAR = 'regular'
    ADMIN = 'admin'

class UserName(BaseModel):
    user_name: str

class LoginData(BaseModel):
    user_name: str
    password: str

class UserAccess(BaseModel):
    access: int

class RegisterData(BaseModel):
    user_name: str
    password: str
    email: str

class TopicBody(BaseModel):
    is_locked: int | None

class CategoryBody(BaseModel):
    id: int

class ReplyBody(BaseModel):
    id: int | None
    text: str | None
    upvote: int | None
    downvote: int | None
    is_best: int | None


class ReplyResponse(BaseModel):
    id: int
    user_name: str
    text: str
    posted_on: datetime
    is_best: str
    upvotes: int
    downvotes: int

class TopicResponse(BaseModel):
    topic_id: int
    title: str
    views: int
    category_name: str
    topic_is_locked: str
    last_activity: datetime
    replies: list[ReplyResponse]

class TopicsResponse(BaseModel):
    topic_id: int
    title: str
    author: str
    views: int
    last_activity: datetime
    is_locked: str

    @classmethod
    def from_query_result(cls, topic_id, title, author, views=None, last_activity=None, is_locked=None):
        if not is_locked:
            is_locked = 'No'
        else: 
            is_locked = 'Yes'
        
        return cls(
            topic_id = topic_id,
            title=title,
            author=author,
            views=views,
            last_activity=last_activity,
            is_locked=is_locked)

class ConversationResponse(BaseModel):
    id: int
    subject: str
    messages: list[Message]

class ConversationsResponse(BaseModel):
    id: int
    subject: str
    user_name: str

class MessageResponse(BaseModel):
    id: int
    text: str
    created_on: datetime
    user_name: str

class PrivilegedUserResponse(BaseModel):
    id: int
    user_name: str
    access: int