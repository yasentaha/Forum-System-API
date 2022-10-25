from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401, create_token
from common.responses import BadRequest, Forbidden, NotFound, Success
from data.models import CategoryBody, Conversation, LoginData, RegisterData, Category, UserAccess
from services import user_service
from services import category_service


users_router = APIRouter(prefix='/users')


@users_router.post('/login')
def login(data: LoginData):
    user = user_service.try_login(data.user_name, data.password)

    if user:
        token = create_token(user)
        return {'token': token}
    
    else:
        return BadRequest('Invalid login data')


@users_router.get('/info')
def user_info(x_token: str = Header()):
    return get_user_or_raise_401(x_token)
    

@users_router.post('/register')
def register(data: RegisterData):
    if not user_service.valid_email(data.email):
        return BadRequest('Please enter a valid email address.')

    if not user_service.valid_username(data.user_name):
        return BadRequest('Please enter a user name that is bigger than 2 and less than 30 symbols')
    
    user = user_service.create(data.user_name, data.password, data.email)
    
    return user or BadRequest(f'Username {data.user_name} is taken.')

@users_router.put('/{user_name}')
def change_access(user_name, category_body: CategoryBody, access: UserAccess, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    user_to_change = user_service.find_by_username(user_name)
    
    if not user.is_admin():
        return Forbidden('You do not have permission to change access for category')
    
    category = category_service.get_by_id_with_users(category_body.id)

    if category is None:
        return NotFound('Category does not exist.')
    
    if user_to_change is None:
        return NotFound('User to change access for does not exist.')
    
    if not user_service.has_access_to_category(user_to_change, category):
        return BadRequest(f'User with {user_name} does not have access to category {category.name}!')

    if category.private():
        user_service.change_access(user_to_change, category, access.access)
        if access.access == 1:
            new_access = 'Read'
        if access.access == 2:
            new_access = 'Read/Write'
        return Success(f'User with {user_name} access changed to {new_access} for category {category.name}!')
    else:
        return BadRequest('You can not change access for public category!')

@users_router.delete('/{user_name}')
def revoke_user_access(user_name, category_body: CategoryBody, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    user_to_revoke = user_service.find_by_username(user_name)
    
    if not user.is_admin():
        return Forbidden('You do not have permission to revoke access')
    
    category = category_service.get_by_id_with_users(category_body.id)

    if category is None:
        return NotFound('Category does not exist.')
    
    if user_to_revoke is None:
        return NotFound('User to revoke access from does not exist!')

    if not user_service.has_access_to_category(user_to_revoke, category):
        return BadRequest(f'User with {user_name} does not have access to category {category.name}!')
    
    if category.private():
        category_service.remove_user_from_category(user_to_revoke.id, category)
        
        return Success(f'User with {user_name} access revoked for category {category.name}!')
    else:
        return BadRequest('You can not revoke access for public category!')
