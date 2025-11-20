"""
Unit tests for ai_service.py
Tests AI service operations with mocked OpenAI API calls
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from ai_service import AIService

class TestAIService:
    """Test AI service operations"""
    
    @pytest.fixture
    def ai_service(self):
        """Create AIService instance with test API key"""
        return AIService("test-api-key")
    
    def test_init(self, ai_service):
        """Test AIService initialization"""
        assert ai_service is not None
        assert ai_service.model == "gpt-4o"
    
    @patch('ai_service.openai.OpenAI')
    def test_get_feedback_response(self, mock_openai_class, ai_service, sample_messages):
        """Test getting feedback response from AI"""
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"score": 7.5, "feedback": "Good prompt with specific details."}'
        
        mock_client.chat.completions.create.return_value = mock_response
        
        # Create new service instance to use mocked client
        service = AIService("test-key")
        service.client = mock_client
        
        # Test
        quality_score, feedback, current_score = service.get_feedback_response(sample_messages, [])
        
        assert quality_score == 7.5
        assert current_score == 7.5
        assert "Good prompt" in feedback
        assert mock_client.chat.completions.create.called
    
    @patch('ai_service.openai.OpenAI')
    def test_get_feedback_response_with_previous_scores(self, mock_openai_class, ai_service, sample_messages):
        """Test feedback response with previous scores"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"score": 8.0, "feedback": "Excellent prompt."}'
        
        mock_client.chat.completions.create.return_value = mock_response
        
        service = AIService("test-key")
        service.client = mock_client
        
        # Test with previous scores
        previous_scores = [6.0, 7.0]
        quality_score, feedback, current_score = service.get_feedback_response(sample_messages, previous_scores)
        
        assert current_score == 8.0
        assert quality_score == 8.0  # Should use current score
        assert "Excellent" in feedback
    
    @patch('ai_service.openai.OpenAI')
    def test_get_chat_response_low_quality(self, mock_openai_class, ai_service, sample_messages):
        """Test chat response for low quality score (terse response)"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "I need more information."
        
        mock_client.chat.completions.create.return_value = mock_response
        
        service = AIService("test-key")
        service.client = mock_client
        
        # Test with low quality score
        response = service.get_chat_response(sample_messages, quality_score=2.0)
        
        assert response == "I need more information."
        # Verify max_tokens was set to 100 for low quality
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]['max_tokens'] == 100
    
    @patch('ai_service.openai.OpenAI')
    def test_get_chat_response_high_quality(self, mock_openai_class, ai_service, sample_messages):
        """Test chat response for high quality score (normal response)"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "This is a detailed response."
        
        mock_client.chat.completions.create.return_value = mock_response
        
        service = AIService("test-key")
        service.client = mock_client
        
        # Test with high quality score
        response = service.get_chat_response(sample_messages, quality_score=8.0)
        
        assert response == "This is a detailed response."
        # Verify max_tokens was set to 1000 for high quality
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]['max_tokens'] == 1000
    
    @patch('ai_service.openai.OpenAI')
    def test_get_feedback_response_json_parsing_error(self, mock_openai_class, ai_service, sample_messages):
        """Test handling of JSON parsing errors in feedback response"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "Invalid JSON response"
        
        mock_client.chat.completions.create.return_value = mock_response
        
        service = AIService("test-key")
        service.client = mock_client
        
        # Should handle JSON error gracefully
        quality_score, feedback, current_score = service.get_feedback_response(sample_messages, [])
        
        assert quality_score == 5.0  # Default fallback
        assert current_score == 5.0

