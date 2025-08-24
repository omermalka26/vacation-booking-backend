from flask import jsonify, request, g 
from models.like import Like          
from models.vacation import Vacation  
class LikeController:
    @staticmethod
    def insert_like():
        user_id = g.user['user_id'] 

        data = request.get_json()
        if not data or 'vacation_id' not in data:
            return jsonify({'error': 'Missing required field: vacation_id.'}), 400

        try:
            vacation_id = int(data['vacation_id'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid vacation_id format.'}), 400

        if not Vacation.get_by_id(vacation_id):
            return jsonify({'error': 'Vacation not found.'}), 404

        result = Like.insert(user_id=user_id, vacation_id=vacation_id)

        if 'error' in result:
           
            if 'User has already liked this vacation' in result['error']:
                return jsonify(result), 409 
            elif 'Invalid User ID or Vacation ID' in result['error']:
                return jsonify(result), 404 
            else:
                return jsonify(result), 500 
        
        return jsonify(result), 201 

    @staticmethod
    def delete_like():
        user_id = g.user['user_id'] 

        data = request.get_json()
        if not data or 'vacation_id' not in data:
            return jsonify({'error': 'Missing required field: vacation_id.'}), 400

        try:
            vacation_id = int(data['vacation_id'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid vacation_id format.'}), 400
        
        result = Like.delete(user_id=user_id, vacation_id=vacation_id)

        if 'error' in result:
            if 'Like not found' in result['error']:
                return jsonify(result), 404 
            else:
                return jsonify(result), 500 
        
        return jsonify(result), 200 