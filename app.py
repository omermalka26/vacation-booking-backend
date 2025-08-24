from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import jwt
from datetime import datetime, timedelta
from models.role import Role
from models.user import User
from models.country import Country
from models.vacation import Vacation
from models.like import Like
from routes.user_routes import user_bp
from routes.role_routes import role_bp
from routes.country_routes import country_bp
from routes.vacation_routes import vacation_bp
from routes.auth_routes import auth_bp
from routes.like_routes import like_bp

app = Flask(__name__)

# Enable CORS for React frontend
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Serve static files (images)
IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

# Use a fixed secret key for development (change in production)
app.config['JWT_SECRET_KEY'] = 'your-super-secret-jwt-key-change-in-production'

# Register the blueprints
app.register_blueprint(user_bp)
app.register_blueprint(role_bp)
app.register_blueprint(country_bp)
app.register_blueprint(vacation_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(like_bp)

# Serve images
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Resource not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500

# Create the database tables
Role.create_table()
User.create_table()
Country.create_table()
Vacation.create_table()
Like.create_table()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 

