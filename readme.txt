Run The Application

Now you can run your application using the flask command. 
From the terminal, tell Flask where to find your application, 
then run it in development mode. 
Remember, you should still be in the top-level vocr directory, not the api package.

1. Create Databse and Schema, From terminal type the following command
    $flask init-db

    in terminal you should see the message 'initialized the Databse'

2. Start the API, From terminal, type following command   
    $python app.py


Visit http://127.0.0.1:4000/api in a browser and you should see the api information message. 
Congratulations, you’re now running your VOCR API application!


DEBUG APPLICATION 

Linux
    export FLASK_APP="app.py"
    export FLASK_DEBUG=1
    python -m flask run --host=0.0.0.0

Windows
    set FLASK_APP="app.py"
    set FLASK_DEBUG=1
    python -m flask run --host=0.0.0.0 --port=5001