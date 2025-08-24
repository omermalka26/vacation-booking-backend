from flask import Blueprint,jsonify,g
from controllers.vacation_controller import VacationController

vacation_bp = Blueprint('vacations', __name__)

@vacation_bp.route('/vacations', methods=['POST'])
def insert_vacation():
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return VacationController.insert_vacation()

@vacation_bp.route('/vacations', methods=['GET'])
def get_all_vacations():
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    return VacationController.get_all_vacations()

@vacation_bp.route('/vacations/<int:vacation_id>', methods=['GET'])
def get_vacation(vacation_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    return VacationController.get_vacation(vacation_id)

@vacation_bp.route('/vacations/<int:vacation_id>', methods=['PUT'])
def update_vacation(vacation_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return VacationController.update_vacation(vacation_id)

@vacation_bp.route('/vacations/<int:vacation_id>', methods=['DELETE'])
def delete_vacation(vacation_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return VacationController.delete_vacation(vacation_id)