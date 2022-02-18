from flask import Flask, render_template, url_for
import os
from flask_socketio import SocketIO

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

    @socketio.on('client_connected')
    def handle_connect(data):
        print('[DEBUG] Client has connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('[DEBUG] Client has disconnected')

    @socketio.on('queston_start')
    def handle_question_start(data):
        print('Name: {0}, Time: {1}'.format(data['qname'], data['qtime']))
    
    @buzz.route('/')
    def hello_world():
        return render_template('hello_world.html')
    
    @buzz.route('/buzzer')
    def buzzer():
        return render_template('buzzer.html')

    @buzz.route('/admin')
    def admin():
        return render_template('admin.html')


    return buzz
