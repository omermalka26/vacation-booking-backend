from flask import Blueprint, jsonify
from controllers.like_controller import LikeController
from decorators.auth_decorator import token_required

like_bp = Blueprint('like_bp', __name__)

@like_bp.route('/likes', methods=['POST'])
@token_required
def add_like():
    return LikeController.insert_like()

@like_bp.route('/likes/<int:vacation_id>', methods=['DELETE'])
@token_required
def remove_like(vacation_id):
    return LikeController.delete_like(vacation_id)