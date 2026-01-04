#!/usr/bin/env python3
"""
Utility script to fix corrupted conversations in the database.

This script helps recover from situations where:
- AI response generation was interrupted (e.g., page refresh)
- Conversations are in an incomplete state
- Messages are malformed or corrupted
"""

import sys
import os
import json
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from database import Database

def check_conversations(db):
    """Check all conversations for issues"""
    print("Checking conversations for issues...\n")
    
    conn = None
    try:
        conn = db._get_connection()
        cursor = conn.cursor()
        
        # Get all conversations
        if db.use_postgres:
            cursor.execute("SELECT conversation_id, user_email, messages FROM conversations")
        else:
            cursor.execute("SELECT conversation_id, user_email, messages FROM conversations")
        
        conversations = cursor.fetchall()
        issues_found = []
        
        for row in conversations:
            conversation_id = row[0]
            user_email = row[1]
            messages_json = row[2]
            
            try:
                if messages_json:
                    messages = json.loads(messages_json)
                else:
                    messages = []
                
                # Check for various issues
                issues = []
                
                # Issue 1: Last message is a user message (AI response incomplete)
                if messages and len(messages) > 0:
                    last_message = messages[-1]
                    if last_message.get('role') == 'user':
                        issues.append("Last message is from user (AI response may be incomplete)")
                
                # Issue 2: Messages is not a list
                if not isinstance(messages, list):
                    issues.append(f"Messages is not a list (type: {type(messages)})")
                
                # Issue 3: Messages with missing required fields
                for i, msg in enumerate(messages):
                    if not isinstance(msg, dict):
                        issues.append(f"Message {i} is not a dictionary")
                    elif 'role' not in msg:
                        issues.append(f"Message {i} missing 'role' field")
                    elif 'content' not in msg:
                        issues.append(f"Message {i} missing 'content' field")
                
                # Issue 4: Malformed JSON
                if not messages_json:
                    issues.append("Messages JSON is empty")
                
                if issues:
                    issues_found.append({
                        'conversation_id': conversation_id,
                        'user_email': user_email,
                        'issues': issues,
                        'message_count': len(messages) if isinstance(messages, list) else 0
                    })
            
            except json.JSONDecodeError as e:
                issues_found.append({
                    'conversation_id': conversation_id,
                    'user_email': user_email,
                    'issues': [f"JSON decode error: {str(e)}"],
                    'message_count': 0
                })
            except Exception as e:
                issues_found.append({
                    'conversation_id': conversation_id,
                    'user_email': user_email,
                    'issues': [f"Unexpected error: {str(e)}"],
                    'message_count': 0
                })
        
        return issues_found
        
    except Exception as e:
        print(f"Error checking conversations: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if conn:
            db._close_connection(conn)

def fix_conversation(db, conversation_id, fix_type='remove_last_user'):
    """Fix a specific conversation"""
    print(f"Fixing conversation {conversation_id}...")
    
    conn = None
    try:
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            print(f"  ERROR: Conversation {conversation_id} not found")
            return False
        
        messages = conversation.get('messages', [])
        if not isinstance(messages, list):
            print(f"  ERROR: Messages is not a list")
            return False
        
        fixed = False
        
        if fix_type == 'remove_last_user':
            # Remove the last user message if it's a user message (AI response was interrupted)
            if messages and len(messages) > 0:
                last_message = messages[-1]
                if last_message.get('role') == 'user':
                    messages = messages[:-1]
                    fixed = True
                    print(f"  Removed last user message (AI response was incomplete)")
        
        elif fix_type == 'clean_messages':
            # Clean messages by ensuring they're valid
            cleaned_messages = []
            for msg in messages:
                if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                    # Ensure content is a string
                    if not isinstance(msg.get('content'), str):
                        msg['content'] = str(msg.get('content', ''))
                    cleaned_messages.append(msg)
            if len(cleaned_messages) != len(messages):
                messages = cleaned_messages
                fixed = True
                print(f"  Cleaned {len(messages) - len(cleaned_messages)} invalid messages")
        
        if fixed:
            # Update conversation with fixed messages
            db.update_conversation(
                conversation_id,
                messages,
                conversation.get('quality_score', 5.0),
                conversation.get('message_scores', []),
                conversation.get('feedback')
            )
            print(f"  Successfully fixed conversation")
            return True
        else:
            print(f"  No fixes needed")
            return False
        
    except Exception as e:
        print(f"  ERROR: Failed to fix conversation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("Fix Corrupted Conversations Utility")
    print("=" * 60)
    print()
    
    # Initialize database
    db = Database()
    
    # Check for issues
    issues = check_conversations(db)
    
    if not issues:
        print("✓ No issues found! All conversations are healthy.")
        return
    
    print(f"Found {len(issues)} conversation(s) with issues:\n")
    
    for issue in issues:
        print(f"Conversation: {issue['conversation_id']}")
        print(f"  User: {issue['user_email']}")
        print(f"  Messages: {issue['message_count']}")
        print(f"  Issues:")
        for i, problem in enumerate(issue['issues'], 1):
            print(f"    {i}. {problem}")
        print()
    
    # Ask user what to do
    print("\n" + "=" * 60)
    print("Options:")
    print("  1. Fix all conversations (remove incomplete AI responses)")
    print("  2. Fix specific conversation")
    print("  3. Just show issues (no fixes)")
    print("  4. Exit")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == '1':
        # Fix all conversations
        print("\nFixing all conversations...")
        fixed_count = 0
        for issue in issues:
            if fix_conversation(db, issue['conversation_id'], 'remove_last_user'):
                fixed_count += 1
        print(f"\n✓ Fixed {fixed_count} conversation(s)")
    
    elif choice == '2':
        # Fix specific conversation
        conv_id = input("Enter conversation ID: ").strip()
        if conv_id:
            fix_conversation(db, conv_id, 'remove_last_user')
    
    elif choice == '3':
        print("\nNo fixes applied. Exiting.")
    
    else:
        print("\nExiting.")

if __name__ == '__main__':
    main()

