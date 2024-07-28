from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    with app.app_context():
        from .controllers import main_controller
        app.register_blueprint(main_controller.bp)

    return app
