import sqlite3

'''
g is a special object that is unique for each request. 
It is used to store data that might be accessed by multiple functions during the request. 
'''

import click
from flask import current_app, g


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# click.command define command line command called init-db
# that calls the init_db function and shows a success message to the user.
@click.command('init-db')
def init_db_command():
    """Clear existing database and create new one"""
    init_db()
    click.echo('Database initialized')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

        return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)