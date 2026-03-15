import React from 'react';
import { useState, useRef, useEffect } from 'react';
import ChatArea from './components/ChatArea';
import { Message, SidebarView } from './types';
import { v4 as uuidv4 } from 'uuid';

// Voice recognition and synthesis
const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
const speechSynthesis = window.speechSynthesis;

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: uuidv4(),
      role: 'assistant',
      content: `# Welcome to EVE AI 🌟

I'm your voice-enabled AI assistant. 

## Voice Commands:
- 🎤 Click the microphone to speak
- Say "EVE" to get my attention
- Commands: stop, continue, repeat, louder, quieter

## My Tone:
I speak with a calm, commanding voice - authoritative yet soothing.

## What I Can Do:
- Voice-activated assistance
- Chain-of-thought reasoning
- Task primitives (documents, code, data)
- Security tools & more

*Type or speak to begin...*`,
      timestamp: Date.now(),
    }
  ]);
  const [currentView, setCurrentView] = useState<SidebarView>('chat');
  const [isProcessing, setIsProcessing] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isListening, setIsListening] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize speech recognition
  useEffect(() => {
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((result: any) => result[0].transcript)
          .join('');

        if (event.results[0].isFinal) {
          handleVoiceInput(transcript);
        }
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, []);

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  // Text to Speech - calm, commanding
  const speak = (text: string) => {
    if (!voiceEnabled || !speechSynthesis) return;

    // Cancel any ongoing speech
    speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;  // Slightly slower - commanding
    utterance.pitch = 1.0;
    utterance.volume = 0.8;
    
    // Select a calm voice
    const voices = speechSynthesis.getVoices();
    const calmVoice = voices.find((v: any) => v.name.includes('Google UK English Female')) || 
                     voices.find((v: any) => v.name.includes('Microsoft Zira')) ||
                     voices[0];
    if (calmVoice) {
      utterance.voice = calmVoice;
    }

    speechSynthesis.speak(utterance);
  };

  // Handle voice input
  const handleVoiceInput = (transcript: string) => {
    if (!transcript.trim()) return;

    // Check for wake word
    const lower = transcript.toLowerCase().trim();
    
    // Add user message
    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content: transcript,
      timestamp: Date.now(),
    };
    setMessages((prev: Message[]) => [...prev, userMessage]);
    setIsProcessing(true);

    // Process the command
    setTimeout(() => {
      const response = generateResponse(transcript);
      const eveMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: response,
        timestamp: Date.now(),
      };
      setMessages((prev: Message[]) => [...prev, eveMessage]);
      setIsProcessing(false);

      // Speak the response if voice is enabled
      if (voiceEnabled) {
        // Extract plain text for speech (remove markdown)
        const plainText = response
          .replace(/#{1,6}\s/g, '')
          .replace(/\*\*/g, '')
          .replace(/\|/g, '')
          .replace(/-/g, '')
          .replace(/```[\s\S]*?```/g, '')
          .substring(0, 500);
        speak(plainText);
      }
    }, 800);
  };

  // Generate response with calm, commanding tone
  const generateResponse = (input: string): string => {
    const lower = input.toLowerCase();

    // Voice commands
    if (lower.includes('stop') || lower.includes('wait')) {
      speechSynthesis.cancel();
      return `# ⏸️ Paused.

I'm here when you're ready. Just say "continue" or tap the microphone.`;
    }

    if (lower.includes('continue') || lower.includes('go')) {
      return `# ▶️ Continuing.

I'm ready. What do you need?`;
    }

    if (lower.includes('repeat')) {
      return `# 🔄 Say that again?

I want to make sure I understand correctly.`;
    }

    if (lower.includes('louder')) {
      return `# 🔊 Volume increased.

Better?`;
    }

    if (lower.includes('quieter') || lower.includes('softer')) {
      return `# 🔉 Reducing volume.

More comfortable?`;
    }

    // Help
    if (lower.includes('help') || lower.includes('what can you do')) {
      return `# 🤖 What I Can Do

### Voice Commands:
- "Stop" - Pause listening
- "Continue" - Resume
- "Repeat" - Ask me to repeat
- "Louder/Quieter" - Adjust volume

### Capabilities:
- Answer questions
- Write code
- Analyze data
- Draft documents
- And much more...

*How may I assist you?*`;
    }

    // Default responses with calm tone
    const responses = [
      `# 🤔 Let me think about that.

One moment, please.`,
      `# 💭 Processing your request.

Give me a moment to formulate the best response.`,
      `# 📝 I understand.

Let me provide you with a comprehensive answer.`,
      `# 🎯 Got it.

Working on your request now.`,
    ];

    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    return randomResponse + `\n\n---\n\n**Your query:** "${input}"\n\nI'm here to help. What would you like to know?`;
  };

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content,
      timestamp: Date.now(),
    };
    
    setMessages((prev: Message[]) => [...prev, userMessage]);
    setIsProcessing(true);

    setTimeout(() => {
      const response = generateEVEResponse(content);
      const eveMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: response,
        timestamp: Date.now(),
      };
      setMessages((prev: Message[]) => [...prev, eveMessage]);
      setIsProcessing(false);

      if (voiceEnabled) {
        const plainText = response.replace(/#{1,6}\s/g, '').replace(/\*\*/g, '').substring(0, 500);
        speak(plainText);
      }
    }, 1000);
  };

  const generateEVEResponse = (input: string): string => {
    const lowerInput = input.toLowerCase();

    // Code
    if (lowerInput.includes('code') || lowerInput.includes('python') || lowerInput.includes('javascript')) {
      return `# 💻 Code Assistance

I've detected a code-related request.

### My Code Capabilities:
- Write new code
- Debug existing code
- Explain code logic
- Optimize performance
- Generate code scaffolds

---

**What specific coding task can I help you with?**`;
    }

    // Search
    if (lowerInput.includes('search') || lowerInput.includes('find') || lowerInput.includes('look up')) {
      return `# 🌐 Web Search

I'm ready to search the web for information.

### Search Capabilities:
- Real-time web search
- Source verification
- Content extraction
- Data synthesis

---

**What would you like me to search for?**`;
    }

    // Security
    if (lowerInput.includes('security') || lowerInput.includes('hack') || lowerInput.includes('scan')) {
      return `# 🛡️ Security Tools

⚠️ **Authorized testing only**

### Available Tools:
- Port scanning
- DNS lookup
- WHOIS lookup
- SSL analysis
- Security headers check

---

**Please specify the target and tool.**`;
    }

    // Default
    return `# ⚡ Processing: "${input}"

### My Analysis:
I've received your message and am formulating a response.

### Core Capabilities:
| Category | Features |
|----------|----------|
| 🤖 AI | Reasoning, planning |
| 💻 Code | Write, debug, explain |
| 🌐 Search | Web research |
| 📁 Files | Read, write, organize |
| 🎤 Voice | Speech I/O |

---

**How may I assist you further?**`;
  };

  return (
    <div className="eve-app">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="logo">
            <span className="logo-icon">◈</span>
            <span className="logo-text">EVE</span>
          </div>
          <button className="toggle-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>
        
        <div className="sidebar-content">
          <button className={`nav-item ${currentView === 'chat' ? 'active' : ''}`} onClick={() => setCurrentView('chat')}>
            <span className="nav-icon">💬</span>
            <span className="nav-text">Chat</span>
          </button>
          <button className={`nav-item ${currentView === 'tools' ? 'active' : ''}`} onClick={() => setCurrentView('tools')}>
            <span className="nav-icon">🔧</span>
            <span className="nav-text">Tools</span>
          </button>
          <button className={`nav-item ${currentView === 'memory' ? 'active' : ''}`} onClick={() => setCurrentView('memory')}>
            <span className="nav-icon">🧠</span>
            <span className="nav-text">Memory</span>
          </button>
          <button className={`nav-item ${currentView === 'settings' ? 'active' : ''}`} onClick={() => setCurrentView('settings')}>
            <span className="nav-icon">⚙️</span>
            <span className="nav-text">Settings</span>
          </button>
        </div>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">👤</div>
            <div className="user-details">
              <span className="user-name">User</span>
              <span className="user-role">Voice Active</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-area">
        {/* Top Bar */}
        <header className="top-bar">
          <div className="breadcrumb">
            <span className="breadcrumb-item">Home</span>
            <span className="breadcrumb-separator">/</span>
            <span className="breadcrumb-item active">{currentView.charAt(0).toUpperCase() + currentView.slice(1)}</span>
          </div>
          <div className="top-bar-actions">
            <button 
              className={`action-btn voice-btn ${isListening ? 'listening' : ''}`}
              onClick={isListening ? stopListening : startListening}
              title={isListening ? 'Stop listening' : 'Voice input'}
            >
              {isListening ? '🔊' : '🎤'}
            </button>
            <button 
              className={`action-btn ${voiceEnabled ? '' : 'muted'}`}
              onClick={() => setVoiceEnabled(!voiceEnabled)}
              title={voiceEnabled ? 'Mute voice' : 'Enable voice'}
            >
              {voiceEnabled ? '🔊' : '🔇'}
            </button>
          </div>
        </header>

        {/* Chat Area */}
        <div className="chat-container">
          <ChatArea messages={messages} isProcessing={isProcessing} />
          
          {/* Input Area */}
          <div className="input-container">
            <div className="input-wrapper">
              <textarea 
                className="message-input" 
                placeholder="Message EVE... (or speak)"
                rows={1}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    const input = (e.target as HTMLTextAreaElement).value;
                    if (input.trim()) {
                      handleSendMessage(input);
                      (e.target as HTMLTextAreaElement).value = '';
                    }
                  }
                }}
              />
              <div className="input-actions">
                <button 
                  className="input-btn voice-input-btn" 
                  onClick={isListening ? stopListening : startListening}
                  title={isListening ? 'Listening...' : 'Voice input'}
                >
                  {isListening ? '🔊' : '🎤'}
                </button>
                <button className="input-btn send-btn" title="Send">
                  ➤
                </button>
              </div>
            </div>
            <div className="input-footer">
              <span className="disclaimer">
                {voiceEnabled ? '🔊 Voice enabled' : '🔇 Voice muted'} • EVE can make mistakes
              </span>
            </div>
          </div>
        </div>
      </main>

      <style>{`
        :root {
          --bg-primary: #0d0d0d;
          --bg-secondary: #161616;
          --bg-tertiary: #1f1f1f;
          --bg-hover: #2a2a2a;
          --accent-primary: #00d4aa;
          --accent-secondary: #00b894;
          --accent-glow: rgba(0, 212, 170, 0.3);
          --text-primary: #ffffff;
          --text-secondary: #a0a0a0;
          --text-muted: #666666;
          --border-color: #2a2a2a;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
          font-family: 'Segoe UI', -apple-system, sans-serif;
          background: var(--bg-primary);
          color: var(--text-primary);
          overflow: hidden;
        }

        .eve-app { display: flex; height: 100vh; }

        .sidebar {
          width: 260px;
          background: var(--bg-secondary);
          border-right: 1px solid var(--border-color);
          display: flex;
          flex-direction: column;
          transition: width 0.3s;
        }
        .sidebar.closed { width: 60px; }

        .sidebar-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 16px;
          border-bottom: 1px solid var(--border-color);
        }

        .logo { display: flex; align-items: center; gap: 10px; }

        .logo-icon {
          font-size: 24px;
          background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .logo-text {
          font-size: 20px;
          font-weight: 700;
          background: linear-gradient(135deg, var(--accent-primary), #00ffcc);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .toggle-btn {
          background: none;
          border: none;
          color: var(--text-secondary);
          cursor: pointer;
          padding: 4px 8px;
        }

        .sidebar-content {
          flex: 1;
          padding: 12px 8px;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .nav-item {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px 16px;
          border: none;
          background: none;
          color: var(--text-secondary);
          cursor: pointer;
          border-radius: 8px;
          font-size: 14px;
          transition: all 0.2s;
          width: 100%;
        }
        .nav-item:hover { background: var(--bg-hover); color: var(--text-primary); }
        .nav-item.active { background: rgba(0, 212, 170, 0.1); color: var(--accent-primary); }

        .sidebar-footer {
          padding: 16px;
          border-top: 1px solid var(--border-color);
        }

        .user-info { display: flex; align-items: center; gap: 12px; }
        .user-avatar {
          width: 36px; height: 36px;
          border-radius: 50%;
          background: var(--bg-tertiary);
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .user-details { display: flex; flex-direction: column; }
        .user-name { font-size: 14px; font-weight: 600; }
        .user-role { font-size: 12px; color: var(--accent-primary); }

        .main-area { flex: 1; display: flex; flex-direction: column; background: var(--bg-primary); }

        .top-bar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px 24px;
          border-bottom: 1px solid var(--border-color);
          background: var(--bg-secondary);
        }

        .breadcrumb { display: flex; gap: 8px; font-size: 14px; }
        .breadcrumb-item { color: var(--text-secondary); }
        .breadcrumb-item.active { color: var(--text-primary); }
        .breadcrumb-separator { color: var(--text-muted); }

        .top-bar-actions { display: flex; gap: 8px; }

        .action-btn {
          width: 40px; height: 40px;
          border-radius: 10px;
          border: none;
          background: var(--bg-tertiary);
          color: var(--text-secondary);
          cursor: pointer;
          font-size: 18px;
          transition: all 0.2s;
        }
        .action-btn:hover { background: var(--bg-hover); color: var(--accent-primary); }
        .action-btn.listening { 
          background: rgba(0, 212, 170, 0.2); 
          color: var(--accent-primary);
          animation: pulse 1.5s infinite;
        }
        .action-btn.muted { opacity: 0.5; }

        @keyframes pulse {
          0%, 100% { box-shadow: 0 0 0 0 var(--accent-glow); }
          50% { box-shadow: 0 0 0 8px transparent; }
        }

        .chat-container { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

        .input-container {
          padding: 16px 24px 24px;
          background: var(--bg-secondary);
        }

        .input-wrapper {
          display: flex;
          align-items: flex-end;
          gap: 12px;
          background: var(--bg-tertiary);
          border-radius: 16px;
          padding: 12px 16px;
          border: 1px solid var(--border-color);
          transition: border-color 0.2s;
        }
        .input-wrapper:focus-within {
          border-color: var(--accent-primary);
          box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .message-input {
          flex: 1;
          background: none;
          border: none;
          color: var(--text-primary);
          font-size: 15px;
          resize: none;
          max-height: 120px;
          outline: none;
          font-family: inherit;
        }
        .message-input::placeholder { color: var(--text-muted); }

        .input-actions { display: flex; gap: 8px; }

        .input-btn {
          width: 36px; height: 36px;
          border-radius: 10px;
          border: none;
          background: none;
          color: var(--text-secondary);
          cursor: pointer;
          font-size: 16px;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .input-btn:hover { background: var(--bg-hover); color: var(--text-primary); }

        .voice-input-btn {
          background: var(--bg-hover);
          font-size: 18px;
        }

        .send-btn {
          background: var(--accent-primary);
          color: var(--bg-primary);
        }
        .send-btn:hover { background: var(--accent-secondary); }

        .input-footer { margin-top: 8px; text-align: center; }
        .disclaimer { font-size: 11px; color: var(--text-muted); }
      `}</style>
    </div>
  );
}

export default App;
