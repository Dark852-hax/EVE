import React from 'react';
import { Message } from '../types';

interface ChatAreaProps {
  messages: Message[];
  isProcessing: boolean;
}

const ChatArea = ({ messages, isProcessing }: ChatAreaProps) => {
  const formatTime = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const renderContent = (content: string) => {
    const lines = content.split('\n');
    const elements: any[] = [];
    let inTable = false;
    let tableLines: string[] = [];

    lines.forEach((line, i) => {
      // Handle tables
      if (line.includes('|') && line.trim().startsWith('|')) {
        if (!inTable) {
          inTable = true;
          tableLines = [];
        }
        tableLines.push(line);
      } else {
        if (inTable) {
          // Render the table
          const rows = tableLines.map(tl => tl.split('|').filter(c => c.trim()));
          if (rows.length > 1) {
            elements.push(
              <table key={`table-${i}`} className="eve-table">
                <tbody>
                  {rows.map((row, ri) => (
                    <tr key={ri}>
                      {row.map((cell: string, ci: number) => (
                        <td key={ci}>{cell}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            );
          }
          inTable = false;
          tableLines = [];
        }

        // Handle headers
        if (line.startsWith('# ')) {
          elements.push(<h1 key={i}>{line.replace('# ', '')}</h1>);
        } else if (line.startsWith('## ')) {
          elements.push(<h2 key={i}>{line.replace('## ', '')}</h2>);
        } else if (line.startsWith('### ')) {
          elements.push(<h3 key={i}>{line.replace('### ', '')}</h3>);
        }
        // Handle bullet points
        else if (line.startsWith('- ') || line.startsWith('• ')) {
          elements.push(<li key={i}>{line.replace(/^[•-] /, '')}</li>);
        }
        // Handle bold
        else if (line.includes('**')) {
          const parts = line.split(/(\*\*[^*]+\*\*)/g);
          elements.push(
            <p key={i}>
              {parts.map((part, j) => 
                part.startsWith('**') && part.endsWith('**') ? 
                  <strong key={j}>{part.replace(/\*\*/g, '')}</strong> : part
              )}
            </p>
          );
        }
        // Empty line
        else if (line.trim() === '') {
          elements.push(<br key={i} />);
        }
        // Regular text
        else {
          elements.push(<p key={i}>{line}</p>);
        }
      }
    });

    return elements;
  };

  return (
    <div className="chat-area">
      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}`}>
            <div className="message-avatar">
              {message.role === 'assistant' ? '◈' : '👤'}
            </div>
            <div className="message-content">
              <div className="message-header">
                <span className="message-author">
                  {message.role === 'assistant' ? 'EVE AI' : 'You'}
                </span>
                <span className="message-time">
                  {formatTime(message.timestamp)}
                </span>
              </div>
              <div className="message-body">
                {renderContent(message.content)}
              </div>
            </div>
          </div>
        ))}
        
        {isProcessing && (
          <div className="message assistant">
            <div className="message-avatar">◈</div>
            <div className="message-content">
              <div className="message-header">
                <span className="message-author">EVE AI</span>
                <span className="message-time">Thinking...</span>
              </div>
              <div className="message-body thinking">
                <div className="thinking-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <style>{`
        .chat-area {
          flex: 1;
          overflow-y: auto;
          padding: 24px;
          background: #0d0d0d;
        }

        .messages-container {
          max-width: 900px;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .message {
          display: flex;
          gap: 16px;
          animation: fadeIn 0.3s ease-out;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
          flex-direction: row-reverse;
        }

        .message-avatar {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: #1f1f1f;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 20px;
          flex-shrink: 0;
          border: 2px solid transparent;
        }

        .message.assistant .message-avatar {
          background: linear-gradient(135deg, #00d4aa, #00b894);
          color: white;
          box-shadow: 0 0 20px rgba(0, 212, 170, 0.4);
        }

        .message-content {
          flex: 1;
          max-width: calc(100% - 60px);
        }

        .message.user .message-content {
          text-align: right;
        }

        .message-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 8px;
        }

        .message.user .message-header {
          flex-direction: row-reverse;
        }

        .message-author {
          font-weight: 600;
          color: #ffffff;
          font-size: 14px;
        }

        .message-time {
          font-size: 12px;
          color: #666;
        }

        .message-body {
          background: #161616;
          border-radius: 16px;
          padding: 16px 20px;
          border: 1px solid #2a2a2a;
          text-align: left;
        }

        .message.user .message-body {
          background: rgba(0, 212, 170, 0.08);
          border-color: rgba(0, 212, 170, 0.2);
        }

        .message-body p {
          margin: 0;
          line-height: 1.7;
          color: #e0e0e0;
        }

        .message-body h1 {
          font-size: 24px;
          font-weight: 700;
          margin: 0 0 16px;
          background: linear-gradient(135deg, #00d4aa, #00ffcc);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .message-body h2 {
          font-size: 18px;
          font-weight: 600;
          margin: 20px 0 12px;
          color: #00d4aa;
        }

        .message-body h3 {
          font-size: 15px;
          font-weight: 600;
          margin: 16px 0 8px;
          color: #ffffff;
        }

        .message-body li {
          margin-left: 24px;
          margin-bottom: 8px;
          line-height: 1.6;
          color: #c0c0c0;
        }

        .message-body strong {
          color: #00d4aa;
        }

        .message-body table {
          width: 100%;
          border-collapse: collapse;
          margin: 12px 0;
          font-size: 13px;
        }

        .message-body table td {
          padding: 8px 12px;
          border: 1px solid #333;
          color: #c0c0c0;
        }

        .thinking {
          display: flex;
          align-items: center;
          padding: 8px 0;
        }

        .thinking-dots {
          display: flex;
          gap: 6px;
        }

        .thinking-dots span {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #00d4aa;
          animation: bounce 1.4s ease-in-out infinite;
        }

        .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
        .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
          40% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default ChatArea;
