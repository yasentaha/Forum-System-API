from data.models import Category, ReplyResponse, Topic, TopicResponse, User, Reply, Role, Conversation, Message, LoginData
from data.database import read_query, insert_query, update_query, read_query_single_element
from datetime import date,datetime

def all():
    data = read_query(
            '''SELECT id, text, created_on, is_best, topic_id, user_id 
                FROM replies''')
    return (Reply.from_query_result(*row) for row in data)

def all_in_topic(topic_id:int):
    #All replies within a topic.
    data = read_query(
            '''SELECT id, text, created_on, is_best, topic_id, user_id 
                FROM replies where topic_id=?''', (topic_id,))
    return (Reply.from_query_result(*row) for row in data)

def get_by_id(id: int):
    
    data = read_query(
        '''SELECT id, text, created_on, is_best, topic_id, user_id
            FROM replies
            WHERE id = ?''', (id,))

    return next((Reply.from_query_result(*row) for row in data), None)

def create(reply: Reply, topic_id: int, user:User) -> Reply:
    generated_id = insert_query(
        'INSERT INTO replies(text,created_on,is_best,topic_id,user_id) VALUES(?,?,?,?,?)',
        (reply.text, datetime.now(), 0, topic_id, user.id))

    reply.id = generated_id

    reply = get_by_id(generated_id)

    update_topic_activity(topic_id, reply)

    return reply

def update_reply_with_topic_id(topic_id:int, reply_id:int):
    update_query('UPDATE replies SET topic_id=? WHERE id=?', (topic_id, reply_id))

def update_topic_activity(topic_id: int, reply: Reply):
    update_query('UPDATE topics SET activity=? WHERE id=?', (reply.created_on,topic_id))

def create_response_object(reply: Reply, user_name: str):
    if not reply.is_best:
        reply_is_best = 'No'
    else: 
        reply_is_best = 'Yes'

    upvotes = reply_upvotes(reply)

    downvotes = reply_downvotes(reply)

    return ReplyResponse(id = reply.id, 
                        user_name = user_name, 
                        text=reply.text, 
                        posted_on = reply.created_on,
                        is_best = reply_is_best, upvotes=upvotes, downvotes=downvotes)

def edit_reply_text(text: str, reply: Reply):
    update_query('UPDATE replies SET text=? WHERE id=?', (text, reply.id))

def user_already_voted(reply: Reply, user: User):
    data = read_query('SELECT 1 from users_replies where reply_id = ? and user_id = ?', (reply.id, user.id))

    return any(data)

def get_user_vote(reply: Reply, user: User):
    vote = (read_query_single_element('SELECT upvote_downvote from users_replies where reply_id = ? and user_id = ?', (reply.id, user.id)))[0]

    return vote

def upvote(reply: Reply, user: User) -> bool:
    if user_already_voted(reply, user) and get_user_vote(reply, user) == 1:
        return False

    if not user_already_voted(reply, user):
        insert_query('INSERT INTO users_replies(user_id,reply_id,upvote_downvote) VALUES(?,?,?)', (user.id, reply.id, 1))
        return True

    if user_already_voted(reply, user) and get_user_vote(reply, user) == -1:
        update_query('UPDATE users_replies SET upvote_downvote=? where reply_id=? and user_id=?', (1, reply.id, user.id))
        return True

def downvote(reply: Reply, user: User):
    if user_already_voted(reply, user) and get_user_vote(reply, user) == -1:
        return False

    if not user_already_voted(reply, user):
        insert_query('INSERT INTO users_replies(user_id,reply_id,upvote_downvote) VALUES(?,?,?)', (user.id, reply.id, -1))
        return True
    
    if user_already_voted(reply, user) and get_user_vote(reply, user) == 1:
        update_query('UPDATE users_replies SET upvote_downvote=? where reply_id=? and user_id=?', (-1, reply.id, user.id))
        return True

def best_reply_present(topic: Topic):
    data = read_query('''SELECT 1 from topics as t 
    join replies as r
    on t.id = r.topic_id
    where r.topic_id = ? and r.is_best = ?''', (topic.id, 1))

    return any(data)

def choose_best(reply_id: int, topic: Topic):
    if best_reply_present(topic):
        return False
    else:
        update_query('UPDATE replies SET is_best=? WHERE id=?', (1, reply_id))
        return True


def delete(reply: Reply):
    update_query('DELETE FROM replies WHERE id = ?', (reply.id,))
    update_query('DELETE FROM users_replies WHERE reply_id = ?', (reply.id))

def reply_upvotes(reply: Reply) -> int:
    upvotes = (read_query_single_element('SELECT SUM(upvote_downvote) from users_replies where reply_id = ? and upvote_downvote = ?', (reply.id, 1)))[0]
    if not upvotes:
        return 0
    else:
        return upvotes

def reply_downvotes(reply: Reply) -> int:
    downvotes = (read_query_single_element('SELECT SUM(upvote_downvote) from users_replies where reply_id = ? and upvote_downvote = ?', (reply.id, -1)))[0]
    if not downvotes:
        return 0
    else:
        return -downvotes