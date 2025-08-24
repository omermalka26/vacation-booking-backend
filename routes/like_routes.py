from flask import Blueprint,jsonify,g
from controllers.like_controller import LikeController


like_bp = Blueprint('like_bp', __name__)

@like_bp.route('/likes', methods=['POST'])
def add_like():
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    return LikeController.insert_like()

@like_bp.route('/likes', methods=['DELETE'])
def remove_like():
    if g.user is None:
        return jsonify({'error':'Log in required'}), 401
    return LikeController.delete_like()