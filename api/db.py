import sqlite3
import click  #Python package for creating beautiful command line interfaces in a composable way with as little code as necessary
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():

    '''
    g is special object that is unique for each request. It is used to store data that might be accessed by multiple function during the request
    The connection is stored and reused instead of creating a new connection if get_db is called  a second time in the same request
    '''
    if "db" not in g:  
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],   #current_app is special object that points to the Flask application handling the request
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        
        g.db.row_factory = sqlite3.Row  #tell the connection return rows.This allows accessing the column by name.
   
    return g.db


def close_db(error):
    db = g.pop("db", None)   #return None if db isn't in g 

    if db is not None:
        db.close()
   

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


'''
defines a command line called 'init-db' that calls the init_db function
'''
@click.command("init-db") 
@with_appcontext
def init_db_command():
    '""Clear the existing data and create new  tables.""'
    init_db()
    click.echo("initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db) #tells Flask to call that function when cleaning up after returning the response
    app.cli.add_command(init_db_command)  #adds a new command that can be called with the flask command
