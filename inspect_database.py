#!/usr/bin/env python3

import sqlite3
import json
from datetime import datetime

def inspect_database(db_path="backend/promptly.db"):
    """Inspect the contents of the database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=" * 60)
        print("DATABASE INSPECTION")
        print("=" * 60)
        
        # Check if database exists and has tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables found: {[table[0] for table in tables]}")
        print()
        
        # Inspect users table
        print("USERS TABLE:")
        print("-" * 30)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        if users:
            for user in users:
                print(f"User ID: {user[0]}")
                print(f"Conversation IDs: {user[1]}")
                print(f"Created: {user[2]}")
                print()
        else:
            print("No users found")
        print()
        
        # Inspect conversations table
        print("CONVERSATIONS TABLE:")
        print("-" * 30)
        cursor.execute("SELECT * FROM conversations")
        conversations = cursor.fetchall()
        if conversations:
            for conv in conversations:
                print(f"Conversation ID: {conv[0]}")
                print(f"User ID: {conv[1]}")
                print(f"Quality Score: {conv[3]}")
                print(f"Created: {conv[4]}")
                print(f"Updated: {conv[5]}")
                
                # Parse and display messages
                try:
                    messages = json.loads(conv[2])
                    print(f"Messages ({len(messages)}):")
                    for i, msg in enumerate(messages):
                        role = msg.get('role', 'unknown')
                        content = msg.get('content', '')
                        timestamp = msg.get('timestamp', 'no timestamp')
                        print(f"  {i+1}. [{role}] {content[:100]}{'...' if len(content) > 100 else ''}")
                        print(f"      Time: {timestamp}")
                except json.JSONDecodeError:
                    print(f"Messages (raw): {conv[2]}")
                print("-" * 30)
        else:
            print("No conversations found")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"Database file not found: {db_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_database()
