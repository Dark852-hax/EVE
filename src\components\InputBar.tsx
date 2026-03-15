import { useState, useRef, useEffect } from 'react';

interface InputBarProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

const InputBar = ({ onSend, disabled }: InputBarProps) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px';
    }
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="input-bar">
      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message EVE..."
            disabled={disabled}
            rows={1}
          />
          <button
            type="submit"
            className="send-button"
            disabled={!message.trim() || disabled}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path
                d="M22 2L11 13"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M22 2L15 22L11 13L2 9L22 2Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </div>
        <div className="input-hint">
          Press Enter to send, Shift+Enter for new line
        </div>
      </form>

      <style>{`
        .input-bar {
          padding: var(--space-md) var(--space-lg);
          background: var(--bg-secondary);
          border-top: 1px solid var(--border);
        }

        .input-form {
          max-width: 800px;
          margin: 0 auto;
        }

        .input-container {
          display: flex;
          align-items: flex-end;
          gap: var(--space-sm);
          background: var(--bg-tertiary);
          border: 1px solid var(--border);
          border-radius: 12px;
          padding: var(--space-sm);
          transition: border-color var(--transition), box-shadow var(--transition);
        }

        .input-container:focus-within {
          border-color: var(--accent-primary);
          box-shadow: var(--shadow-glow);
        }

        .input-container textarea {
          flex: 1;
          background: transparent;
          border: none;
          resize: none;
          padding: var(--space-sm);
          font-family: inherit;
          font-size: 14px;
          line-height: 1.5;
          color: var(--text-primary);
          max-height: 150px;
        }

        .input-container textarea:focus {
          outline: none;
          box-shadow: none;
        }

        .input-container textarea::placeholder {
          color: var(--text-secondary);
        }

        .send-button {
          width: 40px;
          height: 40px;
          border-radius: 8px;
          background: var(--accent-gradient);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all var(--transition);
          flex-shrink: 0;
        }

        .send-button:hover:not(:disabled) {
          transform: scale(1.05);
          box-shadow: var(--shadow-glow);
        }

        .send-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .send-button svg {
          width: 18px;
          height: 18px;
        }

        .input-hint {
          text-align: center;
          font-size: 11px;
          color: var(--text-secondary);
          margin-top: var(--space-xs);
        }
      `}</style>
    </div>
  );
};

export default InputBar;
