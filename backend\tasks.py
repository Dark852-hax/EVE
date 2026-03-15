"""
EVE Task Primitives Module
Reusable building blocks for common tasks
"""

import json
import csv
import io
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

class TaskType(Enum):
    DOCUMENT_DRAFT = "document_draft"
    SUMMARIZE = "summarize"
    DATA_IMPORT = "data_import"
    DATA_EXPORT = "data_export"
    CODE_SCAFFOLD = "code_scaffold"
    CODE_DEBUG = "code_debug"
    SCHEDULE = "schedule"
    REMINDER = "reminder"
    API_ORCHESTRATE = "api_orchestrate"

@dataclass
class TaskResult:
    """Result of a task execution"""
    success: bool
    output: Any
    error: Optional[str]
    metadata: Dict[str, Any]

class TaskPrimitives:
    """Collection of reusable task primitives"""
    
    def __init__(self):
        self.scheduled_tasks: List[Dict] = []
        self.reminders: List[Dict] = []
    
    # ==================== DOCUMENT DRAFTING ====================
    
    def draft_document(
        self,
        doc_type: str,
        content: str,
        template: str = None
    ) -> TaskResult:
        """Draft a document from template or scratch"""
        templates = {
            "report": self._report_template,
            "contract": self._contract_template,
            "email": self._email_template,
            "letter": self._letter_template,
            "memo": self._memo_template,
        }
        
        template_func = templates.get(doc_type, self._default_template)
        
        try:
            result = template_func(content)
            return TaskResult(
                success=True,
                output=result,
                error=None,
                metadata={"type": doc_type, "timestamp": str(datetime.now())}
            )
        except Exception as e:
            return TaskResult(success=False, output=None, error=str(e), metadata={})
    
    def _report_template(self, content: str) -> str:
        return f"""
REPORT
======
Date: {datetime.now().strftime('%Y-%m-%d')}

SUMMARY
-------
{content}

END OF REPORT
"""
    
    def _contract_template(self, content: str) -> str:
        return f"""
CONTRACT
========
Date: {datetime.now().strftime('%Y-%m-%d')}

TERMS AND CONDITIONS
--------------------
{content}

SIGNATURES
----------

_____________________     _____________________
Party A                 Party B

Date: __________        Date: __________
"""
    
    def _email_template(self, content: str) -> str:
        return f"""
Subject: 

Dear ,

{content}

Best regards,
"""
    
    def _letter_template(self, content: str) -> str:
        return f"""
[Your Name]
[Your Address]
[Date]

Dear [Recipient],

{content}

Sincerely,
[Your Signature]
[Your Name]
"""
    
    def _memo_template(self, content: str) -> str:
        return f"""
MEMORANDUM
TO: 
FROM: 
DATE: {datetime.now().strftime('%Y-%m-%d')}
RE: 

{content}
"""
    
    def _default_template(self, content: str) -> str:
        return content
    
    # ==================== SUMMARIZATION ====================
    
    def summarize(
        self,
        text: str,
        max_length: int = 200,
        style: str = "bullet"
    ) -> TaskResult:
        """Summarize text content"""
        try:
            # Simple extractive summarization
            sentences = text.split('.')
            summary = sentences[:3]  # Take first 3 sentences
            
            if style == "bullet":
                output = "• " + "\n• ".join([s.strip() for s in summary if s.strip()])
            else:
                output = " ".join(summary)
            
            return TaskResult(
                success=True,
                output=output,
                error=None,
                metadata={"original_length": len(text), "summary_length": len(output)}
            )
        except Exception as e:
            return TaskResult(success=False, output=None, error=str(e), metadata={})
    
    # ==================== DATA IMPORT/EXPORT ====================
    
    def import_csv(self, csv_data: str) -> TaskResult:
        """Import data from CSV"""
        try:
            reader = csv.DictReader(io.StringIO(csv_data))
            data = list(reader)
            return TaskResult(
                success=True,
                output=data,
                error=None,
                metadata={"rows": len(data)}
            )
        except Exception as e:
            return TaskResult(success=False, output=None, error=str(e), metadata={})
    
    def export_csv(self, data: List[Dict], columns: List[str] = None) -> TaskResult:
        """Export data to CSV"""
        try:
            if not data:
                return TaskResult(success=False, output=None, error="No data to export", metadata={})
            
            if columns is None:
                columns = list(data[0].keys())
            
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
            
            return TaskResult(
                success=True,
                output=output.getvalue(),
                error=None,
                metadata={"rows": len(data), "columns": len(columns)}
            )
        except Exception as e:
            return TaskResult(success=False, output=None, error=str(e), metadata={})
    
    def import_excel(self, excel_data: bytes) -> TaskResult:
        """Import data from Excel"""
        # Placeholder - would need openpyxl
        return TaskResult(
            success=False,
            output=None,
            error="Excel import not implemented",
            metadata={}
        )
    
    def export_excel(self, data: List[Dict]) -> TaskResult:
        """Export data to Excel"""
        # Placeholder - would need openpyxl
        return TaskResult(
            success=False,
            output=None,
            error="Excel export not implemented",
            metadata={}
        )
    
    # ==================== CODE SCAFFOLDING ====================
    
    def scaffold_code(
        self,
        language: str,
        project_type: str,
        features: List[str]
    ) -> TaskResult:
        """Generate code scaffold"""
        scaffolds = {
            ("python", "web"): self._python_web_scaffold,
            ("python", "api"): self._python_api_scaffold,
            ("python", "cli"): self._python_cli_scaffold,
            ("javascript", "web"): self._js_web_scaffold,
            ("javascript", "api"): self._js_api_scaffold,
        }
        
        key = (language.lower(), project_type.lower())
        scaffold_func = scaffolds.get(key, self._generic_scaffold)
        
        try:
            code = scaffold_func(features)
            return TaskResult(
                success=True,
                output=code,
                error=None,
                metadata={"language": language, "type": project_type}
            )
        except Exception as e:
            return TaskResult(success=False, output=None, error=str(e), metadata={})
    
    def _python_web_scaffold(self, features: List[str]) -> str:
        return '''"""Web Application"""
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

# Add your routes here

if __name__ == '__main__':
    app.run(debug=True)
'''
    
    def _python_api_scaffold(self, features: List[str]) -> str:
        return '''"""REST API"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="My API")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

items = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/items")
def get_items():
    return items

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
'''
    
    def _python_cli_scaffold(self, features: List[str]) -> str:
        return '''"""CLI Application"""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='My CLI App')
    parser.add_argument('command', choices=['run', 'help'])
    parser.add_argument('--verbose', '-v', action='store_true')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        print("Running...")
    elif args.command == 'help':
        parser.print_help()

if __name__ == '__main__':
    main()
'''
    
    def _js_web_scaffold(self, features: List[str]) -> str:
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Web App</title>
</head>
<body>
    <h1>Hello World</h1>
    <script src="app.js"></script>
