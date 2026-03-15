"""
EVE Configuration Manager
Handles configuration, multiple AI sessions, and chat contexts.
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

@dataclass
class AIConfig:
    """Configuration for an AI endpoint"""
    id: str
    name: str
    type: str  # 'openai', 'anthropic', 'local', 'custom'
    endpoint: str
    api_key: str
    model: str
    enabled: bool = True

@dataclass
class ChatSession:
    """Represents a chat session"""
    id: str
    name: str
    ai_id: str  # Which AI to use
    created_at: datetime = field(default_factory=datetime.now)
    messages: List[Dict[str, str]] = field(default_factory=list)

class ConfigManager:
    """Manages EVE configuration and sessions"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.sessions: Dict[str, ChatSession] = {}
        self.load_config()
        self._ensure_default_session()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config = self._default_config()
        else:
            self.config = self._default_config()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "default_ai": {
                "id": "default",
                "name": "OpenAI GPT-4",
                "type": "openai",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "model": "gpt-4",
                "api_key": "",
                "enabled": True
            },
            "ais": [
                {
                    "id": "default",
                    "name": "OpenAI GPT-4",
                    "type": "openai",
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "model": "gpt-4",
                    "api_key": "",
                    "enabled": True
                },
                {
                    "id": "default-gpt35",
                    "name": "OpenAI GPT-3.5",
                    "type": "openai",
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "model": "gpt-3.5-turbo",
                    "api_key": "",
                    "enabled": True
                },
                {
                    "id": "local-ollama",
                    "name": "Local (Ollama)",
                    "type": "local",
                    "endpoint": "http://localhost:11434/api/chat",
                    "model": "llama2",
                    "api_key": "",
                    "enabled": True
                },
                {
                    "id": "local-lmstudio",
                    "name": "Local (LM Studio)",
                    "type": "local",
                    "endpoint": "http://localhost:1234/v1/chat/completions",
                    "model": "local-model",
                    "api_key": "",
                    "enabled": True
                }
            ],
            "voice": {
                "enabled": True,
                "speech_to_text": True,
                "text_to_speech": True,
                "voice_rate": 200,
                "voice_volume": 1.0
            }
        }
    
    def _ensure_default_session(self):
        """Ensure there's at least one chat session"""
        if not self.sessions:
            self.create_session("General Chat")
    
    # ==================== AI Management ====================
    
    def get_default_ai(self) -> Dict[str, Any]:
        """Get the default AI configuration"""
        return self.config.get('default_ai', self.config['ais'][0] if self.config.get('ais') else {})
    
    def set_default_ai(self, ai_id: str):
        """Set the default AI"""
        for ai in self.config.get('ais', []):
            if ai['id'] == ai_id:
                self.config['default_ai'] = ai
                self.save_config()
                return True
        return False
    
    def get_all_ais(self) -> List[Dict[str, Any]]:
        """Get all configured AIs"""
        return self.config.get('ais', [])
    
    def add_ai(self, ai_config: Dict[str, Any]) -> str:
        """Add a new AI configuration"""
        ai_id = str(uuid.uuid4())
        ai_config['id'] = ai_id
        if 'ais' not in self.config:
            self.config['ais'] = []
        self.config['ais'].append(ai_config)
        self.save_config()
        return ai_id
    
    def update_ai(self, ai_id: str, ai_config: Dict[str, Any]) -> bool:
        """Update an AI configuration"""
        for i, ai in enumerate(self.config.get('ais', [])):
            if ai['id'] == ai_id:
                ai_config['id'] = ai_id
                self.config['ais'][i] = ai_config
                self.save_config()
                return True
        return False
    
    def remove_ai(self, ai_id: str) -> bool:
        """Remove an AI configuration"""
        for i, ai in enumerate(self.config.get('ais', [])):
            if ai['id'] == ai_id:
                self.config['ais'].pop(i)
                self.save_config()
                return True
        return False
    
    # ==================== Voice Config ====================
    
    def get_voice_config(self) -> Dict[str, Any]:
        """Get voice configuration"""
        return self.config.get('voice', {})
    
    def update_voice_config(self, voice_config: Dict[str, Any]):
        """Update voice configuration"""
        self.config['voice'] = voice_config
        self.save_config()
    
    # ==================== Chat Sessions ====================
    
    def create_session(self, name: str = "New Chat") -> str:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        session = ChatSession(
            id=session_id,
            name=name,
            ai_id=self.get_default_ai().get('id', 'default')
        )
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session"""
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all chat sessions"""
        return [
            {
                'id': s.id,
                'name': s.name,
                'ai_id': s.ai_id,
                'created_at': s.created_at.isoformat(),
                'message_count': len(s.messages)
            }
            for s in self.sessions.values()
        ]
    
    def add_message_to_session(self, session_id: str, role: str, content: str):
        """Add a message to a session"""
        if session_id in self.sessions:
            self.sessions[session_id].messages.append({
                'role': role,
                'content': content
            })
    
    def clear_session(self, session_id: str):
        """Clear a session's messages"""
        if session_id in self.sessions:
            self.sessions[session_id].messages = []
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def rename_session(self, session_id: str, new_name: str) -> bool:
        """Rename a chat session"""
        if session_id in self.sessions:
            self.sessions[session_id].name = new_name
            return True
        return False
    
    # ==================== API Key Management ====================
    
    def set_api_key(self, ai_id: str, api_key: str):
        """Set API key for an AI"""
        for ai in self.config.get('ais', []):
            if ai['id'] == ai_id:
                ai['api_key'] = api_key
                self.save_config()
                return True
        return False
    
    def get_api_key(self, ai_id: str) -> str:
        """Get API key for an AI"""
        for ai in self.config.get('ais', []):
            if ai['id'] == ai_id:
                return ai.get('api_key', '')
        return ''

# Global config manager instance
config_manager = ConfigManager()

# Example usage
if __name__ == "__main__":
    cm = config_manager
    
    print("=== AI Configurations ===")
    for ai in cm.get_all_ais():
        print(f"  - {ai['name']} ({ai['type']}) - {ai['model']}")
    
    print(f"\nDefault AI: {cm.get_default_ai()['name']}")
    
    print("\n=== Chat Sessions ===")
    for session in cm.get_all_sessions():
        print(f"  - {session['name']} ({session['message_count']} messages)")
    
    print("\n=== Voice Config ===")
    print(f"  Enabled: {cm.get_voice_config()}")
