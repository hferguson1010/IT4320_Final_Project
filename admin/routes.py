from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    flash, session
)

admin_bp = Blueprint(
    'admin', __name__,
    template_folder='templates',
    url_prefix='/admin'
)

@admin_bp.route('/', methods=['GET'])
def admin_index():
    return redirect(url_for('admin.login'))

@admin_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@admin_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    # Temporary credentials replace with actual admin login information
    if username == 'admin' and password == 'secret':
        session['admin_logged_in'] = True
        return redirect(url_for('admin.seating'))
    flash('Invalid credentials', 'error')
    return redirect(url_for('admin.login'))