from flask import Blueprint, jsonify
from controllers.country_controller import CountryController
from decorators.auth_decorator import admin_required

country_bp = Blueprint('countries', __name__)

@country_bp.route('/countries', methods=['POST'])
@admin_required
def insert_country():
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
@admin_required
def update_country(country_id):
    return CountryController.update_country(country_id)

@country_bp.route('/countries/<int:country_id>', methods=['DELETE'])
@admin_required
def delete_country(country_id):
    return CountryController.delete_country(country_id)