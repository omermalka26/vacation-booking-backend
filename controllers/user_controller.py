from flask import jsonify, request
from models.user import User
from models.role import Role
from werkzeug.security import generate_password_hash

class UserController:
    @staticmethod
    def insert_user():
        data = request.get_json()
        if not data or not all(k in data for k in ['first_name', 'last_name', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        if 'role_id' in data:
            if data['role_id'] is None or not isinstance(data['role_id'], int):
                return jsonify({'error': 'Invalid role_id format'}), 400
            if not Role.get_by_id(data['role_id']):
                return jsonify({'error': 'Role not found'}), 404
            if data['role_id'] == 2:
                return jsonify({'error': 'Cannot create admin user'}), 403
        
        # Hash password before sending to model
        password_hash = generate_password_hash(data['password'])
        
        result = User.insert(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password_hash=password_hash,
            role_id=data['role_id'] if 'role_id' in data else 1  # Default to role_id 1 if not provided
        )
        
        if result is None:
            return jsonify({'error': 'Email already exists'}), 400
        
        return jsonify(result), 201
    
    @staticmethod
    def get_all_users():
        users = User.get_all()
        return jsonify({'users': users})
    
    @staticmethod
    def get_user(user_id):
        user = User.get_by_id(user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)
    
    @staticmethod
    def update_user(user_id):
        data = request.get_json()
        if not data or not all(k in data for k in ['first_name', 'last_name', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        if 'role_id' in data:
            if data['role_id'] == 2:
                return jsonify({'error': 'Cannot update to admin'}), 403
        
        # Hash password if it's being updated
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])
            
        result = User.update(user_id, **data)
        if result is None:
            return jsonify({'error': 'User not found or update failed'}), 404
        return jsonify(result)
    
    @staticmethod
    def delete_user(user_id):
        result = User.delete(user_id)
        if result is None:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(result)
