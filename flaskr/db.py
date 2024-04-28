

from flask import current_app, g
from flask_pymongo import PyMongo
import click

def get_db():
    if 'db' not in g:
        g.db = PyMongo(current_app).db
    return g.db

def init_db():
    db = get_db()
    return db

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)






