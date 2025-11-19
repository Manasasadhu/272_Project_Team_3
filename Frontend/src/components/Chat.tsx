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
  const [synthesis, setSynthesis] = useState('');

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
    // Convert markdown to HTML
    const convertMarkdownToHtml = (markdown: string): string => {
      let html = markdown;
      
      // Convert headers
      html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
      html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
      html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');
      
      // Convert bold and italic
      html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
      html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
      
      // Convert inline code
      html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
      
      // Convert code blocks
      html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
      
      // Convert blockquotes
      html = html.replace(/^> (.*?)$/gm, '<blockquote>$1</blockquote>');
      
      // Convert horizontal rules
      html = html.replace(/^---$/gm, '<hr>');
      html = html.replace(/^=+$/gm, '<hr>');
      
      // Convert unordered lists
      const ulRegex = /(?:^|\n)((?:[\*\-\+] .*(?:\n|$))+)/g;
      html = html.replace(ulRegex, (match) => {
        const items = match.trim().split('\n').map(line => {
          const content = line.replace(/^[\*\-\+] /, '');
          return `<li>${content}</li>`;
        }).join('');
        return `<ul>${items}</ul>`;
      });
      
      // Convert ordered lists
      const olRegex = /(?:^|\n)((?:\d+\. .*(?:\n|$))+)/g;
      html = html.replace(olRegex, (match) => {
        const items = match.trim().split('\n').map(line => {
          const content = line.replace(/^\d+\. /, '');
          return `<li>${content}</li>`;
        }).join('');
        return `<ol>${items}</ol>`;
      });
      
      // Convert tables (simple markdown tables)
      const tableRegex = /(\|.+\|[\n\r]+\|[\s:\-|]+\|[\n\r]+((?:\|.+\|[\n\r]*)+))/g;
      html = html.replace(tableRegex, (match) => {
        const lines = match.trim().split('\n');
        const headers = lines[0].split('|').filter(h => h.trim()).map(h => h.trim());
        const rows = lines.slice(2).map(line => 
          line.split('|').filter(c => c.trim()).map(c => c.trim())
        );
        
        const headerHtml = '<tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr>';
        const rowsHtml = rows.map(row => 
          '<tr>' + row.map(cell => `<td>${cell}</td>`).join('') + '</tr>'
        ).join('');
        
        return `<table>${headerHtml}${rowsHtml}</table>`;
      });
      
      // Convert links
      html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
      
      // Convert line breaks (preserve paragraph structure)
      html = html.replace(/\n\n+/g, '</p><p>');
      html = html.replace(/\n/g, '<br>');
      
      // Wrap in paragraph if not already wrapped in block element
      if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
      }
      
      return html;
    };

    const synthesisHtml = convertMarkdownToHtml(synthesis);

    // Create HTML content for PDF with synthesis markdown rendered
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Research Synthesis Report</title>
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
            line-height: 1.7;
            color: #334155;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #ffffff;
          }
          h1 {
            color: #1e293b;
            border-bottom: 4px solid #3b82f6;
            padding-bottom: 16px;
            margin-bottom: 24px;
            font-size: 2em;
          }
          h2 {
            color: #1e293b;
            background: linear-gradient(135deg, #eff6ff 0%, #e0f2fe 100%);
            padding: 12px 20px;
            border-left: 4px solid #3b82f6;
            border-radius: 6px;
            margin-top: 32px;
            margin-bottom: 16px;
            font-size: 1.5em;
            page-break-after: avoid;
          }
          h3 {
            color: #475569;
            padding: 10px 14px;
            border-left: 3px solid #3b82f6;
            background: linear-gradient(90deg, #f0f9ff 0%, transparent 100%);
            border-radius: 4px;
            margin-top: 24px;
            margin-bottom: 12px;
            font-size: 1.2em;
            page-break-after: avoid;
          }
          h4 {
            color: #64748b;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.1em;
          }
          .metadata {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border-left: 4px solid #3b82f6;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 32px;
          }
          .metadata-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
          }
          .stat {
            font-weight: 600;
            color: #1e293b;
          }
          .stat-label {
            color: #64748b;
            font-size: 0.9em;
            margin-right: 8px;
          }
          .synthesis-content {
            margin: 24px 0;
          }
          .synthesis-content > h1:first-child {
            margin-top: 0;
          }
          p {
            margin: 12px 0;
            line-height: 1.7;
          }
          strong {
            color: #1e293b;
            font-weight: 600;
          }
          em {
            color: #64748b;
          }
          ul, ol {
            margin: 12px 0 16px 0;
            padding-left: 32px;
          }
          li {
            margin: 6px 0;
            line-height: 1.7;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border-radius: 8px;
            overflow: hidden;
            page-break-inside: avoid;
          }
          th {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: #ffffff;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
          }
          td {
            padding: 12px 16px;
            border: 1px solid #e2e8f0;
          }
          tr:nth-child(even) {
            background: #f8fafc;
          }
          blockquote {
            border-left: 4px solid #3b82f6;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 16px 24px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
            font-style: italic;
            color: #475569;
          }
          code {
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
            color: #b91c1c;
            font-family: 'Monaco', 'Courier New', monospace;
          }
          pre {
            background: #1e293b;
            color: #e2e8f0;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            page-break-inside: avoid;
          }
          pre code {
            background: transparent;
            color: #e2e8f0;
            padding: 0;
          }
          hr {
            border: none;
            border-top: 2px solid #e2e8f0;
            margin: 32px 0;
          }
          a {
            color: #3b82f6;
            text-decoration: none;
          }
          a:hover {
            text-decoration: underline;
          }
          .footer {
            margin-top: 48px;
            padding-top: 24px;
            border-top: 2px solid #e2e8f0;
            text-align: center;
            color: #64748b;
            font-size: 0.9em;
          }
          @media print {
            body {
              padding: 20px;
            }
            .metadata {
              page-break-inside: avoid;
            }
          }
        </style>
      </head>
      <body>
        <h1>Research Synthesis Report</h1>
        
        <div class="metadata">
          <div class="metadata-grid">
            <div><span class="stat-label">Sources Analyzed:</span><span class="stat">${sourcesCount} peer-reviewed papers</span></div>
            <div><span class="stat-label">Generated:</span><span class="stat">${new Date().toLocaleString()}</span></div>
          </div>
        </div>

        <div class="synthesis-content">
          ${synthesisHtml}
        </div>

        <div class="footer">
          <p><strong>Research Agent System</strong></p>
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
    setSynthesis('');
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
          return 90;
        }
        // Cap increment so it never exceeds 90%
        const increment = Math.random() * 15;
        return Math.min(prev + increment, 90);
      });
    }, 500);

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

    // Use current origin for API calls (works for both local and EC2)
    const API_BASE_URL = window.location.hostname === 'localhost' 
      ? 'http://localhost:8080'
      : `http://${window.location.hostname}:8080`;

    console.log('Current hostname:', window.location.hostname);
    console.log('API_BASE_URL:', API_BASE_URL);

    fetch(`${API_BASE_URL}/api/agent/execute`, {
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
        
        // Set sources count from peer-reviewed papers
        // First try to extract from synthesis text (e.g., "28 peer-reviewed papers")
        let peerReviewedCount = 0;
        const synthesisText = synthesis.full_synthesis || synthesis.executive_summary || '';
        const textMatch = synthesisText.match(/(\d+)\s*peer[\s-]?reviewed\s*papers?/i);
        if (textMatch) {
          peerReviewedCount = parseInt(textMatch[1], 10);
        } else {
          // Fallback to API fields
          peerReviewedCount = executionSummary.peer_reviewed_papers || 
                              executionSummary.total_sources_discovered || 
                              executionSummary.sources_discovered || 
                              synthesis.peer_reviewed_papers ||
                              data.peer_reviewed_papers ||
                              0;
        }
        setSourcesCount(peerReviewedCount);
        
        // Set full synthesis
        setSynthesis(synthesis.full_synthesis || synthesis.executive_summary || 'No synthesis available');
        
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
        </aside>      {/* Main Chat Area */}
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
                synthesis={synthesis}
                onExport={handleExportResults}
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
