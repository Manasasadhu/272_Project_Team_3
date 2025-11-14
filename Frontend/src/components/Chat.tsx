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
    const resultsData = {
      sourcesCount,
      findings,
      synthesis,
      recommendations,
      exportedAt: new Date().toISOString(),
    };
    
    const dataStr = JSON.stringify(resultsData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `research-results-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
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

    // Simulate assistant response with delay
    setTimeout(() => {
      clearInterval(progressInterval);
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'This is a simulated response. Connect to your backend to get real responses.',
        sender: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
      
      // Set mock results data
      setSourcesCount(12);
      setFindings([
        {
          id: '1',
          title: 'Research Finding 1',
          description: 'This is a key finding from the research. It represents important data discovered during the analysis phase.',
          source: 'Research Database A',
        },
        {
          id: '2',
          title: 'Research Finding 2',
          description: 'Another significant finding that contributes to the overall research conclusion.',
          source: 'Academic Journal B',
        },
        {
          id: '3',
          title: 'Research Finding 3',
          description: 'A tertiary finding that provides additional context and validation.',
          source: 'Industry Report C',
        },
      ]);
      setSynthesis(
        'The research findings collectively indicate that the topic under study exhibits complex interdependencies. Key patterns emerged suggesting a multi-faceted approach is necessary. The synthesis of available data points to several actionable insights that can inform strategic decision-making. Cross-referencing multiple sources strengthens the validity of these conclusions, with consistent themes appearing across diverse research domains.'
      );
      setRecommendations([
        {
          id: '1',
          title: 'Implement Strategy A',
          description: 'Based on the findings, implementing Strategy A is recommended as a priority action.',
          priority: 'high',
        },
        {
          id: '2',
          title: 'Conduct Further Analysis',
          description: 'Additional research is recommended to validate preliminary findings.',
          priority: 'high',
        },
        {
          id: '3',
          title: 'Establish Monitoring System',
          description: 'Set up a system to track relevant metrics and KPIs.',
          priority: 'medium',
        },
        {
          id: '4',
          title: 'Review Existing Processes',
          description: 'Conduct a review of current processes to identify optimization opportunities.',
          priority: 'low',
        },
      ]);
      setShowResults(true);
      setProcessingProgress(100);
      
      setTimeout(() => {
        setIsProcessing(false);
        setProcessingProgress(0);
      }, 500);
    }, 1500);
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
