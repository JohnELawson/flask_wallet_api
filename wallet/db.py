import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # if not already connected
    if 'db' not in g:
        # connect
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # return rows that behave like dicts
        g.db.row_factory = sqlite3.Row

        return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        # iff conn exists, close
        db.close()


def init_db():
    # get db instance
    db = get_db()

    # read setup sql schema file and execute
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# click cli command
@click.command('init-db')
@with_appcontext
def init_db_command():
    # clear existing data and create new db
    init_db()
    click.echo("initialized the database")


def init_app(app):
    # call close db after cleanup
    app.teardown_appcontext(close_db)
    # adds new command for flask
    app.cli.add_command(init_db_command)
