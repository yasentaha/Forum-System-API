
from data import database
from data.database import insert_query, read_query, read_query_single_element, update_query
from data.models import Category, Conversation, PrivilegedUserResponse, Reply, Role, User, Topic, Message
from mariadb import IntegrityError
from datetime import date
import re

def _hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def find_by_username(user_name: str, get_data_func = database.read_query) -> User | None: #returns a User(BaseModel) or None
    '''Expects a user name, as a string.
    Returns a User (pydantic) Object if a user with the given user_name exists in the database. 
    Otherwise, returns None.'''
    data = get_data_func(
        'SELECT id, user_name, password, role, registered_on, email FROM users WHERE user_name = ?',
        (user_name,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(user_name: str, password: str) -> User | None:
    '''Expects login data - user name and password as strings. If the user exists and given password is the same as the User's,
    it will return a User pydantic object. If not, it will return none.'''
    user = find_by_username(user_name)

    hashed_password = _hash_password(password)

    return user if user and user.password == hashed_password else None


def create(user_name: str, password: str, email: str, insert_data_func=database.insert_query) -> User | None:
    '''Expects registration data and if user name not taken, it will return a User pydantic object.'''
    
    password = _hash_password(password)

    registered_on = date.today()

    try:
        generated_id = insert_data_func(
            'INSERT INTO users(user_name, password, role, registered_on, email) VALUES (?,?,?,?,?)',
            (user_name, password, Role.REGULAR, registered_on, email))

        return User(id=generated_id, 
                    user_name=user_name, 
                    password='', 
                    role=Role.REGULAR, 
                    registered_on=registered_on, 
                    email=email)

    except IntegrityError:
        return None


def valid_username(user_name: str):
    '''Expects a user name as string, and if valid, it will return it, otherwise it will return None.'''
    if len(user_name) < 2 or len(user_name) > 30:
        return None
    else:
        return user_name

def valid_email(email: str):
    '''Expects an email address as string, and if valid, it will return it, otherwise it will return None.'''
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return email
    else:
        return None


def update_role(user_name: str, role: str) -> bool:
    '''Expects a user name with and a role to update for that User. Returns 1 if successful and -1 if not.'''
    successful_update = update_query('UPDATE users SET role=? where user_name=?',(role, user_name))

    return successful_update
    
def change_access(user: User, category: Category, access: int):
    '''Expects User and Category pydantic object and access in the form of int. Returns 1 if successful and -1 if not.'''
    changed_access = update_query('UPDATE users_categories SET access = ? WHERE user_id = ? and category_id = ?', (access, user.id, category.id))

    return changed_access

def all_privileged_for_specific_category(category: Category):
    '''Expects a PRIVATE Category pydantic object and returns all users and their access for that category.'''
    privileged_users = read_query('''SELECT u.id, u.user_name, uc.access 
                                        FROM users AS u
                                        JOIN users_categories AS uc
                                        ON u.id = uc.user_id
                                        WHERE uc.category_id = ?''', (category.id,))
        
    return (PrivilegedUserResponse(id=id, user_name = user_name, access = access) for id, user_name, access in privileged_users)

def owns_reply(user: User, reply: Reply) -> bool:
    return reply.user_id == user.id

def owns_conversation(user: User, conversation: Conversation) -> bool:
    return any([uid for uid in conversation.user_ids if uid == user.id])

def owns_topic(user: User, topic: Topic) -> bool:
    return user.id == topic.user_id

def has_access_to_category(user: User, category: Category):
    if user.is_admin():
        return True
    else:
        return user.id in category.users_ids

def has_readonly_access_to_category(user: User, category: Category):
    data = read_query('SELECT 1 from users_categories where user_id=? and category_id=? and access=?',
    (user.id, category.id, 1)
    )
    return any(data)

def exists(user_id: int):
    data = read_query('SELECT 1 from users where id = ?', (user_id,))

    return any(data)

def get_user_name_by_id(id: int):
    user_name = (read_query_single_element('SELECT user_name from users where id = ?', (id,)))[0]

    return user_name