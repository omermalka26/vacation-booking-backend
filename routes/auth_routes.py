from flask import Blueprint, g, jsonify
from controllers.auth_controller import AuthController
from decorators.auth_decorator import token_required

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
@token_required
def get_current_user():
    return jsonify({'user': g.user})