from flask import Blueprint,jsonify,g
from controllers.country_controller import CountryController

country_bp = Blueprint('countries', __name__)

@country_bp.route('/countries', methods=['POST'])
def insert_country():
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return CountryController.insert_country()

@country_bp.route('/countries', methods=['GET'])
def get_all_countries():
    # Public route - no authentication required
    return CountryController.get_all_countries()

@country_bp.route('/countries/<int:country_id>', methods=['GET'])
def get_country(country_id):
    # Public route - no authentication required
    return CountryController.get_country(country_id)

@country_bp.route('/countries/<int:country_id>', methods=['PUT'])
def update_country(country_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return CountryController.update_country(country_id)

@country_bp.route('/countries/<int:country_id>', methods=['DELETE'])
def delete_country(country_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return CountryController.delete_country(country_id)