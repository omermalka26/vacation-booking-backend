from flask import Blueprint, jsonify
from controllers.user_controller import UserController
from decorators.auth_decorator import admin_required

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['POST'])
@admin_required
def insert_user():
    return UserController.insert_user()

@user_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    return UserController.get_all_users()

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    return UserController.get_user(user_id)

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    return UserController.update_user(user_id)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    return UserController.delete_user(user_id)