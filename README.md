# Vacation Booking System - Backend API

A Flask-based REST API for a vacation booking system with JWT authentication, file uploads, and SQLite database.

## 🚀 Features

- **JWT Authentication**: Secure user authentication and authorization
- **RESTful API**: Complete CRUD operations for vacations
- **File Upload**: Image upload and serving for vacation photos
- **Role-Based Access**: Admin and user role management
- **Like System**: User vacation likes and statistics
- **Database Management**: SQLite with proper schema design

## 🛠️ Tech Stack

- **Backend**: Flask, SQLite, PyJWT
- **Authentication**: JWT tokens with role-based access
- **File Handling**: Werkzeug, Pillow for image processing
- **CORS**: Flask-CORS for cross-origin requests
- **Database**: SQLite with SQLAlchemy-style models

## 📁 Project Structure

```
Project/
├── controllers/          # Business logic layer
│   ├── auth_controller.py
│   ├── vacation_controller.py
│   └── country_controller.py
├── models/              # Database models
│   ├── user.py
│   ├── vacation.py
│   ├── country.py
│   └── like.py
├── routes/              # API endpoints
│   ├── auth_routes.py
│   ├── vacation_routes.py
│   └── country_routes.py
├── decorators/          # Authentication decorators
│   └── auth_decorators.py
├── images/              # Static image files
├── app.py              # Main Flask application
├── constants.py        # Configuration constants
├── requirements.txt    # Python dependencies
└── projectdb.db       # SQLite database
```

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <backend-repo-url>
   cd vacation-booking-backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize database** (if needed):
   ```bash
   python init_roles.py
   python init_countries.py
   ```

6. **Start the server**:
   ```bash
   python app.py
   ```

The API will run on `http://localhost:5000`

## 🔗 Frontend Repository

This backend serves a separate React frontend. You'll need to:

1. **Clone the frontend repository**:
   ```bash
   git clone <frontend-repo-url>
   cd vacation-booking-frontend
   ```

2. **Install dependencies**:
   ```bash
   cd client
   npm install
   ```

3. **Start the frontend**:
   ```bash
   npm start
   ```

The frontend will run on `http://localhost:3000`

## 🔐 Authentication

### Default Admin User
- **Email**: admin@admin.com
- **Password**: admin123

### JWT Token Structure
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "role": "admin",
  "exp": 1234567890
}
```

## 📝 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Vacations
- `GET /vacations` - Get all vacations
- `GET /vacations/:id` - Get specific vacation
- `POST /vacations` - Create vacation (admin only)
- `PUT /vacations/:id` - Update vacation (admin only)
- `DELETE /vacations/:id` - Delete vacation (admin only)
- `GET /vacations/user-likes` - Get user's liked vacations

### Countries
- `GET /countries` - Get all countries

### Likes
- `POST /likes` - Add like to vacation
- `DELETE /likes` - Remove like from vacation

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role_id INTEGER DEFAULT 2
);
```

### Vacations Table
```sql
CREATE TABLE vacations (
    vacation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vacation_description TEXT NOT NULL,
    country_id INTEGER NOT NULL,
    vacation_start DATE NOT NULL,
    vacation_end DATE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    picture_file_name TEXT
);
```

### Countries Table
```sql
CREATE TABLE countries (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT UNIQUE NOT NULL
);
```

### Likes Table
```sql
CREATE TABLE likes (
    like_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    vacation_id INTEGER NOT NULL,
    UNIQUE(user_id, vacation_id)
);
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DATABASE_URL=your-database-url
```

### CORS Configuration
The API is configured to accept requests from:
- `http://localhost:3000` (development)
- Your production frontend domain

## 📁 File Upload

### Image Storage
- Images are stored in the `images/` directory
- Supported formats: JPG, PNG, GIF
- File size limit: 16MB
- Automatic filename generation for security

### Image Serving
Images are served via `/images/<filename>` endpoint for security and performance.

## 🚀 Deployment

### Production Setup
1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   ```

2. **Install production dependencies**:
   ```bash
   pip install gunicorn
   ```

3. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for password security
- **CORS Protection**: Controlled cross-origin access
- **Input Validation**: Comprehensive request validation
- **File Upload Security**: File type and size validation

## 🧪 Testing

### Manual Testing
Use tools like Postman or curl to test endpoints:

```bash
# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@admin.com","password":"admin123"}'

# Get vacations
curl -X GET http://localhost:5000/vacations
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Note**: This is the backend repository. Make sure to also set up the frontend repository for the complete application.
