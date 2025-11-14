// API Configuration
const API_BASE_URL = 'http://localhost:5002/api';

// API Response Types
export interface AuthResponse {
  success: boolean;
  message: string;
  data?: {
    user: {
      id: number;
      email: string;
    };
    token: string;
  };
  error?: string;
}

// Login API Call
export const loginUser = async (email: string, password: string): Promise<AuthResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'Login failed');
    }

    // Store token in localStorage
    if (data.data?.token) {
      localStorage.setItem('authToken', data.data.token);
      localStorage.setItem('userEmail', data.data.user.email);
    }

    return data;
  } catch (error) {
    console.error('Login error:', error);
    return {
      success: false,
      message: error instanceof Error ? error.message : 'An error occurred during login',
    };
  }
};

// Signup API Call
export const signupUser = async (email: string, password: string): Promise<AuthResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'Signup failed');
    }

    // Store token in localStorage
    if (data.data?.token) {
      localStorage.setItem('authToken', data.data.token);
      localStorage.setItem('userEmail', data.data.user.email);
    }

    return data;
  } catch (error) {
    console.error('Signup error:', error);
    return {
      success: false,
      message: error instanceof Error ? error.message : 'An error occurred during signup',
    };
  }
};

// Verify Token API Call
export const verifyToken = async (): Promise<AuthResponse> => {
  try {
    const token = localStorage.getItem('authToken');
    
    if (!token) {
      throw new Error('No token found');
    }

    const response = await fetch(`${API_BASE_URL}/auth/verify`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'Token verification failed');
    }

    return data;
  } catch (error) {
    console.error('Token verification error:', error);
    return {
      success: false,
      message: error instanceof Error ? error.message : 'An error occurred during verification',
    };
  }
};

// Logout
export const logoutUser = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('userEmail');
};

// Get stored token
export const getAuthToken = (): string | null => {
  return localStorage.getItem('authToken');
};

// Get stored user email
export const getUserEmail = (): string | null => {
  return localStorage.getItem('userEmail');
};
