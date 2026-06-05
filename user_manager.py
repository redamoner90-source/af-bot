#!/usr/bin/env python3
"""
User Manager - Manages user data and settings
"""

import json
from pathlib import Path
from typing import Dict, Optional, List

class UserManager:
    def __init__(self, users_file: str = "data/users.json"):
        self.users_file = Path(users_file)
        self.users_file.parent.mkdir(exist_ok=True)
        self.users = self._load_users()

    def _load_users(self) -> Dict:
        """Load users from file"""
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def add_user(self, user_id: str, username: str = "") -> Dict:
        """Add new user or return existing"""
        if user_id not in self.users:
            self.users[user_id] = {
                "user_id": user_id,
                "username": username,
                "devices": [],
                "created_at": str(__import__('datetime').datetime.now())
            }
            self._save_users()
        return self.users[user_id]

    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return self.users.get(user_id)

    def add_device(self, user_id: str, gaid: str, af_uid: str, app_id: str) -> Dict:
        """Add device to user"""
        if user_id not in self.users:
            self.add_user(user_id)
        
        device = {
            "gaid": gaid,
            "af_uid": af_uid,
            "app_id": app_id,
            "added_at": str(__import__('datetime').datetime.now())
        }
        
        self.users[user_id]["devices"].append(device)
        self._save_users()
        return device

    def get_devices(self, user_id: str) -> List[Dict]:
        """Get all devices for user"""
        user = self.get_user(user_id)
        return user.get("devices", []) if user else []

    def update_device(self, user_id: str, device_index: int, gaid: str = None, af_uid: str = None):
        """Update device info"""
        user = self.get_user(user_id)
        if user and device_index < len(user["devices"]):
            if gaid:
                user["devices"][device_index]["gaid"] = gaid
            if af_uid:
                user["devices"][device_index]["af_uid"] = af_uid
            self._save_users()
            return True
        return False

    def delete_device(self, user_id: str, device_index: int) -> bool:
        """Delete device"""
        user = self.get_user(user_id)
        if user and device_index < len(user["devices"]):
            user["devices"].pop(device_index)
            self._save_users()
            return True
        return False

    def user_exists(self, user_id: str) -> bool:
        """Check if user exists"""
        return user_id in self.users

    def get_all_users(self) -> Dict:
        """Get all users"""
        return self.users
