# Vacation Booking API

Backend API for a vacation booking system built with Flask.

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

#### POST /logout
Logout current user

#### GET /me
Get current user information (requires authentication)

### Users

#### GET /users
Get all users (requires admin role)

#### POST /users
Create a new user (requires admin role)
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
Update user (requires admin role)

#### DELETE /users/{user_id}
Delete user (requires admin role)

### Vacations

#### GET /vacations
Get all vacations (requires authentication)

#### POST /vacations
Create a new vacation (requires admin role)
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
Get specific vacation (requires authentication)

#### PUT /vacations/{vacation_id}
Update vacation (requires admin role)

#### DELETE /vacations/{vacation_id}
Delete vacation (requires admin role)

### Countries

#### GET /countries
Get all countries

#### POST /countries
Create a new country (requires admin role)

#### GET /countries/{country_id}
Get specific country

#### PUT /countries/{country_id}
Update country (requires admin role)

#### DELETE /countries/{country_id}
Delete country (requires admin role)

### Likes

#### POST /likes
Like a vacation (requires authentication)
```json
{
  "vacation_id": 1
}
```

#### DELETE /likes/{vacation_id}
Unlike a vacation (requires authentication)

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
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
