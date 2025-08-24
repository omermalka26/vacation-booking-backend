from flask import request, jsonify, current_app
from models.user import User 
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import re
from constants import USER_ROLE_ID, JWT_EXPIRATION_HOURS, MIN_PASSWORD_LENGTH

class AuthController:
    @staticmethod
    def generate_token(user_id):
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        return token

    @staticmethod
    def login_user():
        if request.method == 'POST':
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                
                error = None

                if 'email' not in data:
                    error = 'Email is required.'
                elif 'password' not in data:
                    error = 'Password is required.'
                
                if error:
                    return jsonify({'error': error}), 400
                
                email = data['email']
                password = data['password']
               
                if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
                    return jsonify({'error': 'Invalid email format.'}), 400

                elif len(password) < MIN_PASSWORD_LENGTH:
                    return jsonify({'error': f'Password must be at least {MIN_PASSWORD_LENGTH} characters long.'}), 400
                
                result = User.get_by_email(email) 

                if result is None:
                    return jsonify({'error': 'Incorrect email or password.'}), 401
                elif not check_password_hash(result['password_hash'], password):
                    return jsonify({'error': 'Incorrect email or password.'}), 401

                # Generate JWT token
                token = AuthController.generate_token(result['user_id'])
                
                print("user logged in")
                return jsonify({
                    'message': 'login successful',
                    'token': token,
                    'user': {
                        'user_id': result['user_id'],
                        'first_name': result['first_name'],
                        'last_name': result['last_name'],
                        'email': result['email'],
                        'role_id': result['role_id']
                    }
                })
                
            except Exception as e:
                print(f"Login error: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500

    @staticmethod
    def register_user():
        try:
            data = request.get_json()
                
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            if not all(k in data for k in ['first_name', 'last_name', 'email', 'password']):
                return jsonify({'error': 'Missing required fields'}), 400
                
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            password = data['password']
            role_id = USER_ROLE_ID
            
            # Validation
            if not first_name.strip() or not last_name.strip():
                return jsonify({'error': 'First name and last name cannot be empty'}), 400
                
            if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
                return jsonify({'error': 'Invalid email format.'}), 400

            elif len(password) < MIN_PASSWORD_LENGTH:
                return jsonify({'error': f'Password must be at least {MIN_PASSWORD_LENGTH} characters long.'}), 400
            
            # Hash password before sending to model
            password_hash = generate_password_hash(password)
            result = User.insert(first_name, last_name, email, password_hash, role_id)
        
            if result is None:
                return jsonify({'error': 'Email already exists'}), 400
            
            # Generate JWT token for newly registered user
            token = AuthController.generate_token(result['user_id'])
                
            print("user registered")
            return jsonify({
                'message': 'sign up successful',
                'token': token,
                'user': result
            }), 201
                
        except Exception as e:
            print(f"Registration error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @staticmethod
    def logout_user():
        try:
            # For JWT, logout is handled on the client side by removing the token
            print("user logged out")
            return jsonify({'message': 'logout successful'})
        except Exception as e:
            print(f"Logout error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
        