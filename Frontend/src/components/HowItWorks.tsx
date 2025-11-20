import { Zap } from 'lucide-react';
import '../styles/HowItWorks.css';

interface HowItWorksProps {
  onClose: () => void;
  onGetStarted: () => void;
}

export default function HowItWorks({ onClose, onGetStarted }: HowItWorksProps) {
  return (
    <div className="how-it-works-page">
      {/* Header */}
      <header className="how-header">
        <div className="how-header-content">
          <div className="how-header-left">
            <div className="how-logo-box">
              <span className="how-logo-emoji">🤖</span>
            </div>
            <div>
              <h1 className="how-title">Agentic Research Workflow</h1>
              <p className="how-subtitle">Autonomous Literature Discovery & Synthesis</p>
            </div>
          </div>
          <button onClick={onClose} className="how-close-btn">
            Close
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="how-main">
        
        {/* Introduction */}
        <section className="how-intro fade-in">
          <h2 className="how-section-title gradient-text">How It Works</h2>
          <p className="how-intro-text">
            Our Agentic Research System is an <strong>autonomous workflow</strong> that discovers, validates, extracts, and synthesizes academic research papers in response to your research goals. Unlike traditional search tools that stop after finding papers, our system ensures <strong>goal-adherence at every stage</strong> through continuous governance checks and dynamic semantic matching.
          </p>
          <div className="how-key-principle">
            <p>
              <strong>🎯 Key Principle:</strong> Every decision the system makes—from search queries to paper scoring to synthesis structure—traces directly back to your original research goal.
            </p>
          </div>
        </section>

        {/* Quick Overview */}
        <section className="how-overview fade-in">
          <h3 className="how-overview-title">5-Stage Autonomous Workflow</h3>
          <div className="how-stages-grid">
            <div className="how-stage-item">
              <div className="how-stage-icon pulse-ring">
                <span>🎯</span>
              </div>
              <h4 className="how-stage-name">Planning</h4>
              <p className="how-stage-desc">Goal decomposition</p>
            </div>
            <div className="how-stage-item">
              <div className="how-stage-icon">
                <span>🔍</span>
              </div>
              <h4 className="how-stage-name">Searching</h4>
              <p className="how-stage-desc">Adaptive exploration</p>
            </div>
            <div className="how-stage-item">
              <div className="how-stage-icon">
                <span>⚖️</span>
              </div>
              <h4 className="how-stage-name">Scoring</h4>
              <p className="how-stage-desc">Semantic matching</p>
            </div>
            <div className="how-stage-item">
              <div className="how-stage-icon">
                <span>📄</span>
              </div>
              <h4 className="how-stage-name">Extraction</h4>
              <p className="how-stage-desc">Structured parsing</p>
            </div>
            <div className="how-stage-item">
              <div className="how-stage-icon">
                <span>📊</span>
              </div>
              <h4 className="how-stage-name">Synthesis</h4>
              <p className="how-stage-desc">Meta-analysis</p>
            </div>
          </div>
        </section>

        {/* Stage 1: Planning */}
        <section className="how-stage-card fade-in stage-card">
          <div className="how-stage-layout">
            <div className="how-stage-number-box" style={{ background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)' }}>
              1
            </div>
            <div className="how-stage-content">
              <h3 className="how-stage-title">Planning & Goal Decomposition</h3>
              <p className="how-stage-intro">The Planner Agent analyzes your research goal and creates an intelligent execution plan.</p>
              
              <div className="how-what-happens">
                <h4 className="how-subsection-title">
                  <Zap className="how-icon" />
                  What Happens
                </h4>
                <div className="how-steps-list">
                  <div className="how-step-item">
                    <div className="how-step-num">1</div>
                    <div>
                      <p className="how-step-title">Parse Research Goal</p>
                      <p className="how-step-text">Extract key terms, concepts, and technical vocabulary from your query</p>
                    </div>
                  </div>
                  <div className="how-step-item">
                    <div className="how-step-num">2</div>
                    <div>
                      <p className="how-step-title">Generate Search Queries</p>
                      <p className="how-step-text">Use Gemini 2.5-flash LLM to create 3-5 diverse search queries with heuristic fallback</p>
                    </div>
                  </div>
                  <div className="how-step-item">
                    <div className="how-step-num">3</div>
                    <div>
                      <p className="how-step-title">Map Scope Parameters</p>
                      <p className="how-step-text">Configure depth (rapid/focused/comprehensive/exhaustive), timeframe, and quality thresholds</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="how-example-grid">
                <div className="how-example-box how-example-input">
                  <p className="how-example-label">Example Input:</p>
                  <p className="how-example-content">"Comparison of RIP and OSPF routing protocols"</p>
                </div>
                <div className="how-example-box how-example-output">
                  <p className="how-example-label">Generated Queries:</p>
                  <ul className="how-example-list">
                    <li>• "RIP OSPF comparison"</li>
                    <li>• "routing protocols performance"</li>
                    <li>• "distance vector vs link state"</li>
                  </ul>
                </div>
              </div>

              <div className="how-goal-adherence">
                <p>
                  <strong>🎯 Goal Adherence:</strong> All search queries are dynamically derived from your research goal—no generic or hardcoded queries are used.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Stage 2: Searching */}
        <section className="how-stage-card fade-in stage-card">
          <div className="how-stage-layout">
            <div className="how-stage-number-box" style={{ background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)' }}>
              2
            </div>
            <div className="how-stage-content">
              <h3 className="how-stage-title">Autonomous Exploration & Search</h3>
              <p className="how-stage-intro">The Search Tool executes queries against OpenAlex API and adaptively expands to fill gaps.</p>
              
              <div className="how-phase-box">
                <h4 className="how-subsection-title">Primary Search Phase</h4>
                <div className="how-bullet-list">
                  <div className="how-bullet-item">
                    <div className="how-bullet-dot"></div>
                    <p>Execute each planned query against OpenAlex (max 20 results per query)</p>
                  </div>
                  <div className="how-bullet-item">
                    <div className="how-bullet-dot"></div>
                    <p>Extract metadata: title, author, year, citations, venue, URL, abstract snippet</p>
                  </div>
                  <div className="how-bullet-item">
                    <div className="how-bullet-dot"></div>
                    <p>Store each source to Redis for checkpoint recovery</p>
                  </div>
                </div>
              </div>

              <div className="how-adaptive-box">
                <h4 className="how-subsection-title">🔄 Adaptive Query Expansion</h4>
                <p className="how-adaptive-intro">
                  If initial results show coverage gaps (e.g., &lt;5 papers on a key concept), the system automatically:
                </p>
                <div className="how-arrow-list">
                  <div className="how-arrow-item">
                    <span className="how-arrow">→</span>
                    <p>Analyzes initial results quality and identifies missing topics</p>
                  </div>
                  <div className="how-arrow-item">
                    <span className="how-arrow">→</span>
                    <p>Uses LLM to generate 2 additional refined search queries</p>
                  </div>
                  <div className="how-arrow-item">
                    <span className="how-arrow">→</span>
                    <p>Executes expansion searches to fill gaps</p>
                  </div>
                </div>
              </div>

              <div className="how-stats-box">
                <div className="how-stats-header">
                  <span className="how-stats-label">Typical Results:</span>
                  <span className="how-stats-example">Example: RIP vs OSPF query</span>
                </div>
                <div className="how-stats-grid">
                  <div className="how-stat-item">
                    <div className="how-stat-value" style={{ color: '#6366f1' }}>84</div>
                    <div className="how-stat-label">Papers Discovered</div>
                  </div>
                  <div className="how-stat-item">
                    <div className="how-stat-value" style={{ color: '#8b5cf6' }}>5-7</div>
                    <div className="how-stat-label">Search Queries</div>
                  </div>
                  <div className="how-stat-item">
                    <div className="how-stat-value" style={{ color: '#3b82f6' }}>2-3</div>
                    <div className="how-stat-label">Minutes</div>
                  </div>
                </div>
              </div>

              <div className="how-goal-adherence">
                <p>
                  <strong>🎯 Goal Adherence:</strong> Expansion queries specifically target gaps in coverage while maintaining semantic connection to your core research topic.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Stage 3: Relevance Scoring */}
        <section className="how-stage-card fade-in stage-card">
          <div className="how-stage-layout">
            <div className="how-stage-number-box" style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)' }}>
              3
            </div>
            <div className="how-stage-content">
              <h3 className="how-stage-title">Dynamic Semantic Matching & Scoring</h3>
              <p className="how-stage-intro">The Governance Layer scores every paper using dynamic semantic groups built from your research goal.</p>
              
              <div className="how-semantic-box">
                <h4 className="how-subsection-title">🧠 Dynamic Semantic Groups (NO Hardcoding)</h4>
                <p className="how-semantic-intro">
                  The system parses your research goal at runtime to build semantic keyword groups with synonyms and stemming:
                </p>
                <div className="how-code-box">
                  <p className="how-code-label">Example for "Comparison of RIP and OSPF routing protocols":</p>
                  <div className="how-code-content">
                    <div><span className="how-code-key">routing:</span> ["RIP", "OSPF", "EIGRP", "protocols", "IGP"]</div>
                    <div><span className="how-code-key">comparison:</span> ["vs", "versus", "compared", "analysis", "evaluation"]</div>
                    <div><span className="how-code-key">performance:</span> ["speed", "efficiency", "convergence", "metrics"]</div>
                  </div>
                </div>
              </div>

              <div className="how-scoring-box">
                <h4 className="how-subsection-title">📊 Scoring Formula (Deterministic, No LLM)</h4>
                <div className="how-scoring-grid">
                  <div className="how-score-card" style={{ borderLeftColor: '#8b5cf6' }}>
                    <p className="how-score-title">Semantic Score (70%)</p>
                    <p className="how-score-desc">Keyword matching in title + snippet against semantic groups</p>
                  </div>
                  <div className="how-score-card" style={{ borderLeftColor: '#3b82f6' }}>
                    <p className="how-score-title">Citation Authority (15%)</p>
                    <p className="how-score-desc">Papers with more citations weighted higher</p>
                  </div>
                  <div className="how-score-card" style={{ borderLeftColor: '#10b981' }}>
                    <p className="how-score-title">Recency Score (10%)</p>
                    <p className="how-score-desc">Recent papers get bonus weight</p>
                  </div>
                  <div className="how-score-card" style={{ borderLeftColor: '#f59e0b' }}>
                    <p className="how-score-title">Metadata Match (5%)</p>
                    <p className="how-score-desc">Venue quality (IEEE, ACM, etc.)</p>
                  </div>
                </div>
              </div>

              <div className="how-governance-box">
                <h4 className="how-subsection-title">⚖️ Governance Policies</h4>
                <div className="how-policy-list">
                  <div className="how-policy-item">
                    <svg className="how-check-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <p><strong>Min Year Filter:</strong> Only papers from 1990+ (configurable)</p>
                  </div>
                  <div className="how-policy-item">
                    <svg className="how-check-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <p><strong>Min Citations Filter:</strong> At least 5 citations required</p>
                  </div>
                  <div className="how-policy-item">
                    <svg className="how-check-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <p><strong>Peer-Review Check:</strong> Verified venue quality</p>
                  </div>
                  <div className="how-policy-item">
                    <svg className="how-check-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <p><strong>Dynamic Threshold:</strong> Adjusted to maintain ~40-60% acceptance rate</p>
                  </div>
                </div>
              </div>

              <div className="how-results-box">
                <p className="how-results-label">Example Scoring Results:</p>
                <div className="how-results-list">
                  <div className="how-result-item">
                    <span className="how-result-text">"Comparison of RIP, EIGRP, OSPF Protocols"</span>
                    <span className="how-result-badge how-result-pass">0.88 ✓</span>
                  </div>
                  <div className="how-result-item">
                    <span className="how-result-text">"Survey on Routing in Mobile Networks"</span>
                    <span className="how-result-badge how-result-pass">0.67 ✓</span>
                  </div>
                  <div className="how-result-item">
                    <span className="how-result-text">"Statistical Methods for Data Analysis"</span>
                    <span className="how-result-badge how-result-fail">0.21 ✗</span>
                  </div>
                </div>
                <p className="how-results-summary">Final: 63/84 papers pass (75% acceptance rate)</p>
              </div>

              <div className="how-goal-adherence">
                <p>
                  <strong>🎯 Goal Adherence:</strong> All scoring criteria are dynamically generated from your research goal. Every paper gets a transparent score breakdown showing exactly why it was accepted or rejected.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Stage 4: Extraction */}
        <section className="how-stage-card fade-in stage-card">
          <div className="how-stage-layout">
            <div className="how-stage-number-box" style={{ background: 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)' }}>
              4
            </div>
            <div className="how-stage-content">
              <h3 className="how-stage-title">Structured Content Extraction</h3>
              <p className="how-stage-intro">The Extraction Tool uses GROBID to parse PDFs and extract structured content from validated papers.</p>
              
              <div className="how-extraction-box">
                <h4 className="how-subsection-title">What Gets Extracted</h4>
                <div className="how-extraction-grid">
                  <div className="how-extract-card">
                    <p className="how-extract-title">📝 Abstract</p>
                    <p className="how-extract-desc">Full abstract text and summary</p>
                  </div>
                  <div className="how-extract-card">
                    <p className="how-extract-title">🔬 Methodology</p>
                    <p className="how-extract-desc">Research methods and approaches</p>
                  </div>
                  <div className="how-extract-card">
                    <p className="how-extract-title">💡 Key Findings</p>
                    <p className="how-extract-desc">Results and conclusions</p>
                  </div>
                  <div className="how-extract-card">
                    <p className="how-extract-title">👥 Authors</p>
                    <p className="how-extract-desc">Author names and affiliations</p>
                  </div>
                  <div className="how-extract-card">
                    <p className="how-extract-title">📚 References</p>
                    <p className="how-extract-desc">Citations and bibliography</p>
                  </div>
                  <div className="how-extract-card">
                    <p className="how-extract-title">📊 Metadata</p>
                    <p className="how-extract-desc">Year, venue, DOI, keywords</p>
                  </div>
                </div>
              </div>

              <div className="how-process-box">
                <h4 className="how-subsection-title">Extraction Process</h4>
                <div className="how-steps-list">
                  <div className="how-step-item">
                    <div className="how-step-num-orange">1</div>
                    <div>
                      <p className="how-step-title">Call Java Backend Service</p>
                      <p className="how-step-text">POST to EC2 tools-service: /api/tools/extract with paper URL</p>
                    </div>
                  </div>
                  <div className="how-step-item">
                    <div className="how-step-num-orange">2</div>
                    <div>
                      <p className="how-step-title">GROBID Parsing</p>
                      <p className="how-step-text">Machine learning library extracts structured data from PDF/HTML</p>
                    </div>
                  </div>
                  <div className="how-step-item">
                    <div className="how-step-num-orange">3</div>
                    <div>
                      <p className="how-step-title">Structure & Store</p>
                      <p className="how-step-text">Normalize extracted content and cache to Redis for synthesis stage</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="how-goal-adherence">
                <p>
                  <strong>🎯 Goal Adherence:</strong> Only papers that passed relevance scoring get extracted, ensuring computational resources focus on goal-relevant content.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Stage 5: Synthesis */}
        <section className="how-stage-card fade-in stage-card">
          <div className="how-stage-layout">
            <div className="how-stage-number-box" style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' }}>
              5
            </div>
            <div className="how-stage-content">
              <h3 className="how-stage-title">Intelligent Synthesis & Meta-Analysis</h3>
              <p className="how-stage-intro">The Synthesis Agent generates a comprehensive literature review organized around your research goal.</p>
              
              <div className="how-synthesis-box">
                <h4 className="how-subsection-title">Synthesis Output</h4>
                <div className="how-synthesis-list">
                  <div className="how-synthesis-item">
                    <div className="how-synthesis-icon">📋</div>
                    <div>
                      <p className="how-synthesis-title">Executive Summary</p>
                      <p className="how-synthesis-desc">High-level overview of findings across all papers</p>
                    </div>
                  </div>
                  <div className="how-synthesis-item">
                    <div className="how-synthesis-icon">🔍</div>
                    <div>
                      <p className="how-synthesis-title">Theme-Based Analysis</p>
                      <p className="how-synthesis-desc">Papers grouped by common themes/methodologies</p>
                    </div>
                  </div>
                  <div className="how-synthesis-item">
                    <div className="how-synthesis-icon">📊</div>
                    <div>
                      <p className="how-synthesis-title">Comparative Insights</p>
                      <p className="how-synthesis-desc">Consensus vs. conflicting findings across studies</p>
                    </div>
                  </div>
                  <div className="how-synthesis-item">
                    <div className="how-synthesis-icon">🎯</div>
                    <div>
                      <p className="how-synthesis-title">Research Gaps</p>
                      <p className="how-synthesis-desc">Identified opportunities for future work</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="how-final-box">
                <h4 className="how-subsection-title">🚀 Final Deliverable</h4>
                <p className="how-final-text">
                  A professionally structured literature review with:
                </p>
                <ul className="how-final-list">
                  <li>✓ Properly formatted citations (APA/IEEE)</li>
                  <li>✓ Relevance scores for each paper</li>
                  <li>✓ Interactive table of contents</li>
                  <li>✓ Export to Markdown/PDF</li>
                </ul>
              </div>

              <div className="how-goal-adherence">
                <p>
                  <strong>🎯 Goal Adherence:</strong> The synthesis structure mirrors your original research goal—every section and subsection is organized to answer your specific questions.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Footer CTA */}
        <section className="how-footer-cta fade-in">
          <div className="how-cta-content">
            <h3 className="how-cta-title">Ready to Start Your Research?</h3>
            <p className="how-cta-text">
              Experience autonomous literature discovery with goal-driven governance at every stage.
            </p>
            <button onClick={onGetStarted} className="how-cta-button">
              Get Started
            </button>
          </div>
        </section>

      </main>
    </div>
  );
}
