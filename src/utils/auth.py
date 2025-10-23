import hashlib
import time
from datetime import datetime, timedelta

class AuthManager:
    """Authentication manager for user login/logout"""
    
    def __init__(self):
        # Default credentials (in production, use proper database/config)
        self.users = {
            "admin": self._hash_password("admin123"),
            "operator": self._hash_password("operator123"),
            "guest": self._hash_password("guest123")
        }
        
        self.current_user = None
        self.login_time = None
        self.session_timeout = 3600  # 1 hour
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Authenticate user with username and password - Development mode allows any credentials"""
        # For development: accept any non-empty credentials
        if username.strip() and password.strip():
            self.current_user = username
            self.login_time = time.time()
            print(f"Development mode: Login successful for {username}")
            return True
        
        return False
    
    def is_authenticated(self):
        """Check if user is currently authenticated"""
        if not self.current_user or not self.login_time:
            return False
        
        # Check session timeout
        if time.time() - self.login_time > self.session_timeout:
            self.logout()
            return False
        
        return True
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.login_time = None
    
    def get_current_user(self):
        """Get current authenticated user"""
        if self.is_authenticated():
            return self.current_user
        return None
    
    def extend_session(self):
        """Extend current session"""
        if self.is_authenticated():
            self.login_time = time.time()
    
    def get_session_remaining(self):
        """Get remaining session time in seconds"""
        if not self.is_authenticated():
            return 0
        
        elapsed = time.time() - self.login_time
        remaining = self.session_timeout - elapsed
        return max(0, remaining)
    
    def add_user(self, username, password):
        """Add a new user (admin function)"""
        if self.current_user == "admin":
            self.users[username] = self._hash_password(password)
            return True
        return False
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        if self.authenticate(username, old_password):
            self.users[username] = self._hash_password(new_password)
            return True
        return False