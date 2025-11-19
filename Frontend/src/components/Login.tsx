import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import Navbar from "./Navbar";
import "../styles/Login.css";

interface LoginPageProps {
  onCreateAccount: () => void;
  onLogoClick: () => void;
  onLoginSuccess: (email: string) => void;
}

export default function Login({
  onCreateAccount,
  onLogoClick,
  onLoginSuccess,
}: LoginPageProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: { email?: string; password?: string } = {};

    if (!email.trim()) {
      newErrors.email = "Email is required";
    }
    if (!password.trim()) {
      newErrors.password = "Password is required";
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      setIsLoading(true);
      const API_BASE_URL = window.location.hostname === 'localhost' 
        ? 'http://localhost:8080'
        : `http://${window.location.hostname}:8080`;

      try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok && data.success) {
          console.log("Login successful:", email);
          if (rememberMe) {
            localStorage.setItem('userEmail', email);
          }
          onLoginSuccess(email);
        } else {
          setErrors({ email: data.message || 'Invalid credentials' });
        }
      } catch (error) {
        console.error('Login error:', error);
        setErrors({ email: 'Unable to connect to server. Please try again.' });
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="login-page">
      <Navbar
        onLogoClick={onLogoClick}
        onSignIn={() => {}}
        onSignUp={onCreateAccount}
        currentPage="login"
      />
      <div className="login-container">
        <div className="login-card">
          <h1 className="login-title">Sign In</h1>
          <p className="login-subtitle">Enter your credentials to continue</p>

          <form onSubmit={handleSubmit} className="login-form">
            {/* Email Field */}
            <div className="form-group">
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  if (errors.email) setErrors(prev => ({ ...prev, email: undefined }));
                }}
                className={`form-input ${errors.email ? "error" : ""}`}
              />
              {errors.email && (
                <span className="error-message">{errors.email}</span>
              )}
            </div>

            {/* Password Field */}
            <div className="form-group password-group">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (errors.password) setErrors(prev => ({ ...prev, password: undefined }));
                }}
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
              {errors.password && (
                <span className="error-message">{errors.password}</span>
              )}
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="form-options">
              <label className="remember-me">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="checkbox"
                />
                <span>Remember me</span>
              </label>
              <a href="#" className="forgot-password">
                Forgot password?
              </a>
            </div>

            {/* Sign In Button */}
            <button type="submit" className="sign-in-btn" disabled={isLoading}>
              {isLoading ? 'Signing In...' : 'Sign In'}
            </button>

            {/* Create Account Link */}
            <p className="create-account">
              Don't have an account?{" "}
              <button
                type="button"
                onClick={onCreateAccount}
                className="create-link"
              >
                Create one
              </button>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
