from flask import Flask, render_template, url_for
import os

def create_app():
    # CONFIGURE APP
    buzz = Flask(__name__, instance_relative_config=True)
    buzz.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = "Admin159",
        DATABASE = os.path.join(buzz.instance_path, "buzzer_system.sqlite")
    )

    # ENSURE INSTANCE FOLDER EXISTS (where database is being kept)
    try:
        os.makedirs(buzz.instance_path)
    except OSError:
        pass

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
