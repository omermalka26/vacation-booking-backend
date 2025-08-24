from flask import jsonify, request
from models.country import Country

class CountryController:
    @staticmethod
    def insert_country():
        data = request.get_json()
        if 'country_name' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        result = Country.insert(
           country_name=data['country_name']
        )
        
        if result is None:
            return jsonify({'error': 'Country name already exists'}), 400
        return jsonify(result), 201
    
    @staticmethod
    def get_all_countries():
        countries = Country.get_all()
        return jsonify({'countries': countries})
    
    @staticmethod
    def get_country(country_id):
        country = Country.get_by_id(country_id)
        if country is None:
            return jsonify({'error': 'Country not found'}), 404
        return jsonify(country)
    
    @staticmethod
    def update_country(country_id):
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result = Country.update(country_id, **data)
        if result is None:
            return jsonify({'error': 'Country not found or update failed'}), 404
        return jsonify(result)
    
    @staticmethod
    def delete_country(country_id):
        result = Country.delete(country_id)
        if result is None:
            return jsonify({'error': 'Country not found'}), 404
        return jsonify(result)