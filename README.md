# EVE - Ultimate AI Assistant v4.0

**Created by:** Hassan Muzenda

EVE is an advanced AI assistant with enterprise-grade capabilities including multimodal I/O, reasoning, task primitives, safety, and interoperability.

## 🚀 Features

### 🤖 AI Capabilities
- **Chain-of-Thought Reasoning** - Step-by-step reasoning with confidence scores
- **Task Planning** - Breaks complex goals into clear steps
- **Multiple AI Support** - Add and switch between different AI endpoints
- **Plugin System** - Add custom AI repositories and endpoints
- **Multiple Chat Sessions** - Separate conversations by topic
- **Voice Chat** - Text-to-Speech and Speech-to-Text

### 🌐 Multimodal I/O
- **Text** - Full text input/output
- **Voice** - Speech-to-text and text-to-speech
- **Images** - Image analysis and description
- **Provenance** - Always show sources and confidence levels

### 🛠️ Task Primitives
- **Document Drafting** - Reports, contracts, emails, letters, memos
- **Summarization** - Text summarization in various styles
- **Data Import/Export** - CSV and Excel support
- **Code Scaffolding** - Generate code in multiple languages
- **Code Debugging** - Analyze and suggest fixes
- **Scheduling** - Task scheduling
- **Reminders** - Set and manage reminders
- **API Orchestration** - Coordinate multiple APIs

### 🛡️ Safety, Privacy & Compliance
- **Role-Based Access** - Admin, Power User, Standard, Guest, Child
- **Encryption** - Data encryption at rest
- **Audit Logs** - Full traceability
- **Human-in-the-Loop** - Approval required for high-risk actions
- **Opt-in Memory** - User controls memory storage
- **Content Filtering** - Inappropriate content filtering
- **Age Adaptation** - Responses adapted for children

### 🔌 Interoperability & Connectors
- **Google Calendar** - Calendar integration
- **Google Drive** - Cloud storage
- **Outlook** - Calendar and email
- **Gmail** - Email integration
- **Dropbox** - Cloud storage
- **OneDrive** - Cloud storage
- **Salesforce CRM** - CRM integration
- **Custom APIs** - Register and orchestrate custom endpoints

### 🛡️ Security & Pen Testing Tools
- **Port Scanner** - TCP port scanning
- **DNS Lookup** - DNS enumeration
- **WHOIS Lookup** - Domain registration info
- **Security Headers Analysis** - HTTP security headers
- **SSL/TLS Analysis** - Certificate analysis
- **Password Strength** - Password testing
- **Hash Identifier** - Hash type identification
- **Report Generator** - Professional pen test reports

### 💾 Memory System
- Persistent SQLite memory
- Conversation history
- User preferences
- Learned facts

### 🌍 Localization
- **14 Languages**: English, Shona, Japanese, Korean, Russian, Chinese, Spanish, French, German, Portuguese, Arabic, Hindi, Swahili, Zulu
- **Simple Language Mode** - For accessibility
- **Voice Prompts** - Audio feedback

### 👥 Age-Specific Features
- **Ages 10-18**: Homework help, tutoring, study summaries
- **Ages 19-64**: Professional workflows, research, code assistance
- **Ages 65-90**: Medication reminders, simplified UI, appointment help

## 📁 Project Structure

```
eve/
├── backend/
│   ├── ai_engine.py        # Core AI reasoning
│   ├── memory.py          # SQLite memory
│   ├── tools.py           # General tools
│   ├── plugins.py         # Custom AI plugins
│   ├── security.py        # Pen testing tools
│   ├── voice.py          # Voice (TTS/STT)
│   ├── language.py        # Multi-language
│   ├── multimodal.py      # Text, voice, image I/O
│   ├── tasks.py          # Task primitives
│   ├── safety.py         # Safety & compliance
│   ├── connectors.py     # External integrations
│   ├── reasoning.py      # Planning engine
│   ├── config_manager.py # Sessions & AI config
│   ├── server.py         # FastAPI server
│   ├── config.json       # Configuration
│   └── requirements.txt
│
├── src/                   # React frontend
└── electron/             # Desktop app
```

## 🚦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+

### Backend Setup
```bash
cd eve/backend
pip install -r requirements.txt
```

### Run Backend
```bash
python server.py
```

## 🌐 Access

- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs

## ⚠️ Legal Notice

**IMPORTANT:** This tool is for AUTHORIZED SECURITY TESTING ONLY.
- Only use on systems you have explicit permission to test

---

**EVE AI** - Created by Hassan Muzenda  
**Version:** 4.0.0  
**Built with ❤️**
