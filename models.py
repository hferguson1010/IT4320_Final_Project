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
    passengerName = db.Column(db.String(200), nullable=False)
    seatRow = db.Column(db.Integer, nullable=False)
    seatColumn = db.Column(db.Integer, nullable=False)
    eTicketNumber = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reservation {self.passengerName} {self.eTicketNumber}>'