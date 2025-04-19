import os
from flask import Flask



def create_app(test_config=None, instance_relative_config=True):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'dateverwerking.sqlite')
    )

    #used to test if app exists
    @app.route("/hello")
    def hello_world():
        return "Hello, World!"
    
    #init db
    import db
    db.init_app(app)

    #register login screen

    
    #check if we can create a folder in the instance path
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app