import sqlite3
import click
from flask import app, current_app, g
from flask.cli import with_appcontext

def init_app(app):
    #function in parameter will be called on request completion
    app.teardown_appcontext(close_db)
    #argument corresponds to the name of the function
    app.cli.add_command(init_db_command)

def get_db():
    # check if database is current populated in g
    # add if it is not
    if ('db' not in g):
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

#if database is in g, delete it from g and close connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# run the schema file that structures the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Database Initialized')

# INSERTS QUESTION INTO TABLE
def insert_question(qName):
    db = get_db()
    db.execute(
        "INSERT INTO questions (question_name)"
        " VALUES (?)",
        (qName,)
    )
    db.commit()

def get_last_question():
    db = get_db()

    questions = db.execute(
        "SELECT * FROM questions ORDER BY id DESC"
    ).fetchall()

    # basic greatest value algorithm
    hightestId = 0
    for q in questions:
        if q["id"] > hightestId:
            hightestId = q["id"]

    return hightestId

def get_question_id_by_name(qName):
    db = get_db()
    
    questions = db.execute(
        "SELECT * FROM questions ORDER BY id DESC"
    ).fetchall()

    selectedQuestion = None
    for q in questions:
        if q['question_name'] == qName:
            selectedQuestion = q

    if selectedQuestion == None:
        return None

    return selectedQuestion

# AUTOMATICALLY INSERTS A USER ID FOR BUZZ IN TABLE BASED OFF LAST QUESTION
def insert_answer(userId, qId):
    db = get_db()

    db.execute(
        "INSERT INTO answers (question_id, user)"
        " VALUES (?, ?)",
        (qId, userId,)
    )
    db.commit()
