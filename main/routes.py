from flask import (
    Blueprint, render_template,
    request, redirect, url_for, flash
)

main_bp = Blueprint(
    'main', __name__,
    template_folder='templates'
)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/', methods=['POST'])
def index_post():
    choice = request.form.get('action')
    if choice == 'reserve':
        return redirect(url_for('main.reserve'))
    elif choice == 'admin':
        return redirect(url_for('admin.login'))
    flash('Please select a valid option.')
    return redirect(url_for('main.index'))

@main_bp.route('/reserve', methods=['GET'])
def reserve():
    return render_template('reserve.html')