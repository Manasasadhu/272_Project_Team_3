# Quick Start Guide

## ✅ Backend is Ready!

Your backend API with authentication is now set up. Here's what you need to do:

## 📋 Prerequisites
- MySQL server installed and running
- Node.js installed

## 🚀 Steps to Run

### 1. Set up the Database
You need to create the database and table. Run this command:

```bash
mysql -u root -p < database/schema.sql
```

Or manually create it:
```sql
CREATE DATABASE IF NOT EXISTS auth_db;
USE auth_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_email (email)
);
```

### 2. Configure Environment Variables
Edit the `.env` file with your MySQL credentials:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=auth_db
JWT_SECRET=your_secret_key_change_this
PORT=5000
```

### 3. Start the Server
```bash
# Development mode (auto-reload)
npm run dev

# Or production mode
npm start
```

The server will run on `http://localhost:5000`

## 📡 API Endpoints

### Signup
```bash
POST http://localhost:5000/api/auth/signup
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123",
  "name": "Test User"
}
```

### Login
```bash
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

### Verify Token
```bash
GET http://localhost:5000/api/auth/verify
Authorization: Bearer YOUR_JWT_TOKEN
```

## 🧪 Test with curl

### Test Signup:
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","name":"Test User"}'
```

### Test Login:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## 🔧 Troubleshooting

**MySQL Connection Error?**
- Make sure MySQL is running
- Check your credentials in `.env`
- Verify the database exists

**Port already in use?**
- Change the PORT in `.env` file
- Or stop the process using port 5000

## 📁 Project Structure
```
Backend/
├── config/
│   └── database.js       # Database connection
├── database/
│   └── schema.sql        # Database schema
├── models/
│   └── User.js          # User model
├── routes/
│   └── auth.js          # Authentication routes
├── server.js            # Main server file
├── .env                 # Environment variables
└── package.json         # Dependencies
```
