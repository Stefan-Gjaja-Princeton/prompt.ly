import sqlite3
import json
import os

# Check if database exists
db_path = "backend/promptly.db"
if not os.path.exists(db_path):
    print("❌ Database file does not exist!")
    print(f"Looking for: {os.path.abspath(db_path)}")
    exit(1)

print("✅ Database file exists")
print(f"Location: {os.path.abspath(db_path)}")
print(f"Size: {os.path.getsize(db_path)} bytes")
print()

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables: {[t[0] for t in tables]}")
    
    # Check users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"Users: {user_count}")
    
    # Check conversations
    cursor.execute("SELECT COUNT(*) FROM conversations")
    conv_count = cursor.fetchone()[0]
    print(f"Conversations: {conv_count}")
    
    if conv_count > 0:
        print("\nRecent conversations:")
        cursor.execute("SELECT conversation_id, user_id, current_quality_score, updated_at FROM conversations ORDER BY updated_at DESC LIMIT 5")
        for row in cursor.fetchall():
            print(f"  {row[0][:8]}... | User: {row[1]} | Score: {row[2]} | Updated: {row[3]}")
    
    conn.close()
    
except Exception as e:
    print(f"Error reading database: {e}")
