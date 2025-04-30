from flask import Flask
from main.routes import main_bp
from admin.routes import admin_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'your-secret-key-here'

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5016)
