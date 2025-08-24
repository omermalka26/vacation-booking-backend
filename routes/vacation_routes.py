from flask import Blueprint, jsonify
from controllers.vacation_controller import VacationController
from decorators.auth_decorator import token_required, admin_required

vacation_bp = Blueprint('vacations', __name__)

@vacation_bp.route('/vacations', methods=['POST'])
@admin_required
def insert_vacation():
    return VacationController.insert_vacation()

@vacation_bp.route('/vacations', methods=['GET'])
@token_required
def get_all_vacations():
    return VacationController.get_all_vacations()

@vacation_bp.route('/vacations/<int:vacation_id>', methods=['GET'])
@token_required
def get_vacation(vacation_id):
    return VacationController.get_vacation(vacation_id)

@vacation_bp.route('/vacations/<int:vacation_id>', methods=['PUT'])
@admin_required
def update_vacation(vacation_id):
    return VacationController.update_vacation(vacation_id)

@vacation_bp.route('/vacations/<int:vacation_id>', methods=['DELETE'])
@admin_required
def delete_vacation(vacation_id):
    return VacationController.delete_vacation(vacation_id)