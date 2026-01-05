#!/usr/bin/env python3
"""Advanced Task Manager - A complete CLI task tracking applicationFeatures: CRUD operations, persistence, statistics, OOP design"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd 

# ============================================================================
# STAGE 3: OOP - Task Class
# ============================================================================

class Task:
    """Represents a single task with metadata"""
    
    def __init__(self, title: str, task_id: Optional[int] = None, 
                 completed: bool = False, created_at: Optional[str] = None,
                 completed_at: Optional[str] = None):
        self.id = task_id
        self.title = title
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at
    
    def complete(self):
        """Mark task as completed"""
        self.completed = True
        self.completed_at = datetime.now().isoformat()
    
    def uncomplete(self):
        """Mark task as incomplete"""
        self.completed = False
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary"""
        return cls(
            title=data["title"],
            task_id=data.get("id"),
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at")
        )
    
    def __repr__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title}"


