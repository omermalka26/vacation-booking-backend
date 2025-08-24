from flask import Blueprint, jsonify
from controllers.role_controller import RoleController
from decorators.auth_decorator import admin_required

role_bp = Blueprint('roles', __name__)

@role_bp.route('/roles', methods=['POST'])
@admin_required
def insert_role():
    return RoleController.insert_role()

@role_bp.route('/roles', methods=['GET'])
@admin_required
def get_all_roles():
    return RoleController.get_all_roles()

@role_bp.route('/roles/<int:role_id>', methods=['GET'])
@admin_required
def get_role(role_id):
    return RoleController.get_role(role_id)

@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
@admin_required
def update_role(role_id):
    return RoleController.update_role(role_id)

@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@admin_required
def delete_role(role_id):
    return RoleController.delete_role(role_id)