# Backend API Documentation

## Overview
This is a Node.js/Express backend with MySQL database for user authentication.

## Setup Instructions

### 1. Install Dependencies
```bash
cd Backend
npm install
```

### 2. Configure Database
1. Make sure MySQL is installed and running
2. Create the database and table:
```bash
mysql -u root -p < database/schema.sql
```

Or manually run the SQL commands in `database/schema.sql`

### 3. Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Update the values in `.env`:
```
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=auth_db
JWT_SECRET=your_secret_key_here
PORT=5000
```

### 4. Start the Server
```bash
# Development mode (auto-reload on changes)
npm run dev

# Production mode
npm start
```

## API Endpoints

### 1. Signup
**POST** `/api/auth/signup`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 2. Login
**POST** `/api/auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 3. Verify Token
**GET** `/api/auth/verify`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
}
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Security Features
- Password hashing with bcrypt
- JWT token-based authentication
- CORS configuration
- SQL injection prevention with parameterized queries
- Input validation

## Tech Stack
- Node.js
- Express.js
- MySQL
- bcrypt (password hashing)
- jsonwebtoken (JWT authentication)
- dotenv (environment variables)
