from unicodedata import category
from fastapi import APIRouter, Header
from pydantic import BaseModel
from common.responses import BadRequest, Forbidden, InternalServerError, NoContent, NotFound, Success, Unauthorized, BlankValue
from common.auth import get_user_or_raise_401
from common.responses import NotFound
from data.models import Category, Topic, TopicsResponse, User, PrivilegedUserResponse, UserName
from services import category_service, topic_service, user_service


class CategoryResponseModel(BaseModel):
    category: Category
    topics: list[TopicsResponse]

class PrivilegedCategory(BaseModel):
    category: Category
    users: list[PrivilegedUserResponse]

categories_router = APIRouter(prefix='/categories')


@categories_router.get('/')
def get_categories(sort: str | None = None, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user.is_admin():
        categories = category_service.all()

    if not user.is_admin():
        categories = category_service.all_for_user(user_id=user.id) 

    if sort and (sort == 'asc' or sort == 'desc'):
        return category_service.sort(categories, reverse=sort == 'desc')
    else:
        return categories


@categories_router.get('/{id}')
def get_category_by_id(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    category = category_service.get_by_id_with_users(id)

    if category is None:
        return NotFound('Category does not exist.')

    if category.private() and not user_service.has_access_to_category(user, category):
        return Forbidden('You do not have access to this Category!')

    else:
        return CategoryResponseModel(
            category=category,
            topics=topic_service.all_in_category(category.id))


@categories_router.post('/')
def create_category(category: Category, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if len(category.name) <= 3:
        return BlankValue('The category name must not be less than 3 characters!')

    if not user.is_admin():
        return Forbidden('You do not have permission to create category!')

    created_category = category_service.create(category)

    return CategoryResponseModel(category=created_category, topics=[])


@categories_router.put('/{id}/lock')
def lock_category(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    category = category_service.get_by_id(id)

    if not user.is_admin():
        return Forbidden('You do not have permission to lock category')

    if category is None:
        return NotFound()

    if category.locked():
        return BadRequest('The category is already locked!')

    category_service.lock(category)

    return CategoryResponseModel(
        category=category,
        topics=topic_service.all_in_category(category.id))


@categories_router.put('/{id}')
def make_private_non_private(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    category = category_service.get_by_id_with_users(id)

    if not user.is_admin():
        return Forbidden('You do not have permission to change category status')

    if category is None:
        return NotFound('Category does not exist!')

    if category.private():
        [category_service.remove_user_from_category(user_id, category) for user_id in category.users_ids]
        category_service.make_private_non_private(category, 0)
        return Success(f'Category {category.name} is now public!')

    else:
        category_service.make_private_non_private(category, 1)
        return Success(f'Category {category.name} is now private!')



@categories_router.put('/{id}/users')
def add_user_to_category(id: int, user_name: UserName, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    category = category_service.get_by_id(id)
    user_to_add = user_service.find_by_username(user_name.user_name)

    if not user.is_admin():
        return Forbidden('You can not add users!')

    if category is None:
        return NotFound('Category does not exist.')

    if user_to_add is None:
        return NotFound('User does not exist.')

    if category.private():
        if category_service.add_user_to_category(user_to_add, category):
            return Success(f'{user_to_add.user_name} added successfully to Category {category.name}')
        else:
            return BadRequest('User already added to category')
    else:
        return BadRequest('You can not add user to Public category.')

@categories_router.get('/{id}/users')
def show_privileged_users(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    category = category_service.get_by_id(id)

    if not user.is_admin():
        return Forbidden('You can not add users!')

    if category is None:
        return NotFound('Category does not exist')

    if category.private():
        privilliged_users = user_service.all_privileged_for_specific_category(category)
        info = f'is_private: 0 - Public, 1 - Private; is_locked: 0 - Unlocked, 1 - Locked; Access: 1 - Read Only, 2 - Read/Write'
        return info, PrivilegedCategory(category=category, users = privilliged_users)
    else:
        return BadRequest('No privileged users in public category!')