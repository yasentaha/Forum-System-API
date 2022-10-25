from data.database import insert_query, read_query, read_query_single_element, update_query
from data.models import Conversation, MessageResponse, Reply, Role, User, Topic, Message
from datetime import date,datetime
from mariadb import IntegrityError



def create(message: Message, conversation_id: int, user:User) -> Message:
    generated_id = insert_query(
        '''INSERT INTO messages(text,created_on,user_id) VALUES(?,?,?)
            ''',
        (message.text, datetime.now(),user.id))

    message.id = generated_id
    insert_message_to_conversation(conversation_id, message.id)

    return get_by_id(generated_id)

def get_by_id(id: int):
    
    data = read_query(
            '''SELECT m.id, m.text, m.created_on, mc.conversation_id, m.user_id 
                FROM messages AS m
                    LEFT JOIN conversations_messages AS mc
                    ON m.id = mc.message_id 
                    WHERE m.id=?''', (id,))

    return next((Message.from_query_result(*row) for row in data), None)

def insert_message_to_conversation(conversation_id: int, message_id: int):

    insert_query(
        f'INSERT INTO conversations_messages(message_id, conversation_id) VALUES {(message_id, conversation_id)}')

def all_messages_in_conversation(conversation_id:int):
    
    data = read_query(
            '''SELECT m.id, m.text, m.created_on, mc.conversation_id, m.user_id 
                FROM messages AS m
                    LEFT JOIN conversations_messages AS mc
                    ON m.id = mc.message_id 
                    WHERE mc.conversation_id=?''', (conversation_id,))
    
    return [Message.from_query_result(*row) for row in data]

def create_response_object(message: Message, user: User):
    return MessageResponse(id=message.id, text=message.text, created_on= message.created_on, user_name= user.user_name)