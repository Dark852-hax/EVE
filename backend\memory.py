"""
EVE AI Memory System
Persistent memory storage for EVE to remember conversations and learned information.
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict
from pathlib import Path
import sqlite3

# Database path
MEMORY_DB_PATH = os.path.join(os.path.dirname(__file__), 'eve_memory.db')

class MemoryType:
    """Types of memory EVE can store"""
    CONVERSATION = "conversation"
    KNOWLEDGE = "knowledge"
    PREFERENCE = "preference"
    FACT = "fact"
    SKILL = "skill"

@dataclass
class Memory:
    """Represents a single memory entry"""
    id: str
    memory_type: str
    content: str
    importance: float  # 0-1 scale
    created_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            **asdict(self),
            'created_at': self.created_at.isoformat(),
            'accessed_at': self.accessed_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Memory':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['accessed_at'] = datetime.fromisoformat(data['accessed_at'])
        return cls(**data)

class MemoryDatabase:
    """SQLite database for EVE's memory"""
    
    def __init__(self, db_path: str = MEMORY_DB_PATH):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                importance REAL DEFAULT 0.5,
                created_at TEXT NOT NULL,
                accessed_at TEXT NOT NULL,
                access_count INTEGER DEFAULT 0,
                tags TEXT,
                metadata TEXT
            )
        ''')
        
        # Create index for faster searching
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_memory_type ON memories(memory_type)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance DESC)
        ''')
        
        conn.commit()
        conn.close()
    
    def store_memory(self, memory: Memory) -> bool:
        """Store a new memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO memories 
                (id, memory_type, content, importance, created_at, accessed_at, 
                 access_count, tags, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory.id,
                memory.memory_type,
                memory.content,
                memory.importance,
                memory.created_at.isoformat(),
                memory.accessed_at.isoformat(),
                memory.access_count,
                json.dumps(memory.tags),
                json.dumps(memory.metadata)
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing memory: {e}")
            return False
    
    def retrieve_memories(
        self, 
        memory_type: Optional[str] = None,
        tag: Optional[str] = None,
        min_importance: float = 0.0,
        limit: int = 10
    ) -> List[Memory]:
        """Retrieve memories based on filters"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM memories WHERE importance >= ?"
        params = [min_importance]
        
        if memory_type:
            query += " AND memory_type = ?"
            params.append(memory_type)
        
        if tag:
            query += " AND tags LIKE ?"
            params.append(f'%"{tag}"%')
        
        query += " ORDER BY importance DESC, accessed_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in rows:
            data = dict(row)
            data['tags'] = json.loads(data['tags']) if data['tags'] else []
            data['metadata'] = json.loads(data['metadata']) if data['metadata'] else {}
            memories.append(Memory.from_dict(data))
        
        return memories
    
    def search_memories(self, query: str, limit: int = 5) -> List[Memory]:
        """Search memories by content"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM memories 
            WHERE content LIKE ? OR tags LIKE ?
            ORDER BY importance DESC, access_count DESC
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in rows:
            data = dict(row)
            data['tags'] = json.loads(data['tags']) if data['tags'] else []
            data['metadata'] = json.loads(data['metadata']) if data['metadata'] else {}
            memories.append(Memory.from_dict(data))
        
        return memories
    
    def update_access(self, memory_id: str) -> bool:
        """Update access time and count for a memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE memories 
                SET access_count = access_count + 1, accessed_at = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), memory_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating memory access: {e}")
            return False
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting memory: {e}")
            return False
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about stored memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total count
        cursor.execute('SELECT COUNT(*) FROM memories')
        total = cursor.fetchone()[0]
        
        # Count by type
        cursor.execute('''
            SELECT memory_type, COUNT(*) 
            FROM memories 
            GROUP BY memory_type
        ''')
        by_type = dict(cursor.fetchall())
        
        # Average importance
        cursor.execute('SELECT AVG(importance) FROM memories')
        avg_importance = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_memories': total,
            'by_type': by_type,
            'average_importance': avg_importance
        }

