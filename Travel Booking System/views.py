from flask import Blueprint, render_template, flash, jsonify
from flask_login import login_required, current_user
import requests
from .models import Package,Hotel
some_blueprint = Blueprint("some_blueprint", __name__)


@some_blueprint.route("/")
def index():
    return render_template("home.html", user=current_user)


@some_blueprint.route("/about")
def about():
    return render_template("about.html", user=current_user)


@some_blueprint.route("/service")
def service():
    return render_template("services.html", user=current_user)


@some_blueprint.route('/packages')
def pack():
    travel_packages = Package.query.all()
    return render_template('packages.html',user=current_user,packages=travel_packages)
@some_blueprint.route('/Hotels')
def hotel():
    Hotels = Hotel.query.all()
    return render_template('hotels.html',user=current_user,Hotel=Hotels)