</body>
</html>
'''
    
    def _js_api_scaffold(self, features: List[str]) -> str:
        return '''const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

app.get('/', (req, res) => {
    res.json({ message: 'API Running' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
'''
    
    def _generic_scaffold(self, features: List[str]) -> str:
        return "# Add your code here\n"
    
    # ==================== CODE DEBUGGING ====================
    
    def debug_code(
        self,
        code: str,
        language: str,
        error: str = None
    ) -> TaskResult:
        """Analyze and suggest fixes for code"""
        try:
            suggestions = []
            
            # Basic static analysis
            if "python" in language.lower():
                suggestions.extend(self._python_analysis(code, error))
            elif "javascript" in language.lower():
                suggestions.extend(self._js_analysis(code, error))
            
            return TaskResult(
                success=True,
                output={
                    "suggestions": suggestions,
                    "analyzed": True
                },
                error=None,
                metadata={"language": language}
            )
        except Exception as e:
            return TaskResult(success=False, output=None, error=str(e), metadata={})
    
    def _python_analysis(self, code: str, error: str) -> List[str]:
        suggestions = []
        if "indentation" in code.lower():
            suggestions.append("Check indentation - Python uses whitespace")
        if "undefined" in code.lower():
            suggestions.append("Variable may be undefined - check spelling")
        if error:
            suggestions.append(f"Error detected: {error}")
        return suggestions
    
    def _js_analysis(self, code: str, error: str) -> List[str]:
        suggestions = []
        if "const" not in code and "let" not in code:
            suggestions.append("Consider using 'const' or 'let' instead of 'var'")
        if "==" in code:
            suggestions.append("Use '===' for strict equality")
        return suggestions
    
    # ==================== SCHEDULING ====================
    
    def schedule_task(
        self,
        task_name: str,
        description: str,
        scheduled_time: datetime,
        recurrence: str = None
    ) -> TaskResult:
        """Schedule a task"""
        task = {
            "id": len(self.scheduled_tasks) + 1,
            "name": task_name,
            "description": description,
            "scheduled_time": scheduled_time.isoformat(),
            "recurrence": recurrence,
            "status": "scheduled"
        }
        self.scheduled_tasks.append(task)
        
        return TaskResult(
            success=True,
            output=task,
            error=None,
            metadata={}
        )
    
    def get_scheduled_tasks(self) -> List[Dict]:
        """Get all scheduled tasks"""
        return self.scheduled_tasks
    
    # ==================== REMINDERS ====================
    
    def set_reminder(
        self,
        reminder_text: str,
        remind_at: datetime,
        repeat: str = None
    ) -> TaskResult:
        """Set a reminder"""
        reminder = {
            "id": len(self.reminders) + 1,
            "text": reminder_text,
            "remind_at": remind_at.isoformat(),
            "repeat": repeat,
            "active": True
        }
        self.reminders.append(reminder)
        
        return TaskResult(
            success=True,
            output=reminder,
            error=None,
            metadata={}
        )
    
    def get_reminders(self) -> List[Dict]:
        """Get all active reminders"""
        return [r for r in self.reminders if r.get("active", False)]
    
    def complete_reminder(self, reminder_id: int) -> TaskResult:
        """Mark reminder as complete"""
        for r in self.reminders:
            if r["id"] == reminder_id:
                r["active"] = False
                return TaskResult(success=True, output=r, error=None, metadata={})
        return TaskResult(success=False, output=None, error="Reminder not found", metadata={})
    
    # ==================== API ORCHESTRATION ====================
    
    async def orchestrate_apis(
        self,
        apis: List[Dict[str, Any]]
    ) -> TaskResult:
        """Orchestrate multiple API calls"""
        results = []
        
        for api in apis:
            result = {
                "api": api.get("name"),
                "status": "pending",
                "data": None
            }
            results.append(result)
        
        return TaskResult(
            success=True,
            output=results,
            error=None,
            metadata={"count": len(apis)}
        )


# Task primitive templates
TASK_TEMPLATES = {
    "document_types": ["report", "contract", "email", "letter", "memo"],
    "data_formats": ["csv", "excel", "json", "xml"],
    "code_languages": ["python", "javascript", "java", "go", "rust"],
    "schedule_types": ["once", "daily", "weekly", "monthly"],
    "reminder_repeats": ["none", "daily", "weekly", "monthly"]
}