class ConversationMemory:
    """Manages conversation history with smart summarization"""
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.messages: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to conversation history"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.messages.append(message)
        
        # Trim if exceeds max
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_recent(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent messages"""
        return self.messages[-count:]
    
    def get_full_context(self) -> str:
        """Get full conversation as formatted string"""
        context = "Conversation history:\n\n"
        for msg in self.messages:
            role = "User" if msg['role'] == 'user' else "EVE"
            context += f"{role}: {msg['content'][:200]}...\n"
        return context
    
    def summarize_old_messages(self, keep_count: int = 10) -> str:
        """Summarize old messages and return summary"""
        if len(self.messages) <= keep_count:
            return ""
        
        old_messages = self.messages[:-keep_count]
        
        # Simple summary - in production, use AI
        summary = f"[Summary of {len(old_messages)} previous messages]: "
        topics = set()
        
        for msg in old_messages:
            content = msg['content'].lower()
            # Extract simple keywords
            keywords = ['code', 'file', 'web', 'search', 'python', 'help', 'question']
            for kw in keywords:
                if kw in content:
                    topics.add(kw)
        
        if topics:
            summary += f"Discussed: {', '.join(topics)}"
        else:
            summary += "General conversation"
        
        # Keep recent messages and add summary
        self.messages = [{'role': 'system', 'content': summary}] + self.messages[-keep_count:]
        
        return summary
    
    def clear(self):
        """Clear all conversation history"""
        self.messages = []

class EVEMemory:
    """
    Main memory system for EVE.
    Combines conversation history, persistent knowledge, and learned facts.
    """
    
    def __init__(self):
        self.db = MemoryDatabase()
        self.conversation = ConversationMemory()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def remember(
        self, 
        content: str, 
        memory_type: str = MemoryType.CONVERSATION,
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Store something in EVE's memory"""
        import uuid
        memory = Memory(
            id=str(uuid.uuid4()),
            memory_type=memory_type,
            content=content,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {}
        )
        return self.db.store_memory(memory)
    
    def recall(
        self, 
        query: Optional[str] = None,
        memory_type: Optional[str] = None,
        tag: Optional[str] = None
    ) -> List[Memory]:
        """Recall memories"""
        if query:
            return self.db.search_memories(query)
        return self.db.retrieve_memories(
            memory_type=memory_type,
            tag=tag,
            limit=10
        )
    
    def add_to_conversation(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation.add_message(role, content)
    
    def get_conversation_context(self, recent_count: int = 5) -> str:
        """Get conversation context for AI"""
        return self.conversation.get_full_context()
    
    def learn_fact(self, fact: str, importance: float = 0.7) -> bool:
        """Store an important fact"""
        return self.remember(
            content=fact,
            memory_type=MemoryType.FACT,
            importance=importance,
            tags=['fact', 'learned']
        )
    
    def remember_preference(self, key: str, value: str) -> bool:
        """Remember user preference"""
        return self.remember(
            content=f"{key}: {value}",
            memory_type=MemoryType.PREFERENCE,
            importance=0.8,
            tags=['preference', key]
        )
    
    def get_preference(self, key: str) -> Optional[str]:
        """Get user preference"""
        memories = self.db.retrieve_memories(
            memory_type=MemoryType.PREFERENCE,
            tag=key,
            limit=1
        )
        if memories:
            return memories[0].content.split(': ', 1)[1] if ': ' in memories[0].content else None
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            **self.db.get_memory_stats(),
            'session_id': self.session_id,
            'conversation_length': len(self.conversation.messages)
        }

# Example usage
if __name__ == "__main__":
    # Test the memory system
    memory = EVEMemory()
    
    # Remember something
    memory.learn_fact("The user prefers dark mode interface")
    memory.learn_fact("User is working on a Python project")
    
    # Remember a conversation
    memory.add_to_conversation("user", "Can you help me with Python?")
    memory.add_to_conversation("assistant", "Of course! I can help with Python.")
    
    # Recall
    facts = memory.recall(memory_type=MemoryType.FACT)
    print("Known facts:")
    for fact in facts:
        print(f"  - {fact.content}")
    
    # Get stats
    stats = memory.get_stats()
    print(f"\nMemory stats: {stats}")
