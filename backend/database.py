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
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    conversation_ids TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    messages TEXT,
                    current_quality_score REAL DEFAULT NULL,
                    message_scores TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
        finally:
            if conn:
                conn.close()
    
    def create_user(self, user_id: str) -> bool:
        """Create a new user"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (user_id, conversation_ids) VALUES (?, ?)",
                (user_id, json.dumps([]))
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
    
    def get_user_conversations(self, user_id: str) -> List[str]:
        """Get all conversation IDs for a user"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            cursor.execute("SELECT conversation_ids FROM users WHERE user_id = ?", (user_id,))
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
    
    def create_conversation(self, user_id: str, conversation_id: str) -> bool:
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
                "INSERT INTO conversations (conversation_id, user_id, messages) VALUES (?, ?, ?)",
                (conversation_id, user_id, json.dumps([]))
            )
            
            # Update user's conversation list
            conversations = self.get_user_conversations(user_id)
            conversations.append(conversation_id)
            cursor.execute(
                "UPDATE users SET conversation_ids = ? WHERE user_id = ?",
                (json.dumps(conversations), user_id)
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
                "SELECT user_id, messages, current_quality_score, message_scores FROM conversations WHERE conversation_id = ?",
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
                    'user_id': result[0],
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
                "SELECT user_id, messages, created_at, updated_at FROM conversations WHERE conversation_id = ?",
                (conversation_id,)
            )
            result = cursor.fetchone()
            
            if result:
                messages = json.loads(result[1])
                first_message = messages[0]['content'] if messages else "New conversation"
                return {
                    'conversation_id': conversation_id,
                    'user_id': result[0],
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
