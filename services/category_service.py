from mariadb import IntegrityError
from data.database import read_query, insert_query, update_query
from data.models import Category, User


def all(get_data=None):

    if get_data is None:
        get_data=read_query

    data = get_data('select id, name,description,is_private,is_locked from categories order by id')

    return (Category(id=id, name=name, description=description, is_private=is_private, is_locked = is_locked)
            for id, name, description, is_private, is_locked in data)

def all_for_user(user_id: int, get_data=None):

    if get_data is None:
        get_data=read_query

    public_data = get_data('''select id, name,description,is_private,is_locked from categories
                        where is_private=?''',(0,))

    private_data = get_data('''select c.id, c.name,c.description,c.is_private,c.is_locked from categories as c
                        join users_categories as uc
                        on c.id = uc.category_id
                        where c.is_private=? and uc.user_id=?''',(1, user_id))
    if private_data:
        data = public_data.extend(private_data)
    else:
        data = public_data

    return (Category(id=id, name=name, description=description, is_private=is_private, is_locked = is_locked)
            for id, name, description, is_private, is_locked in data)

def get_by_id_with_users(id: int, get_data=None):

    if get_data is None:
        get_data=read_query

    data = get_data(
            '''SELECT c.id, c.name,c.description,c.is_private,c.is_locked, uc.user_id
                from categories AS c
                LEFT JOIN users_categories AS uc
                ON c.id = uc.category_id
                WHERE c.id = ?''', (id,))

    flatten_data = _flatten_category_users(data)

    return next((Category(id=id, name=name, description=description, is_private=is_private, is_locked = is_locked, users_ids=users_ids)
            for id, name, description, is_private, is_locked, users_ids in flatten_data.values()), None)

def _flatten_category_users(data: list[tuple]):
    flattened = {}
    for category_id, name, description, is_private, is_locked, user_id in data:
        if category_id not in flattened:
            flattened[category_id] = (category_id, name, description, is_private, is_locked,[])

        if user_id:
            flattened[category_id][-1].append(user_id)

    return flattened

def get_by_id(id: int, get_data=None):

    if get_data is None:
        get_data=read_query

    data = get_data('select id, name,description,is_private, is_locked from categories where id = ?', (id,))

    return next((Category(id=id, name=name, description=description, is_private=is_private, is_locked=is_locked)
                 for id, name, description, is_private, is_locked in data), None)

def sort(categories: list[Category], *, attribute='name', reverse=False):

    if attribute == 'name':
        def sort_fn(c: Category): return c.name
    else:
        def sort_fn(c: Category): return c.id

    return sorted(categories, key=sort_fn, reverse=reverse)

def exists(id: int,get_data=None):

    if get_data is None:
        get_data=read_query

    return any(
        get_data(
            'select id, name,description,is_private,is_locked from categorieswhere id = ?',
            (id,)))


def create(category: Category,insert_data=None):

    if insert_data is None:
        insert_data=insert_query

    generated_id = insert_data(
        'insert into categories(name,description,is_private,is_locked) values(?,?,?,?)',
        (category.name, category.description, category.is_private, category.is_locked))

    category.id = generated_id

    return category

def make_private_non_private(category: Category, status: int,update_data=None):
    if update_data is None:
        update_data=update_query

    update_data(
        '''UPDATE categories
            SET is_private = ? 
             WHERE id = ?''',(status, category.id))

def add_user_to_category(users: User, category: Category, default_access = 2,insert_data=None):

    if insert_data is None:
        insert_data=insert_query
    
    try:
        insert_data(
        '''INSERT INTO users_categories(user_id, category_id, access) values(?,?,?)''',
        (users.id, category.id, default_access))
        return True
    
    except IntegrityError:
        return False

def remove_user_from_category(user_id, category: Category,update_data=None):

    if update_data is None:
        update_data=update_query
    update_data(
        '''DELETE FROM users_categories WHERE user_id = ? and category_id = ?''',
    (user_id, category.id))

def lock(category: Category,update_data=None):
    if update_data is None:
        update_data=update_query
    update_data(
        '''UPDATE categories
            SET is_locked = ? 
             WHERE id = ?''',(1, category.id))

