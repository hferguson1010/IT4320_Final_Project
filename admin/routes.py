
from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    flash, session
)
from models import Admin, Reservation

admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin',
    template_folder='templates'
)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # grab credentials
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # look up admin
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.seating'))
        # on failure, flash and redirect back
        flash('Invalid credentials', 'error')
        return redirect(url_for('admin.login'))

    # GET → show the login form
    return render_template('login.html')


@admin_bp.route('/seating', methods=['GET'])
def seating():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    # fetch reservations and pass into template
    reservations = Reservation.query.order_by(
        Reservation.seatRow, Reservation.seatColumn
    ).all()
    return render_template(
        'seating.html',
        reservations=reservations
    )