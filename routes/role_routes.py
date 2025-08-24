from flask import Blueprint,jsonify,g
from controllers.role_controller import RoleController

role_bp = Blueprint('roles', __name__)

@role_bp.route('/roles', methods=['POST'])
def insert_role():
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return RoleController.insert_role()


@role_bp.route('/roles', methods=['GET'])
def get_all_roles():
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return RoleController.get_all_roles()

@role_bp.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return RoleController.get_role(role_id)

@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return RoleController.update_role(role_id)

@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return RoleController.delete_role(role_id)