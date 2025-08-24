from flask import Blueprint,g,jsonify
from controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['POST'])
def insert_user():
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return UserController.insert_user()
   

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return UserController.get_all_users()

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return UserController.get_user(user_id)

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return UserController.update_user(user_id)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    if g.user['role_id'] != 2:
        return jsonify({'error':'Admin required'}), 403
    return UserController.delete_user(user_id)