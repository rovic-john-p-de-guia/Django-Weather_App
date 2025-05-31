# Django Weather App

A simple weather application built with Django that allows users to search for locations and view current weather information.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenWeatherMap API key:
```
OPENWEATHER_API_KEY=your_api_key_here
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 to use the application.

## Features
- Search for weather by location
- View current weather conditions
- Responsive design
- Error handling for invalid locations
- User authentication with JWT tokens

## Authentication API Endpoints

### 1. Register User
- **Method**: POST
- **URL**: `/api/auth/register/`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password2": "securepassword123"
  }
  ```

### 2. Login
- **Method**: POST
- **URL**: `/api/auth/login/`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
    "username": "testuser",
    "password": "securepassword123"
  }
  ```

### 3. Refresh Token
- **Method**: POST
- **URL**: `/api/auth/token/refresh/`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
    "refresh": "your_refresh_token"
  }
  ```

### 4. Protected Route
- **Method**: GET
- **URL**: `/api/auth/protected/`
- **Headers**: 
  ```
  Authorization: Bearer your_access_token
  ``` 

## Rate Limiting

All authentication endpoints are protected by a custom rate limiting mechanism:
- **Limit:** 5 requests per minute per user (or per IP if not authenticated)
- **Exceeded Limit:** Returns HTTP 429 Too Many Requests

**Sample 429 Response:**
```json
{
  "error": "Rate limit exceeded. Try again later."
}
```

**Rate-limited Endpoints:**
- `POST /auth/api/register/`
- `POST /auth/api/login/`
- `GET /auth/api/protected/`

**Headers:**
- For authenticated requests: `Authorization: Bearer <your_access_token>`
- For unauthenticated requests: No special header required

**Example:**
If you make more than 5 requests to any of the above endpoints within 60 seconds, you will receive a 429 error as shown above. 