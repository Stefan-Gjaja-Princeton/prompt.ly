import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "promptly.db"):
        self.db_path = db_path
        self.clear_locks()
        self.init_database()
    
    def clear_locks(self):
        """Clear any existing database locks"""
        try:
            import os
            wal_file = f"{self.db_path}-wal"
            shm_file = f"{self.db_path}-shm"
            
            if os.path.exists(wal_file):
                os.remove(wal_file)
            if os.path.exists(shm_file):
                os.remove(shm_file)
        except Exception as e:
            print(f"Warning: Could not clear database locks: {e}")
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            
            # Create users table (email-based auth)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    google_id TEXT,
                    profile_picture_url TEXT,
                    conversation_ids TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id TEXT PRIMARY KEY,
                    user_email TEXT,
                    messages TEXT,
                    current_quality_score REAL DEFAULT NULL,
                    message_scores TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_email) REFERENCES users (email)
                )
            ''')
            
            conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
        finally:
            if conn:
                conn.close()
    
    def create_user(self, email: str, first_name: str = None, last_name: str = None, google_id: str = None, profile_picture_url: str = None) -> bool:
        """Create a new user (idempotent for existing users)"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO users (email, first_name, last_name, google_id, profile_picture_url, conversation_ids) VALUES (?, ?, ?, ?, ?, ?)",
                (email, first_name, last_name, google_id, profile_picture_url, json.dumps([]))
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Fetch a user record by email"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT email, first_name, last_name, google_id, profile_picture_url, created_at, last_login FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return {
                'email': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'google_id': row[3],
                'profile_picture_url': row[4],
                'created_at': row[5],
                'last_login': row[6],
            }
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def update_user_login(self, email: str) -> None:
        """Update last_login when a user signs in"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE email = ?", (email,))
            conn.commit()
        except Exception as e:
            print(f"Error updating user last_login: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_user_conversations(self, email: str) -> List[str]:
        """Get all conversation IDs for a user"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            cursor.execute("SELECT conversation_ids FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            
            if result:
                return json.loads(result[0])
            return []
        except Exception as e:
            print(f"Error getting user conversations: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def create_conversation(self, email: str, conversation_id: str) -> bool:
        """Create a new conversation"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")  # Enable WAL mode for better concurrency
            cursor = conn.cursor()
            
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Create conversation
            cursor.execute(
                "INSERT INTO conversations (conversation_id, user_email, messages) VALUES (?, ?, ?)",
                (conversation_id, email, json.dumps([]))
            )
            
            # Update user's conversation list
            conversations = self.get_user_conversations(email)
            conversations.append(conversation_id)
            cursor.execute(
                "UPDATE users SET conversation_ids = ? WHERE email = ?",
                (json.dumps(conversations), email)
            )
            
            # Commit transaction
            cursor.execute("COMMIT")
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error creating conversation: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get conversation data"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_email, messages, current_quality_score, message_scores FROM conversations WHERE conversation_id = ?",
                (conversation_id,)
            )
            result = cursor.fetchone()
            
            if result:
                message_scores = []
                if result[3]:
                    try:
                        message_scores = json.loads(result[3])
                    except json.JSONDecodeError:
                        message_scores = []
                
                return {
                    'user_email': result[0],
                    'messages': json.loads(result[1]),
                    'quality_score': result[2] if result[2] is not None else None,
                    'message_scores': message_scores
                }
            return None
        except Exception as e:
            print(f"Error getting conversation: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def update_conversation(self, conversation_id: str, messages: List[Dict], quality_score: float, message_scores: List[float] = None):
        """Update conversation with new messages and quality score"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            
            # Handle message scores
            scores_json = json.dumps(message_scores) if message_scores else None
            
            cursor.execute(
                "UPDATE conversations SET messages = ?, current_quality_score = ?, message_scores = ?, updated_at = CURRENT_TIMESTAMP WHERE conversation_id = ?",
                (json.dumps(messages), quality_score, scores_json, conversation_id)
            )
            conn.commit()
        except Exception as e:
            print(f"Error updating conversation: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_conversation_summary(self, conversation_id: str) -> Optional[Dict]:
        """Get conversation summary for the sidebar"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_email, messages, created_at, updated_at FROM conversations WHERE conversation_id = ?",
                (conversation_id,)
            )
            result = cursor.fetchone()
            
            if result:
                messages = json.loads(result[1])
                first_message = messages[0]['content'] if messages else "New conversation"
                return {
                    'conversation_id': conversation_id,
                    'user_email': result[0],
                    'title': first_message[:50] + "..." if len(first_message) > 50 else first_message,
                    'created_at': result[2],
                    'updated_at': result[3],
                    'message_count': len(messages)
                }
            return None
        except Exception as e:
            print(f"Error getting conversation summary: {e}")
            return None
        finally:
            if conn:
                conn.close()
