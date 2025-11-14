# Frontend-Backend Connection Guide

## ✅ Setup Complete!

Your frontend is now connected to the backend for authentication!

## 🏗️ Architecture Overview

```
Frontend (React + Vite) ←→ Backend (Express + MySQL)
http://localhost:3000      http://localhost:5002
```

## 📁 What Was Created

### 1. API Service (`src/services/api.ts`)
- **loginUser()** - Handles user login
- **signupUser()** - Handles user registration
- **verifyToken()** - Verifies JWT token
- **logoutUser()** - Clears authentication data
- **getAuthToken()** - Retrieves stored token
- **getUserEmail()** - Retrieves stored user email

### 2. Updated Components
- **Login.tsx** - Now calls backend API for authentication
- **Signup.tsx** - Now calls backend API for registration

## 🚀 How to Run Both

### Terminal 1 - Backend
```bash
cd Backend
node server.js
```
Backend runs on: **http://localhost:5002**

### Terminal 2 - Frontend  
```bash
cd Frontend
node node_modules/vite/bin/vite.js
```
Frontend runs on: **http://localhost:3000**

## 🔄 How It Works

### User Signup Flow:
1. User enters email and password in Signup form
2. Frontend calls `signupUser(email, password)`
3. API sends POST request to `http://localhost:5002/api/auth/signup`
4. Backend creates user with hashed password in MySQL
5. Backend returns JWT token
6. Frontend stores token in localStorage
7. User is redirected to login page

### User Login Flow:
1. User enters email and password in Login form
2. Frontend calls `loginUser(email, password)`
3. API sends POST request to `http://localhost:5002/api/auth/login`
4. Backend verifies credentials against MySQL database
5. Backend returns JWT token
6. Frontend stores token in localStorage
7. User is redirected to Chat page

## 🔐 Authentication Data Storage

The app stores authentication data in browser's localStorage:
- **authToken** - JWT token for authenticated requests
- **userEmail** - User's email address

## 📡 API Endpoints

### Signup
```
POST http://localhost:5002/api/auth/signup
Body: { "email": "user@example.com", "password": "password123" }
Response: { "success": true, "data": { "user": {...}, "token": "..." } }
```

### Login
```
POST http://localhost:5002/api/auth/login
Body: { "email": "user@example.com", "password": "password123" }
Response: { "success": true, "data": { "user": {...}, "token": "..." } }
```

### Verify Token
```
GET http://localhost:5002/api/auth/verify
Headers: { "Authorization": "Bearer YOUR_TOKEN" }
Response: { "success": true, "data": { "user": {...} } }
```

## 🧪 Testing the Connection

### Test Signup:
1. Start both frontend and backend
2. Open http://localhost:3000
3. Click "Create Account"
4. Enter email and password
5. Click "Create Account"
6. Check browser console for success message
7. Check MySQL database for new user

### Test Login:
1. Go to login page
2. Enter registered email and password
3. Click "Sign In"
4. Should redirect to Chat page if successful
5. Check browser console for login data

### Verify in MySQL:
```sql
USE auth_db;
SELECT * FROM users;
```

## 🐛 Troubleshooting

### CORS Error?
Make sure backend server.js has CORS enabled for http://localhost:3000

### Connection Refused?
- Check if backend is running on port 5002
- Check if frontend is running on port 3000

### 401 Unauthorized?
- Check if email/password are correct
- Check if user exists in database

### Token not saved?
- Check browser's localStorage in DevTools (F12 → Application → Local Storage)

## 🔒 Security Features

✅ Password hashing with bcryptjs
✅ JWT token authentication  
✅ HTTP-only secure token storage
✅ Input validation on both frontend and backend
✅ SQL injection prevention with parameterized queries

## 📝 Next Steps

You can now:
1. Use the token for authenticated API requests
2. Add protected routes in frontend
3. Add user profile features
4. Implement password reset
5. Add email verification

## 💡 Tips

- Always keep backend running when testing login/signup
- Check browser console for detailed error messages
- Use browser DevTools Network tab to inspect API calls
- Check MySQL database to verify users are being created
