from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    flash, session
)
from models import Admin, Reservation, db

admin_bp = Blueprint(
    'admin', __name__,
    url_prefix='/admin',
    template_folder='templates'
)

def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(12)]

@admin_bp.route('/', methods=['GET', 'POST'])
def login():
    seating_chart = [['available' for _ in range(4)] for _ in range(12)]
    reservations = []
    total_sales = 0

    if request.method == 'POST' and 'username' in request.form:
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin.login'))
        flash('Invalid credentials', 'error')
        return redirect(url_for('admin.login'))

    if session.get('admin_logged_in'):
        reservations = Reservation.query.order_by(
            Reservation.seatRow, Reservation.seatColumn
        ).all()
        cost_matrix = get_cost_matrix()
        for r in reservations:
            seating_chart[r.seatRow][r.seatColumn] = 'reserved'
            total_sales += cost_matrix[r.seatRow][r.seatColumn]

    return render_template(
        'login.html',
        seating_chart=seating_chart,
        reservations=reservations,
        total_sales=total_sales
    )

@admin_bp.route('/delete/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    if not session.get('admin_logged_in'):
        flash('Please log in first.', 'error')
        return redirect(url_for('admin.login'))

    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash(f'Reservation for {reservation.passengerName} deleted.', 'success')
    return redirect(url_for('admin.login'))