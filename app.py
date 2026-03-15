"""
EVE AI v4.0 - Universal AI Assistant
Python only - connects to real AI APIs and GitHub
"""

import json
import os
import asyncio
import urllib.request
import urllib.error
import ssl
from datetime import datetime
from typing import Dict, List, Optional, Any
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==================== CONFIG ====================

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'backend', 'config.json')

def load_config() -> Dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"default_ai": {"api_key": "", "model": "gpt-4", "endpoint": "https://api.openai.com/v1/chat/completions"}}

config = load_config()

# ==================== AI ENGINE ====================

class AIEngine:
    def __init__(self):
        self.config = config
        self.default_ai = self.config.get('default_ai', {})
        self.api_key = self.default_ai.get('api_key', '')
        self.model = self.default_ai.get('model', 'gpt-4')
        self.endpoint = self.default_ai.get('endpoint', 'https://api.openai.com/v1/chat/completions')
    
    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key != "YOUR_OPENAI_API_KEY_HERE")
    
    async def generate_response(self, message: str, history: List[Dict] = None) -> str:
        if not self.is_configured():
            return self._not_configured_response()
        
        messages = self._build_messages(message, history or [])
        
        try:
            result = await self._call_api(messages)
            return result
        except Exception as e:
            return f"# Error\n\nFailed to connect to AI: {str(e)}\n\nPlease check your API key in config.json"
    
    def _build_messages(self, message: str, history: List[Dict]) -> List[Dict]:
        messages = [{"role": "system", "content": """You are EVE, a universal AI assistant created by Hassan Muzenda. 
You are calm, commanding, and professional. You help with:
- Answering questions with reasoning
- Writing and debugging code
- Research and web search
- Document drafting
- File operations
- General problem solving

Always be helpful, accurate, and concise."""}]
        
        for msg in history[-10:]:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
        
        messages.append({"role": "user", "content": message})
        return messages
    
    async def _call_api(self, messages: List[Dict]) -> str:
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.api_key}'}
        
        data = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }).encode('utf-8')
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(self.endpoint, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    
    def _not_configured_response(self) -> str:
        return """# API Not Configured

Your AI API key is not set. Please configure it to use EVE.

## Setup Instructions:

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Edit: `eve/backend/config.json`
3. Add your API key:

```json
{
  "default_ai": {
    "api_key": "sk-your-key-here"
  }
}
```

## Supported AIs:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic Claude (coming soon)
- Local models (Ollama, LM Studio)

---

Once configured, EVE will respond using your API!"""

# ==================== GITHUB CONNECTOR ====================

class GitHubConnector:
    def __init__(self):
        self.token = config.get('github', {}).get('token', '')
        self.base_url = "https://api.github.com"
    
    async def search_repos(self, query: str) -> List[Dict]:
        if not self.token or self.token == "YOUR_GITHUB_TOKEN_HERE":
            return [{"error": "GitHub token not configured"}]
        
        url = f"{self.base_url}/search/repositories?q={urllib.parse.quote(query)}"
        headers = {'Authorization': f'token {self.token}', 'Accept': 'application/vnd.github.v3+json'}
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data.get('items', [])[:10]
        except Exception as e:
            return [{"error": str(e)}]
    
    async def list_repos(self, username: str) -> List[Dict]:
        if not self.token or self.token == "YOUR_GITHUB_TOKEN_HERE":
            return [{"error": "GitHub token not configured"}]
        
        url = f"{self.base_url}/users/{username}/repos?sort=updated&per_page=20"
        headers = {'Authorization': f'token {self.token}', 'Accept': 'application/vnd.github.v3+json'}
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return [{"error": str(e)}]

# ==================== AGI ENGINE ====================
AGI_AVAILABLE = False
try:
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    from agi_engine import AGIEngine as AGI
    AGI_AVAILABLE = True
except ImportError:
    print("[EVE] AGI Engine not available")

# ==================== MAIN EVE APP ====================

class EVEApp:
    def __init__(self):
        self.ai = AIEngine()
        self.github = GitHubConnector()
        self.sessions: Dict[str, List[Dict]] = {'default': []}
        self.agi = AGI() if AGI_AVAILABLE else None
        if self.agi:
            print("[EVE] AGI Engine loaded!")
    
    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({'role': role, 'content': content, 'timestamp': datetime.now().isoformat()})
    
    def get_history(self, session_id: str) -> List[Dict]:
        return self.sessions.get(session_id, [])
    
    async def process_message(self, message: str, session_id: str = 'default') -> Dict[str, Any]:
        # Check for special commands
        if message.lower().startswith('github:') or 'github' in message.lower():
            return await self._handle_github(message, session_id)
        
        if message.lower().startswith('config:') or 'configure' in message.lower():
            return self._handle_config(message, session_id)
        
        # Check for AGI mode command
        if message.lower().startswith('agi:') or message.lower().startswith('autonomous'):
            if self.agi:
                result = await self.agi.process(message)
                return {'response': result['response'], 'session_id': session_id, 'api_configured': self.ai.is_configured(), 'mode': 'AGI'}
            else:
                return {'response': 'AGI mode not available', 'session_id': session_id}
        
        # Use AGI engine if available and API is not configured (for free tool use)
        if self.agi and not self.ai.is_configured():
            result = await self.agi.process(message)
            return {'response': result['response'], 'session_id': session_id, 'api_configured': False, 'mode': 'AGI'}
        
        # Default: use OpenAI API
        history = self.get_history(session_id)
        response = await self.ai.generate_response(message, history)
        
        self.add_message(session_id, 'user', message)
        self.add_message(session_id, 'assistant', response)
        
        return {'response': response, 'session_id': session_id, 'api_configured': self.ai.is_configured()}
    
    async def _handle_github(self, message: str, session_id: str) -> Dict[str, Any]:
        msg_lower = message.lower()
        
        if 'search' in msg_lower or 'find' in msg_lower:
            query = message.lower().replace('github', '').replace('search', '').replace('find', '').strip()
            if not query:
                return {'response': '# GitHub Search\n\nUsage: `github search <query>`\n\nExample: `github search python ai`', 'session_id': session_id}
            
            results = await self.github.search_repos(query)
            
            if results and 'error' in results[0]:
                return {'response': f"# GitHub Error\n\n{results[0]['error']}\n\nConfigure your GitHub token in the settings.", 'session_id': session_id}
            
            output = "# GitHub Search Results\n\n"
            for i, repo in enumerate(results, 1):
                output += f"### {i}. {repo.get('full_name', 'N/A')}\n"
                output += f"- Stars: {repo.get('stargazers_count', 0)} | Forks: {repo.get('forks_count', 0)}\n"
                output += f"- {repo.get('description', 'No description')}\n"
                output += f"- [View on GitHub]({repo.get('html_url', '')})\n\n"
            
            return {'response': output, 'session_id': session_id}
        
        if msg_lower.startswith('github my '):
            username = message.lower().replace('github my ', '').strip()
            repos = await self.github.list_repos(username)
            
            if repos and 'error' in repos[0]:
                return {'response': f"# Error\n\n{repos[0]['error']}", 'session_id': session_id}
            
            output = f"# {username}'s Repositories\n\n"
            for repo in repos[:10]:
                output += f"**{repo.get('name', 'N/A')}** - {repo.get('stargazers_count', 0)} stars\n"
                output += f"_{repo.get('description', 'No description')}_\n\n"
            
            return {'response': output, 'session_id': session_id}
        
        return {'response': '''# GitHub Commands

## Search Repositories:
```
github search python ai
```

## List User Repos:
```
github my username
```

## Configure Token:
Set your GitHub token in settings.
''', 'session_id': session_id}
    
    def _handle_config(self, message: str, session_id: str) -> Dict[str, Any]:
        msg_lower = message.lower()
        
        if 'api_key' in msg_lower or 'set key' in msg_lower:
            return {'response': '''# Configure API Key

Edit the file: `eve/backend/config.json`

Add your OpenAI key:

```json
{
  "default_ai": {
    "api_key": "sk-your-key-here"
  }
}
```

Get your key from: https://platform.openai.com/api-keys
''', 'session_id': session_id}
        
        if 'github' in msg_lower or 'token' in msg_lower:
            return {'response': '''# Configure GitHub Token

Edit `eve/backend/config.json` and add:

```json
{
  "github": {
    "token": "ghp_your_token_here"
  }
}
```

Generate token at: https://github.com/settings/tokens
''', 'session_id': session_id}
        
        status = "Configured" if self.ai.is_configured() else "Not Configured"
        return {'response': f'''# EVE Configuration

## AI API Status: {status}

## GitHub: Token not set

### To Configure:
1. Edit `eve/backend/config.json`
2. Add your API keys
3. Restart EVE
''', 'session_id': session_id}

eve = EVEApp()

# ==================== BEAUTIFUL MODERN UI ====================

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EVE AI - Universal Assistant</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0a0a0f;
            --bg-card: #12121a;
            --bg-input: #1a1a24;
            --accent: #00d4aa;
            --accent-glow: rgba(0, 212, 170, 0.3);
            --accent-dim: rgba(0, 212, 170, 0.1);
            --text: #e8e8ed;
            --text-dim: #8888a0;
            --text-muted: #55556a;
            --border: #2a2a3a;
            --success: #00d4aa;
            --warning: #ffaa00;
            --error: #ff4466;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            height: 100vh;
            overflow: hidden;
            line-height: 1.6;
        }

        /* Background Pattern */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(0, 212, 170, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(100, 100, 255, 0.05) 0%, transparent 50%),
                repeating-linear-gradient(0deg, transparent, transparent 50px, rgba(255,255,255,0.01) 50px, rgba(255,255,255,0.01) 51px),
                repeating-linear-gradient(90deg, transparent, transparent 50px, rgba(255,255,255,0.01) 50px, rgba(255,255,255,0.01) 51px);
            pointer-events: none;
            z-index: 0;
        }

        .app { display: flex; height: 100vh; position: relative; z-index: 1; }

        /* Sidebar */
        .sidebar {
            width: 280px;
            background: var(--bg-card);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            position: relative;
        }

        .sidebar::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 1px;
            height: 100%;
            background: linear-gradient(180deg, transparent, var(--accent), transparent);
            opacity: 0.3;
        }

        .logo-section {
            padding: 24px;
            border-bottom: 1px solid var(--border);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .logo-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--accent), #00ffcc);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 700;
            color: var(--bg-dark);
            box-shadow: 0 8px 32px var(--accent-glow);
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-4px); }
        }

        .logo-text {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent), #00ffcc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo-subtitle {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 4px;
        }

        .nav-section {
            flex: 1;
            padding: 16px 12px;
            overflow-y: auto;
        }

        .nav-label {
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1.2px;
            padding: 8px 12px;
            margin-bottom: 8px;
        }

        .nav-btn {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 16px;
            border: none;
            background: transparent;
            color: var(--text-dim);
            cursor: pointer;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
            width: 100%;
            text-align: left;
            margin-bottom: 4px;
        }

        .nav-btn:hover {
            background: var(--bg-input);
            color: var(--text);
        }

        .nav-btn.active {
            background: var(--accent-dim);
            color: var(--accent);
        }

        .nav-btn .icon {
            font-size: 18px;
            width: 24px;
            text-align: center;
        }

        .sidebar-footer {
            padding: 16px;
            border-top: 1px solid var(--border);
        }

        .status-card {
            background: var(--bg-input);
            border-radius: 12px;
            padding: 16px;
        }

        .status-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 0;
        }

        .status-label {
            font-size: 12px;
            color: var(--text-dim);
        }

        .status-badge {
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 20px;
            font-weight: 500;
        }

        .status-badge.ready {
            background: rgba(0, 212, 170, 0.15);
            color: var(--success);
        }

        .status-badge.not-ready {
            background: rgba(255, 100, 100, 0.15);
            color: var(--error);
        }

        /* Main Area */
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: transparent;
        }

        /* Header */
        .header {
            padding: 20px 32px;
            background: rgba(18, 18, 26, 0.8);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .page-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--text);
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .header-btn {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--bg-card);
            color: var(--text-dim);
            cursor: pointer;
            font-size: 18px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .header-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        .header-btn.listening {
            background: var(--accent-dim);
            border-color: var(--accent);
            color: var(--accent);
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0 var(--accent-glow); }
            50% { box-shadow: 0 0 0 8px transparent; }
        }

        /* Chat */
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 32px;
        }

        .chat-wrapper {
            max-width: 800px;
            margin: 0 auto;
        }

        .message {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
            flex-direction: row-reverse;
        }

        .avatar {
            width: 44px;
            height: 44px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
            background: var(--bg-card);
        }

        .message.assistant .avatar {
            background: linear-gradient(135deg, var(--accent), #00ffcc);
            box-shadow: 0 8px 24px var(--accent-glow);
        }

        .msg-content {
            flex: 1;
            max-width: calc(100% - 70px);
        }

        .msg-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
        }

        .message.user .msg-header {
            flex-direction: row-reverse;
        }

        .msg-author {
            font-weight: 600;
            font-size: 14px;
        }

        .msg-time {
            font-size: 12px;
            color: var(--text-muted);
        }

        .msg-body {
            background: var(--bg-card);
            border-radius: 18px;
            padding: 20px 24px;
            border: 1px solid var(--border);
            position: relative;
        }

        .message.user .msg-body {
            background: linear-gradient(135deg, rgba(0, 212, 170, 0.1), rgba(0, 212, 170, 0.05));
            border-color: rgba(0, 212, 170, 0.2);
        }

        .msg-body h1 {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 16px;
            color: var(--accent);
        }

        .msg-body h2 {
            font-size: 16px;
            font-weight: 600;
            margin: 20px 0 12px;
            color: var(--text);
        }

        .msg-body h3 {
            font-size: 14px;
            font-weight: 600;
            margin: 16px 0 8px;
            color: var(--text);
        }

        .msg-body p {
            margin-bottom: 12px;
            color: #c8c8d0;
            line-height: 1.7;
        }

        .msg-body a {
            color: var(--accent);
            text-decoration: none;
        }

        .msg-body a:hover {
            text-decoration: underline;
        }

        .msg-body ul, .msg-body ol {
            margin: 12px 0;
            padding-left: 24px;
        }

        .msg-body li {
            margin-bottom: 8px;
            color: #b0b0c0;
        }

        .msg-body code {
            background: var(--bg-input);
            padding: 3px 8px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            color: var(--accent);
        }

        .msg-body pre {
            background: var(--bg-input);
            padding: 16px;
            border-radius: 12px;
            overflow-x: auto;
            margin: 12px 0;
            border: 1px solid var(--border);
        }

        .msg-body pre code {
            background: none;
            padding: 0;
            color: #d0d0e0;
        }

        .msg-body strong {
            color: var(--accent);
            font-weight: 600;
        }

        .msg-body em {
            color: var(--text-dim);
            font-style: italic;
        }

        /* Input */
        .input-area {
            padding: 24px 32px;
            background: rgba(18, 18, 26, 0.9);
            backdrop-filter: blur(20px);
            border-top: 1px solid var(--border);
        }

        .input-wrapper {
            max-width: 800px;
            margin: 0 auto;
            background: var(--bg-card);
            border-radius: 20px;
            padding: 8px;
            border: 1px solid var(--border);
            transition: all 0.2s;
            display: flex;
            gap: 8px;
        }

        .input-wrapper:focus-within {
            border-color: var(--accent);
            box-shadow: 0 0 0 4px var(--accent-glow);
        }

        .msg-input {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text);
            font-size: 15px;
            padding: 14px 18px;
            outline: none;
            resize: none;
            font-family: inherit;
            max-height: 150px;
        }

        .msg-input::placeholder {
            color: var(--text-muted);
        }

        .input-btn {
            width: 50px;
            height: 50px;
            border-radius: 14px;
            border: none;
            background: var(--bg-input);
            color: var(--text-dim);
            cursor: pointer;
            font-size: 18px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .input-btn:hover {
            background: var(--bg-card);
            color: var(--accent);
        }

        .input-btn.send {
            background: var(--accent);
            color: var(--bg-dark);
        }

        .input-btn.send:hover {
            background: #00ffcc;
            transform: scale(1.05);
        }

        /* Thinking */
        .thinking {
            display: flex;
            gap: 6px;
            padding: 8px 0;
        }

        .thinking span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent);
            animation: bounce 1.4s ease-in-out infinite;
        }

        .thinking span:nth-child(2) { animation-delay: 0.2s; }
        .thinking span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }

        /* Settings Panel */
        .settings-panel {
            display: none;
            padding: 32px;
            max-width: 800px;
            margin: 0 auto;
        }

        .settings-panel.active {
            display: block;
        }

        .settings-section {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
        }

        .settings-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text);
        }

        .settings-desc {
            font-size: 14px;
            color: var(--text-dim);
            margin-bottom: 16px;
        }

        .input-group {
            margin-bottom: 16px;
        }

        .input-label {
            display: block;
            font-size: 13px;
            font-weight: 500;
            color: var(--text-dim);
            margin-bottom: 8px;
        }

        .text-input {
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 16px;
            color: var(--text);
            font-size: 14px;
            outline: none;
            transition: all 0.2s;
        }

        .text-input:focus {
            border-color: var(--accent);
        }

        .btn-primary {
            background: var(--accent);
            color: var(--bg-dark);
            border: none;
            padding: 14px 28px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-primary:hover {
            background: #00ffcc;
            transform: translateY(-2px);
        }

        /* GitHub Panel */
        .github-panel {
            display: none;
            padding: 32px;
            max-width: 900px;
            margin: 0 auto;
        }

        .github-panel.active {
            display: block;
        }

        .repo-card {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid var(--border);
            transition: all 0.2s;
        }

        .repo-card:hover {
            border-color: var(--accent);
            transform: translateY(-2px);
        }

        .repo-name {
            font-size: 16px;
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 8px;
        }

        .repo-desc {
            font-size: 14px;
            color: var(--text-dim);
            margin-bottom: 12px;
        }

        .repo-stats {
            display: flex;
            gap: 20px;
            font-size: 13px;
            color: var(--text-muted);
        }

        .repo-stat {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Welcome */
        .welcome-card {
            background: linear-gradient(135deg, var(--bg-card), var(--bg-input));
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 24px;
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }

        .welcome-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, var(--accent-glow), transparent 70%);
            pointer-events: none;
        }

        .welcome-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 12px;
            background: linear-gradient(135deg, var(--text), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .welcome-subtitle {
            font-size: 15px;
            color: var(--text-dim);
            margin-bottom: 24px;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }

        .feature-item {
            background: var(--bg-dark);
            border-radius: 12px;
            padding: 16px;
            border: 1px solid var(--border);
        }

        .feature-icon {
            font-size: 24px;
            margin-bottom: 8px;
        }

        .feature-title {
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 4px;
        }

        .feature-desc {
            font-size: 12px;
            color: var(--text-muted);
        }

        .quick-commands {
            margin-top: 24px;
        }

        .quick-commands h3 {
            font-size: 14px;
            color: var(--text-dim);
            margin-bottom: 12px;
        }

        .command-chip {
            display: inline-block;
            background: var(--bg-input);
            border: 1px solid var(--border);
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 12px;
            color: var(--text-dim);
            margin-right: 8px;
            margin-bottom: 8px;
            font-family: 'JetBrains Mono', monospace;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="app">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="logo-section">
                <div class="logo">
                    <div class="logo-icon">E</div>
                    <div>
                        <div class="logo-text">EVE</div>
                        <div class="logo-subtitle">Universal AI Assistant</div>
                    </div>
                </div>
            </div>
            
            <div class="nav-section">
                <div class="nav-label">Menu</div>
                <button class="nav-btn active" data-view="chat">
                    <span class="icon">💬</span>
                    <span>Chat</span>
                </button>
                <button class="nav-btn" data-view="github">
                    <span class="icon">🔗</span>
                    <span>GitHub</span>
                </button>
                <button class="nav-btn" data-view="settings">
                    <span class="icon">⚙️</span>
                    <span>Settings</span>
                </button>
                <button class="nav-btn" data-view="plugins">
                    <span class="icon">🔌</span>
                    <span>Plugins</span>
                </button>
            </div>

            <div class="sidebar-footer">
                <div class="status-card">
                    <div class="status-row">
                        <span class="status-label">AI API</span>
                        <span class="status-badge not-ready" id="apiStatus">Not Set</span>
                    </div>
                    <div class="status-row">
                        <span class="status-label">GitHub</span>
                        <span class="status-badge not-ready" id="ghStatus">Not Set</span>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Main Area -->
        <main class="main">
            <!-- Header -->
            <header class="header">
                <div class="header-left">
                    <h1 class="page-title" id="pageTitle">Chat</h1>
                </div>
                <div class="header-right">
                    <button class="header-btn" onclick="toggleVoice()" id="voiceBtn" title="Voice">🎤</button>
                    <button class="header-btn" onclick="toggleMute()" id="muteBtn" title="Mute">🔊</button>
                </div>
            </header>

            <!-- Chat View -->
            <div class="chat-container" id="chatView">
                <div class="chat-wrapper" id="messages">
                    <!-- Welcome -->
                    <div class="welcome-card">
                        <h1 class="welcome-title">Welcome to EVE AI</h1>
                        <p class="welcome-subtitle">Your universal AI assistant with real intelligence.</p>
                        
                        <div class="feature-grid">
                            <div class="feature-item">
                                <div class="feature-icon">🤖</div>
                                <div class="feature-title">Real AI Power</div>
                                <div class="feature-desc">Connected to OpenAI API</div>
                            </div>
                            <div class="feature-item">
                                <div class="feature-icon">🔗</div>
                                <div class="feature-title">GitHub</div>
                                <div class="feature-desc">Search & explore repos</div>
                            </div>
                            <div class="feature-item">
                                <div class="feature-icon">🎤</div>
                                <div class="feature-title">Voice</div>
                                <div class="feature-desc">Speak to EVE</div>
                            </div>
                            <div class="feature-item">
                                <div class="feature-icon">🧠</div>
                                <div class="feature-title">Reasoning</div>
                                <div class="feature-desc">Chain-of-thought</div>
                            </div>
                        </div>

                        <div class="quick-commands">
                            <h3>Quick Commands:</h3>
                            <span class="command-chip">github search python</span>
                            <span class="command-chip">github my username</span>
                            <span class="command-chip">config:api_key</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Settings Panel -->
            <div class="settings-panel" id="settingsPanel">
                <div class="settings-section">
                    <h2 class="settings-title">API Configuration</h2>
                    <p class="settings-desc">Connect EVE to your AI provider.</p>
                    
                    <div class="input-group">
                        <label class="input-label">OpenAI API Key</label>
                        <input type="password" class="text-input" id="apiKeyInput" placeholder="sk-...">
                    </div>
                    
                    <button class="btn-primary" onclick="saveApiKey()">Save API Key</button>
                </div>

                <div class="settings-section">
                    <h2 class="settings-title">GitHub Integration</h2>
                    <p class="settings-desc">Connect to GitHub for repository search.</p>
                    
                    <div class="input-group">
                        <label class="input-label">GitHub Personal Access Token</label>
                        <input type="password" class="text-input" id="ghTokenInput" placeholder="ghp_...">
                    </div>
                    
                    <button class="btn-primary" onclick="saveGhToken()">Save Token</button>
                </div>
            </div>

            <!-- GitHub Panel -->
            <div class="github-panel" id="githubPanel">
                <div class="settings-section">
                    <h2 class="settings-title">Search GitHub</h2>
                    <p class="settings-desc">Search for repositories.</p>
                    
                    <div class="input-group">
                        <input type="text" class="text-input" id="ghSearchInput" placeholder="Search repositories...">
                    </div>
                    
                    <button class="btn-primary" onclick="searchGh()">Search</button>
                </div>
                
                <div id="ghResults"></div>
            </div>

            <!-- Input -->
            <div class="input-area">
                <div class="input-wrapper">
                    <textarea class="msg-input" id="userInput" placeholder="Message EVE..." rows="1"></textarea>
                    <button class="input-btn" onclick="toggleVoice()" title="Voice">🎤</button>
                    <button class="input-btn send" onclick="sendMessage()" title="Send">➤</button>
                </div>
            </div>
        </main>
    </div>

    <script>
        let sessionId = 'default';
        let isListening = false;
        let voiceEnabled = true;
        let isProcessing = false;

        // Navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const view = btn.dataset.view;
                showView(view);
            });
        });

        function showView(view) {
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            document.querySelector(`[data-view="${view}"]`).classList.add('active');
            
            document.getElementById('chatView').style.display = view === 'chat' ? 'block' : 'none';
            document.getElementById('settingsPanel').classList.toggle('active', view === 'settings');
            document.getElementById('githubPanel').classList.toggle('active', view === 'github');
            
            document.getElementById('pageTitle').textContent = view.charAt(0).toUpperCase() + view.slice(1);
        }

        // Speech Recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            recognition.onresult = (e) => {
                const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
                if (e.results[0].isFinal) {
                    document.getElementById('userInput').value = transcript;
                    sendMessage();
                }
            };
            recognition.onend = () => { isListening = false; updateVoiceBtn(); };
        }

        function toggleVoice() {
            if (!recognition) { alert('Voice not supported'); return; }
            if (isListening) recognition.stop();
            else recognition.start();
            isListening = !isListening;
            updateVoiceBtn();
        }

        function updateVoiceBtn() {
            document.getElementById('voiceBtn').classList.toggle('listening', isListening);
        }

        function toggleMute() {
            voiceEnabled = !voiceEnabled;
            document.getElementById('muteBtn').textContent = voiceEnabled ? '🔊' : '🔇';
        }

        function speak(text) {
            if (!voiceEnabled) return;
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(text);
            u.rate = 0.9; u.pitch = 1.0; u.volume = 0.8;
            window.speechSynthesis.speak(u);
        }

        async function sendMessage() {
            const input = document.getElementById('userInput');
            const msg = input.value.trim();
            if (!msg || isProcessing) return;

            addMessage(msg, 'user');
            input.value = '';
            isProcessing = true;
            showThinking();

            try {
                const formData = new FormData();
                formData.append('message', msg);
                formData.append('session_id', sessionId);

                const response = await fetch('/api/chat', { method: 'POST', body: formData });
                const data = await response.json();
                hideThinking();
                addMessage(data.response || 'No response', 'assistant');

                if (data.api_configured) {
                    document.getElementById('apiStatus').textContent = 'Ready';
                    document.getElementById('apiStatus').className = 'status-badge ready';
                }

                if (voiceEnabled) {
                    const plain = data.response.replace(/#{1,6}\\s/g,'').replace(/\\*\\*/g,'').replace(/`/g,'').substring(0,500);
                    speak(plain);
                }
            } catch (e) {
                hideThinking();
                addMessage('# Error\\n\\nFailed: ' + e.message, 'assistant');
            }
            isProcessing = false;
        }

        function addMessage(content, role) {
            const div = document.getElementById('messages');
            const time = new Date().toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'});
            
            const escaped = content
                .replace(/&/g, '&')
                .replace(/</g, '<')
                .replace(/>/g, '>');
            
            const formatted = escaped
                .replace(/^# (.+)$/gm, '<h1>$1</h1>')
                .replace(/^## (.+)$/gm, '<h2>$1</h2>')
                .replace(/^### (.+)$/gm, '<h3>$1</h3>')
                .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/`([^`]+)`/g, '<code>$1</code>')
                .replace(/```([\\s\\S]+?)```/g, '<pre><code>$1</code></pre>')
                .replace(/^\\- (.+)$/gm, '<li>$1</li>')
                .replace(/\\n/g, '<br>');
            
            div.innerHTML += `
                <div class="message ${role}">
                    <div class="avatar">${role==='assistant'?'E':'👤'}</div>
                    <div class="msg-content">
                        <div class="msg-header">
                            <span class="msg-author">${role==='assistant'?'EVE AI':'You'}</span>
                            <span class="msg-time">${time}</span>
                        </div>
                        <div class="msg-body">${formatted}</div>
                    </div>
                </div>`;
            div.parentElement.scrollTop = div.parentElement.scrollHeight;
        }

        function showThinking() {
            document.getElementById('messages').innerHTML += `
                <div class="message assistant" id="thinking">
                    <div class="avatar">E</div>
                    <div class="msg-content">
                        <div class="msg-header">
                            <span class="msg-author">EVE AI</span>
                        </div>
                        <div class="msg-body"><div class="thinking"><span></span><span></span><span></span></div></div>
                    </div>
                </div>`;
        }

        function hideThinking() {
            const t = document.getElementById('thinking');
            if (t) t.remove();
        }

        // Settings
        function saveApiKey() {
            const key = document.getElementById('apiKeyInput').value;
            alert('Save to config.json manually for now. Key: ' + key.substring(0, 10) + '...');
        }

        function saveGhToken() {
            const token = document.getElementById('ghTokenInput').value;
            alert('Save to config.json manually for now. Token: ' + token.substring(0, 10) + '...');
        }

        async function searchGh() {
            const query = document.getElementById('ghSearchInput').value;
            if (!query) return;
            
            addMessage('github search ' + query, 'user');
            showThinking();
            
            try {
                const formData = new FormData();
                formData.append('message', 'github search ' + query);
                const response = await fetch('/api/chat', { method: 'POST', body: formData });
                const data = await response.json();
                hideThinking();
                addMessage(data.response, 'assistant');
            } catch (e) {
                hideThinking();
                addMessage('Error: ' + e.message, 'assistant');
            }
        }

        document.getElementById('userInput').addEventListener('keydown', e => {
            if(e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>'''

# ==================== HTTP HANDLER ====================

class EVEHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'online',
                'version': '4.0',
                'ai_configured': AIEngine().is_configured()
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            data = {}
            for part in post_data.decode().split('&'):
                if '=' in part:
                    key, val = part.split('=', 1)
                    data[key] = urllib.parse.unquote(val)
            
            message = data.get('message', '')
            session_id = data.get('session_id', 'default')
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(eve.process_message(message, session_id))
            loop.close()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[EVE] {args[0]}")

# ==================== MAIN ====================

def run_server(host='localhost', port=8000):
    print(f"""
======================================
     EVE AI v4.0 - Running
======================================
     
     Open: http://{host}:{port}
     
======================================
    """)
    
    server = HTTPServer((host, port), EVEHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nShutting down...")
        server.shutdown()

if __name__ == "__main__":
    run_server()
