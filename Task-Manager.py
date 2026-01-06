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

# ============================================================================
# STAGE 1 & 2: Core Functions with Persistence
# ============================================================================

class TaskManager:
    """Main task manager with all operations"""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def add_task(self, title: str) -> Task:
        """Add a new task"""
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        
        task = Task(title=title.strip(), task_id=self.next_id)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task
    
    def show_tasks(self, filter_completed: Optional[bool] = None):
        """Display all tasks or filtered by completion status"""
        if not self.tasks:
            print("📭 No tasks found. Add some tasks to get started!")
            return
        
        filtered_tasks = self.tasks
        if filter_completed is not None:
            filtered_tasks = [t for t in self.tasks if t.completed == filter_completed]
        
        if not filtered_tasks:
            status = "completed" if filter_completed else "pending"
            print(f"📭 No {status} tasks found.")
            return
        
        print("\n" + "="*60)
        print("📋 YOUR TASKS")
        print("="*60)
        for task in filtered_tasks:
            status = "✅" if task.completed else "⬜"
            created = datetime.fromisoformat(task.created_at).strftime("%Y-%m-%d %H:%M")
            print(f"{task.id}. {status} {task.title}")
            print(f"   Created: {created}")
            if task.completed and task.completed_at:
                completed = datetime.fromisoformat(task.completed_at).strftime("%Y-%m-%d %H:%M")
                print(f"   Completed: {completed}")
            print("-" * 60)
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed"""
        task = self._find_task(task_id)
        if task:
            task.complete()
            self.save_tasks()
            print(f"✅ Task '{task.title}' marked as completed!")
            return True
        else:
            print(f"❌ Task with ID {task_id} not found.")
            return False
    
    def uncomplete_task(self, task_id: int) -> bool:
        """Mark a task as incomplete"""
        task = self._find_task(task_id)
        if task:
            task.uncomplete()
            self.save_tasks()
            print(f"⬜ Task '{task.title}' marked as incomplete!")
            return True
        else:
            print(f"❌ Task with ID {task_id} not found.")
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        task = self._find_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"🗑️  Task '{task.title}' deleted!")
            return True
        else:
            print(f"❌ Task with ID {task_id} not found.")
            return False
    
    def _find_task(self, task_id: int) -> Optional[Task]:
        """Find task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

