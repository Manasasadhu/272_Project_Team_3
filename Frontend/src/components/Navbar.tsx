import '../styles/Navbar.css';

interface NavbarProps {
  onLogoClick: () => void;
  onSignIn: () => void;
  onSignUp: () => void;
  onHowItWorks?: () => void;
  currentPage?: 'landing' | 'login' | 'signup' | 'chat';
}

export default function Navbar({ onLogoClick, onSignIn, onSignUp, onHowItWorks, currentPage }: NavbarProps) {
  return (
    <header className="navbar">
      <div className="navbar-content">
        <button onClick={onLogoClick} className="navbar-logo">
          <h1>
            <span className="logo-goal">Goal-Oriented</span>
            {' '}
            <span className="logo-research">Research Synthesis</span>
            {' '}
            <span className="logo-agent">Agent</span>
          </h1>
        </button>
        <nav className="navbar-menu">
          {currentPage !== 'chat' && onHowItWorks && (
            <button onClick={onHowItWorks} className="navbar-link navbar-button">How It Works</button>
          )}
          {currentPage !== 'login' && currentPage !== 'chat' && (
            <button onClick={onSignIn} className="navbar-link navbar-button">
              Sign In
            </button>
          )}
          {currentPage !== 'signup' && currentPage !== 'chat' && (
            <button onClick={onSignUp} className="navbar-button navbar-signup-btn">
              Sign Up
            </button>
          )}
        </nav>
      </div>
    </header>
  );
}
