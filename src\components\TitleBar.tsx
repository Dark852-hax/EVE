import { useState } from 'react';

const TitleBar = () => {
  const [isMaximized, setIsMaximized] = useState(false);

  const handleMinimize = () => {
    // Electron API would handle this
    console.log('Minimize');
  };

  const handleMaximize = () => {
    setIsMaximized(!isMaximized);
    console.log('Maximize');
  };

  const handleClose = () => {
    console.log('Close');
  };

  return (
    <div className="title-bar">
      <div className="title-bar-drag">
        <div className="title-bar-logo">
          <span className="logo-icon">◈</span>
          <span className="logo-text">EVE AI</span>
        </div>
      </div>
      <div className="title-bar-controls">
        <button className="control-btn minimize" onClick={handleMinimize} title="Minimize">
          <svg width="12" height="12" viewBox="0 0 12 12">
            <rect fill="currentColor" width="10" height="1" x="1" y="6" />
          </svg>
        </button>
        <button className="control-btn maximize" onClick={handleMaximize} title="Maximize">
          {isMaximized ? (
            <svg width="12" height="12" viewBox="0 0 12 12">
              <rect fill="none" stroke="currentColor" width="7" height="7" x="1.5" y="3.5" />
              <polyline fill="none" stroke="currentColor" points="3.5,3.5 3.5,1.5 10.5,1.5 10.5,8.5 8.5,8.5" />
            </svg>
          ) : (
            <svg width="12" height="12" viewBox="0 0 12 12">
              <rect fill="none" stroke="currentColor" width="9" height="9" x="1.5" y="1.5" />
            </svg>
          )}
        </button>
        <button className="control-btn close" onClick={handleClose} title="Close">
          <svg width="12" height="12" viewBox="0 0 12 12">
            <line stroke="currentColor" x1="2" y1="2" x2="10" y2="10" strokeWidth="1.5" />
            <line stroke="currentColor" x1="10" y1="2" x2="2" y2="10" strokeWidth="1.5" />
          </svg>
        </button>
      </div>

      <style>{`
        .title-bar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 36px;
          background: var(--bg-secondary);
          border-bottom: 1px solid var(--border);
          -webkit-app-region: drag;
          user-select: none;
        }

        .title-bar-drag {
          flex: 1;
          display: flex;
          align-items: center;
          height: 100%;
          padding-left: var(--space-md);
        }

        .title-bar-logo {
          display: flex;
          align-items: center;
          gap: var(--space-sm);
        }

        .logo-icon {
          font-size: 18px;
          background: var(--accent-gradient);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .logo-text {
          font-size: 13px;
          font-weight: 600;
          color: var(--text-primary);
          letter-spacing: 0.5px;
        }

        .title-bar-controls {
          display: flex;
          -webkit-app-region: no-drag;
        }

        .control-btn {
          width: 46px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: var(--text-secondary);
          transition: all var(--transition);
        }

        .control-btn:hover {
          background: var(--bg-tertiary);
          color: var(--text-primary);
        }

        .control-btn.close:hover {
          background: var(--error);
          color: white;
        }

        .control-btn svg {
          width: 12px;
          height: 12px;
        }
      `}</style>
    </div>
  );
};

export default TitleBar;
