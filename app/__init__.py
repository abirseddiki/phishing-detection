from flask import Flask
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from .controllers import main_controller

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .controllers import main_controller
        app.register_blueprint(main_controller.bp)
        from .controllers.client_controller import client_bp
        app.register_blueprint(client_bp, url_prefix='/api')
        from .controllers.url_controller import url_bp
        app.register_blueprint(url_bp, url_prefix='/api')
        from .controllers.check_controller import check_bp
        app.register_blueprint(check_bp, url_prefix='/api')
        from .controllers.model_audit_controller import model_audit_bp
        app.register_blueprint(model_audit_bp, url_prefix='/api')
        from .controllers.feedback_controller import feedback_bp
        app.register_blueprint(feedback_bp, url_prefix='/api')
        from .controllers.download_controller import download_bp
        app.register_blueprint(download_bp, url_prefix='/api')

    # Initialize APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=run_job, trigger="interval", hours=1, args=[app])

    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    return app

def run_job(app):
    with app.app_context():
        main_controller.run_scraper_job()
