# Weather App with CRUD Operations

A Django-based weather application that provides weather information and supports CRUD operations for locations, weather records, and user favorites.

## Features

- Weather information retrieval
- User authentication
- CRUD operations for:
  - Locations
  - Weather Records
  - User Favorites
- RESTful API endpoints
- JWT authentication

## API Documentation

All API endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

### Locations API

#### List Locations
- **Method**: GET
- **URL**: `/weather/api/locations/`
- **Query Parameters**:
  - `name`: Filter locations by name (optional)
- **Response**:
```json
[
    {
        "id": 1,
        "name": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "country": "USA",
        "created_at": "2024-03-15T10:00:00Z",
        "updated_at": "2024-03-15T10:00:00Z"
    }
]
```

#### Create Location
- **Method**: POST
- **URL**: `/weather/api/locations/`
- **Request Body**:
```json
{
    "name": "New York",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "country": "USA"
}
```

#### Get Location
- **Method**: GET
- **URL**: `/weather/api/locations/{id}/`

#### Update Location
- **Method**: PUT/PATCH
- **URL**: `/weather/api/locations/{id}/`

#### Delete Location
- **Method**: DELETE
- **URL**: `/weather/api/locations/{id}/`

### Weather Records API

#### List Weather Records
- **Method**: GET
- **URL**: `/weather/api/weather-records/`
- **Query Parameters**:
  - `location_id`: Filter by location (optional)
- **Response**:
```json
[
    {
        "id": 1,
        "location": 1,
        "location_name": "New York",
        "temperature": 20.5,
        "humidity": 65,
        "pressure": 1013,
        "wind_speed": 5.2,
        "description": "Clear sky",
        "recorded_at": "2024-03-15T10:00:00Z",
        "created_at": "2024-03-15T10:00:00Z",
        "updated_at": "2024-03-15T10:00:00Z"
    }
]
```

#### Create Weather Record
- **Method**: POST
- **URL**: `/weather/api/weather-records/`
- **Request Body**:
```json
{
    "location": 1,
    "temperature": 20.5,
    "humidity": 65,
    "pressure": 1013,
    "wind_speed": 5.2,
    "description": "Clear sky",
    "recorded_at": "2024-03-15T10:00:00Z"
}
```

#### Get Weather Record
- **Method**: GET
- **URL**: `/weather/api/weather-records/{id}/`

#### Update Weather Record
- **Method**: PUT/PATCH
- **URL**: `/weather/api/weather-records/{id}/`

#### Delete Weather Record
- **Method**: DELETE
- **URL**: `/weather/api/weather-records/{id}/`

### User Favorites API

#### List User Favorites
- **Method**: GET
- **URL**: `/weather/api/favorites/`
- **Response**:
```json
[
    {
        "id": 1,
        "user": 1,
        "user_username": "john_doe",
        "location": 1,
        "location_details": {
            "id": 1,
            "name": "New York",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "country": "USA"
        },
        "created_at": "2024-03-15T10:00:00Z",
        "updated_at": "2024-03-15T10:00:00Z"
    }
]
```

#### Add Favorite
- **Method**: POST
- **URL**: `/weather/api/favorites/`
- **Request Body**:
```json
{
    "location": 1
}
```

#### Get Favorite
- **Method**: GET
- **URL**: `/weather/api/favorites/{id}/`

#### Remove Favorite
- **Method**: DELETE
- **URL**: `/weather/api/favorites/{id}/`

#### Toggle Favorite
- **Method**: POST
- **URL**: `/weather/api/favorites/{location_id}/toggle_favorite/`

#### List My Favorites
- **Method**: GET
- **URL**: `/weather/api/favorites/my_favorites/`

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 200: Success
- 201: Created
- 204: No Content (for successful deletion)
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error Response Format:
```json
{
    "error": "Error message description"
}
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To get a token:

1. Register a user at `/auth/register/`
2. Login at `/auth/login/` to receive your JWT token
3. Include the token in subsequent requests in the Authorization header

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