"""
Unit tests for database.py
Tests database operations: create_user, create_conversation, get_conversation, update_conversation
"""
import pytest
import json
from database import Database

class TestDatabase:
    """Test database operations"""
    
    def test_create_user(self, test_db, sample_user_email):
        """Test creating a new user"""
        result = test_db.create_user(sample_user_email)
        assert result is True
        
        # Verify user exists
        user = test_db.get_user_by_email(sample_user_email)
        assert user is not None
        assert user['email'] == sample_user_email
    
    def test_create_user_duplicate(self, test_db, sample_user_email):
        """Test creating duplicate user (should be idempotent)"""
        test_db.create_user(sample_user_email)
        result = test_db.create_user(sample_user_email)  # Try again
        assert result is True  # Should succeed (idempotent)
    
    def test_get_user_by_email_not_found(self, test_db):
        """Test getting non-existent user"""
        user = test_db.get_user_by_email("nonexistent@example.com")
        assert user is None
    
    def test_create_conversation(self, test_db, sample_user_email, sample_conversation_id):
        """Test creating a new conversation"""
        # Create user first
        test_db.create_user(sample_user_email)
        
        # Create conversation
        result = test_db.create_conversation(sample_user_email, sample_conversation_id)
        assert result is True
        
        # Verify conversation exists
        conversation = test_db.get_conversation(sample_conversation_id)
        assert conversation is not None
        assert conversation['conversation_id'] == sample_conversation_id
        assert conversation['user_email'] == sample_user_email
    
    def test_get_conversation_not_found(self, test_db):
        """Test getting non-existent conversation"""
        conversation = test_db.get_conversation("nonexistent-id")
        assert conversation is None
    
    def test_update_conversation(self, test_db, sample_user_email, sample_conversation_id, sample_messages):
        """Test updating conversation with messages and scores"""
        # Setup: create user and conversation
        test_db.create_user(sample_user_email)
        test_db.create_conversation(sample_user_email, sample_conversation_id)
        
        # Update conversation
        quality_score = 7.5
        message_scores = [7.5]
        feedback = "Good prompt!"
        
        test_db.update_conversation(
            sample_conversation_id,
            sample_messages,
            quality_score,
            message_scores,
            feedback
        )
        
        # Verify update
        conversation = test_db.get_conversation(sample_conversation_id)
        assert conversation is not None
        assert conversation['quality_score'] == quality_score
        assert conversation['feedback'] == feedback
        # message_scores is already parsed from JSON, so use it directly
        assert len(conversation['message_scores']) == 1
    
    def test_get_user_conversations(self, test_db, sample_user_email):
        """Test getting all conversations for a user"""
        # Create user and conversations
        test_db.create_user(sample_user_email)
        test_db.create_conversation(sample_user_email, "conv-1")
        test_db.create_conversation(sample_user_email, "conv-2")
        
        # Get conversations
        conv_ids = test_db.get_user_conversations(sample_user_email)
        assert len(conv_ids) == 2
        assert "conv-1" in conv_ids
        assert "conv-2" in conv_ids
    
    def test_get_conversation_summary(self, test_db, sample_user_email, sample_conversation_id):
        """Test getting conversation summary"""
        # Setup
        test_db.create_user(sample_user_email)
        test_db.create_conversation(sample_user_email, sample_conversation_id)
        
        # Get summary
        summary = test_db.get_conversation_summary(sample_conversation_id)
        assert summary is not None
        assert 'conversation_id' in summary
        assert 'updated_at' in summary

