# Web Buzzer
This project is a very simple program for playing a trivia-like game over a LAN network. Go to host:5000/buzzer for the buzzer client and host:5000/admin for the admin controls. This project is built with the Python web framework [Flask](https://flask.palletsprojects.com/en/2.1.x/) and uses [Flask SocketIO](https://flask-socketio.readthedocs.io/en/latest/) for quick communication between client and server.

## Build Instructions
**Windows**:

Ensure to have [Python installed](https://wiki.python.org/moin/BeginnersGuide/Download) and [added to PATH](https://www.educative.io/edpresso/how-to-add-python-to-path-variable-in-windows). 

Open cmd or powershell and navigate to the location of this repository
create a Python virtual environmnet and install dependencies using the commands: 
```
X:\Path\To\Project> py -m venv venv

(venv) X:\Path\To\Project> pip install -r requirements.txt
```

Afterwards, you need to set the environment variable that tells flask what flask how to load the application like so:
```
(venv) X:\Path\To\Project> set FLASK_ENV="Buzzer"
```

You can re-initialize the database (this clears users and past questions) by using the command:

```
(venv) X:\Path\To\Project> flask init-db
```

To run the server on your local machine after these steps, use the command:
```
(venv) X:\Path\To\Project> flask run
```

To run and make avaliable to others on your network, run the command:
```
(venv) X:\Path\To\Project> flask run --host=0.0.0.0:PORT
```

Navigate to http://(hostip):PORT in a web browswer to access the game

## Security Notice

This app is by no means meant to be exposed publically, and the built-in WSGI server is not meant to be a production server. Please do not expose this to any sort of public network. This application is not secure, and is purely made for fun. This is your fair warning.

If for whatever reason you really want to expose this (which I don't recommend), put a production WSGI server in front of it.
