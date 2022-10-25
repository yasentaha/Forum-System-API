from data.models import Category, ReplyResponse, Topic, TopicResponse, TopicsResponse, User, Reply, Role, Conversation, Message, LoginData
from data.database import read_query, insert_query, update_query, read_query_single_element
from datetime import date,datetime


def all(search: str = None):
    if search is None:
        data = read_query(
            '''SELECT t.id, t.title, u.user_name as author, t.views, t.activity as last_activity, t.is_locked 
                FROM topics as t
                LEFT JOIN
                users as u
                ON t.user_id = u.id''')
    
    else:
        data = read_query(
            '''SELECT t.id, t.title, u.user_name as author, t.views, t.activity as last_activity, t.is_locked 
                FROM topics as t
                LEFT JOIN
                users as u
                ON t.user_id = u.id
               WHERE t.title LIKE ?''', (f'%{search}%',))

    return (TopicsResponse.from_query_result(*row) for row in data)

def all_in_category(category_id: int ,search: str = None):
    if search is None:
        data = read_query(
            '''SELECT t.id, t.title, u.user_name as author, t.views, t.activity as last_activity, t.is_locked 
                FROM topics as t
                LEFT JOIN
                users as u
                ON t.user_id = u.id
                WHERE t.category_id = ?''', (category_id,))
    
    else:
        data = read_query(
            '''SELECT t.id, t.title, u.user_name as author, t.views, t.activity as last_activity, t.is_locked 
                FROM topics as t
                LEFT JOIN
                users as u
                ON t.user_id = u.id
                WHERE t.category_id = ? AND title LIKE ?''', (category_id, f'%{search}%'))

    return (TopicsResponse.from_query_result(*row) for row in data)

def get_by_id(id: int):
    data = read_query(
        '''SELECT id, title, views, activity, is_locked, user_id, category_id
            FROM topics
            WHERE id = ?''', (id,))

    return next((Topic.from_query_result(*row) for row in data), None)


def sort(topics: list[Topic], *, attribute='title', reverse=False):
    if attribute == 'views':
        def sort_fn(t: Topic): return t.views
    elif attribute == 'activity':
        def sort_fn(t: Topic): return t.activity
    else:
        def sort_fn(t: Topic): return t.title
    return sorted(topics, key=sort_fn, reverse=reverse)

def exists(topic_id: int):
    data = read_query('SELECT 1 from topics where id = ?', (topic_id,))

    return any(data)

def update_views(id: int):
    current_topic_views = (read_query_single_element('SELECT views from topics where id=?', (id,)))[0]

    updated_views = current_topic_views + 1

    update_query('UPDATE topics SET views=? WHERE id=?', (updated_views, id))

def create(topic: Topic, user: User, category: Category) -> Topic:
    generated_id = insert_query(
        'INSERT INTO topics(title,views,category_id,user_id) VALUES(?,?,?,?)',
        (topic.title,0,category.id, user.id))

    topic.id = generated_id

    new_topic = get_by_id(generated_id)

    return new_topic

def get_topic_category_id(topic_id:int):
    category_id = (read_query_single_element('''SELECT category_id from topics
                                                where id=?''', (topic_id,)))[0]
    return category_id

def get_topic_replies(topic_id: int) -> list[Reply]:
    data = read_query(
        '''SELECT r.id, r.text, r.created_on, r.is_best, r.topic_id, r.user_id
                FROM replies as r
                WHERE r.topic_id=?''',
        (topic_id,))

    return [Reply.from_query_result(*row) for row in data]

def _flatten_topic_replies(data: list[tuple]):
    flattened = {}
    for id, title, category_id, reply_id in data:
        if id not in flattened:
            flattened[id] = (id, title, category_id, reply_id, [])

        flattened[id][-1].append(reply_id)

    return flattened

def delete(topic: Topic):
    update_query('DELETE FROM replies WHERE topic_id = ?', (topic.id,))
    update_query('DELETE FROM topics WHERE id = ?', (topic.id,))

def create_response_object(topic: Topic, category_name: str, topic_replies: list[ReplyResponse]):
    topic_locked = topic.locked()
    if not topic_locked:
        topic_locked = 'No'
    else: 
        topic_locked = 'Yes'
    return TopicResponse(topic_id=topic.id, title=topic.title, views=topic.views, category_name=category_name, topic_is_locked=topic_locked, last_activity = topic.activity, replies=topic_replies)

def lock(topic: Topic):
    locked = update_query(
        '''UPDATE topics 
            SET is_locked = ? 
             WHERE id = ?''',(1, topic.id))

    return locked