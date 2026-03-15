"""
EVE AI Plugin System
Allows users to add custom AI repositories and endpoints.
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import aiohttp

# Plugin storage file
PLUGINS_FILE = os.path.join(os.path.dirname(__file__), 'plugins.json')

@dataclass
class AIPlugin:
    """Represents a custom AI repository/endpoint"""
    id: str
    name: str
    type: str  # 'openai', 'anthropic', 'local', 'custom'
    endpoint: str  # API endpoint URL
    api_key: str = ""  # Optional API key
    model: str = "default"
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

class PluginManager:
    """Manages AI plugins/repositories"""
    
    def __init__(self):
        self.plugins: Dict[str, AIPlugin] = {}
        self.load_plugins()
    
    def load_plugins(self):
        """Load plugins from file"""
        if os.path.exists(PLUGINS_FILE):
            try:
                with open(PLUGINS_FILE, 'r') as f:
                    data = json.load(f)
                    for plugin_data in data.get('plugins', []):
                        plugin = AIPlugin(
                            id=plugin_data['id'],
                            name=plugin_data['name'],
                            type=plugin_data['type'],
                            endpoint=plugin_data['endpoint'],
                            api_key=plugin_data.get('api_key', ''),
                            model=plugin_data.get('model', 'default'),
                            enabled=plugin_data.get('enabled', True),
                            config=plugin_data.get('config', {})
                        )
                        self.plugins[plugin.id] = plugin
            except Exception as e:
                print(f"Error loading plugins: {e}")
    
    def save_plugins(self):
        """Save plugins to file"""
        data = {
            'plugins': [
                {
                    'id': p.id,
                    'name': p.name,
                    'type': p.type,
                    'endpoint': p.endpoint,
                    'api_key': p.api_key,
                    'model': p.model,
                    'enabled': p.enabled,
                    'config': p.config
                }
                for p in self.plugins.values()
            ]
        }
        with open(PLUGINS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_plugin(self, plugin: AIPlugin) -> bool:
        """Add a new plugin"""
        try:
            self.plugins[plugin.id] = plugin
            self.save_plugins()
            return True
        except Exception as e:
            print(f"Error adding plugin: {e}")
            return False
    
    def remove_plugin(self, plugin_id: str) -> bool:
        """Remove a plugin"""
        try:
            if plugin_id in self.plugins:
                del self.plugins[plugin_id]
                self.save_plugins()
                return True
            return False
        except Exception as e:
            print(f"Error removing plugin: {e}")
            return False
    
    def get_plugin(self, plugin_id: str) -> Optional[AIPlugin]:
        """Get a plugin by ID"""
        return self.plugins.get(plugin_id)
    
    def list_plugins(self) -> List[Dict]:
        """List all plugins"""
        return [
            {
                'id': p.id,
                'name': p.name,
                'type': p.type,
                'endpoint': p.endpoint,
                'model': p.model,
                'enabled': p.enabled
            }
            for p in self.plugins.values()
        ]
    
    async def chat_with_plugin(
        self, 
        plugin_id: str, 
        messages: List[Dict],
        system_prompt: str = ""
    ) -> Dict[str, Any]:
        """Send chat request to a custom plugin endpoint"""
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            return {'success': False, 'error': 'Plugin not found'}
        
        if not plugin.enabled:
            return {'success': False, 'error': 'Plugin is disabled'}
        
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            if plugin.api_key:
                headers['Authorization'] = f'Bearer {plugin.api_key}'
            
            payload = {
                'model': plugin.model,
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 2000
            }
            
            if system_prompt:
                payload['system'] = system_prompt
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    plugin.endpoint,
                    json=payload,
                    headers=headers,
                    timeout=60
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'success': True,
                            'response': data.get('choices', [{}])[0].get('message', {}).get('content', ''),
                            'raw': data
                        }
                    else:
                        return {
                            'success': False,
                            'error': f'API error: {response.status}'
                        }
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Pre-built plugin templates
PLUGIN_TEMPLATES = [
    {
        'name': 'OpenAI GPT-4',
        'type': 'openai',
        'endpoint': 'https://api.openai.com/v1/chat/completions',
        'description': 'OpenAI GPT-4 API'
    },
    {
        'name': 'OpenAI GPT-3.5 Turbo',
        'type': 'openai',
        'endpoint': 'https://api.openai.com/v1/chat/completions',
        'description': 'OpenAI GPT-3.5 Turbo API'
    },
    {
        'name': 'Anthropic Claude',
        'type': 'anthropic',
        'endpoint': 'https://api.anthropic.com/v1/messages',
        'description': 'Anthropic Claude API'
    },
    {
        'name': 'Local AI (Ollama)',
        'type': 'local',
        'endpoint': 'http://localhost:11434/api/chat',
        'description': 'Ollama local AI'
    },
    {
        'name': 'LM Studio',
        'type': 'local',
        'endpoint': 'http://localhost:1234/v1/chat/completions',
        'description': 'LM Studio local AI'
    },
    {
        'name': 'Custom REST API',
        'type': 'custom',
        'endpoint': '',
        'description': 'Add your own AI endpoint'
    }
]

# Example usage
if __name__ == "__main__":
    manager = PluginManager()
    
    # Add a custom plugin
    import uuid
    plugin = AIPlugin(
        id=str(uuid.uuid4()),
        name="My Custom AI",
        type="custom",
        endpoint="https://my-ai-api.com/chat",
        api_key="your-api-key-here",
        model="gpt-4"
    )
    manager.add_plugin(plugin)
    
    print("Available plugins:")
    for p in manager.list_plugins():
        print(f"  - {p['name']} ({p['type']})")
    
    print("\nPlugin templates:")
    for t in PLUGIN_TEMPLATES:
        print(f"  - {t['name']}: {t['description']}")
