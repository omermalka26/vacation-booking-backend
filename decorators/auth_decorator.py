from functools import wraps
from flask import request, jsonify, g
import jwt
from flask import current_app
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode the token
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = User.get_by_id(data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
                
            g.user = current_user
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode the token
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = User.get_by_id(data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Check if user is admin (role_id = 2)
            if current_user['role_id'] != 2:
                return jsonify({'error': 'Admin access required'}), 403
                
            g.user = current_user
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated
