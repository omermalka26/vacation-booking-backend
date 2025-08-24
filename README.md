# Vacation Booking API

Backend API for a vacation booking system built with Flask and JWT authentication.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will run on `http://localhost:5000`

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. After login/register, you'll receive a token that should be included in the Authorization header for protected routes.

**Format:** `Authorization: Bearer <your-token>`

## API Endpoints

### Authentication

#### POST /login
Login with email and password
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "user@example.com",
    "role_id": 1
  }
}
```

#### POST /register
Register a new user
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "sign up successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "role_id": 1
  }
}
```

#### POST /logout
Logout current user (client-side token removal)

#### GET /me
Get current user information (requires JWT token)

### Users

#### GET /users
Get all users (requires admin role + JWT token)

#### POST /users
Create a new user (requires admin role + JWT token)
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123",
  "role_id": 1
}
```

#### PUT /users/{user_id}
Update user (requires admin role + JWT token)

#### DELETE /users/{user_id}
Delete user (requires admin role + JWT token)

### Vacations

#### GET /vacations
Get all vacations (requires JWT token)

#### POST /vacations
Create a new vacation (requires admin role + JWT token)
```json
{
  "country_id": 1,
  "vacation_description": "Amazing vacation in Italy",
  "vacation_start": "2024-06-01",
  "vacation_end": "2024-06-07",
  "price": 1500.00,
  "picture_file_name": "italy.jpg"
}
```

#### GET /vacations/{vacation_id}
Get specific vacation (requires JWT token)

#### PUT /vacations/{vacation_id}
Update vacation (requires admin role + JWT token)

#### DELETE /vacations/{vacation_id}
Delete vacation (requires admin role + JWT token)

### Countries

#### GET /countries
Get all countries (public - no authentication required)

#### POST /countries
Create a new country (requires admin role + JWT token)

#### GET /countries/{country_id}
Get specific country (public - no authentication required)

#### PUT /countries/{country_id}
Update country (requires admin role + JWT token)

#### DELETE /countries/{country_id}
Delete country (requires admin role + JWT token)

### Likes

#### POST /likes
Like a vacation (requires JWT token)
```json
{
  "vacation_id": 1
}
```

#### DELETE /likes/{vacation_id}
Unlike a vacation (requires JWT token)

## Database Schema

### Users
- user_id (PRIMARY KEY)
- first_name
- last_name
- email (UNIQUE)
- password (hashed)
- role_id (FOREIGN KEY)

### Roles
- role_id (PRIMARY KEY)
- role_name

### Countries
- country_id (PRIMARY KEY)
- country_name
- country_description
- country_picture

### Vacations
- vacation_id (PRIMARY KEY)
- country_id (FOREIGN KEY)
- vacation_description
- vacation_start
- vacation_end
- price
- picture_file_name

### Likes
- like_id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- vacation_id (FOREIGN KEY)

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:3000
- http://127.0.0.1:3000

## JWT Token

- **Expiration:** 24 hours
- **Algorithm:** HS256
- **Header Format:** `Authorization: Bearer <token>`

## Error Responses

All error responses follow this format:
```json
{
  "error": "Error message"
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized (missing or invalid token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 500: Internal Server Error

## Testing with Postman

1. **Register/Login** to get a JWT token
2. **Add Authorization header** to protected routes:
   - Key: `Authorization`
   - Value: `Bearer <your-token>`
3. **Test protected endpoints** like `/me`, `/vacations`, etc.

## Project Structure

```
Project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── decorators/
│   └── auth_decorator.py  # JWT authentication decorators
├── models/               # Database models
├── controllers/          # Business logic
├── routes/              # API endpoints
└── images/              # Static images
```
