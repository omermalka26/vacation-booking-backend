from flask import Blueprint, g, jsonify
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return AuthController.login_user()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return AuthController.logout_user()

@auth_bp.route('/register', methods=['POST'])
def register():
    return AuthController.register_user()

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    if g.user is None:
        return jsonify({'error': 'Not authenticated'}), 401
    return jsonify({'user': g.user})