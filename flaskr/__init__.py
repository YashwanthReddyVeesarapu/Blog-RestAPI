from flask import Flask
from flask_pymongo import PyMongo


from . import db


from flaskr.auth import auth_bp
from flaskr.blog import blog_bp

mongo = PyMongo()


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/blog"


    db.init_app(app)



    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    @app.route('/')
    def hello_world():
        return 'Welcome to Blog API!'

    return app





