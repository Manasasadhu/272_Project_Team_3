import { ArrowRight, BookOpen, Zap, BarChart3, RefreshCw, TrendingUp, CheckCircle } from 'lucide-react';
import Navbar from './Navbar';
import '../styles/Landing.css';

interface LandingPageProps {
  onSignIn: () => void;
  onSignUp: () => void;
  onHowItWorks: () => void;
}

export default function Landing({ onSignIn, onSignUp, onHowItWorks }: LandingPageProps) {
  return (
    <div className="landing-container">
      {/* Header Navigation */}
      <Navbar 
        onLogoClick={() => {}} 
        onSignIn={onSignIn} 
        onSignUp={onSignUp}
        onHowItWorks={onHowItWorks}
        currentPage="landing"
      />

      {/* Hero Section */}
      <main className="landing-main">
        <div className="hero-content-new">
          <div className="hero-center">
            <div className="logo-container">
              <div className="logo-badge">
                <BookOpen className="hero-icon" size={48} />
              </div>
            </div>
            <h1 className="hero-title-new">AI-Powered Literature Review</h1>
            <p className="hero-description-new">
              Automate your research paper discovery and analysis with intelligent agents
            </p>
            <div className="hero-buttons">
              <button onClick={onSignUp} className="get-started-btn-new">
                Start New Review
              </button>
              <button onClick={onHowItWorks} className="view-examples-btn">
                How It Works
              </button>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <section className="features-section">
          <h2 className="features-title">Key Features</h2>
          <div className="features-grid">
            <div className="feature-card feature-blue">
              <Zap className="feature-icon" size={32} />
              <h3 className="feature-title">Automated Search</h3>
              <p className="feature-desc">Fetches papers from OpenAlex automatically</p>
            </div>
            
            <div className="feature-card feature-purple">
              <BarChart3 className="feature-icon" size={32} />
              <h3 className="feature-title">Smart Extraction</h3>
              <p className="feature-desc">GROBID-powered parameter extraction</p>
            </div>
            
            <div className="feature-card feature-amber">
              <RefreshCw className="feature-icon" size={32} />
              <h3 className="feature-title">Agentic Orchestration Cycle</h3>
              <p className="feature-desc">Intelligent iteration until goals are achieved</p>
            </div>
            
            <div className="feature-card feature-green">
              <TrendingUp className="feature-icon" size={32} />
              <h3 className="feature-title">Quality Scoring</h3>
              <p className="feature-desc">Intelligent evaluation of results</p>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="how-it-works-section">
          <h2 className="features-title">How It Works</h2>
          <div className="process-steps">
            <div className="process-step">
              <div className="step-number">1</div>
              <h3 className="step-title">Submit Query</h3>
              <p className="step-desc">Enter your research topic and parameters</p>
            </div>
            <ArrowRight className="step-arrow" size={24} />
            
            <div className="process-step">
              <div className="step-number">2</div>
              <h3 className="step-title">Fetch & Extract</h3>
              <p className="step-desc">AI retrieves and analyzes relevant papers</p>
            </div>
            <ArrowRight className="step-arrow" size={24} />
            
            <div className="process-step">
              <div className="step-number">3</div>
              <h3 className="step-title">Quality Check</h3>
              <p className="step-desc">Evaluates results against goals</p>
            </div>
            <ArrowRight className="step-arrow" size={24} />
            
            <div className="process-step">
              <div className="step-number">4</div>
              <h3 className="step-title">Get Results</h3>
              <p className="step-desc">Comprehensive review with citations</p>
            </div>
          </div>
          <div className="how-it-works-cta">
            <button onClick={onHowItWorks} className="learn-more-btn">
              Learn More About Our Process
            </button>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="benefits-section">
          <h2 className="features-title">Why Choose Our Platform</h2>
          <div className="benefits-list">
            <div className="benefit-item">
              <CheckCircle className="benefit-icon" size={20} />
              <p>Real-time progress tracking showing current analysis step</p>
            </div>
            <div className="benefit-item">
              <CheckCircle className="benefit-icon" size={20} />
              <p>Export options in multiple formats (PDF, BibTeX, CSV, JSON)</p>
            </div>
            <div className="benefit-item">
              <CheckCircle className="benefit-icon" size={20} />
              <p>Integrated with OpenAlex and GROBID for accurate extraction</p>
            </div>
            <div className="benefit-item">
              <CheckCircle className="benefit-icon" size={20} />
              <p>Save time with automated paper discovery and analysis</p>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section className="contact-section">
          <h2 className="contact-title">Need Help?</h2>
          <p className="contact-description">
            Have questions or need assistance? Our team is here to help you get the most out of your research.
          </p>
          <div className="contact-info">
            <div className="contact-card">
              <h3 className="contact-heading">Contact Us</h3>
              <div className="contact-details">
                <p className="contact-email">
                  <a href="mailto:manasa.sadhu@sjsu.edu">manasa.sadhu@sjsu.edu</a>
                </p>
                <p className="contact-email">
                  <a href="mailto:samvedsandeep.joshi@sjsu.edu">samvedsandeep.joshi@sjsu.edu</a>
                </p>
              </div>
            </div>
            <div className="contact-card">
              <h3 className="contact-heading">Address</h3>
              <div className="contact-details">
                <p>San Jose State University</p>
                <p>One Washington Square</p>
                <p>San Jose, CA 95192</p>
              </div>
            </div>
            <div className="contact-card">
              <h3 className="contact-heading">Support</h3>
              <div className="contact-details">
                <p>
                  <button onClick={onHowItWorks} className="contact-link-btn">
                    Documentation & Guides
                  </button>
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Legacy Diagram (Optional - can remove if not needed) */}
        <section className="diagram-section" style={{ display: 'none' }}>
          <div className="hero-right">
            <div className="diagram">
              <svg width="700" height="350" viewBox="0 0 700 350" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <marker id="arrowhead-gray" markerWidth="12" markerHeight="12" refX="10" refY="3" orient="auto">
                    <polygon points="0 0, 12 3, 0 6" fill="#999" />
                  </marker>
                </defs>
                <line x1="180" y1="175" x2="260" y2="175" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                <line x1="260" y1="160" x2="180" y2="160" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                <path d="M 310 230 L 310 290" stroke="#999" strokeWidth="2.5" fill="none" markerEnd="url(#arrowhead-gray)" />
                <line x1="360" y1="155" x2="500" y2="120" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                <line x1="360" y1="175" x2="500" y2="175" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                <line x1="360" y1="195" x2="500" y2="230" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                <line x1="500" y1="100" x2="360" y2="155" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                <line x1="500" y1="175" x2="360" y2="175" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                <line x1="500" y1="250" x2="360" y2="195" stroke="#999" strokeWidth="2.5" markerEnd="url(#arrowhead-gray)" />
                <rect x="60" y="120" width="120" height="110" rx="15" fill="none" stroke="#FF9944" strokeWidth="2.5"/>
                <text x="120" y="180" fontFamily="Arial, sans-serif" fontSize="15" fontWeight="500" textAnchor="middle" fill="#333">User request</text>
                <rect x="260" y="120" width="100" height="110" rx="15" fill="none" stroke="#44DD88" strokeWidth="2.5"/>
                <text x="310" y="180" fontFamily="Arial, sans-serif" fontSize="15" fontWeight="500" textAnchor="middle" fill="#333">Agent</text>
                <rect x="500" y="70" width="170" height="80" rx="15" fill="none" stroke="#FF6B9D" strokeWidth="2.5"/>
                <text x="520" y="105" fontFamily="Arial, sans-serif" fontSize="22" fill="#FF6B9D">📋</text>
                <text x="600" y="115" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="500" fill="#333">Planning</text>
                <rect x="500" y="145" width="170" height="80" rx="15" fill="none" stroke="#FF6B9D" strokeWidth="2.5"/>
                <text x="520" y="180" fontFamily="Arial, sans-serif" fontSize="22" fill="#FF6B9D">☰</text>
                <text x="600" y="190" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="500" fill="#333">Memory</text>
                <rect x="500" y="220" width="170" height="80" rx="15" fill="none" stroke="#FF6B9D" strokeWidth="2.5"/>
                <text x="520" y="255" fontFamily="Arial, sans-serif" fontSize="22" fill="#FF6B9D">⚒️</text>
                <text x="600" y="265" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="500" fill="#333">Tools</text>
              </svg>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}