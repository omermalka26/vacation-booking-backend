from flask import jsonify, request
from models.role import Role
from constants import USER_ROLE_ID, ADMIN_ROLE_ID

class RoleController:
    @staticmethod
    def insert_role():
        data = request.get_json()
        if 'role_name' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        result = Role.insert(
           role_name=data['role_name']
        )
        
        if result is None:
            return jsonify({'error': 'role_name already exists'}), 400
        return jsonify(result), 201
    
    @staticmethod
    def get_all_roles():
        roles = Role.get_all()
        return jsonify({'roles': roles})
    
    @staticmethod
    def get_role(role_id):
        role = Role.get_by_id(role_id)
        if role is None:
            return jsonify({'error': 'Role not found'}), 404
        return jsonify(role)
    
    @staticmethod
    def update_role(role_id):
        if role_id == USER_ROLE_ID or role_id == ADMIN_ROLE_ID:
            return jsonify({'error':'cannot update system roles'}), 400
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        result = Role.update(role_id, **data)
        if result is None:
            return jsonify({'error': 'Role not found or update failed'}), 404
        return jsonify(result)
    
    @staticmethod
    def delete_role(role_id):
        if role_id == USER_ROLE_ID or role_id == ADMIN_ROLE_ID:
            return jsonify({'error':'cannot delete system roles'})
        result = Role.delete(role_id)
        if result is None:
            return jsonify({'error': 'Role not found'}), 404
        return jsonify(result)
    
    