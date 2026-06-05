#!/usr/bin/env python3
"""
Scheduler - Handles scheduled tasks for AppsFlyer events
"""

import json
from pathlib import Path
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Dict, List, Optional, Callable

class TaskScheduler:
    def __init__(self, tasks_file: str = "data/scheduled_tasks.json"):
        self.tasks_file = Path(tasks_file)
        self.tasks_file.parent.mkdir(exist_ok=True)
        self.scheduler = BackgroundScheduler()
        self.tasks = self._load_tasks()
        self.callbacks = {}

    def _load_tasks(self) -> Dict:
        """Load tasks from file"""
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_tasks(self):
        """Save tasks to file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def start(self):
        """Start scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()

    def stop(self):
        """Stop scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()

    def add_task(self, task_id: str, user_id: str, event_type: str, 
                 event_data: Dict, repeat: str, time: str) -> Dict:
        """Add new scheduled task"""
        task = {
            "task_id": task_id,
            "user_id": user_id,
            "event_type": event_type,
            "event_data": event_data,
            "repeat": repeat,  # once, daily, hourly
            "time": time,  # HH:MM format
            "created_at": str(datetime.now()),
            "active": True
        }
        
        self.tasks[task_id] = task
        self._save_tasks()
        return task

    def get_user_tasks(self, user_id: str) -> List[Dict]:
        """Get all tasks for user"""
        return [task for task in self.tasks.values() if task["user_id"] == user_id]

    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get task by ID"""
        return self.tasks.get(task_id)

    def delete_task(self, task_id: str) -> bool:
        """Delete task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._save_tasks()
            # Cancel scheduled job if exists
            try:
                self.scheduler.remove_job(task_id)
            except:
                pass
            return True
        return False

    def toggle_task(self, task_id: str) -> bool:
        """Toggle task active status"""
        if task_id in self.tasks:
            self.tasks[task_id]["active"] = not self.tasks[task_id]["active"]
            self._save_tasks()
            return True
        return False

    def schedule_job(self, task_id: str, callback: Callable):
        """Schedule a job with APScheduler"""
        task = self.get_task(task_id)
        if not task or not task["active"]:
            return False

        try:
            repeat = task["repeat"]
            time_str = task["time"]
            
            if repeat == "once":
                # Schedule for specific time today or tomorrow
                hour, minute = map(int, time_str.split(":"))
                trigger = CronTrigger(hour=hour, minute=minute)
            elif repeat == "daily":
                hour, minute = map(int, time_str.split(":"))
                trigger = CronTrigger(hour=hour, minute=minute)
            elif repeat == "hourly":
                minute = int(time_str.split(":")[1]) if ":" in time_str else 0
                trigger = CronTrigger(minute=minute)
            else:
                return False

            self.scheduler.add_job(
                callback,
                trigger=trigger,
                id=task_id,
                replace_existing=True,
                args=[task_id]
            )
            return True
        except Exception as e:
            print(f"Error scheduling job {task_id}: {e}")
            return False

    def get_all_tasks(self) -> Dict:
        """Get all tasks"""
        return self.tasks
