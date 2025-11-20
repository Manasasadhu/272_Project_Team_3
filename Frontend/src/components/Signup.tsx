import { useState } from "react";
import { Eye, EyeOff, ArrowLeft } from "lucide-react";
import Navbar from "./Navbar";
import "../styles/Signup.css";

interface SignupPageProps {
  onBackToLogin: () => void;
  onLogoClick: () => void;
  onSignupSuccess: (email: string) => void;
}

export default function Signup({
  onBackToLogin,
  onLogoClick,
  onSignupSuccess,
}: SignupPageProps) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccessOptions, setShowSuccessOptions] = useState(false);

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};

    // Relaxed email validation - accepts any valid email format (.com, .edu, .org, etc.)
    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Please enter a valid email address";
    }
    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 5) {
      newErrors.password = "Password must be at least 5 characters";
    } else if (!/[A-Z]/.test(formData.password)) {
      newErrors.password = "Password must include at least one capital letter";
    } else if (!/[0-9]/.test(formData.password)) {
      newErrors.password = "Password must include at least one number";
    } else if (!/[!@#$%^&*(),.?":{}|<>]/.test(formData.password)) {
      newErrors.password = "Password must include at least one special character";
    }
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = "Please confirm your password";
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
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
        [name]: "",
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      setIsLoading(true);
      const API_BASE_URL = window.location.hostname === 'localhost' 
        ? 'http://localhost:8080'
        : `http://${window.location.hostname}:8080`;

      try {
        const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            email: formData.email, 
            password: formData.password 
          }),
        });

        const data = await response.json();

        if (response.ok && data.success) {
          console.log("Signup successful:", formData.email);
          setShowSuccessOptions(true);
        } else {
          setErrors({ email: data.message || 'Signup failed. Please try again.' });
        }
      } catch (error) {
        console.error('Signup error:', error);
        setErrors({ email: 'Unable to connect to server. Please try again.' });
      } finally {
        setIsLoading(false);
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
          {showSuccessOptions ? (
            <>
              <div className="success-icon">✓</div>
              <h1 className="signup-title">Account Created!</h1>
              <p className="signup-subtitle">Your account has been successfully created.</p>
              
              <div className="success-options">
                <button 
                  onClick={() => onSignupSuccess(formData.email)}
                  className="start-review-btn"
                >
                  Start New Review
                </button>
                <button 
                  onClick={onBackToLogin}
                  className="back-to-login-btn"
                >
                  Sign In Later
                </button>
              </div>
            </>
          ) : (
            <>
              <button onClick={onLogoClick} className="back-to-home-btn">
                <ArrowLeft size={20} />
                <span>Back to Home</span>
              </button>
              <h1 className="signup-title">Create Account</h1>
              <p className="signup-subtitle">Join us today</p>

              <form onSubmit={handleSubmit} className="signup-form">
                {/* Email Field */}
                <div className="form-group">
                  <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    className={`form-input ${errors.email ? "error" : ""}`}
                  />
                  {formData.email && !formData.email.includes("@") && (
                    <p className="email-hint">
                      Email must include @
                    </p>
                  )}
                  {errors.email && (
                    <span className="error-message">{errors.email}</span>
                  )}
                </div>

                {/* Password Field */}
                <div className="form-group">
                  <p className="password-hint">
                    Password must be at least 5 characters and include: 1 capital letter, 1 number, and 1 special character
                  </p>
                  <div className="password-group">
                    <input
                      type={showPassword ? "text" : "password"}
                      name="password"
                      placeholder="Password"
                      value={formData.password}
                      onChange={handleChange}
                      className={`form-input ${errors.password ? "error" : ""}`}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="password-toggle"
                      aria-label="Toggle password visibility"
                    >
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                  {errors.password && (
                    <span className="error-message">{errors.password}</span>
                  )}
                </div>

                {/* Confirm Password Field */}
                <div className="form-group">
                  <div className="password-group">
                    <input
                      type={showConfirmPassword ? "text" : "password"}
                      name="confirmPassword"
                      placeholder="Confirm Password"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      className={`form-input ${
                        errors.confirmPassword ? "error" : ""
                      }`}
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="password-toggle"
                      aria-label="Toggle confirm password visibility"
                    >
                      {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                  {errors.confirmPassword && (
                    <span className="error-message">{errors.confirmPassword}</span>
                  )}
                </div>

                {/* Sign Up Button */}
                <button type="submit" className="sign-up-btn" disabled={isLoading}>
                  {isLoading ? 'Creating Account...' : 'Create Account'}
                </button>

                {/* Back to Login Link */}
                <p className="back-to-login">
                  Already have an account?{" "}
                  <button
                    type="button"
                    onClick={onBackToLogin}
                    className="back-link"
                  >
                    Sign In
                  </button>
                </p>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}