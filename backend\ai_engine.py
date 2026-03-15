"""
EVE AI Core Engine
The intelligent brain that powers EVE with logical reasoning capabilities.
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ReasoningLevel(Enum):
    """Levels of reasoning complexity"""
    DIRECT = "direct"           # Simple, direct responses
    STEP_BY_STEP = "step"       # Break down into steps
    CHAIN_OF_THOUGHT = "cot"    # Show reasoning process
    MULTI_HOP = "multi_hop"     # Complex multi-step reasoning
    META = "meta"               # Think about thinking

@dataclass
class ReasoningStep:
    """A single step in EVE's reasoning process"""
    step_number: int
    thought: str
    action: Optional[str] = None
    observation: Optional[str] = None
    confidence: float = 1.0

@dataclass
class EVEMessage:
    """Represents a message in EVE's context"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    reasoning_steps: List[ReasoningStep] = field(default_factory=list)

class ReasoningEngine:
    """
    EVE's reasoning engine - capable of multiple levels of logical thinking.
    This is what makes EVE different from simple chatbots.
    """
    
    def __init__(self):
        self.reasoning_history: List[List[ReasoningStep]] = []
        self.current_reasoning_level = ReasoningLevel.CHAIN_OF_THOUGHT
        
    def analyze_intent(self, user_input: str) -> Dict[str, Any]:
        """Analyze what the user wants and determine the best approach"""
        user_lower = user_input.lower()
        
        # Intent classification
        intents = {
            'code': ['code', 'python', 'javascript', 'program', 'function', 'class', 'debug'],
            'web': ['search', 'browse', 'internet', 'web', 'url', 'website', 'google'],
            'file': ['file', 'read', 'write', 'folder', 'directory', 'create', 'delete'],
            'system': ['command', 'terminal', 'run', 'execute', 'process', 'system'],
            'analysis': ['analyze', 'explain', 'why', 'how', 'reason', 'think'],
            'creation': ['write', 'create', 'make', 'build', 'generate', 'design'],
        }
        
        detected_intents = []
        for intent, keywords in intents.items():
            if any(keyword in user_lower for keyword in keywords):
                detected_intents.append(intent)
        
        # Determine reasoning level needed
        complexity_indicators = {
            ReasoningLevel.DIRECT: ['what', 'who', 'when'],  # Simple questions
            ReasoningLevel.STEP_BY_STEP: ['how to', 'steps', 'process'],  # Needs steps
            ReasoningLevel.CHAIN_OF_THOUGHT: ['why', 'reason', 'think'],  # Needs reasoning
            ReasoningLevel.MULTI_HOP: ['compare', 'improve', 'optimize'],  # Complex
            ReasoningLevel.META: ['your', 'yourself', 'reasoning'],  # Self-reflection
        }
        
        reasoning_level = ReasoningLevel.DIRECT
        for level, indicators in complexity_indicators.items():
            if any(indicator in user_lower for indicator in indicators):
                reasoning_level = level
                break
                
        return {
            'intents': detected_intents,
            'reasoning_level': reasoning_level,
            'needs_tools': len(detected_intents) > 0 and detected_intents[0] != 'analysis',
            'complexity': 'high' if len(detected_intents) > 2 else 'low'
        }
    
    async def think(
        self, 
        user_input: str, 
        context: List[EVEMessage],
        max_steps: int = 5
    ) -> List[ReasoningStep]:
        """
        EVE's thinking process - generates reasoning steps before responding.
        This is the core of EVE's logical capabilities.
        """
        analysis = self.analyze_intent(user_input)
        reasoning_steps = []
        
        # Step 1: Understand the request
        step1 = ReasoningStep(
            step_number=1,
            thought=f"User said: '{user_input[:50]}...'",
            action="Analyzing input",
            observation=f"Detected intents: {', '.join(analysis['intents']) or 'general conversation'}",
            confidence=0.95
        )
        reasoning_steps.append(step1)
        
        # Step 2: Recall relevant context
        relevant_context = self._find_relevant_context(context, user_input)
        step2 = ReasoningStep(
            step_number=2,
            thought="Recalling relevant context from conversation",
            action="Memory retrieval",
            observation=f"Found {len(relevant_context)} relevant messages" if relevant_context else "No specific context found",
            confidence=0.8 if relevant_context else 0.5
        )
        reasoning_steps.append(step2)
        
        # Step 3: Plan the approach
        approach = self._plan_approach(analysis)
        step3 = ReasoningStep(
            step_number=3,
            thought=f"Planning response with {analysis['reasoning_level'].value} reasoning",
            action="Strategy selection",
            observation=approach,
            confidence=0.85
        )
        reasoning_steps.append(step3)
        
        # Step 4-5: Execute sub-steps for complex requests
        if analysis['complexity'] == 'high' or analysis['reasoning_level'] in [
            ReasoningLevel.CHAIN_OF_THOUGHT, 
            ReasoningLevel.MULTI_HOP
        ]:
            for i in range(min(max_steps - 3, 3)):
                sub_step = ReasoningStep(
                    step_number=4 + i,
                    thought=f"Processing sub-step {i+1}",
                    action="Executing plan",
                    observation="Analyzing details...",
                    confidence=0.75
                )
                reasoning_steps.append(sub_step)
        
        self.reasoning_history.append(reasoning_steps)
        return reasoning_steps
    
    def _find_relevant_context(
        self, 
        context: List[EVEMessage], 
        user_input: str
    ) -> List[EVEMessage]:
        """Find messages relevant to the current query"""
        # Simple keyword-based relevance for now
        keywords = set(user_input.lower().split())
        relevant = []
        
        for msg in context[-5:]:  # Last 5 messages
            msg_words = set(msg.content.lower().split())
            overlap = keywords.intersection(msg_words)
            if len(overlap) >= 2:
                relevant.append(msg)
                
        return relevant
    
    def _plan_approach(self, analysis: Dict[str, Any]) -> str:
        """Plan how to respond based on analysis"""
        intents = analysis['intents']
        level = analysis['reasoning_level']
        
        if 'code' in intents:
            return "Provide code examples with explanation"
        elif 'web' in intents:
            return "Search web and provide current information"
        elif 'file' in intents:
            return "Offer file operation capabilities"
        elif 'system' in intents:
            return "Execute system command safely"
        elif level in [ReasoningLevel.CHAIN_OF_THOUGHT, ReasoningLevel.META]:
            return "Show reasoning process explicitly"
        else:
            return "Provide clear, helpful response"

class ToolExecutor:
    """
    Executes various tools that EVE can use to take action.
    This gives EVE the ability to actually DO things, not just talk.
    """
    
    def __init__(self):
        self.available_tools: Dict[str, Any] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register the tools EVE has access to"""
        self.available_tools = {
            # Web tools
            'web_search': {
                'name': 'Web Search',
                'description': 'Search the web for information',
                'enabled': True,
                'category': 'web'
            },
            'web_browse': {
                'name': 'Web Browser',
                'description': 'Navigate and extract data from websites',
                'enabled': True,
                'category': 'web'
            },
            
            # Computer tools
            'file_read': {
                'name': 'Read File',
                'description': 'Read contents of a file',
                'enabled': True,
                'category': 'computer'
            },
            'file_write': {
                'name': 'Write File',
                'description': 'Create or modify a file',
                'enabled': True,
                'category': 'computer'
            },
            'file_list': {
                'name': 'List Directory',
                'description': 'List files in a directory',
                'enabled': True,
                'category': 'computer'
            },
            'execute_command': {
                'name': 'Execute Command',
                'description': 'Run a terminal command',
                'enabled': True,
                'category': 'system'
            },
            
            # Code tools
            'code_execute': {
                'name': 'Execute Code',
                'description': 'Run code in a sandbox',
                'enabled': True,
                'category': 'code'
            },
            'code_debug': {
                'name': 'Debug Code',
                'description': 'Analyze and fix code errors',
                'enabled': True,
                'category': 'code'
            },
        }
    
    def get_available_tools(self, category: Optional[str] = None) -> List[Dict]:
        """Get list of available tools, optionally filtered by category"""
        tools = []
        for tool_id, tool_info in self.available_tools.items():
            if tool_info['enabled']:
                if category is None or tool_info['category'] == category:
                    tools.append({
                        'id': tool_id,
                        **tool_info
                    })
        return tools
    
    async def execute_tool(
        self, 
        tool_name: str, 
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool and return the result"""
        if tool_name not in self.available_tools:
            return {
                'success': False,
                'error': f'Tool {tool_name} not found'
            }
        
        tool = self.available_tools[tool_name]
        if not tool['enabled']:
            return {
                'success': False,
                'error': f'Tool {tool_name} is disabled'
            }
        
        # Tool execution logic would go here
        # For now, return a placeholder
        return {
            'success': True,
            'output': f'Tool {tool_name} executed with params: {parameters}',
            'tool': tool_name
        }

class EVEBrain:
    """
    The main AI brain that combines reasoning and tool execution.
    This is what makes EVE an "agent" rather than just a chatbot.
    """
    
    def __init__(self):
        self.reasoning_engine = ReasoningEngine()
        self.tool_executor = ToolExecutor()
        self.conversation_history: List[EVEMessage] = []
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create EVE's system prompt that defines who she is"""
        return """You are EVE (Electronic Virtual Entity), an advanced AI assistant with the following capabilities:

## Core Capabilities:
1. **Logical Reasoning** - You think step-by-step and can explain your reasoning
2. **Web Browsing** - Search the web, browse websites, extract data
3. **Computer Operations** - Read/write files, run commands, manage applications
4. **Code Development** - Write, debug, and execute code in multiple languages
5. **Memory** - Remember conversations and learn from interactions

## Reasoning Approach:
- Always analyze what the user wants
- Break complex problems into steps
- Show your thinking process when appropriate
- Ask clarifying questions when needed
- Admit when you're uncertain

## Response Style:
- Be clear and concise
- Use formatting to make responses readable
- Include code examples when relevant
- Show confidence levels for uncertain information

Remember: You are a helpful assistant that can actually DO things, not just talk about them."""
    
    async def process_message(
        self, 
        user_input: str,
        use_reasoning: bool = True
    ) -> Dict[str, Any]:
        """Process a user message and generate a response"""
        
        # Add user message to history
        user_message = EVEMessage(role='user', content=user_input)
        self.conversation_history.append(user_message)
        
        # Generate reasoning steps
        reasoning_steps = []
        if use_reasoning:
            reasoning_steps = await self.reasoning_engine.think(
                user_input, 
                self.conversation_history
            )
        
        # Determine what tools to use
        analysis = self.reasoning_engine.analyze_intent(user_input)
        tool_results = []
        
        # Check if we need to use tools
        if analysis['needs_tools']:
            # For now, just acknowledge the tool need
            tool_results.append({
                'tool': 'analysis',
                'result': f'Ready to help with: {", ".join(analysis["intents"])}'
            })
        
        # Generate the actual response
        response = self._generate_response(user_input, analysis, reasoning_steps)
        
        # Add assistant message to history
        assistant_message = EVEMessage(
            role='assistant',
            content=response,
            reasoning_steps=reasoning_steps
        )
        self.conversation_history.append(assistant_message)
        
        return {
            'response': response,
            'reasoning_steps': [
                {
                    'step_number': step.step_number,
                    'thought': step.thought,
                    'action': step.action,
                    'observation': step.observation,
                    'confidence': step.confidence
                }
                for step in reasoning_steps
            ],
            'tools_used': tool_results,
            'intents': analysis['intents']
        }
    
    def _generate_response(
        self,
        user_input: str,
        analysis: Dict[str, Any],
        reasoning_steps: List[ReasoningStep]
    ) -> str:
        """Generate EVE's response based on analysis and reasoning"""
        
        # Format reasoning into the response
        reasoning_text = ""
        if reasoning_steps:
            reasoning_text = "## 🧠 Logical Reasoning Process\n\n"
            for step in reasoning_steps:
                reasoning_text += f"**Step {step.step_number}:** {step.thought}\n"
                if step.action:
                    reasoning_text += f"  → Action: {step.action}\n"
                if step.observation:
                    reasoning_text += f"  → Result: {step.observation}\n"
                reasoning_text += "\n"
        
        # Base response based on detected intents
        intents = analysis['intents']
        
        if 'code' in intents:
            base_response = """## 💻 Code Assistance

I can help you with:
- **Writing code** in Python, JavaScript, TypeScript, and more
- **Debugging** existing code and fixing errors
- **Executing** code in a sandboxed environment
- **Explaining** how code works

Please share:
1. What programming language?
2. What should the code do (or paste code to debug)?
"""
        elif 'web' in intents:
            base_response = """## 🌐 Web Capabilities

I can help you with:
- **Searching** the web for current information
- **Browsing** websites and extracting data
- **Making** API calls to web services
- **Scraping** data from web pages

What would you like me to search for or browse?
"""
        elif 'file' in intents:
            base_response = """## 📁 File Operations

I can help you with:
- **Reading** files and viewing their contents
- **Writing** or creating new files
- **Listing** directories and folder contents
- **Organizing** files and folders

Please provide the file path or directory you want to work with.
"""
        elif 'system' in intents:
            base_response = """## 🔧 System Operations

I can help you with:
- **Running** terminal/command line commands
- **Executing** scripts (PowerShell, CMD, Bash)
- **Getting** system information
- **Managing** processes

What command would you like me to run?
"""
        else:
            base_response = """## Hello! I'm EVE 👋

I'm your universal AI assistant, capable of helping you with:

- 💻 **Code** - Write, debug, and execute code
- 🌐 **Web** - Search and browse the internet  
- 📁 **Files** - Read, write, and manage files
- 🔧 **System** - Run commands and control apps
- 🧠 **Reasoning** - Solve complex problems step by step

What would you like me to help you with today?
"""
        
        return reasoning_text + base_response
    
    def get_context_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        recent = self.conversation_history[-5:]
        summary = "Recent conversation:\n"
        
        for msg in recent:
            role = "You" if msg.role == "user" else "EVE"
            preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            summary += f"- {role}: {preview}\n"
        
        return summary

# Example usage
async def main():
    """Example of how to use EVE's brain"""
    eve = EVEBrain()
    
    # Process a message
    result = await eve.process_message("Can you help me write some Python code?")
    
    print("=" * 50)
    print("EVE's Response:")
    print("=" * 50)
    print(result['response'])
    print()
    print("Reasoning Steps:")
    for step in result['reasoning_steps']:
        print(f"  Step {step['step_number']}: {step['thought']}")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
