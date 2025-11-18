import "../styles/Navbar.css";

interface NavbarProps {
  onLogoClick: () => void;
  onSignIn: () => void;
  onSignUp: () => void;
  currentPage?: "landing" | "login" | "signup" | "chat";
}

export default function Navbar({
  onLogoClick,
  onSignIn,
  onSignUp,
  currentPage,
}: NavbarProps) {
  return (
    <header className="navbar">
      <div className="navbar-content">
        <button onClick={onLogoClick} className="navbar-logo">
          <h1>Goal-Oriented Knowledge Discovery Agent</h1>
        </button>
        <nav className="navbar-menu">
          {currentPage !== "login" && currentPage !== "chat" && (
            <button onClick={onSignIn} className="navbar-link navbar-button">
              Sign In
            </button>
          )}
          {currentPage !== "signup" && currentPage !== "chat" && (
            <button
              onClick={onSignUp}
              className="navbar-button navbar-signup-btn"
            >
              Sign Up
            </button>
          )}
        </nav>
      </div>
    </header>
  );
}
