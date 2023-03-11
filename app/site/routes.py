from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema
from flask_login import current_user, login_required

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route("/")
def home():
    return render_template("index.html")

@site.route("/profile")
def profile():
    return render_template("profile.html")

@site.route("/Cars")
@login_required
def Cars():
    cars = Car.query.all()
    return render_template("Cars.html", cars=cars)

@site.route('/add_car', methods=['POST'])
@login_required
def add_car():
    vin = request.form['Vin']
    make = request.form['Make']
    model = request.form['Model']
    year = request.form['Year']
    user_id = current_user.id

    car = Car(Vin=vin, Make=make, Model=model, Year=year, user_id=user_id)
    db.session.add(car)
    db.session.commit()
    
    return redirect(url_for('site.Cars'))

@site.route('/delete_car/<id>', methods=['POST'])
@login_required
def delete_car(id):
    car = Car.query.get(id)
    if car:
        if car.user_id == current_user.id:
            db.session.delete(car)
            db.session.commit()
            return jsonify({'message': 'Car deleted successfully.'}), 200
        else: 
            return jsonify({'message': 'You do not have permission to delete this car.'}), 403
    else:
        return jsonify({'message': 'Car not found.'}), 404
    return redirect(url_for('site.Cars'))

@site.errorhandler(400)
@site.errorhandler(401)
@site.errorhandler(403)
@site.errorhandler(404)
@site.errorhandler(500)
def error_handler(error):
    error_code = error.code
    error_message = error.description
    return render_template('error.html', error_code=error_code, error_message=error_message), error_code
