from flask import jsonify, request
from models.vacation import Vacation
from datetime import datetime, date # Needed for date validation
from constants import MAX_PRICE, MIN_PRICE
import os
from werkzeug.utils import secure_filename


class VacationController:
    @staticmethod
    def insert_vacation():
        # Check if this is a multipart form data request (file upload)
        if request.content_type and 'multipart/form-data' in request.content_type:
            return VacationController.insert_vacation_with_file()
        
        # Regular JSON request
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
            if not (MIN_PRICE <= price_val <= MAX_PRICE):
                return jsonify({'error': f'Price must be a positive number and not exceed {MAX_PRICE}.'}), 400
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

        # --- 5. Check if start date is in the past (only for new vacations) ---
        # For updates, we allow past dates since vacations might already have started
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
    def insert_vacation_with_file():
        """Handle vacation creation with file upload"""
        try:
            # Get form data
            vacation_description = request.form.get('vacation_description')
            country_id = request.form.get('country_id')
            vacation_start = request.form.get('vacation_start')
            vacation_end = request.form.get('vacation_end')
            price = request.form.get('price')
            
            # Check required fields
            if not all([vacation_description, country_id, vacation_start, vacation_end, price]):
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Handle file upload
            if 'image' not in request.files:
                return jsonify({'error': 'No image file provided'}), 400
            
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No image file selected'}), 400
            
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            
            # Ensure images directory exists
            images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
            os.makedirs(images_dir, exist_ok=True)
            
            # Save the file
            file_path = os.path.join(images_dir, filename)
            file.save(file_path)
            
            # Validate price
            try:
                price_val = float(price)
                if not (MIN_PRICE <= price_val <= MAX_PRICE):
                    return jsonify({'error': f'Price must be a positive number and not exceed {MAX_PRICE}.'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Price must be a valid number.'}), 400
            
            # Validate dates
            try:
                start_date_obj = datetime.strptime(vacation_start, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(vacation_end, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Vacation dates must be in YYYY-MM-DD format.'}), 400
            
            if end_date_obj < start_date_obj:
                return jsonify({'error': 'Vacation end date cannot be before the start date.'}), 400
            
            today = date.today()
            if start_date_obj < today:
                return jsonify({'error': 'Vacation start date cannot be in the past.'}), 400
            
            # Insert into database
            result = Vacation.insert(
                country_id=int(country_id),
                vacation_description=vacation_description,
                vacation_start=vacation_start,
                vacation_end=vacation_end,
                price=price_val,
                picture_file_name=filename
            )
            
            if 'error' in result:
                return jsonify(result), 409
            else:
                return jsonify(result), 201
                
        except Exception as e:
            return jsonify({'error': f'Error processing file upload: {str(e)}'}), 500

    
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
        # Check if this is a multipart form data request (file upload)
        if request.content_type and 'multipart/form-data' in request.content_type:
            return VacationController.update_vacation_with_file(vacation_id)
        
        # Regular JSON request
        data = request.get_json()
        print(f"Update vacation {vacation_id} with data: {data}")  # Debug logging

        
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
            if not (MIN_PRICE <= price_val <= MAX_PRICE):
                return jsonify({'error': f'Price must be a positive number and not exceed {MAX_PRICE}.'}), 400
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

        # For updates, we allow past dates since vacations might already have started
        # No need to check if start date is in the past for updates
        
        result = Vacation.update(vacation_id, **data)
        
       
        if 'error' in result:
           
            if "Vacation not found" in result['error']:
                return jsonify(result), 404 
           
            return jsonify(result), 409
        return jsonify(result)

    @staticmethod
    def update_vacation_with_file(vacation_id):
        """Handle vacation update with file upload"""
        try:
            # Get form data
            vacation_description = request.form.get('vacation_description')
            country_id = request.form.get('country_id')
            vacation_start = request.form.get('vacation_start')
            vacation_end = request.form.get('vacation_end')
            price = request.form.get('price')
            
            # Check required fields
            if not all([vacation_description, country_id, vacation_start, vacation_end, price]):
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Handle file upload
            if 'image' not in request.files:
                return jsonify({'error': 'No image file provided'}), 400
            
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No image file selected'}), 400
            
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            
            # Ensure images directory exists
            images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
            os.makedirs(images_dir, exist_ok=True)
            
            # Save the file
            file_path = os.path.join(images_dir, filename)
            file.save(file_path)
            
            # Validate price
            try:
                price_val = float(price)
                if not (MIN_PRICE <= price_val <= MAX_PRICE):
                    return jsonify({'error': f'Price must be a positive number and not exceed {MAX_PRICE}.'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Price must be a valid number.'}), 400
            
            # Validate dates
            try:
                start_date_obj = datetime.strptime(vacation_start, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(vacation_end, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Vacation dates must be in YYYY-MM-DD format.'}), 400
            
            if end_date_obj < start_date_obj:
                return jsonify({'error': 'Vacation end date cannot be before the start date.'}), 400
            
            # Update in database with new filename
            result = Vacation.update(vacation_id, 
                country_id=int(country_id),
                vacation_description=vacation_description,
                vacation_start=vacation_start,
                vacation_end=vacation_end,
                price=price_val,
                picture_file_name=filename
            )
            
            if 'error' in result:
                if "Vacation not found" in result['error']:
                    return jsonify(result), 404
                return jsonify(result), 409
            else:
                return jsonify(result)
                
        except Exception as e:
            return jsonify({'error': f'Error processing file upload: {str(e)}'}), 500

    
    @staticmethod
    def delete_vacation(vacation_id):
        result = Vacation.delete(vacation_id)
        if result is None:
            return jsonify({'error': 'Vacation not found'}), 404
        return jsonify(result)

    @staticmethod
    def get_user_liked_vacations():
        from decorators.auth_decorator import g
        user_id = g.user['user_id']
        liked_vacations = Vacation.get_user_liked_vacations(user_id)
        return jsonify({'liked_vacations': liked_vacations})