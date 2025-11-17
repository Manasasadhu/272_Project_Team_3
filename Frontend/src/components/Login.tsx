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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email && password) {
      console.log("Login attempt:", email);
      onLoginSuccess(email);
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
                onChange={(e) => setEmail(e.target.value)}
                className="form-input"
                required
              />
            </div>

            {/* Password Field */}
            <div className="form-group password-group">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
                required
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
            <button type="submit" className="sign-in-btn">
              Sign In
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
