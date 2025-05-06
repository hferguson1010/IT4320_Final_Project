from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    flash, session
)
from models import Admin, Reservation

admin_bp = Blueprint(
    'admin', __name__,
    template_folder='templates',
    url_prefix='/admin'
)

@admin_bp.route('/', methods=['GET', 'POST'])
def login():
    seating_chart = None
    reservations = None
    total_sales = 0

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('admin.login'))

    if session.get('admin_logged_in'):
        cost_matrix = get_cost_matrix()
        seating_chart = [[None for _ in range(4)] for _ in range(12)]
        total_sales = 0
        reservations = Reservation.query.all()
        for r in reservations:
            seating_chart[r.seatRow][r.seatColumn] = 'reserved'
            total_sales += cost_matrix[r.seatRow][r.seatColumn]

    return render_template(
        'login.html',
        seating_chart=seating_chart,
        reservations=reservations,
        total_sales=total_sales
    )

def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(12)]