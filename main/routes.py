from flask import (
    Blueprint, render_template,
    request, redirect, url_for, flash
)
from models import db, Reservation


def generate_eticket(first_name):
    constant = "INFOTC4320"
    result = []
    first_name = first_name.strip()

    max_len = max(len(first_name), len(constant))

    for i in range(max_len):
        if i < len(first_name):
            result.append(first_name[i])
        if i < len(constant):
            result.append(constant[i])

    return ''.join(result)


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

@main_bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    seating_chart = [[None for _ in range(4)] for _ in range(12)]

    reservations = Reservation.query.all()
    for res in reservations:
        seating_chart[res.seatRow][res.seatColumn] = res.passengerName

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        row = request.form.get('row')
        seat = request.form.get('seat')

        if not first_name or not last_name or not row or not seat:
            flash('All fields are required.', 'error')
            return redirect(url_for('main.reserve'))

        row = int(row)
        seat = int(seat)

        existing_reservation = Reservation.query.filter_by(seatRow=row, seatColumn=seat).first()
        if existing_reservation:
            flash('That seat is already reserved!', 'error')
            return redirect(url_for('main.reserve'))

        e_ticket_number = generate_eticket(first_name)

        new_reservation = Reservation(
            passengerName=f"{first_name} {last_name}",
            seatRow=row,
            seatColumn=seat,
            eTicketNumber=e_ticket_number
        )

        db.session.add(new_reservation)
        db.session.commit()

        flash(f'Reservation successful! Your eTicket number is {e_ticket_number}', 'success')
        return redirect(url_for('main.reserve'))

    return render_template('reserve.html', seating_chart=seating_chart)
