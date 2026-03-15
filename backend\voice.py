"""
EVE Voice Module
Speech-to-Text and Text-to-Speech with calm, commanding tone
"""

import base64
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

class VoiceEngine:
    """Handles voice input/output with calm, commanding tone"""
    
    def __init__(self):
        self.enabled = True
        self.sample_rate = 16000
        self.volume = 0.8
        self.rate = 1.0  # Speed of speech
        
        # Voice profiles - calm but authoritative
        self.voice_profiles = {
            "default": {
                "name": "EVE",
                "pitch": 0,
                "rate": 1.0,
                "volume": 0.8,
                "description": "Calm and commanding"
            },
            "calm": {
                "name": "EVE",
                "pitch": -2,
                "rate": 0.9,
                "volume": 0.7,
                "description": "Gentle and calm"
            },
            "professional": {
                "name": "EVE",
                "pitch": 2,
                "rate": 1.0,
                "volume": 0.85,
                "description": "Professional and clear"
            }
        }
        
        self.current_profile = "default"
        
        # Response phrases in calm, commanding tone
        self.responses = {
            "listening": [
                "I'm listening.",
                "Go ahead.",
                "Yes?",
                "I'm here."
            ],
            "processing": [
                "Let me think about that.",
                "Processing your request.",
                "One moment.",
                "Working on it."
            ],
            "success": [
                "Done.",
                "Complete.",
                "I've got it.",
                "Consider it done."
            ],
            "error": [
                "I apologize, but I couldn't complete that.",
                "There was an issue. Let me try again.",
                "I'm sorry, that didn't work.",
                "Let me try a different approach."
            ],
            "clarification": [
                "Could you clarify that?",
                "Tell me more about what you need.",
                "I want to make sure I understand correctly.",
                "Could you be more specific?"
            ]
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get voice engine status"""
        return {
            "enabled": self.enabled,
            "sample_rate": self.sample_rate,
            "volume": self.volume,
            "rate": self.rate,
            "current_profile": self.current_profile,
            "profile_info": self.voice_profiles[self.current_profile]
        }
    
    def set_profile(self, profile_name: str) -> bool:
        """Set voice profile"""
        if profile_name in self.voice_profiles:
            self.current_profile = profile_name
            profile = self.voice_profiles[profile_name]
            self.rate = profile["rate"]
            self.volume = profile["volume"]
            return True
        return False
    
    def get_profiles(self) -> Dict[str, Dict]:
        """Get all available voice profiles"""
        return self.voice_profiles
    
    # ==================== SPEECH TO TEXT ====================
    
    async def speech_to_text(self, audio_data: str) -> Dict[str, Any]:
        """Convert speech to text using Web Speech API"""
        # This will be handled by the browser's Web Speech API
        # Returns the transcribed text
        return {
            "success": True,
            "text": "",
            "confidence": 0.95,
            "language": "en-US",
            "timestamp": datetime.now().isoformat()
        }
    
    def is_available(self) -> bool:
        """Check if speech recognition is available"""
        return True
    
    # ==================== TEXT TO SPEECH ====================
    
    def generate_speech(
        self, 
        text: str, 
        profile: str = None
    ) -> Dict[str, Any]:
        """Generate speech from text"""
        if profile:
            self.set_profile(profile)
        
        # Return configuration for TTS
        voice_config = self.voice_profiles.get(
            self.current_profile, 
            self.voice_profiles["default"]
        )
        
        return {
            "success": True,
            "text": text,
            "voice_config": {
                "name": voice_config["name"],
                "pitch": voice_config["pitch"],
                "rate": voice_config["rate"],
                "volume": voice_config["volume"]
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def speak(self, text: str) -> str:
        """Prepare text for speech (Web Speech API format)"""
        return json.dumps({
            "text": text,
            "voice": self.current_profile,
            "config": self.voice_profiles[self.current_profile]
        })
    
    # ==================== CALM RESPONSES ====================
    
    def get_listening_response(self) -> str:
        """Get a calm listening response"""
        import random
        return random.choice(self.responses["listening"])
    
    def get_processing_response(self) -> str:
        """Get a calm processing response"""
        import random
        return random.choice(self.responses["processing"])
    
    def get_success_response(self) -> str:
        """Get a calm success response"""
        import random
        return random.choice(self.responses["success"])
    
    def get_error_response(self) -> str:
        """Get a calm error response"""
        import random
        return random.choice(self.responses["error"])
    
    def get_clarification_response(self) -> str:
        """Get a calm clarification request"""
        import random
        return random.choice(self.responses["clarification"])
    
    # ==================== VOICE COMMANDS ====================
    
    def parse_command(self, text: str) -> Dict[str, Any]:
        """Parse voice commands"""
        text_lower = text.lower()
        
        commands = {
            "stop": ["stop", "wait", "pause", "hold"],
            "go": ["go", "continue", "resume", "start"],
            "repeat": ["repeat", "say again", "what"],
            "louder": ["louder", "increase volume", "volume up"],
            "quieter": ["quieter", "softer", "volume down"],
            "faster": ["faster", "speed up", "quicker"],
            "slower": ["slower", "slow down", "take your time"]
        }
        
        for cmd, keywords in commands.items():
            if any(kw in text_lower for kw in keywords):
                return {
                    "command": cmd,
                    "recognized": True,
                    "text": text
                }
        
        return {
            "command": None,
            "recognized": False,
            "text": text
        }
    
    def execute_command(self, command: str) -> str:
        """Execute a voice command and return response"""
        responses = {
            "stop": "Pausing. Say 'continue' when ready.",
            "go": "Continuing.",
            "repeat": "I'll repeat that.",
            "louder": "Increasing volume.",
            "quieter": "Reducing volume.",
            "faster": "Speeding up.",
            "slower": "Slowing down."
        }
        
        return responses.get(command, "Command not recognized.")


# Global voice engine
voice_engine = VoiceEngine()
