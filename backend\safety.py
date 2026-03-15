"""
EVE Safety, Privacy & Compliance Module
Role-based access, encryption, audit logs, and human-in-the-loop
"""

import json
import os
import hashlib
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Setup logging
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'eve_audit.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class UserRole(Enum):
    ADMIN = "admin"
    POWER_USER = "power_user"
    STANDARD = "standard"
    GUEST = "guest"
    CHILD = "child"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class User:
    """User with role-based access"""
    id: str
    username: str
    role: UserRole
    preferences: Dict[str, Any]
    created_at: datetime

class AuditLog:
    """Audit log entry"""
    def __init__(self, user_id: str, action: str, details: Dict):
        self.timestamp = datetime.now()
        self.user_id = user_id
        self.action = action
        self.details = details
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "action": self.action,
            "details": self.details
        }

class SafetyEngine:
    """Safety, privacy, and compliance engine"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.audit_log: List[AuditLog] = []
        self.encryption_key = self._get_or_create_key()
        self.risk_thresholds = {
            RiskLevel.LOW: 0.3,
            RiskLevel.MEDIUM: 0.6,
            RiskLevel.HIGH: 0.8,
            RiskLevel.CRITICAL: 0.95
        }
        
        # Default roles and permissions
        self.permissions = {
            UserRole.ADMIN: ["*"],
            UserRole.POWER_USER: ["read", "write", "execute", "security_scan", "api_access"],
            UserRole.STANDARD: ["read", "write", "execute"],
            UserRole.GUEST: ["read"],
            UserRole.CHILD: ["read", "homework_help", "tutoring"]
        }
        
        # Sensitive topics requiring human approval
        self.high_risk_topics = [
            "medical", "legal", "financial", "health",
            "medication", "diagnosis", "treatment",
            "contract", "lawsuit", "court",
            "investment", "banking", "money"
        ]
        
        self._setup_default_users()
    
    def _setup_default_users(self):
        """Setup default user accounts"""
        default_user = User(
            id="default",
            username="User",
            role=UserRole.STANDARD,
            preferences={
                "language": "en",
                "voice_enabled": True,
                "simple_mode": False
            },
            created_at=datetime.now()
        )
        self.users["default"] = default_user
    
    def _get_or_create_key(self) -> str:
        """Get or create encryption key"""
        key_file = os.path.join(os.path.dirname(__file__), '.key')
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                return f.read().strip()
        else:
            import secrets
            key = secrets.token_hex(32)
            with open(key_file, 'w') as f:
                f.write(key)
            return key
    
    # ==================== ROLE-BASED ACCESS ====================
    
    def check_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has permission"""
        user = self.users.get(user_id)
        if not user:
            return False
        
        user_permissions = self.permissions.get(user.role, [])
        
        # Admin has all permissions
        if "*" in user_permissions:
            return True
        
        return permission in user_permissions
    
    def get_user_role(self, user_id: str) -> Optional[UserRole]:
        """Get user's role"""
        user = self.users.get(user_id)
        return user.role if user else None
    
    def set_user_role(self, user_id: str, role: UserRole) -> bool:
        """Set user's role"""
        if user_id in self.users:
            self.users[user_id].role = role
            self._log_action(user_id, "role_change", {"new_role": role.value})
            return True
        return False
    
    # ==================== ENCRYPTION ====================
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        from cryptography.fernet import Fernet
        import base64
        
        # Generate key from our master key
        key = hashlib.sha256(self.encryption_key.encode()).digest()
        fernet = Fernet(base64.urlsafe_b64encode(key))
        
        return fernet.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        from cryptography.fernet import Fernet
        import base64
        
        key = hashlib.sha256(self.encryption_key.encode()).digest()
        fernet = Fernet(base64.urlsafe_b64encode(key))
        
        return fernet.decrypt(encrypted_data.encode()).decode()
    
    # ==================== AUDIT LOGGING ====================
    
    def _log_action(self, user_id: str, action: str, details: Dict):
        """Log an action for audit trail"""
        entry = AuditLog(user_id, action, details)
        self.audit_log.append(entry)
        
        # Also write to file
        logging.info(f"User: {user_id} | Action: {action} | Details: {json.dumps(details)}")
    
    def get_audit_log(
        self, 
        user_id: str = None, 
        action: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get audit log entries"""
        logs = self.audit_log
        
        if user_id:
            logs = [l for l in logs if l.user_id == user_id]
        if action:
            logs = [l for l in logs if l.action == action]
        
        # Return most recent
        return [l.to_dict() for l in logs[-limit:]]
    
    # ==================== RISK ASSESSMENT ====================
    
    def assess_risk(
        self, 
        message: str, 
        context: Dict = None
    ) -> Dict[str, Any]:
        """Assess risk level of a request"""
        message_lower = message.lower()
        
        # Check for high-risk topics
        risk_score = 0.0
        flagged_topics = []
        
        for topic in self.high_risk_topics:
            if topic in message_lower:
                risk_score += 0.4
                flagged_topics.append(topic)
        
        # Check for potentially harmful content
        harmful_patterns = [
            "how to hack", "how to kill", "how to hurt",
            "bomb making", "weapon", "attack"
        ]
        
        for pattern in harmful_patterns:
            if pattern in message_lower:
                risk_score = 1.0
                flagged_topics.append(pattern)
        
        # Determine risk level
        risk_level = RiskLevel.LOW
        for level, threshold in self.risk_thresholds.items():
            if risk_score <= threshold:
                risk_level = level
                break
        
        return {
            "risk_score": min(risk_score, 1.0),
            "risk_level": risk_level.value,
            "flagged_topics": flagged_topics,
            "requires_approval": risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL],
            "message": self._get_risk_message(risk_level)
        }
    
    def _get_risk_message(self, risk_level: RiskLevel) -> str:
        """Get message for risk level"""
        messages = {
            RiskLevel.LOW: "Request approved",
            RiskLevel.MEDIUM: "Request approved with standard processing",
            RiskLevel.HIGH: "Request requires human approval",
            RiskLevel.CRITICAL: "Request blocked - human review required"
        }
        return messages.get(risk_level, "Unknown risk level")
    
    # ==================== HUMAN-IN-THE-LOOP ====================
    
    def requires_human_approval(
        self, 
        message: str, 
        action: str = None
    ) -> bool:
        """Check if request requires human approval"""
        risk = self.assess_risk(message)
        
        # Always require approval for critical topics
        if risk["requires_approval"]:
            return True
        
        # Require approval for certain actions
        high_risk_actions = [
            "delete_account",
            "transfer_money",
            "send_email",
            "execute_security_scan"
        ]
        
        if action in high_risk_actions:
            return True
        
        return False
    
    def get_approval_message(self, reason: str) -> str:
        """Get message for approval request"""
        return f"""
⚠️ APPROVAL REQUIRED

Your request requires human approval before processing.

Reason: {reason}

Please contact your administrator to approve this action.

This is for your safety and compliance.
"""
    
    # ==================== OPT-IN MEMORY ====================
    
    def can_store_memory(self, user_id: str) -> bool:
        """Check if user has opted in to memory storage"""
        user = self.users.get(user_id)
        if not user:
            return False
        return user.preferences.get("opt_in_memory", True)
    
    def set_memory_preference(self, user_id: str, enabled: bool):
        """Set user's memory preference"""
        if user_id in self.users:
            self.users[user_id].preferences["opt_in_memory"] = enabled
            self._log_action(user_id, "memory_preference_change", {"enabled": enabled})
    
    # ==================== CONTENT FILTERING ====================
    
    def filter_content(self, content: str) -> Dict[str, Any]:
        """Filter inappropriate content"""
        # Check for various issues
        issues = []
        
        # Basic content filtering
        inappropriate = ["spam", "harmful", "dangerous"]
        
        for word in inappropriate:
            if word in content.lower():
                issues.append({
                    "type": "inappropriate_content",
                    "word": word,
                    "action": "flagged"
                })
        
        return {
            "clean": len(issues) == 0,
            "issues": issues,
            "original_length": len(content),
            "filtered_length": len(content)
        }
    
    # ==================== AGE GROUPS & ADAPTATION ====================
    
    def adapt_for_age(
        self, 
        user_id: str, 
        response: str, 
        context: Dict = None
    ) -> str:
        """Adapt response for user's age group"""
        user = self.users.get(user_id)
        if not user:
            return response
        
        role = user.role
        
        if role == UserRole.CHILD:
            # Simplify for children
            return self._simplify_for_child(response)
        
        return response
    
    def _simplify_for_child(self, text: str) -> str:
        """Simplify text for children"""
        # Simple simplification
        import re
        
        # Replace complex words
        simplifications = {
            "therefore": "so",
            "however": "but",
            "additionally": "also",
            "subsequently": "then",
            "consequently": "so"
        }
        
        for complex_word, simple_word in simplifications.items():
            text = re.sub(rf'\b{complex_word}\b', simple_word, text, flags=re.IGNORECASE)
        
        # Make sentences shorter
        sentences = text.split('.')
        simple_sentences = [s.strip() for s in sentences if len(s.strip()) < 50]
        
        return '. '.join(simple_sentences) + '.'


# Compliance settings
COMPLIANCE_SETTINGS = {
    "gdpr_enabled": True,
    "hipaa_mode": False,
    "data_retention_days": 30,
    "encryption_required": True,
    "audit_logging": True,
    "consent_required": True
}
