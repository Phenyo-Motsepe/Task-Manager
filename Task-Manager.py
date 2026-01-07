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

# ========================================================================
    # STAGE 2: Persistence
    # ========================================================================
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            data = {
                "next_id": self.next_id,
                "tasks": [task.to_dict() for task in self.tasks]
            }
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.next_id = data.get("next_id", 1)
                    self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
                print(f"✅ Loaded {len(self.tasks)} tasks from {self.filename}")
            else:
                self.tasks = []
                self.next_id = 1
        except json.JSONDecodeError:
            print("⚠️  Error reading tasks file. Starting fresh.")
            self.tasks = []
            self.next_id = 1
        except Exception as e:
            print(f"⚠️  Error loading tasks: {e}")
            self.tasks = []
            self.next_id = 1
    
    def export_report(self, filename: str = "task_report.txt"):
        """Export a text report of all tasks"""
        try:
            with open(filename, "w") as f:
                f.write("TASK MANAGER REPORT\n")
                f.write("="*60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                stats = self.get_statistics()
                f.write(f"Total Tasks: {stats['total']}\n")
                f.write(f"Completed: {stats['completed']}\n")
                f.write(f"Pending: {stats['pending']}\n")
                f.write(f"Completion Rate: {stats['completion_rate']:.1f}%\n\n")
                
                f.write("\nALL TASKS\n")
                f.write("-"*60 + "\n")
                for task in self.tasks:
                    status = "DONE" if task.completed else "TODO"
                    f.write(f"[{status}] {task.title}\n")
                    f.write(f"  Created: {task.created_at}\n")
                    if task.completed_at:
                        f.write(f"  Completed: {task.completed_at}\n")
                    f.write("\n")
            
            print(f"📄 Report exported to {filename}")
        except Exception as e:
            print(f"⚠️  Error exporting report: {e}")
    
    # ========================================================================
    # STAGE 4: Statistics & Analytics
    # ========================================================================
    
    def get_statistics(self) -> Dict:
        """Calculate task statistics"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        # Tasks completed today
        today = datetime.now().date()
        completed_today = sum(
            1 for t in self.tasks 
            if t.completed_at and 
            datetime.fromisoformat(t.completed_at).date() == today
        )
        
        # Tasks completed this week
        week_ago = datetime.now() - timedelta(days=7)
        completed_this_week = sum(
            1 for t in self.tasks 
            if t.completed_at and 
            datetime.fromisoformat(t.completed_at) > week_ago
        )
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": completion_rate,
            "completed_today": completed_today,
            "completed_this_week": completed_this_week
        }
    
    def show_statistics(self):
        """Display detailed statistics"""
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("📊 TASK STATISTICS")
        print("="*60)
        print(f"📝 Total Tasks: {stats['total']}")
        print(f"✅ Completed: {stats['completed']}")
        print(f"⬜ Pending: {stats['pending']}")
        print(f"📈 Completion Rate: {stats['completion_rate']:.1f}%")
        print(f"🎯 Completed Today: {stats['completed_today']}")
        print(f"📅 Completed This Week: {stats['completed_this_week']}")
        print("="*60)
    
    def analyze_with_pandas(self):
        """Analyze tasks using pandas (requires pandas installed)"""
        try:
            if not self.tasks:
                print("📭 No tasks to analyze.")
                return
            
            # Convert to DataFrame
            df = pd.DataFrame([task.to_dict() for task in self.tasks])
            
            print("\n" + "="*60)
            print("📊 PANDAS ANALYSIS")
            print("="*60)
            
            # Basic statistics
            print(f"\n✅ Completion Rate: {df['completed'].mean()*100:.1f}%")
            
            # Group by completion status
            print("\n📈 Task Distribution:")
            print(df['completed'].value_counts())
            
            # Convert dates and analyze
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['day_of_week'] = df['created_at'].dt.day_name()
            
            print("\n📅 Tasks Created by Day of Week:")
            print(df['day_of_week'].value_counts().sort_index())
            
            print("="*60)
            
        except ImportError:
            print("⚠️  pandas not installed. Install with: pip install pandas")
        except Exception as e:
            print(f"⚠️  Error during analysis: {e}")
