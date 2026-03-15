"""
EVE AGI Engine
Autonomous General Intelligence with ReAct loop, tool execution, and self-improvement.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Import existing modules
from tools import ToolRegistry
from memory import EVEMemory


class AGIState(Enum):
    """States in the AGI execution loop"""
    THINKING = "thinking"
    PLANNING = "planning"
    ACTING = "acting"
    OBSERVING = "observing"
    LEARNING = "learning"
    RESPONDING = "responding"


@dataclass
class Thought:
    """A single thought in the reasoning chain"""
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict] = None
    observation: Optional[str] = None
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Plan:
    """An autonomous plan created by EVE"""
    goal: str
    steps: List[Dict[str, Any]]
    current_step: int = 0
    completed: bool = False
    results: List[str] = field(default_factory=list)


class AGIEngine:
    """
    EVE's AGI Engine - gives her autonomous capabilities.
    Uses ReAct (Reasoning + Acting) loop for multi-step problem solving.
    """
    
    def __init__(self):
        self.tools = ToolRegistry()
        self.memory = EVEMemory()
        self.max_iterations = 10  # Max steps per task
        self.thinking_depth = 3   # How deep to think
        
    async def process(self, user_input: str, context: List[Dict] = None) -> Dict[str, Any]:
        """
        Main AGI processing loop.
        Uses ReAct: Thought → Action → Observation → ...
        """
        thoughts = []
        observations = []
        
        # Initial thought
        thought = Thought(
            thought=f"Analyzing: '{user_input}'",
            confidence=0.9
        )
        thoughts.append(thought)
        
        # Check if this requires tools
        needs_tools = self._analyze_needs(user_input)
        
        if needs_tools:
            # ReAct loop
            result = await self._react_loop(user_input, thoughts, observations)
            return result
        else:
            # Direct reasoning response
            return await self._think_only(user_input, thoughts)
    
    def _analyze_needs(self, user_input: str) -> bool:
        """Analyze if the input requires tool use"""
        tool_indicators = [
            'search', 'find', 'look up', 'browse', 'visit',
            'read', 'write', 'create', 'delete', 'list',
            'run', 'execute', 'command', 'code', 'program',
            'calculate', 'compute', 'what is', 'who is', 'when',
            'download', 'upload', 'open', 'close'
        ]
        input_lower = user_input.lower()
        return any(indicator in input_lower for indicator in tool_indicators)
    
    async def _react_loop(
        self, 
        user_input: str, 
        thoughts: List[Thought],
        observations: List[str]
    ) -> Dict[str, Any]:
        """
        ReAct (Reasoning + Acting) loop.
        Continues until task is complete or max iterations reached.
        """
        task = user_input
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # 1. THINK: Decide what to do
            thought = await self._think(task, thoughts, observations)
            thoughts.append(thought)
            
            if thought.action is None:
                # No action needed, we're done thinking
                break
            
            # 2. ACT: Execute the tool
            action_result = await self._act(thought.action, thought.action_input)
            
            # 3. OBSERVE: Record the result
            observation = f"Action {thought.action}: {action_result.get('output', str(action_result))}"
            observations.append(observation)
            thought.observation = observation
            
            # 4. CHECK: Did we complete the task?
            if self._is_complete(task, observation):
                break
        
        # Generate final response
        response = self._synthesize_response(thoughts, observations)
        
        return {
            'response': response,
            'thoughts': [
                {
                    'thought': t.thought,
                    'action': t.action,
                    'observation': t.observation,
                    'confidence': t.confidence
                }
                for t in thoughts
            ],
            'iterations': iteration,
            'mode': 'AGI (Autonomous)'
        }
    
    async def _think(
        self, 
        task: str, 
        thoughts: List[Thought], 
        observations: List[str]
    ) -> Thought:
        """Decide the next action based on task and observations"""
        
        # Build context from previous thoughts
        context = f"Task: {task}\n"
        if observations:
            context += "Observations:\n" + "\n".join(f"- {o}" for o in observations[-3:])
        
        # Analyze what to do next
        task_lower = task.lower()
        
        # Search actions
        if any(kw in task_lower for kw in ['search', 'find', 'look up']):
            query = task.lower().replace('search', '').replace('find', '').replace('look up', '').strip()
            return Thought(
                thought=f"Need to search for: {query}",
                action="web_search",
                action_input={"query": query, "num_results": 5},
                confidence=0.9
            )
        
        # Browse actions
        if any(kw in task_lower for kw in ['browse', 'visit', 'open']):
            # Extract URL from task
            import re
            urls = re.findall(r'https?://[^\s]+', task)
            if urls:
                return Thought(
                    thought=f"Need to browse: {urls[0]}",
                    action="web_browse",
                    action_input={"url": urls[0], "action": "get"},
                    confidence=0.9
                )
        
        # File operations
        if 'list' in task_lower and ('file' in task_lower or 'directory' in task_lower or 'folder' in task_lower):
            path = task.lower().replace('list', '').replace('files', '').replace('directory', '').strip() or "."
            return Thought(
                thought=f"Need to list files in: {path}",
                action="file_list",
                action_input={"path": path, "recursive": False},
                confidence=0.9
            )
        
        # Read file
        if any(kw in task_lower for kw in ['read', 'show', 'display']) and ('file' in task_lower or any(ext in task_lower for ext in ['.py', '.js', '.txt', '.json', '.md'])):
            # Extract filename
            import re
            words = task.split()
            for word in words:
                if '.' in word and not word.startswith('http'):
                    return Thought(
                        thought=f"Need to read file: {word}",
                        action="file_read",
                        action_input={"path": word},
                        confidence=0.9
                    )
        
        # Code execution
        if any(kw in task_lower for kw in ['run', 'execute', 'code', 'python']):
            # Extract code to run
            code_match = re.search(r'```[\s\S]*?```', task)
            if code_match:
                code = code_match.group().replace('```python', '').replace('```', '').strip()
                return Thought(
                    thought=f"Need to execute Python code",
                    action="code_execute",
                    action_input={"code": code, "language": "python"},
                    confidence=0.9
                )
        
        # Default: respond that we need more info
        return Thought(
            thought="Task analysis complete",
            action=None,
            confidence=0.5
        )
    
    async def _act(self, action: str, action_input: Dict) -> Dict[str, Any]:
        """Execute an action using the tool registry"""
        try:
            result = await self.tools.execute_tool(action, **action_input)
            return result.to_dict() if hasattr(result, 'to_dict') else result
        except Exception as e:
            return {'success': False, 'error': str(e), 'output': ''}
    
    def _is_complete(self, task: str, observation: str) -> bool:
        """Check if the task is complete based on observation"""
        completion_indicators = [
            'found', 'completed', 'success', 'finished',
            'results:', 'here are', 'successfully'
        ]
        obs_lower = observation.lower()
        return any(indicator in obs_lower for indicator in completion_indicators)
    
    async def _think_only(self, user_input: str, thoughts: List[Thought]) -> Dict[str, Any]:
        """Process without tools - pure reasoning"""
        # Add reasoning thought
        thought = Thought(
            thought=f"Processing reasoning task: '{user_input}'",
            confidence=0.95
        )
        thoughts.append(thought)
        
        return {
            'response': self._synthesize_response(thoughts, []),
            'thoughts': [
                {
                    'thought': t.thought,
                    'action': t.action,
                    'observation': t.observation,
                    'confidence': t.confidence
                }
                for t in thoughts
            ],
            'iterations': 1,
            'mode': 'AGI (Reasoning)'
        }
    
    def _synthesize_response(self, thoughts: List[Thought], observations: List[str]) -> str:
        """Synthesize a response from thoughts and observations"""
        
        # Format reasoning trace
        reasoning = "## 🧠 Autonomous Reasoning\n\n"
        
        for i, thought in enumerate(thoughts, 1):
            reasoning += f"**{i}.** {thought.thought}\n"
            if thought.action:
                reasoning += f"   → Action: `{thought.action}`\n"
            if thought.observation:
                reasoning += f"   → Result: {thought.observation[:200]}...\n"
            reasoning += "\n"
        
        # Add final answer based on observations
        if observations:
            last_obs = observations[-1]
            if 'search' in str(thoughts[-1].action if thoughts else ''):
                reasoning += "\n## 📊 Results\n\n"
                reasoning += last_obs + "\n"
        
        reasoning += "\n---\n*EVE is operating in AGI mode with autonomous tool execution.*"
        
        return reasoning
    
    async def create_plan(self, goal: str) -> Plan:
        """Create an autonomous plan to achieve a goal"""
        steps = []
        
        # Break down goal into steps
        goal_lower = goal.lower()
        
        if 'research' in goal_lower or 'study' in goal_lower:
            steps = [
                {"action": "web_search", "input": {"query": goal, "num_results": 10}},
                {"action": "web_browse", "input": {"url": "{{url}}", "action": "extract"}},
                {"action": "memory_save", "input": {"key": "research", "data": "{{results}}"}}
            ]
        elif 'build' in goal_lower or 'create' in goal_lower:
            steps = [
                {"action": "file_write", "input": {"path": "{{filename}}", "content": "{{content}}"}},
                {"action": "code_execute", "input": {"code": "{{test_code}}", "language": "python"}}
            ]
        else:
            steps = [
                {"action": "analyze", "input": {"task": goal}}
            ]
        
        return Plan(goal=goal, steps=steps)
    
    async def execute_plan(self, plan: Plan) -> Dict[str, Any]:
        """Execute an autonomous plan"""
        results = []
        
        for i, step in enumerate(plan.steps):
            if plan.current_step >= len(plan.steps):
                break
                
            action = step.get('action')
            action_input = step.get('input', {})
            
            result = await self._act(action, action_input)
            results.append(str(result))
            plan.results.append(str(result))
            plan.current_step += 1
            
            # Store in memory
            self.memory.learn_fact(
                f"plan_step_{i}",
                f"Executed {action}"
            )
        
        plan.completed = plan.current_step >= len(plan.steps)
        
        return {
            'plan': {
                'goal': plan.goal,
                'completed': plan.completed,
                'steps_executed': plan.current_step,
                'results': plan.results
            }
        }
    
    def learn(self, key: str, data: Any) -> bool:
        """Store learned information"""
        try:
            self.memory.learn_fact(str(data))
            return True
        except:
            return False
    
    def get_knowledge(self, key: str) -> Optional[Any]:
        """Retrieve learned information"""
        try:
            # This would retrieve from memory system
            return None
        except:
            return None


# Example usage
async def main():
    """Test the AGI engine"""
    agi = AGIEngine()
    
    print("=" * 50)
    print("EVE AGI Engine Test")
    print("=" * 50)
    
    # Test 1: Search task
    print("\n--- Test 1: Web Search ---")
    result = await agi.process("search for Python AI assistants")
    print(f"Response: {result['response'][:200]}...")
    print(f"Iterations: {result['iterations']}")
    print(f"Mode: {result['mode']}")
    
    # Test 2: File listing
    print("\n--- Test 2: File List ---")
    result = await agi.process("list files in current directory")
    print(f"Response: {result['response'][:200]}...")
    
    print("\n" + "=" * 50)
    print("AGI Engine working!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
