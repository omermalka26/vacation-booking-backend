from flask import jsonify, request
from models.vacation import Vacation
from datetime import datetime, date # Needed for date validation


class VacationController:
    @staticmethod
    def insert_vacation():
        data = request.get_json()

        # --- 1. Check for missing required fields ---
        required_fields = [
            'country_id', 'vacation_description', 'vacation_start',
            'vacation_end', 'price', 'picture_file_name'
        ]
        for field in required_fields:
            # Check if field is missing or if its value is None or an empty string
            if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
                return jsonify({'error': f"Missing or empty required field: '{field}'"}), 400

        # --- 2. Price validation ---
        try:
            # Convert price to float immediately for validation and consistency
            price_val = float(data['price']) 
            if not (0 <= price_val <= 10000):
                return jsonify({'error': 'Price must be a positive number and not exceed 10,000.'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Price must be a valid number.'}), 400

        # --- 3. Date format validation and conversion ---
        vacation_start_str = data['vacation_start']
        vacation_end_str = data['vacation_end']

        try:
            start_date_obj = datetime.strptime(vacation_start_str, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(vacation_end_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Vacation dates must be in YYYY-MM-DD format.'}), 400

        # --- 4. Check if end date is before start date ---
        if end_date_obj < start_date_obj:
            return jsonify({'error': 'Vacation end date cannot be before the start date.'}), 400

        # --- 5. Check if start date is in the past ---
        today = date.today()
        if start_date_obj < today:
            return jsonify({'error': 'Vacation start date cannot be in the past.'}), 400

        # --- If all validations pass, call the cleaner insert function in the model ---
        # Pass the original string dates, as the model's SQL expects them that way
        result = Vacation.insert(
            country_id=data['country_id'],
            vacation_description=data['vacation_description'],
            vacation_start=vacation_start_str,
            vacation_end=vacation_end_str,
            price=price_val,
            picture_file_name=data['picture_file_name']
        )

        # --- Handle the model's return (success or database-level error) ---
        if 'error' in result:
            # For database-level errors (e.g., IntegrityError), a 409 Conflict or 500 Internal Server Error is appropriate
            return jsonify(result), 409 # Using 409 for conflicts/database errors
        else:
            return jsonify(result), 201 # 201 Created for successful insertion

    
    @staticmethod
    def get_all_vacations():
        vacations = Vacation.get_all()
        return jsonify({'vacations': vacations})
    
    @staticmethod
    def get_vacation(vacation_id):
        vacation = Vacation.get_by_id(vacation_id)
        if vacation is None:
            return jsonify({'error': 'Vacation not found'}), 404
        return jsonify(vacation)
    
    @staticmethod
    def update_vacation(vacation_id):
        data = request.get_json()

        
        required_fields = [
            'country_id',
            'vacation_description',
            'vacation_start',
            'vacation_end',
            'price'
           
        ]

        for field in required_fields:
            if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
                return jsonify({'error': f"Missing or empty required field for update: '{field}'. All fields except 'picture_file_name' must be provided."}), 400

      
        try:
            price_val = float(data['price'])
            if not (0 <= price_val <= 10000):
                return jsonify({'error': 'Price must be a positive number and not exceed 10,000.'}), 400
            data['price'] = price_val
        except (ValueError, TypeError):
            return jsonify({'error': 'Price must be a valid number.'}), 400

        
        vacation_start_str = data['vacation_start']
        vacation_end_str = data['vacation_end']

        try:
            start_date_obj = datetime.strptime(vacation_start_str, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(vacation_end_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Vacation dates must be in YYYY-MM-DD format.'}), 400

        
        if end_date_obj < start_date_obj:
            return jsonify({'error': 'Vacation end date cannot be before the start date.'}), 400

        
        today = date.today()
        if start_date_obj < today:
            return jsonify({'error': 'Vacation start date cannot be in the past.'}), 400
        
      
        result = Vacation.update(vacation_id, **data)
        
       
        if 'error' in result:
           
            if "Vacation not found" in result['error']:
                return jsonify(result), 404 
           
            return jsonify(result), 409
        return jsonify(result)


    
    @staticmethod
    def delete_vacation(vacation_id):
        result = Vacation.delete(vacation_id)
        if result is None:
            return jsonify({'error': 'Vacation not found'}), 404
        return jsonify(result)