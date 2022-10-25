from data.database import insert_query, read_query, read_query_single_element, update_query
from data.models import Conversation, ConversationResponse, ConversationsResponse, Reply, Role, User, Topic, Message
from mariadb import IntegrityError

def create(conversation: Conversation) -> Conversation:
    generated_id = insert_query(
        'INSERT INTO conversations(subject) VALUES(?)',
        (conversation.subject,))

    conversation.id = generated_id

    return conversation

def get_user_conversations(user: User):
    data = read_query('''SELECT c.id, c.subject, u.user_name
                        from conversations as c
                        LEFT JOIN users_conversations AS uc
                        ON c.id = uc.conversation_id
                        LEFT JOIN users as u
                        on u.id = uc.user_id
                        where c.id in (SELECT c.id
                        FROM conversations AS c
                        LEFT JOIN users_conversations AS uc
                        ON c.id = uc.conversation_id
                        WHERE uc.user_id = ?) and u.user_name != ?''', (user.id, user.user_name))


    return (ConversationsResponse(id = id, subject=subject, user_name=user_name) for id, subject, user_name in data)



def _flatten_conversations_messages(data: list[tuple], from_user_id):
    flattened = {}
    for id, subject, user_id in data:
        if from_user_id != user_id and id not in flattened:
            flattened[id] = (id, subject, user_id)

    return flattened

def _flatten_conversations_messages_GET(data: list[tuple]):
    flattened = {}
    for id, subject, user_id, message_id in data:
        if id not in flattened:
            flattened[id] = (id, subject, [], [])

        if message_id is not None:
            flattened[id][-1].append(message_id)

    for id, subject, user_id, message_id in data:
        if user_id is not None:
            flattened[id][-2].append(user_id)

    return flattened    

def user_already_in_conversation(user_id: int, conversation_id: int):
    data = read_query('SELECT 1 from users_conversations where user_id = ? and conversation_id = ?', (user_id, conversation_id))

    return any(data)

def insert_user_to_conversation(user_id: int, conversation_id: int):
    if not user_already_in_conversation(user_id, conversation_id):
        insert_query(
        f'INSERT INTO users_conversations(user_id, conversation_id) VALUES {(user_id, conversation_id)}')

def create_response_object(conversation: Conversation, conversation_messages: list[Message]):
    return ConversationResponse(id=conversation.id, subject = conversation.subject, messages = conversation_messages)

def get_by_id(id: int):
    data = read_query(
        '''SELECT 
            c.id, c.subject, uc.user_id, m.id
        FROM
            conversations AS c
        LEFT JOIN
            users_conversations AS uc ON c.id = uc.conversation_id
        LEFT JOIN
            messages AS m ON m.user_id = uc.user_id
        WHERE
            c.id = ?''', (id,))

    flattened_data = _flatten_conversations_messages_GET(data)

    return next((Conversation.from_query_result(*obj) for obj in flattened_data.values()), None)
