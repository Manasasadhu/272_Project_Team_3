import { ArrowRight } from 'lucide-react';
import Navbar from './Navbar';
import '../styles/Landing.css';

interface LandingPageProps {
  onSignIn: () => void;
  onSignUp: () => void;
}

export default function Landing({ onSignIn, onSignUp }: LandingPageProps) {
  return (
    <div className="landing-container">
      {/* Header Navigation */}
      <Navbar 
        onLogoClick={() => {}} 
        onSignIn={onSignIn} 
        onSignUp={onSignUp}
        currentPage="landing"
      />

      {/* Hero Section */}
      <main className="landing-main">
        <div className="hero-content">
          <div className="hero-left">
            <h2 className="hero-title">Conversational AI for the Modern World</h2>
            <p className="hero-description">
              Experience the next generation of AI chat. Our intelligent assistant is 
              designed to understand your needs, answer your questions, and help you 
              with your tasks, all in a natural and conversational way. Whether you need 
              help with research, brainstorming ideas, or simply want to chat, our AI is 
              here to help.
            </p>
            <button onClick={onSignUp} className="get-started-btn">
              Get Started
              <ArrowRight size={20} />
            </button>
          </div>

          <div className="hero-right">
            <div className="diagram">
              <svg width="700" height="350" viewBox="0 0 700 350" xmlns="http://www.w3.org/2000/svg">
                {/* Define arrowheads */}
                <defs>
                  <marker id="arrowhead-gray" markerWidth="12" markerHeight="12" refX="10" refY="3" orient="auto">
                    <polygon points="0 0, 12 3, 0 6" fill="#999" />
                  </marker>
                </defs>
                
                {/* Arrow from User Request to Agent */}
                <line x1="180" y1="175" x2="260" y2="175" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                
                {/* Arrow from Agent back to User Request */}
                <line x1="260" y1="160" x2="180" y2="160" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                
                {/* Down arrow from Agent to Tools */}
                <path d="M 310 230 L 310 290" stroke="#999" strokeWidth="2.5" fill="none" markerEnd="url(#arrowhead-gray)" />
                
                {/* Arrow from Agent to Planning */}
                <line x1="360" y1="155" x2="500" y2="120" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                
                {/* Arrow from Agent to Memory */}
                <line x1="360" y1="175" x2="500" y2="175" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                
                {/* Arrow from Agent to Tools */}
                <line x1="360" y1="195" x2="500" y2="230" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                
                {/* Return arrow from Planning to Agent */}
                <line x1="500" y1="100" x2="360" y2="155" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                
                {/* Return arrow from Memory to Agent */}
                <line x1="500" y1="175" x2="360" y2="175" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                
                {/* Return arrow from Tools to Agent */}
                <line x1="500" y1="250" x2="360" y2="195" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                
                {/* User Request Box */}
                <rect x="60" y="120" width="120" height="110" rx="15" fill="none" stroke="#FF9944" strokeWidth="2.5"/>
                <text x="120" y="180" fontFamily="Arial, sans-serif" fontSize="15" fontWeight="500" textAnchor="middle" fill="#333">User request</text>
                
                {/* Agent Box */}
                <rect x="260" y="120" width="100" height="110" rx="15" fill="none" stroke="#44DD88" strokeWidth="2.5"/>
                <text x="310" y="180" fontFamily="Arial, sans-serif" fontSize="15" fontWeight="500" textAnchor="middle" fill="#333">Agent</text>
                
                {/* Planning Box */}
                <rect x="500" y="70" width="170" height="80" rx="15" fill="none" stroke="#FF6B9D" strokeWidth="2.5"/>
                <text x="520" y="105" fontFamily="Arial, sans-serif" fontSize="22" fill="#FF6B9D">📋</text>
                <text x="600" y="115" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="500" fill="#333">Planning</text>
                
                {/* Memory Box */}
                <rect x="500" y="145" width="170" height="80" rx="15" fill="none" stroke="#FF6B9D" strokeWidth="2.5"/>
                <text x="520" y="180" fontFamily="Arial, sans-serif" fontSize="22" fill="#FF6B9D">☰</text>
                <text x="600" y="190" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="500" fill="#333">Memory</text>
                
                {/* Tools Box */}
                <rect x="500" y="220" width="170" height="80" rx="15" fill="none" stroke="#FF6B9D" strokeWidth="2.5"/>
                <text x="520" y="255" fontFamily="Arial, sans-serif" fontSize="22" fill="#FF6B9D">⚒️</text>
                <text x="600" y="265" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="500" fill="#333">Tools</text>
              </svg>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
