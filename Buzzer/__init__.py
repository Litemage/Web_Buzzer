from flask import Flask, render_template, url_for, redirect, request, flash, session, g, send_from_directory
import functools
import os
from flask_socketio import SocketIO
from Buzzer.db import get_db, init_app, insert_answer, insert_question, get_last_question
from flask_minify import minify

# ================================== HELPERS ==================================

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("login")
        return view(**kwargs)

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

    #Minify stuff
    minify(app=buzz, html=True, js=True, cssless=True)

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
    
    @socketio.on('queston_start')
    def handle_question_start(data):
        db = get_db()
        insert_question(data['qname'])
        socketio.emit('question_active', data['qname'])

    @socketio.on('question_stop')
    def handle_question_stop():
        socketio.emit('server_question_stop')

    @socketio.on('question_answer')
    def handle_question_answer():
        user_id = session.get('user_id')
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()

        # get last question
        lastQuestion = get_last_question()
        # insert a answer row into answers based off of last question
        insert_answer(user_id, lastQuestion)

        socketio.emit('server_question_answer', user['username'])
        # socketio.emit('server_question_stop')
    
    # ================================== ROUTES ==================================

    @buzz.route('/')
    def hello_world():
        return render_template('hello_world.html')

    @buzz.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(buzz.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    

    @buzz.route('/buzzer')
    @login_required
    def buzzer():
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
                else:
                    user = db.execute(
                        'SELECT * FROM users WHERE username = ?',
                        (username,)
                    ).fetchone()
                    session.clear()
                    session['user_id'] = user['id']
                    return redirect('buzzer')
            flash(error)
            
        return render_template('login.html')
            


    return buzz
