from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"
    

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    passengerName = db.Column(db.String(100), nullable=False)
    seatRow = db.Column(db.Integer, nullable=False)
    seatColumn = db.Column(db.Integer, nullable=False)
    eTicketNumber = db.Column(db.String(20), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Reservation {self.passengerName} - Row {self.seatRow}, Seat {self.seatColumn}>'
