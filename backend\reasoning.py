"""
EVE Reasoning & Planning Engine
Breaks complex goals into clear steps, shows intermediate reasoning
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ReasoningType(Enum):
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    REACT = "react"
    REFLEXION = "reflexion"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    WAITING_APPROVAL = "waiting_approval"

@dataclass
class ReasoningStep:
    """A single step in reasoning"""
    step_number: int
    thought: str
    action: str = None
    observation: str = None
    confidence: float = 1.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class Task:
    """A task to be completed"""
    id: str
    description: str
    status: TaskStatus
    steps: List[ReasoningStep] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str = ""

class ReasoningEngine:
    """Engine for complex reasoning and planning"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.current_reasoning: List[ReasoningStep] = []
        self.reasoning_type = ReasoningType.CHAIN_OF_THOUGHT
    
    # ==================== CHAIN OF THOUGHT ====================
    
    async def think(
        self,
        problem: str,
        show_reasoning: bool = True
    ) -> Dict[str, Any]:
        """Think through a problem step by step"""
        self.current_reasoning = []
        
        # Step 1: Understand the problem
        step1 = ReasoningStep(
            step_number=1,
            thought=f"Understanding the problem: {problem}",
            action="Analyzing",
            confidence=0.9
        )
        self.current_reasoning.append(step1)
        
        # Step 2: Break down the problem
        step2 = ReasoningStep(
            step_number=2,
            thought="Breaking down into smaller components",
            action="Decomposing",
            confidence=0.85
        )
        self.current_reasoning.append(step2)
        
        # Step 3: Consider approaches
        step3 = ReasoningStep(
            step_number=3,
            thought="Considering possible approaches",
            action="Evaluating",
            confidence=0.8
        )
        self.current_reasoning.append(step3)
        
        # Step 4: Select best approach
        step4 = ReasoningStep(
            step_number=4,
            thought="Selecting the most effective approach",
            action="Deciding",
            confidence=0.9
        )
        self.current_reasoning.append(step4)
        
        # Step 5: Execute and verify
        step5 = ReasoningStep(
            step_number=5,
            thought="Implementing solution and verifying",
            action="Executing",
            confidence=0.95
        )
        self.current_reasoning.append(step5)
        
        return {
            "reasoning_steps": [s.__dict__ for s in self.current_reasoning],
            "final_thought": self.current_reasoning[-1].thought if self.current_reasoning else "",
            "confidence": sum(s.confidence for s in self.current_reasoning) / len(self.current_reasoning) if self.current_reasoning else 0
        }
    
    # ==================== TASK PLANNING ====================
    
    def create_task(
        self,
        description: str,
        dependencies: List[str] = None
    ) -> str:
        """Create a new task"""
        import uuid
        task_id = str(uuid.uuid4())[:8]
        
        task = Task(
            id=task_id,
            description=description,
            status=TaskStatus.PENDING,
            dependencies=dependencies or []
        )
        
        self.tasks[task_id] = task
        return task_id
    
    def add_step_to_task(
        self,
        task_id: str,
        thought: str,
        action: str = None
    ) -> bool:
        """Add a step to a task"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        step = ReasoningStep(
            step_number=len(task.steps) + 1,
            thought=thought,
            action=action
        )
        task.steps.append(step)
        
        return True
    
    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus
    ) -> bool:
        """Update task status"""
        if task_id not in self.tasks:
            return False
        
        self.tasks[task_id].status = status
        if status == TaskStatus.COMPLETED:
            self.tasks[task_id].completed_at = datetime.now().isoformat()
        
        return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task details"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks"""
        return [
            {
                "id": t.id,
                "description": t.description,
                "status": t.status.value,
                "steps_count": len(t.steps),
                "created_at": t.created_at,
                "completed_at": t.completed_at
            }
            for t in self.tasks.values()
        ]
    
    # ==================== HIGH RISK ACTIONS ====================
    
    def requires_approval(self, action: str) -> bool:
        """Check if action requires human approval"""
        high_risk_actions = [
            "security_scan",
            "delete_account",
            "transfer_money",
            "send_email",
            "execute_code",
            "access_sensitive_data"
        ]
        return action.lower() in high_risk_actions
    
    def mark_for_approval(self, task_id: str) -> bool:
        """Mark task for human approval"""
        if task_id not in self.tasks:
            return False
        
        self.tasks[task_id].status = TaskStatus.WAITING_APPROVAL
        return True
    
    def approve_task(self, task_id: str) -> bool:
        """Approve a waiting task"""
        if task_id not in self.tasks:
            return False
        
        self.tasks[task_id].status = TaskStatus.PENDING
        return True
    
    # ==================== PLAN EXECUTION ====================
    
    async def execute_plan(
        self,
        task_id: str,
        executor_func = None
    ) -> Dict[str, Any]:
        """Execute a task plan"""
        if task_id not in self.tasks:
            return {"success": False, "error": "Task not found"}
        
        task = self.tasks[task_id]
        results = []
        
        for step in task.steps:
            self.update_task_status(task_id, TaskStatus.IN_PROGRESS)
            
            # Execute step (if function provided)
            observation = ""
            if executor_func:
                observation = await executor_func(step)
            
            step.observation = observation
            results.append({
                "step": step.step_number,
                "thought": step.thought,
                "observation": observation
            })
        
        self.update_task_status(task_id, TaskStatus.COMPLETED)
        
        return {
            "success": True,
            "task_id": task_id,
            "steps_executed": len(results),
            "results": results
        }


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        engine = ReasoningEngine()
        
        # Create a complex task
        task_id = engine.create_task(
            "Research and analyze security vulnerabilities",
            dependencies=[]
        )
        
        # Add steps
        engine.add_step_to_task(task_id, "Gather information about target", "Research")
        engine.add_step_to_task(task_id, "Identify potential vulnerabilities", "Analysis")
        engine.add_step_to_task(task_id, "Document findings", "Documentation")
        
        print("Task created:", task_id)
        print("Steps:", len(engine.get_task(task_id).steps))
        
        # Test reasoning
        result = await engine.think("How to improve cybersecurity?")
        print("\nReasoning steps:")
        for step in result["reasoning_steps"]:
            print(f"  {step['step_number']}. {step['thought']}")
    
    asyncio.run(main())
