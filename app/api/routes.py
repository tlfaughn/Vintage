from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

#make a route 
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    Vin = request.json['Vin']
    Make = request.json['Make']
    Model = request.json['Model']
    Year = request.json['Year']
    user = User.query.get(current_user_token.id)

    car = Car(Vin=Vin, Make=Make, Model=Model, Year=Year, user_id=user.id)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    user_id = current_user_token.id
    cars = Car.query.filter_by(user_id=user_id).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_car(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}), 401


@api.route('/cars/<id>', methods=['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.Vin = request.json['Vin']
    car.Make = request.json['Make']
    car.Model = request.json['Model']
    car.Year = request.json['Year']
    car.user_id = current_user_token.id

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)