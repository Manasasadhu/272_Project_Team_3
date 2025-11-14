import { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import Navbar from './Navbar';
import { signupUser } from '../services/api';
import '../styles/Signup.css';

interface SignupPageProps {
  onBackToLogin: () => void;
  onLogoClick: () => void;
}

export default function Signup({ onBackToLogin, onLogoClick }: SignupPageProps) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError('');
    
    if (validateForm()) {
      setLoading(true);
      
      try {
        const result = await signupUser(formData.email, formData.password);
        
        if (result.success) {
          console.log('Signup successful:', result.data);
          alert('Account created successfully!');
          onBackToLogin(); // Redirect to login page
        } else {
          setApiError(result.message || 'Signup failed. Please try again.');
        }
      } catch (err) {
        setApiError('An unexpected error occurred. Please try again.');
        console.error('Signup error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="signup-page">
      <Navbar 
        onLogoClick={onLogoClick} 
        onSignIn={onBackToLogin} 
        onSignUp={() => {}}
        currentPage="signup"
      />
      <div className="signup-container">
        <div className="signup-card">
        <h1 className="signup-title">Create Account</h1>
        <p className="signup-subtitle">Join us today</p>

        <form onSubmit={handleSubmit} className="signup-form">
          {/* API Error Message */}
          {apiError && (
            <div className="error-banner" style={{
              padding: '10px',
              marginBottom: '15px',
              backgroundColor: '#fee',
              border: '1px solid #fcc',
              borderRadius: '4px',
              color: '#c33',
              fontSize: '14px'
            }}>
              {apiError}
            </div>
          )}

          {/* Email Field */}
          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              className={`form-input ${errors.email ? 'error' : ''}`}
            />
            {errors.email && (
              <span className="error-message">{errors.email}</span>
            )}
          </div>

          {/* Password Field */}
          <div className="form-group password-group">
            <input
              type={showPassword ? 'text' : 'password'}
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className={`form-input ${errors.password ? 'error' : ''}`}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="password-toggle"
              aria-label="Toggle password visibility"
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
            {errors.password && (
              <span className="error-message">{errors.password}</span>
            )}
          </div>

          {/* Confirm Password Field */}
          <div className="form-group password-group">
            <input
              type={showConfirmPassword ? 'text' : 'password'}
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className={`form-input ${errors.confirmPassword ? 'error' : ''}`}
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="password-toggle"
              aria-label="Toggle confirm password visibility"
            >
              {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
            {errors.confirmPassword && (
              <span className="error-message">{errors.confirmPassword}</span>
            )}
          </div>

          {/* Sign Up Button */}
          <button type="submit" className="sign-up-btn" disabled={loading}>
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>

          {/* Back to Login Link */}
          <p className="back-to-login">
            Already have an account?{' '}
            <button type="button" onClick={onBackToLogin} className="back-link">
              Sign In
            </button>
          </p>
        </form>
      </div>
    </div>
    </div>
  );
}
