import { Download, Save, Copy, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';
import '../styles/ResultsDisplay.css';

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

interface ResultsDisplayProps {
  sourcesCount: number;
  findings: Finding[];
  synthesis: string;
  recommendations: Recommendation[];
  onExport: () => void;
  onSave: () => void;
}

export default function ResultsDisplay({
  sourcesCount,
  findings,
  synthesis,
  recommendations,
  onExport,
  onSave,
}: ResultsDisplayProps) {
  const [expandedSections, setExpandedSections] = useState<{
    findings: boolean;
    synthesis: boolean;
    recommendations: boolean;
  }>({
    findings: true,
    synthesis: true,
    recommendations: true,
  });

  const toggleSection = (section: 'findings' | 'synthesis' | 'recommendations') => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const handleCopyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="results-display">
      {/* Header */}
      <div className="results-header">
        <div className="results-title">
          <h2>Research Results</h2>
          <span className="results-subtitle">Complete Analysis</span>
        </div>
        <div className="results-actions">
          <button className="action-btn save-btn" onClick={onSave} title="Save results">
            <Save size={18} />
            <span>Save</span>
          </button>
          <button className="action-btn export-btn" onClick={onExport} title="Export results">
            <Download size={18} />
            <span>Export</span>
          </button>
        </div>
      </div>

      {/* Sources Count */}
      <div className="sources-summary">
        <div className="source-card">
          <div className="source-number">{sourcesCount}</div>
          <div className="source-label">Sources Found</div>
        </div>
      </div>

      {/* Key Findings Section */}
      <section className="results-section">
        <button
          className="section-header"
          onClick={() => toggleSection('findings')}
        >
          <div className="section-title">
            <h3>Key Findings</h3>
            <span className="finding-count">{findings.length}</span>
          </div>
          {expandedSections.findings ? (
            <ChevronUp size={20} />
          ) : (
            <ChevronDown size={20} />
          )}
        </button>

        {expandedSections.findings && (
          <div className="section-content">
            <div className="findings-list">
              {findings.length > 0 ? (
                findings.map((finding) => (
                  <div key={finding.id} className="finding-item">
                    <div className="finding-header">
                      <h4>{finding.title}</h4>
                      {finding.source && (
                        <span className="finding-source">{finding.source}</span>
                      )}
                    </div>
                    <p>{finding.description}</p>
                  </div>
                ))
              ) : (
                <p className="no-data">No findings available</p>
              )}
            </div>
          </div>
        )}
      </section>

      {/* Synthesis Section */}
      <section className="results-section">
        <button
          className="section-header"
          onClick={() => toggleSection('synthesis')}
        >
          <div className="section-title">
            <h3>Synthesis</h3>
          </div>
          {expandedSections.synthesis ? (
            <ChevronUp size={20} />
          ) : (
            <ChevronDown size={20} />
          )}
        </button>

        {expandedSections.synthesis && (
          <div className="section-content">
            <div className="synthesis-block">
              <p>{synthesis || 'No synthesis available'}</p>
              <button
                className="copy-btn"
                onClick={() => handleCopyToClipboard(synthesis)}
                title="Copy to clipboard"
              >
                <Copy size={16} />
              </button>
            </div>
          </div>
        )}
      </section>

      {/* Recommendations Section */}
      <section className="results-section">
        <button
          className="section-header"
          onClick={() => toggleSection('recommendations')}
        >
          <div className="section-title">
            <h3>Recommendations</h3>
            <span className="recommendation-count">{recommendations.length}</span>
          </div>
          {expandedSections.recommendations ? (
            <ChevronUp size={20} />
          ) : (
            <ChevronDown size={20} />
          )}
        </button>

        {expandedSections.recommendations && (
          <div className="section-content">
            <div className="recommendations-list">
              {recommendations.length > 0 ? (
                recommendations.map((rec) => (
                  <div
                    key={rec.id}
                    className={`recommendation-item priority-${rec.priority}`}
                  >
                    <div className="recommendation-header">
                      <h4>{rec.title}</h4>
                      <span className={`priority-badge priority-${rec.priority}`}>
                        {rec.priority.charAt(0).toUpperCase() + rec.priority.slice(1)}
                      </span>
                    </div>
                    <p>{rec.description}</p>
                  </div>
                ))
              ) : (
                <p className="no-data">No recommendations available</p>
              )}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
