"""
EVE AI Server - FastAPI Backend
"""

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import uvicorn
import os

# Import EVE modules
from ai_engine import AIEngine
from memory import Memory
from tools import Tools
from plugins import PluginManager
from voice import VoiceEngine
from security import SecurityTools
from language import LanguageManager
from multimodal import MultimodalEngine
from tasks import TaskPrimitives
from safety import SafetyEngine
from connectors import ConnectorManager
from reasoning import ReasoningEngine

app = FastAPI(title="EVE AI", version="4.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EVE components
ai_engine = AIEngine()
memory = Memory()
tools = Tools()
plugin_manager = PluginManager()
voice_engine = VoiceEngine()
security_tools = SecurityTools()
language_manager = LanguageManager()
multimodal = MultimodalEngine()
tasks = TaskPrimitives()
safety = SafetyEngine()
connectors = ConnectorManager()
reasoning = ReasoningEngine()

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: Optional[List[Dict]] = None
    confidence: Optional[float] = None

class VoiceRequest(BaseModel):
    text: Optional[str] = None
    audio_data: Optional[str] = None
    profile: Optional[str] = "default"

class VoiceResponse(BaseModel):
    success: bool
    text: Optional[str] = None
    audio: Optional[str] = None
    message: str = ""

# ==================== ROOT ====================

@app.get("/")
async def root():
    return {
        "name": "EVE AI",
        "version": "4.0.0",
        "creator": "Hassan Muzenda",
        "status": "online",
        "capabilities": [
            "ai_reasoning",
            "voice_io",
            "multimodal",
            "security_tools",
            "task_primitives",
            "plugins",
            "memory",
            "connectors"
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "4.0.0"}

# ==================== CHAT ====================

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint with reasoning"""
    try:
        # Get session or create new one
        session_id = request.session_id or f"session_{memory.get_session_count()}"
        
        # Get conversation history
        history = memory.get_history(session_id)
        
        # Use reasoning engine for complex tasks
        reasoning_result = await reasoning.think(request.message)
        
        # Generate AI response
        response = await ai_engine.generate_response(
            message=request.message,
            history=history,
            context=request.context
        )
        
        # Store in memory
        memory.add_message(session_id, "user", request.message)
        memory.add_message(session_id, "assistant", response)
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            sources=reasoning_result.get("reasoning_steps", []),
            confidence=reasoning_result.get("confidence", 0.9)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== VOICE ====================

@app.get("/voice/status")
async def voice_status():
    """Get voice engine status"""
    return voice_engine.get_status()

@app.post("/voice/tts", response_model=VoiceResponse)
async def text_to_speech(request: VoiceRequest):
    """Convert text to speech"""
    try:
        if not request.text:
            return VoiceResponse(success=False, message="No text provided")
        
        # Generate speech config
        result = voice_engine.generate_speech(request.text, request.profile)
        
        return VoiceResponse(
            success=True,
            text=request.text,
            message="Ready for speech synthesis"
        )
    except Exception as e:
        return VoiceResponse(success=False, message=str(e))

@app.post("/voice/stt", response_model=VoiceResponse)
async def speech_to_text(request: VoiceRequest):
    """Convert speech to text"""
    try:
        # This is handled by client-side Web Speech API
        return VoiceResponse(
            success=True,
            message="Use browser's SpeechRecognition API for STT"
        )
    except Exception as e:
        return VoiceResponse(success=False, message=str(e))

@app.get("/voice/profiles")
async def voice_profiles():
    """Get available voice profiles"""
    return voice_engine.get_profiles()

@app.post("/voice/profile/{profile_name}")
async def set_voice_profile(profile_name: str):
    """Set voice profile"""
    success = voice_engine.set_profile(profile_name)
    return {"success": success, "profile": profile_name}

# ==================== SESSIONS ====================

@app.get("/sessions")
async def list_sessions():
    """List all chat sessions"""
    return memory.list_sessions()

@app.post("/sessions/create")
async def create_session():
    """Create new chat session"""
    session_id = memory.create_session()
    return {"session_id": session_id}

@app.post("/sessions/{session_id}/delete")
async def delete_session(session_id: str):
    """Delete a session"""
    memory.delete_session(session_id)
    return {"success": True}

@app.post("/sessions/{session_id}/clear")
async def clear_session(session_id: str):
    """Clear session history"""
    memory.clear_session(session_id)
    return {"success": True}

# ==================== AI CONFIG ====================

@app.get("/ai/list")
async def list_ais():
    """List available AI configurations"""
    return ai_engine.list_ais()

@app.post("/ai/add")
async def add_ai(config: Dict[str, Any]):
    """Add new AI configuration"""
    return ai_engine.add_ai(config)

@app.post("/ai/{ai_id}/set-default")
async def set_default_ai(ai_id: str):
    """Set default AI"""
    return ai_engine.set_default_ai(ai_id)

# ==================== TOOLS ====================

@app.get("/tools")
async def list_tools():
    """List all available tools"""
    return tools.list_tools()

@app.post("/tools/execute")
async def execute_tool(tool_name: str, params: Dict[str, Any]):
    """Execute a tool"""
    return await tools.execute_tool(tool_name, params)

# ==================== SECURITY ====================

@app.get("/security/tools")
async def security_tool_list():
    """List security tools"""
    return security_tools.list_tools()

@app.post("/security/scan")
async def security_scan(target: str, tool: str):
    """Run security scan"""
    return await security_tools.scan(target, tool)

# ==================== LANGUAGE ====================

@app.get("/language/list")
async def list_languages():
    """List available languages"""
    return language_manager.get_available_languages()

@app.post("/language/set/{lang_code}")
async def set_language(lang_code: str):
    """Set current language"""
    success = language_manager.set_language(lang_code)
    return {"success": success, "language": lang_code}

@app.get("/language/translations")
async def get_translations():
    """Get all translations"""
    return language_manager.get_all_translations()

# ==================== TASKS ====================

@app.post("/tasks/draft")
async def draft_document(doc_type: str, content: str):
    """Draft a document"""
    return tasks.draft_document(doc_type, content)

@app.post("/tasks/summarize")
async def summarize_text(text: str, style: str = "bullet"):
    """Summarize text"""
    return tasks.summarize(text, style=style)

@app.post("/tasks/scaffold")
async def scaffold_code(language: str, project_type: str, features: List[str]):
    """Generate code scaffold"""
    return tasks.scaffold_code(language, project_type, features)

# ==================== SAFETY ====================

@app.get("/safety/audit")
async def get_audit_log(user_id: str = None, limit: int = 100):
    """Get audit log"""
    return safety.get_audit_log(user_id=user_id, limit=limit)

@app.post("/safety/assess")
async def assess_risk(message: str):
    """Assess message risk"""
    return safety.assess_risk(message)

# ==================== REASONING ====================

@app.post("/reasoning/think")
async def think(problem: str):
    """Chain-of-thought reasoning"""
    return await reasoning.think(problem)

@app.get("/reasoning/tasks")
async def list_tasks():
    """List reasoning tasks"""
    return reasoning.get_all_tasks()

# ==================== CONNECTORS ====================

@app.get("/connectors")
async def list_connectors():
    """List available connectors"""
    return connectors.get_connectors()

@app.post("/connectors/{connector_id}/connect")
async def connect_service(connector_id: str, credentials: Dict[str, str]):
    """Connect to a service"""
    return connectors.connect(connector_id, credentials)

# ==================== MEMORY ====================

@app.get("/memory/{session_id}")
async def get_memory(session_id: str):
    """Get session memory"""
    return memory.get_history(session_id)

@app.post("/memory/{session_id}/learn")
async def learn_fact(session_id: str, fact: str, data: Dict[str, Any]):
    """Learn a fact"""
    return memory.learn_fact(session_id, fact, data)

# ==================== MULTIMODAL ====================

@app.post("/multimodal/analyze")
async def analyze_input(mode: str, content: str):
    """Analyze multimodal input"""
    from multimodal import InputMode
    from datetime import datetime
    
    user_input = InputMode(
        mode=InputMode[mode.upper()],
        content=content,
        metadata={},
        timestamp=datetime.now().isoformat()
    )
    
    return await multimodal.process_input(user_input)

# ==================== PLUGINS ====================

@app.get("/plugins")
async def list_plugins():
    """List installed plugins"""
    return plugin_manager.list_plugins()

@app.post("/plugins/add")
async def add_plugin(name: str, endpoint: str):
    """Add a plugin"""
    return plugin_manager.add_plugin(name, endpoint)

# ==================== RUN SERVER ====================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
