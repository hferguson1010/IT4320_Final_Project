import os
from flask import Flask, session, flash, request
from flask_sqlalchemy import SQLAlchemy
from main.routes import main_bp
from admin.routes import admin_bp
from models import db

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'your‐secret‐key‐here'
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'final_project_files', 'reservations.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.before_request
    def auto_logout_outside_admin():
        if session.get('admin_logged_in'):
            if not request.path.startswith('/admin'):
                session.clear()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5016)
