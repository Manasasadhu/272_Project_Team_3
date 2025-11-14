import { X } from 'lucide-react';
import '../styles/ProcessingIndicator.css';

interface ProcessingIndicatorProps {
  isVisible: boolean;
  message?: string;
  onCancel: () => void;
  progress?: number;
}

export default function ProcessingIndicator({
  isVisible,
  message = 'Processing your request...',
  onCancel,
  progress = 0,
}: ProcessingIndicatorProps) {
  if (!isVisible) return null;

  return (
    <div className="processing-overlay">
      <div className="processing-card">
        <div className="processing-header">
          <h3>Processing</h3>
          <button
            className="close-btn"
            onClick={onCancel}
            aria-label="Cancel processing"
          >
            <X size={20} />
          </button>
        </div>

        <div className="processing-content">
          {/* Spinner */}
          <div className="spinner-container">
            <div className="spinner-large"></div>
          </div>

          {/* Status Message */}
          <p className="processing-message">{message}</p>

          {/* Progress Bar */}
          <div className="progress-container">
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${Math.min(progress, 100)}%` }}
              ></div>
            </div>
            <span className="progress-text">{Math.round(progress)}%</span>
          </div>

          {/* Cancel Button */}
          <button className="cancel-btn" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
