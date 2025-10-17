from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from database import Database
from ai_service import AIService
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize services
db = Database()

# Check if API key is available
if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your-api-key-here":
    print("❌ ERROR: OpenAI API key not found!")
    print("Please set your API key in one of these ways:")
    print("1. Edit backend/api_key.py and replace 'your-api-key-here' with your actual key")
    print("2. Set environment variable: export OPENAI_API_KEY='your-key-here'")
    print("3. Create backend/.env file with: OPENAI_API_KEY=your-key-here")
    exit(1)

ai_service = AIService(Config.OPENAI_API_KEY)

# Default user ID for now (no login system yet)
DEFAULT_USER_ID = "default_user"

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations for the default user"""
    try:
        conversation_ids = db.get_user_conversations(DEFAULT_USER_ID)
        conversations = []
        
        for conv_id in conversation_ids:
            summary = db.get_conversation_summary(conv_id)
            if summary:
                conversations.append(summary)
        
        # Sort by updated_at descending
        conversations.sort(key=lambda x: x['updated_at'], reverse=True)
        return jsonify(conversations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    try:
        conversation_id = str(uuid.uuid4())
        
        # Ensure user exists
        db.create_user(DEFAULT_USER_ID)
        
        # Create conversation
        success = db.create_conversation(DEFAULT_USER_ID, conversation_id)
        
        if success:
            return jsonify({
                "conversation_id": conversation_id,
                "message": "Conversation created successfully"
            })
        else:
            return jsonify({"error": "Failed to create conversation"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get a specific conversation"""
    try:
        conversation = db.get_conversation(conversation_id)
        if conversation:
            return jsonify(conversation)
        else:
            return jsonify({"error": "Conversation not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations/<conversation_id>/messages', methods=['POST'])
def send_message(conversation_id):
    """Send a message to a conversation"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get current conversation
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404
        
        messages = conversation['messages']
        current_quality_score = conversation['quality_score'] or 5.0  # Default to 5.0 for AI response if no score yet
        previous_scores = conversation.get('message_scores', [])
        
        # Add user message
        messages.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get feedback and score FIRST (before AI response)
        rolling_average_score, feedback, current_message_score = ai_service.get_feedback_response(messages, previous_scores)
        
        print(f"DEBUG: Previous scores: {previous_scores}")
        print(f"DEBUG: Current message score: {current_message_score}")
        print(f"DEBUG: Rolling average score: {rolling_average_score}")
        
        # Update conversation with new messages and rolling average score FIRST
        new_message_scores = previous_scores + [current_message_score]
        db.update_conversation(conversation_id, messages, rolling_average_score, new_message_scores)
        
        # Return feedback immediately (before AI response)
        return jsonify({
            "feedback_ready": True,
            "quality_score": rolling_average_score,
            "feedback": feedback,
            "messages": messages
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations/<conversation_id>/response', methods=['POST'])
def get_ai_response(conversation_id):
    """Get AI response for a conversation after feedback is ready"""
    try:
        # Get current conversation
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404
        
        messages = conversation['messages']
        current_quality_score = conversation['quality_score'] or 5.0
        
        # Get AI response using the current score
        ai_response = ai_service.get_chat_response(messages, current_quality_score)
        
        # Add AI response to messages
        messages.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update conversation with AI response
        db.update_conversation(conversation_id, messages, current_quality_score, conversation.get('message_scores', []))
        
        return jsonify({
            "ai_response": ai_response,
            "messages": messages
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations/<conversation_id>/title', methods=['PUT'])
def update_conversation_title(conversation_id):
    """Update conversation title (for future use)"""
    try:
        data = request.get_json()
        title = data.get('title', '')
        
        # This would require adding a title field to the database
        # For now, just return success
        return jsonify({"message": "Title updated successfully"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure default user exists
    db.create_user(DEFAULT_USER_ID)
    
    print("Starting Prompt.ly backend server...")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
