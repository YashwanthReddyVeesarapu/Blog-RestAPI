from datetime import datetime
from bson import ObjectId

from flaskr.db import get_db


class User:
    _id: ObjectId | None = None
    email: str
    password: str

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def save(self):
        db = get_db()
        db.users.insert_one(self.__dict__)

    @staticmethod
    def get_by_email(email):
        db = get_db()
        user = db.users.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id'])
            return user
        return None
    
    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
            del user['password']
            return user
        return None
    

class Post:
    _id: ObjectId | None = None
    title: str
    content: str
    author_id: str
    description: str
    last_updated: datetime | None = None
    deleted: bool | None = False

    def __init__(self, title, content, author_id, description):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.description = description
        self.last_updated = datetime.now()
        self.deleted = False


    def save(self):
        db = get_db()
        res = db.posts.insert_one(self.__dict__)
        post_id = str(res.inserted_id)
        return post_id  

    @staticmethod
    def get_all():
        db = get_db()
        posts = db.posts.find({'deleted': False})
        res = []
        for post in posts:
            post['_id'] = str(post['_id'])
            res.append(post)

        return res
    

    @staticmethod
    def get_by_id(post_id):
        db = get_db()
        post = db.posts.find_one({'_id': ObjectId(post_id), 'deleted': False})
        if post:
            post['_id'] = str(post['_id'])
            return post
        return None


    @staticmethod
    def update(post_id, title, content, description):
        db = get_db()
        res = db.posts.update_one({'_id': ObjectId(post_id)}, {'$set': {'title': title, 'content': content, 'description': description, 'last_updated': datetime.now()}})
        if res.modified_count == 0:
            return False
        return True
    
    @staticmethod
    def delete(post_id):
        db = get_db()
        res = db.posts.update_one({'_id': ObjectId(post_id)}, {'$set': {'deleted': True}})
        if res.modified_count == 1:
            return True
        return False
    
    @staticmethod
    def undelete(post_id):
        db = get_db()
        post = db.posts.find_one({'_id': ObjectId(post_id)})
        if post:
            db.posts.update_one({'_id': ObjectId(post_id)}, {'$set': {'deleted': False}})
            return True
        return False
    