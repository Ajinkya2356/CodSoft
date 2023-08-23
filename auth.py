from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users, Package, Bookings, Booking, Passenger,Contact,Hotel,Hotel_Bookings
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import (
    login_user,
    login_required,
    logout_user,
    LoginManager,
)
from flask_login import current_user
import requests, time
from datetime import datetime
from .opensky_api import OpenSkyApi
import random



login_manager = LoginManager()
auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            fname = request.form.get("fname")
            psw = request.form.get("password")
            cpsw = request.form.get("cpassword")
            mobile = request.form.get("mobile")
            age = int(request.form.get("age"))
            address = request.form.get("address")
            gender = request.form.get("gender")
            state = request.form.get("state")

            if Users.query.filter_by(email=email).first():
                raise ValueError("Email is already used")
            elif len(email) < 4:
                raise ValueError("Email must be greater than 4 characters")
            elif len(fname) < 2:
                raise ValueError("First name must be greater than 2 characters")
            elif psw != cpsw:
                raise ValueError("The passwords don't match")
            elif len(psw) < 7:
                raise ValueError("Password must be at least 7 characters")
            elif int(age) < 0:
                raise ValueError("Invalid age")
            elif len(mobile) != 10:
                raise ValueError("Invalid Mobile Number")

            new_user = Users(
                email=email,
                First_name=fname,
                password=generate_password_hash(psw, method="sha256"),
                mobile=mobile,
                address=address,
                age=age,
                gender=gender,
                state=state,
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully!", category="success")
            return redirect(url_for("auth.login"))

        except ValueError as e:
            flash(str(e), category="error")

    return render_template("register.html", user=current_user)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            psw = request.form.get("password")
            user = Users.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.password, psw):
                    login_user(user, remember=True)
                    flash("Logged in successfully!", category="success")
                    return redirect("/")
                else:
                    raise ValueError("Incorrect password")
            else:
                raise ValueError("User does not exist")
        except ValueError as e:
            flash(str(e), category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!")
    return redirect(url_for("auth.login"))


@auth.route("/admin", methods=["GET", "POST"])
def adminl():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            psw = request.form.get("password")
            if email == "Admin@123" and psw == "1234543":
                # login_user(user, remember=True)
                # flash("Logged in successfully!", category="success")
                return redirect(url_for("auth.admind"))
            else:
                # raise ValueError("Incorrect password")
                pass
        except ValueError as e:
            # flash(str(e), category="error")
            pass

    return render_template("adminl.html")


@auth.route("/admind", methods=["POST", "GET"])
def admind():
    return render_template("admind.html")


@auth.route("/alogout")
def admin_logout():
    logout_user()
    return redirect(url_for("auth.adminl"))


@auth.route("/addpack", methods=["GET", "POST"])
def add_pack():
    if request.method == "POST":
        pname = request.form.get("pname")
        price = request.form.get("price")
        Days = request.form.get("days")
        np = request.form.get("np")
        url = request.form.get("url")
        new_pack = Package(name=pname, price=price, image_url=url, pdays=Days, np=np)
        db.session.add(new_pack)
        db.session.commit()
        return redirect(url_for("auth.admind"))
    return render_template("admin_add.html")

@auth.route("/addhotel", methods=["GET", "POST"])
def add_hotel():
    if request.method == "POST":
        hname = request.form.get("hname")
        price = request.form.get("price")
        url = request.form.get("url")
        city=request.form.get("city")
        rating=request.form.get("rating")
        new_hotel = Hotel(name=hname, price=price, url=url,city=city, rating=rating)
        db.session.add(new_hotel)
        db.session.commit()
        return redirect(url_for("auth.admind"))
    return render_template("adminh.html")

@auth.route("/checkout/<int:package_id>", methods=["GET", "POST"])
@login_required
def payment(package_id):
    package = Package.query.get(package_id)

    if request.method == "POST":
        if package:
            package_id = package_id
            username = current_user.First_name
            user_email = current_user.email
            no_persons = package.np
            card_number = request.form.get("cardno")
            expiryyear = request.form.get("expiry")
            cvvcode = request.form.get("cvv")
            booked = Bookings.query.filter_by(packagename=package.name).first()
            if booked:
                flash("You have already booked this pack", category="error")
                redirect("/packages")
            elif int(expiryyear) < 2023:
                flash("Card is expired", category="error")
                redirect("/packages")
            else:
                new_booking = Bookings(
                    package_id=package_id,
                    username=username,
                    user_email=user_email,
                    no_persons=no_persons,
                    packagename=package.name,
                    card_number=card_number,
                    expiry_year=expiryyear,
                    cvvcode=cvvcode,
                )
                db.session.add(new_booking)
                db.session.commit()
                flash("Package Booked Successfully", category="success")
                redirect("/packages")
        else:
            flash("Package Not found", category="error")

    return render_template("checkout.html", user=current_user, package=package)


@auth.route("/mybookings/<int:user_id>")
@login_required
def mybookings(user_id):
    Booked = Bookings.query.filter_by(user_email=current_user.email)
    return render_template("mybookings.html", booked=Booked, user=current_user)


@auth.route("/myhotels/<int:user_id>")
@login_required
def myhotels(user_id):
    Booked = Hotel_Bookings.query.filter_by(user_email=current_user.email)
    return render_template("myhbookings.html", booked=Booked, user=current_user)
standard_flights = []


@auth.route("/flights", methods=["GET", "POST"])
def view_flights():
    username = "Ajinkya_20"
    password = "Ajinkya@api23"

    api = OpenSkyApi(username, password)
    airport_code = "EDDF"
    begin = 1517227200
    end = 1517230800
    airport_code_to_name = {
        "EDDF": "Frankfurt Airport",
        "EDDT": "Berlin Tegel Airport",
        "EGLL": "London Heathrow Airport",
        "LFPG": "Charles de Gaulle Airport",
        "KJFK": "John F. Kennedy International Airport",
        "KLAX": "Los Angeles International Airport",
        "RJTT": "Tokyo Haneda Airport",
        "OMDB": "Dubai International Airport",
        "ZBAA": "Beijing Capital International Airport",
        "KORD": "Chicago O'Hare International Airport",
        "RKSI": "Incheon International Airport",
        "WSSS": "Singapore Changi Airport",
        "VTBS": "Suvarnabhumi Airport",
        "VIDP": "Indira Gandhi International Airport",
        "CYYZ": "Toronto Pearson International Airport",
        "EHAM": "Amsterdam Schiphol Airport",
        "EDDM": "Munich Airport",
        "KSFO": "San Francisco International Airport",
        "VHHH": "Hong Kong International Airport",
        "OMAA": "Abu Dhabi International Airport",
        "KDFW": "Dallas/Fort Worth International Airport",
        "EDDB": "Berlin Brandenburg Airport",
        "NZAA": "Auckland Airport",
        "LEMD": "Adolfo Suárez Madrid–Barajas Airport",
        "LFBO": "Toulouse–Blagnac Airport",
        "EGKK": "London Gatwick Airport",
        "LIRF": "Leonardo da Vinci–Fiumicino Airport",
        "CYYZ": "Toronto Pearson International Airport",
        "LSZH": "Zurich Airport",
        "EDDH": "Hamburg Airport",
    }
    print(len(airport_code_to_name))

    def unix_to_standard_time(unix_timestamp):
        standard_time = datetime.utcfromtimestamp(unix_timestamp).strftime("%H:%M:%S")
        return standard_time

    def unix_to_standard_date(unix_timestamp):
        standard_date = datetime.utcfromtimestamp(unix_timestamp).strftime("%Y-%m-%d")
        return standard_date

    flights_data = api.get_flights_from_interval(begin, end)
    print(flights_data)
    flight_id_counter = 1
    for flight_data in flights_data:
        source_code = flight_data.estDepartureAirport
        destination_code = flight_data.estArrivalAirport
        source = airport_code_to_name.get(source_code, "Unknown Airport")
        if source == "Unknown Airport":
            source = random.choice(list(airport_code_to_name.values()))
        destination = airport_code_to_name.get(destination_code, "Unknown Airport")
        if destination == "Unknown Airport":
            destination = random.choice(list(airport_code_to_name.values()))
        departure_time = flight_data.firstSeen
        arrival_time = flight_data.lastSeen
        departure_standard_time = unix_to_standard_time(departure_time)
        arrival_standard_time = unix_to_standard_time(arrival_time)
        departure_standard_date = unix_to_standard_date(departure_time)
        arrival_standard_date = unix_to_standard_date(arrival_time)

        flight = {
            "source": source,
            "destination": destination,
            "departure_date": departure_standard_date,
            "arrival_date": arrival_standard_date,
            "departure_time": departure_standard_time,
            "arrival_time": arrival_standard_time,
            "airline": flight_data.callsign,
            "flight_id": flight_data.icao24,
            "no_of_seats": 50,
        }
        flight_id_counter += 1
        standard_flights.append(flight)
    return render_template("flights.html", flights=standard_flights, user=current_user)


@auth.route("/search_flights", methods=["POST"])
def search_flights():
    source_to_search = request.form.get("source_airport")
    destination_to_search = request.form.get("destination_airport")
    start_date = datetime.strptime(request.form.get("ddate"), "%Y-%m-%d")
    end_date = datetime.strptime(request.form.get("adate"), "%Y-%m-%d")
    matching_flights = []
    for flight in standard_flights:
        departure_time = datetime.strptime(flight["departure_date"], "%Y-%m-%d")
        arrival_time = datetime.strptime(flight["arrival_date"], "%Y-%m-%d")
        if (
            source_to_search.lower() in flight["source"].lower()
            and destination_to_search.lower() in flight["destination"].lower()
        ):
            if (
                start_date <= departure_time <= end_date
                or start_date <= arrival_time <= end_date
            ):
                matching_flights.append(flight)
    print(matching_flights)
    return render_template("flights.html", flights=matching_flights, user=current_user)


@auth.route("/Booking/<string:flight_id>", methods=["GET", "POST"])
@login_required
def booking(flight_id):
    username = "Ajinkya_20"
    password = "Ajinkya@api23"

    api = OpenSkyApi(username, password)
    airport_code = "EDDF"
    begin = 1517227200
    end = 1517230800
    airport_code_to_name = {
        "EDDF": "Frankfurt Airport",
        "EDDT": "Berlin Tegel Airport",
        "EGLL": "London Heathrow Airport",
        "LFPG": "Charles de Gaulle Airport",
        "KJFK": "John F. Kennedy International Airport",
        "KLAX": "Los Angeles International Airport",
        "RJTT": "Tokyo Haneda Airport",
        "OMDB": "Dubai International Airport",
        "ZBAA": "Beijing Capital International Airport",
        "KORD": "Chicago O'Hare International Airport",
        "RKSI": "Incheon International Airport",
        "WSSS": "Singapore Changi Airport",
        "VTBS": "Suvarnabhumi Airport",
        "VIDP": "Indira Gandhi International Airport",
        "CYYZ": "Toronto Pearson International Airport",
        "EHAM": "Amsterdam Schiphol Airport",
        "EDDM": "Munich Airport",
        "KSFO": "San Francisco International Airport",
        "VHHH": "Hong Kong International Airport",
        "OMAA": "Abu Dhabi International Airport",
        "KDFW": "Dallas/Fort Worth International Airport",
        "EDDB": "Berlin Brandenburg Airport",
        "NZAA": "Auckland Airport",
        "LEMD": "Adolfo Suárez Madrid–Barajas Airport",
        "LFBO": "Toulouse–Blagnac Airport",
        "EGKK": "London Gatwick Airport",
        "LIRF": "Leonardo da Vinci–Fiumicino Airport",
        "CYYZ": "Toronto Pearson International Airport",
        "LSZH": "Zurich Airport",
        "EDDH": "Hamburg Airport",
    }
    print(len(airport_code_to_name))

    def unix_to_standard_time(unix_timestamp):
        standard_time = datetime.utcfromtimestamp(unix_timestamp).strftime("%H:%M:%S")
        return standard_time

    def unix_to_standard_date(unix_timestamp):
        standard_date = datetime.utcfromtimestamp(unix_timestamp).strftime("%Y-%m-%d")
        return standard_date

    flights_data = api.get_flights_from_interval(begin, end)
    
    flight_id_counter = 1
    for flight_data in flights_data:
        source_code = flight_data.estDepartureAirport
        destination_code = flight_data.estArrivalAirport
        source = airport_code_to_name.get(source_code, "Unknown Airport")
        if source == "Unknown Airport":
            source = random.choice(list(airport_code_to_name.values()))
        destination = airport_code_to_name.get(destination_code, "Unknown Airport")
        if destination == "Unknown Airport":
            destination = random.choice(list(airport_code_to_name.values()))
        departure_time = flight_data.firstSeen
        arrival_time = flight_data.lastSeen
        departure_standard_time = unix_to_standard_time(departure_time)
        arrival_standard_time = unix_to_standard_time(arrival_time)
        departure_standard_date = unix_to_standard_date(departure_time)
        arrival_standard_date = unix_to_standard_date(arrival_time)

        flight = {

            "source": source,
            "destination": destination,
            "departure_date": departure_standard_date,
            "arrival_date": arrival_standard_date,
            "departure_time": departure_standard_time,
            "arrival_time": arrival_standard_time,
            "airline": flight_data.callsign,
            "flight_id": flight_data.icao24,
            "no_of_seats": 50,
        }
        flight_id_counter += 1
        standard_flights.append(flight)
    # fly = []

    for flight in standard_flights:
        if flight["flight_id"] == flight_id:
            matched_flight=flight
    print(matched_flight)
    if request.method == "POST":
        passenger_name = request.form.get("firstname")
        passenger_email = request.form.get("email")
        no_of_persons = int(request.form.get("np"))
        phone=int(request.form.get('phone'))
        # first_flight = fly[0]
        source = matched_flight['source']
        destination=matched_flight['destination']
        departure_time=matched_flight['departure_time']
        arrival_time=matched_flight['arrival_time']
        purchased = Booking.query.get(flight_id)
        passenger = Passenger(name=passenger_name, email=passenger_email,phone_number=phone)
        db.session.add(passenger)
        db.session.commit()
        
        booking_date = datetime.now().date()
        booking = Booking(
            flight_id=flight_id,
            passenger=passenger,
            No_of_Persons=no_of_persons,
            booking_date=booking_date,
            user=current_user,
            source=source,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
        )
        db.session.add(booking)
        db.session.commit()

        flash("Booking successful", category="success")
        redirect("/flights")

    return render_template("flight_checkout.html", flights=matched_flight, user=current_user)

@auth.route("/mytickets/<int:user_id>")
@login_required
def mytickets(user_id):
    Booked = Booking.query.filter_by(user_id=user_id)
    return render_template("mytickets.html", booked=Booked, user=current_user)

@auth.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=="POST":
        name=request.form.get('name')
        email=request.form.get('email')
        subject=request.form.get('subject')
        message=request.form.get('message')
        new_contact=Contact(name=name,email=email,subject=subject,message=message)
        db.session.add(new_contact)
        db.session.commit()
        flash("Details Submitted Successfully",category="success")
    return render_template("contact.html", user=current_user)


    
@auth.route("/hcheckout/<int:h_id>", methods=["GET", "POST"])
@login_required
def hpayment(h_id):
    hotel = Hotel.query.get(h_id)

    if request.method == "POST":
        if hotel:
            h_id = h_id
            username = current_user.First_name
            user_email = current_user.email
            price=hotel.price
            card_number = request.form.get("cardno")
            expiryyear = request.form.get("expiry")
            cvvcode = request.form.get("cvv")
            booked = Hotel_Bookings.query.filter_by(hname=hotel.name).first()
            if booked:
                flash("You have already booked this pack", category="error")
                redirect("/packages")
            elif int(expiryyear) < 2023:
                flash("Card is expired", category="error")
                redirect("/packages")
            else:
                new_booking = Hotel_Bookings(
                    h_id=h_id,
                    username=username,
                    user_email=user_email,
                    price=hotel.price,
                    hname=hotel.name,
                    card_number=card_number,
                    expiry_year=expiryyear,
                    cvvcode=cvvcode,
                )
                db.session.add(new_booking)
                db.session.commit()
                flash("Hotel Booked Successfully", category="success")
                redirect("/")
        else:
            flash("Hotel Not found", category="error")

    return render_template("hcheckout.html", user=current_user, hotel=hotel)




