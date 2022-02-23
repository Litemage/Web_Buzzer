from flask import Flask, render_template, url_for, redirect, request, flash, session, g
import functools
import os
from flask_socketio import SocketIO
from Buzzer.db import get_db, init_app


# ================================== HELPERS ==================================

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            print('[DEBUG] user is none')
            return redirect("login")
        return view(**kwargs)

    print('[DEBUG] returning wrapped_view')
    print(wrapped_view)
    return wrapped_view

def page_not_found(e):
    #set 404 explicitly
    return render_template('404.html'), 404

# ================================== CONFIG & INIT ==================================

def create_app():
    # CONFIGURE APP
    buzz = Flask(__name__, instance_relative_config=True)
    buzz.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = "Admin159",
        DATABASE = os.path.join(buzz.instance_path, "buzzer_system.sqlite")
    )

    #Register Error handlers
    buzz.register_error_handler(404, page_not_found)

    #init database
    init_app(buzz)

    # ENSURE INSTANCE FOLDER EXISTS (where database is being kept)
    try:
        os.makedirs(buzz.instance_path)
    except OSError:
        pass

    @buzz.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM users WHERE id = ?', (user_id,)
            ).fetchone()

    def get_username():
        user_id = session.get('user_id')
        user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        return user['username']

    # ================================== SOCKETS ==================================

    socketio = SocketIO(buzz)

    @socketio.on('connect')
    def handle_connect(data):
        print('[DEBUG] A Client has connected')

    @socketio.on('queston_start')
    def handle_question_start(data):
        print('[DEBUG] Name: {0}, Time: {1}'.format(data['qname'], data['qtime']))
        socketio.emit('question_active', data['qname'])

    @socketio.on('question_stop')
    def handle_question_stop():
        print('[DEBUG] Received question stop from admin')
        socketio.emit('server_question_stop')

    @socketio.on('question_answer')
    def handle_question_answer():
        user_id = session.get('user_id')
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()
        print(f"[DEBUG] User: {user['username']}")
        socketio.emit('server_question_answer', user['username'])
        socketio.emit('server_question_stop')
    
    # ================================== ROUTES ==================================

    @buzz.route('/')
    def hello_world():
        return render_template('hello_world.html')
    

    @buzz.route('/buzzer')
    @login_required
    def buzzer():
        print('Going to render template')
        return render_template('buzzer.html', username=get_username())

    @buzz.route('/admin')
    def admin():
        return render_template('admin.html')
        
        

    #disable this route before release
    @buzz.route('/login', methods=('GET', 'POST'))
    def login():     
        if request.method == 'POST':
            username = request.form['username']
            db = get_db()
            error = None

            if not username:
                error = 'No username received, can\'t write'
            
            if error is None:
                try:
                    db.execute(
                        "INSERT INTO users (username) VALUES (?)",
                        (username,)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"User \"{username}\" already registered"
                    print("Username Already exists")
                else:
                    user = db.execute(
                        'SELECT * FROM users WHERE username = ?',
                        (username,)
                    ).fetchone()
                    session.clear()
                    session['user_id'] = user['id']
                    print("[DEBUG] tried to redirect")
                    print(redirect('buzzer'))
                    return redirect('buzzer')
            print(f'[DEBUG] error raised: {error}')
            flash(error)
            
        return render_template('login.html')
            


    return buzz
