import os
from flask import Flask
from . import db
from .main_api import main_api
from datetime import datetime, timedelta


def create_api(config=None):
    '''
    __name__ is the name of the current Python module. 
    The app needs to know where it’s located to set up some paths, 
    and __name__ is a convenient way to tell it that
    '''
    
    '''
    instance_relative_config=True 
    tells the app that configuration files are relative to the instance folder. 
    The instance folder is located outside the api package 
    and can hold local data that shouldn’t be committed to version control, 
    such as configuration secrets and the database file.
    '''

    app = Flask(__name__, instance_relative_config=True)
    
    '''sets some default configuration that the app will use:'''
    app.config.from_mapping(
        ENV = "dev",
        PERMANENT_SESSION_LIFETIME = timedelta(minutes=15),
        SECRET_KEY = "dev",  #SECRET_KEY is used by Flask and extensions to keep data safe
        DATABASE = os.path.join(app.instance_path, "api.sqlite")   #DATABASE is the path where the SQLite database file will be saved       
    )
       

    if config is None:
        #Load the instance config, if it exists
        #overrides the default configuration with values taken from the config.py file in the instance folder if it exists.
        app.config.from_pyfile("config.py", silent=True)
    else:
        #Load config if passed in
        app.config.from_mapping(config)  #config can also be passed to the factory, and will be used instead of the instance configuration.

    '''
    ensures that app.instance_path exists.
    Flask doesn’t create the instance folder automatically, 
    but it needs to be created because your project will create the SQLite database file there.
    '''
    try:        
        os.makedirs(app.instance_path)  #Create folder of instance_path (default name = instance)
        
    except OSError:
        pass


    '''
    Import and call db function from the factory
    '''
    db.init_app(app)


    '''
    Call API
    '''
    main_api(app)
   
    

    return app


    