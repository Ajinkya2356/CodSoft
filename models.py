from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime


class Users(db.Model, UserMixin):
    __tablename__ = "user"
    is_active = True
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    First_name = db.Column(db.String(150), nullable=False)
    mobile = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200))
    gender = db.Column(db.String(30))
    state = db.Column(db.String(40))


class Package(db.Model):
    __tablename__ = "Package"
    p_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    name = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    pdays = db.Column(db.Integer, nullable=False)
    np = db.Column(db.Integer, nullable=False)

class Hotel(db.Model):
    __tablename__ = "Hotel"
    h_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    name = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    rating=db.Column(db.Float(),nullable=False)
    city=db.Column(db.String(40),nullable=False)

class Bookings(db.Model):
    __tablename__ = "Booking"
    b_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(60), nullable=False)
    package_id = db.Column(db.Integer(), db.ForeignKey("Package.p_id"), nullable=False)
    no_persons = db.Column(db.Integer, nullable=False)
    bookingdate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    packagename=db.Column(db.String(50),nullable=False)
    card_number=db.Column(db.String(50),nullable=False)
    expiry_year=db.Column(db.Integer,nullable=False)
    cvvcode=db.Column(db.String(50),nullable=False,unique=True)

class Hotel_Bookings(db.Model):
    __tablename__ = "Hotel_Booking"
    b_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(60), nullable=False)
    h_id = db.Column(db.Integer(), db.ForeignKey("Hotel.h_id"), nullable=False)
    bookingdate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    hname=db.Column(db.String(50),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    card_number=db.Column(db.String(50),nullable=False)
    expiry_year=db.Column(db.Integer,nullable=False)
    cvvcode=db.Column(db.String(50),nullable=False,unique=True)

class Passenger(db.Model):
    __tablename__ = 'passengers'

    passenger_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20),nullable=False)
    phone_number = db.Column(db.String(20),nullable=False)


class Booking(db.Model):
    __tablename__ = 'bookings'
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    flight_id=db.Column(db.Integer,nullable=False,unique=True)
    booking_id = db.Column(db.Integer, primary_key=True)
    No_of_Persons=db.Column(db.Integer,nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.passenger_id'))
    booking_date = db.Column(db.Date)
    passenger = db.relationship("Passenger")
    user=db.relationship("Users")
    source=db.Column(db.String(100),nullable=False)
    destination=db.Column(db.String(100),nullable=False)
    departure_time=db.Column(db.String(30),nullable=False)
    arrival_time=db.Column(db.String(30),nullable=False)

class Contact(db.Model):
    __tablename__ = "Contact"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name=db.Column(db.String(50),nullable=False)
    subject=db.Column(db.String(150),nullable=False)
    message=db.Column(db.Text(200),nullable=False)









