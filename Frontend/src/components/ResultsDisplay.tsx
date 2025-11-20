import { Download, Copy, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';
import SynthesisView from './SynthesisView';
import '../styles/ResultsDisplay.css';

interface ResultsDisplayProps {
  sourcesCount: number;
  synthesis: string;
  onExport: () => void;
}

export default function ResultsDisplay({
  sourcesCount,
  synthesis,
  onExport,
}: ResultsDisplayProps) {
  const [expandedSections, setExpandedSections] = useState<{
    synthesis: boolean;
  }>({
    synthesis: true,
  });

  const toggleSection = (section: 'synthesis') => {
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
            {synthesis ? (
              <div className="synthesis-container">
                <SynthesisView text={synthesis} />
                <button
                  className="copy-btn-floating"
                  onClick={() => handleCopyToClipboard(synthesis)}
                  title="Copy to clipboard"
                >
                  <Copy size={16} />
                  <span>Copy</span>
                </button>
              </div>
            ) : (
              <p className="no-data">No synthesis available</p>
            )}
          </div>
        )}
      </section>
    </div>
  );
}
