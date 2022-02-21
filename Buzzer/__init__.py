from flask import Flask, render_template, url_for, redirect, request
import functools
import os
from flask_socketio import SocketIO


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("login.html")
    
    return wrapped_view

def create_app():
    # CONFIGURE APP
    buzz = Flask(__name__, instance_relative_config=True)
    buzz.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = "Admin159",
        DATABASE = os.path.join(buzz.instance_path, "buzzer_system.sqlite")
    )

    socketio = SocketIO(buzz)

    # ENSURE INSTANCE FOLDER EXISTS (where database is being kept)
    try:
        os.makedirs(buzz.instance_path)
    except OSError:
        pass

    @socketio.on('connect')
    def handle_connect(data):
        print('[DEBUG] Client has connected')

    @socketio.on('queston_start')
    def handle_question_start(data):
        print('[DEBUG] Name: {0}, Time: {1}'.format(data['qname'], data['qtime']))
        socketio.emit('question_active')

    @socketio.on('question_stop')
    def handle_question_stop():
        print('[DEBUG] Received question stop from admin')
        socketio.emit('server_question_stop')
    
    @buzz.route('/')
    def hello_world():
        return render_template('hello_world.html')
    

    @buzz.route('/buzzer')
    def buzzer():
        return render_template('buzzer.html')

    @buzz.route('/admin')
    def admin():
        return render_template('admin.html')

    @buzz.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            # Take in username and put it in database
            raise NotImplementedError


    return buzz
