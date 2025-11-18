import { useState, useEffect } from 'react';
import { Plus, LogOut, Trash2, ChevronDown, ChevronUp } from 'lucide-react';
import Navbar from './Navbar';
import ProcessingIndicator from './ProcessingIndicator';
import ResultsDisplay from './ResultsDisplay';
import '../styles/Chat.css';

interface ChatPageProps {
  onLogout: () => void;
  userName?: string;
}

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

interface ChatSession {
  id: string;
  title: string;
  createdAt: Date;
}

interface Finding {
  id: string;
  title: string;
  description: string;
  source?: string;
}

interface Recommendation {
  id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
}

export default function Chat({ onLogout, userName = 'User' }: ChatPageProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [activeChatId, setActiveChatId] = useState<string>('new-chat');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [chatToDelete, setChatToDelete] = useState<string | null>(null);
  const [researchGoal, setResearchGoal] = useState('');
  const [showOptionalParams, setShowOptionalParams] = useState(false);
  const [timeRange, setTimeRange] = useState('');
  const [researchDepth, setResearchDepth] = useState('');
  const [sourceQuality, setSourceQuality] = useState('');
  const [sourceDiversity, setSourceDiversity] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingProgress, setProcessingProgress] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [sourcesCount, setSourcesCount] = useState(0);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [synthesis, setSynthesis] = useState('');
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  // Load chat sessions from localStorage on component mount
  useEffect(() => {
    const savedSessions = localStorage.getItem('chatSessions');
    if (savedSessions) {
      try {
        const sessions = JSON.parse(savedSessions);
        // Convert timestamp strings back to Date objects
        const parsedSessions = sessions.map((session: any) => ({
          ...session,
          createdAt: new Date(session.createdAt),
        }));
        setChatSessions(parsedSessions);
      } catch (error) {
        console.error('Failed to load chat sessions:', error);
      }
    }
  }, []);

  // Save chat sessions to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('chatSessions', JSON.stringify(chatSessions));
  }, [chatSessions]);

  const handleCancelProcessing = () => {
    setIsProcessing(false);
    setProcessingProgress(0);
  };

  const handleExportResults = () => {
    // Create HTML content for PDF
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
          }
          h1 {
            color: #2563eb;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 10px;
          }
          h2 {
            color: #1e40af;
            margin-top: 30px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 8px;
          }
          h3 {
            color: #1e3a8a;
            margin-top: 20px;
          }
          .metadata {
            background-color: #f3f4f6;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
          }
          .stat {
            display: inline-block;
            margin-right: 20px;
            font-weight: bold;
          }
          .finding, .recommendation {
            background-color: #f9fafb;
            border-left: 4px solid #2563eb;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
          }
          .finding-title, .rec-title {
            font-weight: bold;
            color: #1e40af;
            margin-bottom: 8px;
          }
          .source {
            color: #6b7280;
            font-size: 0.9em;
            font-style: italic;
            margin-top: 8px;
          }
          .priority {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 10px;
          }
          .priority-high {
            background-color: #fee2e2;
            color: #dc2626;
          }
          .priority-medium {
            background-color: #fef3c7;
            color: #d97706;
          }
          .priority-low {
            background-color: #dbeafe;
            color: #2563eb;
          }
          .synthesis {
            background-color: #eff6ff;
            border: 1px solid #bfdbfe;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
          }
          .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
            font-size: 0.9em;
          }
        </style>
      </head>
      <body>
        <h1>Research Results Report</h1>
        
        <div class="metadata">
          <span class="stat">Sources Analyzed: ${sourcesCount}</span>
          <span class="stat">Findings: ${findings.length}</span>
          <span class="stat">Recommendations: ${recommendations.length}</span>
          <br><br>
          <span class="stat">Generated: ${new Date().toLocaleString()}</span>
        </div>

        <h2>Executive Summary & Synthesis</h2>
        <div class="synthesis">
          ${synthesis.split('\n').map(para => `<p>${para}</p>`).join('')}
        </div>

        ${findings.length > 0 ? `
          <h2>Key Findings</h2>
          ${findings.map((finding, index) => `
            <div class="finding">
              <div class="finding-title">${index + 1}. ${finding.title}</div>
              <div>${finding.description}</div>
              ${finding.source ? `<div class="source">Source: ${finding.source}</div>` : ''}
            </div>
          `).join('')}
        ` : ''}

        ${recommendations.length > 0 ? `
          <h2>Recommendations & Identified Gaps</h2>
          ${recommendations.map((rec, index) => `
            <div class="recommendation">
              <div class="rec-title">
                ${index + 1}. ${rec.title}
                <span class="priority priority-${rec.priority}">${rec.priority.toUpperCase()}</span>
              </div>
              <div>${rec.description}</div>
            </div>
          `).join('')}
        ` : ''}

        <div class="footer">
          <p>This report was generated by the Research Agent System</p>
          <p>© ${new Date().getFullYear()} - All Rights Reserved</p>
        </div>
      </body>
      </html>
    `;

    // Create a new window for printing
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(htmlContent);
      printWindow.document.close();
      
      // Wait for content to load then trigger print
      printWindow.onload = () => {
        setTimeout(() => {
          printWindow.print();
          // Note: Window will close automatically after print dialog
        }, 250);
      };
    } else {
      alert('Please allow pop-ups to export the PDF');
    }
  };

  const handleSaveResults = () => {
    const resultsData = {
      sourcesCount,
      findings,
      synthesis,
      recommendations,
      savedAt: new Date().toISOString(),
    };
    
    // Save to localStorage (can be replaced with backend API call)
    const savedResults = JSON.parse(localStorage.getItem('savedResults') || '[]');
    savedResults.push(resultsData);
    localStorage.setItem('savedResults', JSON.stringify(savedResults));
    
    alert('Results saved successfully!');
  };

  const MIN_CHARS = 10;
  const MAX_CHARS = 500;
  const charCount = researchGoal.length;
  const isValid = charCount >= MIN_CHARS && charCount <= MAX_CHARS;

  const handleNewChat = () => {
    // Save current chat to history if it has messages and is not already in history
    if (messages.length > 0 && activeChatId === 'new-chat') {
      const firstUserMessage = messages.find(m => m.sender === 'user');
      if (firstUserMessage) {
        const newSession: ChatSession = {
          id: Date.now().toString(),
          title: firstUserMessage.text.substring(0, 30),
          createdAt: new Date(),
        };
        setChatSessions([newSession, ...chatSessions]);
      }
    }
    
    // Clear current chat and start new one
    setMessages([]);
    setResearchGoal('');
    setShowResults(false);
    setSourcesCount(0);
    setFindings([]);
    setSynthesis('');
    setRecommendations([]);
    setActiveChatId('new-chat');
  };

  const handleDeleteChat = (sessionId: string) => {
    setChatToDelete(sessionId);
    setShowDeleteModal(true);
  };

  const confirmDelete = () => {
    if (!chatToDelete) return;
    setChatSessions(chatSessions.filter(s => s.id !== chatToDelete));
    if (activeChatId === chatToDelete) {
      setActiveChatId('new-chat');
      setMessages([]);
      setResearchGoal('');
    }
    setShowDeleteModal(false);
    setChatToDelete(null);
  };

  const cancelDelete = () => {
    setShowDeleteModal(false);
    setChatToDelete(null);
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!researchGoal.trim() || !isValid || isProcessing) return;

    setIsProcessing(true);
    setProcessingProgress(0);

    // If this is a new chat (first message), create a session
    if (activeChatId === 'new-chat' || !chatSessions.find(s => s.id === activeChatId)) {
      const newSession: ChatSession = {
        id: Date.now().toString(),
        title: researchGoal.substring(0, 30),
        createdAt: new Date(),
      };
      setChatSessions([newSession, ...chatSessions]);
      setActiveChatId(newSession.id);
    }

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: researchGoal,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages([...messages, userMessage]);
    const currentResearchGoal = researchGoal;
    setResearchGoal('');

    // Simulate progress
    const progressInterval = setInterval(() => {
      setProcessingProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return prev;
        }
        return prev + Math.random() * 30;
      });
    }, 300);

    // Call backend API
    const requestBody = {
      researchGoal: currentResearchGoal,
      scopeParameters: {
        ...(timeRange && { timeRange }),
        ...(researchDepth && { researchDepth }),
        ...(sourceQuality && { sourceQuality }),
        ...(sourceDiversity && { sourceDiversity }),
      },
    };

    fetch('http://localhost:8080/api/agent/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    })
      .then(response => response.json())
      .then(data => {
        clearInterval(progressInterval);
        
        // Extract results from synthesis
        const synthesis = data.synthesis || {};
        const executionSummary = data.execution_summary || data.executionSummary || {};
        
        // Create assistant message with executive summary
        const executiveSummary = synthesis.executive_summary || synthesis.full_synthesis || 'Research completed successfully.';
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: `${executiveSummary}\n\nBelow are the detailed findings. Please feel free to save or download them.`,
          sender: 'assistant',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
        
        // Set sources count
        setSourcesCount(executionSummary.total_sources_discovered || executionSummary.sources_discovered || 0);
        
        // Extract all findings from primary themes
        const themes = synthesis.primary_themes || [];
        const extractedFindings: Finding[] = themes.map((theme: any, index: number) => ({
          id: String(index + 1),
          title: typeof theme === 'string' ? theme : (theme.theme || theme.title || `Finding ${index + 1}`),
          description: typeof theme === 'object' ? (theme.description || theme.evidence || 'No description available') : theme,
          source: typeof theme === 'object' ? (theme.source || 'Research Database') : 'Research Database',
        }));
        setFindings(extractedFindings);
        
        // Set full synthesis
        setSynthesis(synthesis.full_synthesis || synthesis.executive_summary || 'No synthesis available');
        
        // Extract recommendations from gaps identified
        const gaps = synthesis.gaps_identified || [];
        const extractedRecommendations: Recommendation[] = gaps.map((gap: any, index: number) => ({
          id: String(index + 1),
          title: typeof gap === 'string' ? gap : (gap.title || `Gap ${index + 1}`),
          description: typeof gap === 'object' ? (gap.description || gap.suggestion || 'Further research needed') : gap,
          priority: index < 2 ? 'high' : index < 4 ? 'medium' : 'low',
        }));
        setRecommendations(extractedRecommendations);
        
        setShowResults(true);
        setProcessingProgress(100);
        
        setTimeout(() => {
          setIsProcessing(false);
          setProcessingProgress(0);
        }, 500);
      })
      .catch(error => {
        clearInterval(progressInterval);
        console.error('Error calling backend:', error);
        
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: `Error: Failed to connect to backend. ${error.message}`,
          sender: 'assistant',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
        
        setIsProcessing(false);
        setProcessingProgress(0);
      });
  };

  return (
    <div className="chat-page">
      <Navbar 
        onLogoClick={onLogout}
        onSignIn={onLogout}
        onSignUp={() => {}}
        currentPage="chat"
      />
      <div className="chat-container">
      {/* Sidebar */}
      <aside className="chat-sidebar">
        <button className="new-chat-btn" onClick={handleNewChat}>
          <Plus size={20} />
          <span>New Chat</span>
        </button>

        <div className="chat-history">
          <h3>History</h3>
          <div className="history-list">
            {chatSessions.map((session) => (
              <div
                key={session.id}
                className={`history-item-wrapper ${activeChatId === session.id ? 'active' : ''}`}
              >
                <button
                  className="history-item"
                  onClick={() => setActiveChatId(session.id)}
                >
                  {session.title}
                </button>
                <button
                  className="delete-history-btn"
                  onClick={() => handleDeleteChat(session.id)}
                  aria-label="Delete chat"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="user-section">
          <div className="user-profile">
            <div className="user-avatar">{userName.charAt(0).toUpperCase()}</div>
            <div className="user-info">
              <p className="user-name">{userName}</p>
            </div>
          </div>
          <button className="logout-btn" onClick={onLogout}>
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="chat-main">
        {/* Messages Area */}
        <div className="chat-messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender === 'user' ? 'user-message' : 'assistant-message'}`}
            >
              <div className="message-content">
                <p>{message.text}</p>
              </div>
            </div>
          ))}
          
          {/* Results Display */}
          {showResults && (
            <div className="results-section-wrapper">
              <ResultsDisplay
                sourcesCount={sourcesCount}
                findings={findings}
                synthesis={synthesis}
                recommendations={recommendations}
                onExport={handleExportResults}
                onSave={handleSaveResults}
              />
            </div>
          )}
        </div>

        {/* Research Goal Input Area */}
        <form className="research-form-container" onSubmit={handleSendMessage}>
          {/* Optional Parameters Collapsible Section */}
          <div className="optional-params">
            <button
              type="button"
              className="params-toggle"
              onClick={() => setShowOptionalParams(!showOptionalParams)}
            >
              <span>Optional Parameters</span>
              {showOptionalParams ? (
                <ChevronUp size={20} />
              ) : (
                <ChevronDown size={20} />
              )}
            </button>

            {showOptionalParams && (
              <div className="params-content">
                <div className="params-row">
                  <div className="form-group">
                    <label htmlFor="time-range" className="form-label">
                      Time Range
                    </label>
                    <select
                      id="time-range"
                      className="form-select"
                      value={timeRange}
                      onChange={(e) => setTimeRange(e.target.value)}
                    >
                      <option value="">Select time range...</option>
                      <option value="1">1 year</option>
                      <option value="2">2 years</option>
                      <option value="3">3 years</option>
                      <option value="4">4 years</option>
                      <option value="5">5 years</option>
                      <option value="6">6 years</option>
                      <option value="7">7 years</option>
                      <option value="8">8 years</option>
                      <option value="9">9 years</option>
                      <option value="10">10 years</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="research-depth" className="form-label">
                      Research Depth
                    </label>
                    <select
                      id="research-depth"
                      className="form-select"
                      value={researchDepth}
                      onChange={(e) => setResearchDepth(e.target.value)}
                    >
                      <option value="">Select depth...</option>
                      <option value="rapid">Rapid</option>
                      <option value="focused">Focused</option>
                      <option value="comprehensive">Comprehensive</option>
                      <option value="exhaustive">Exhaustive</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="source-quality" className="form-label">
                      Source Quality
                    </label>
                    <select
                      id="source-quality"
                      className="form-select"
                      value={sourceQuality}
                      onChange={(e) => setSourceQuality(e.target.value)}
                    >
                      <option value="">Select quality...</option>
                      <option value="cutting_edge">Cutting Edge</option>
                      <option value="high_impact">High Impact</option>
                      <option value="established">Established</option>
                      <option value="baseline">Baseline</option>
                    </select>
                  </div>

                  <div className="form-group checkbox-group-inline">
                    <label htmlFor="source-diversity" className="checkbox-label">
                      <input
                        id="source-diversity"
                        type="checkbox"
                        className="checkbox-input"
                        checked={sourceDiversity}
                        onChange={(e) => setSourceDiversity(e.target.checked)}
                      />
                      <span>Diverse Sources</span>
                    </label>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="research-goal" className="form-label">
              Research Goal
            </label>
            <div className="search-input-wrapper">
              <textarea
                id="research-goal"
                className="research-input"
                placeholder="Enter your research question here..."
                value={researchGoal}
                onChange={(e) => setResearchGoal(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey) && isValid && !isProcessing) {
                    handleSendMessage(e as any);
                  }
                }}
                rows={3}
              />
              <button
                type="submit"
                className={`submit-btn ${(!isValid || isProcessing) ? 'disabled' : ''}`}
                disabled={!isValid || isProcessing}
              >
                {isProcessing ? (
                  <>
                    <span className="spinner"></span>
                    Processing...
                  </>
                ) : (
                  'Send'
                )}
              </button>
            </div>
            <div className="char-count">
              <span className={`count-text ${charCount > MAX_CHARS ? 'error' : ''}`}>
                {charCount}/{MAX_CHARS}
              </span>
              <span className="count-info">
                {charCount < MIN_CHARS ? `Minimum ${MIN_CHARS} characters` : ''}
                {charCount > MAX_CHARS ? 'Maximum exceeded' : ''}
                {charCount >= MIN_CHARS && charCount <= MAX_CHARS ? 'Ready to submit' : ''}
              </span>
            </div>
          </div>
        </form>
      </main>
    </div>

    {/* Delete Confirmation Modal */}
    {showDeleteModal && (
      <div className="modal-overlay" onClick={cancelDelete}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <h2>Delete Chat?</h2>
          <p>Are you sure you want to delete this chat? This action cannot be undone.</p>
          <div className="modal-buttons">
            <button className="modal-btn cancel-btn" onClick={cancelDelete}>
              Cancel
            </button>
            <button className="modal-btn delete-btn" onClick={confirmDelete}>
              Delete
            </button>
          </div>
        </div>
      </div>
    )}

    {/* Processing Indicator */}
    <ProcessingIndicator
      isVisible={isProcessing}
      message="Processing your request..."
      progress={processingProgress}
      onCancel={handleCancelProcessing}
    />
    </div>
  );
}
