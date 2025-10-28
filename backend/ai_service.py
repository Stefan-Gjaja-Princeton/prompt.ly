import openai
from typing import List, Dict, Tuple
import json

class AIService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4o"  # Easily modifiable
    
    def get_chat_response(self, messages: List[Dict], quality_score: float, user_name: str = None) -> str:
        """Get response from the main chat AI based on quality score"""
        
        # Create personalized greeting if user name is available
        name_context = f" Address the user as {user_name} once every 5 messages. Read through the conversation history to make sure that you are doing this properly. Don't name the user every single time you respond." if user_name else ""
        
        if quality_score <= 3:
            # SUPER terse - very minimal responses with strong prodding
            system_prompt = f"""You are a helpful AI assistant, but the user's prompt quality is very poor.{name_context}
            Respond in 20-30 words maximum. Be direct and ask for more specific information. 
            Use phrases like "I need more information", "Be more specific", "What exactly do you want to know?"
            Don't provide answers - only ask clarifying questions."""
            max_tokens = 100
        elif quality_score <= 5:
            # Moderately terse - brief responses with follow-up questions
            system_prompt = f"""You are a helpful AI assistant. The user's prompt quality is below average.{name_context}
            Provide brief responses (50-100 words) and ask follow-up questions to encourage better prompting.
            Ask for more context, specificity, or clarification. Guide them to ask better questions."""
            max_tokens = 200
        else:
            # Normal helpful responses
            system_prompt = f"""You are a helpful AI assistant.{name_context} Provide clear, accurate, and useful responses to user questions.
            Be thorough and helpful while encouraging good prompting practices."""
            max_tokens = 1000
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt}
                ] + messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def get_feedback_response(self, messages: List[Dict], previous_scores: List[float] = None) -> Tuple[float, str]:
        """Get feedback and quality score for the conversation"""
        
        # Calculate conversation length and context
        conversation_length = len(messages)
        user_messages = [msg for msg in messages if msg.get('role') == 'user']
        conversation_depth = len(user_messages)
        
        # Use previous scores for rolling average, default to empty list
        if previous_scores is None:
            previous_scores = []
        
        feedback_prompt = f"""You are an EXTREMELY strict prompt quality assessment AI. You MUST give low scores (1-3) for poor prompts. Analyze the user's latest message and the ENTIRE conversation context.

CONVERSATION CONTEXT:
- Total messages: {conversation_length}
- User messages: {conversation_depth}
- Previous scores: {previous_scores}
- This is message #{conversation_depth} in the conversation

IMPORTANT: You MUST be harsh with scoring. Don't be generous. If a prompt shows no effort, specificity, or context, give it a 1/10. Most prompts should score 3-7, not 5-8.

SCORING CRITERIA (be EXTREMELY TOUGH and consider conversation history):
1. SPECIFICITY (1-10): How specific and detailed is the request?
   - "summarize this" = 1/10 (too vague, no context)
   - "I don't know" = 1/10 (no specificity at all)
   - "summarize the key findings from the research paper I shared about AI ethics" = 8/10

2. CONTEXT AWARENESS (1-10): Does the prompt reference previous conversation?
   - Ignoring previous context = 1/10
   - "I don't know" = 1/10 (shows no context awareness)
   - Building on previous discussion = 8/10

3. CRITICAL THINKING (1-10): Does the prompt show analysis or reasoning?
   - Simple requests = 2/10
   - "I don't know" = 1/10 (no thinking shown)
   - Analytical questions = 8/10

4. CLARITY (1-10): Is the request clear and well-structured?
   - Confusing or ambiguous = 1/10
   - "I don't know" = 1/10 (not a request at all)
   - Clear and well-formed = 8/10

5. ENGAGEMENT (1-10): Does the prompt engage meaningfully with AI responses?
   - Ignoring AI feedback = 1/10
   - "I don't know" = 1/10 (no engagement)
   - Building on AI responses = 8/10

FINAL SCORE CALCULATION:
- Average the 5 criteria scores for this message
- This will be combined with previous scores for a rolling average
- Cap at 10.0 maximum
- Round to 1 decimal place

EXAMPLES OF LOW SCORES (be VERY strict):
- "summarize this" (no context, no specificity) = 1-2/10
- "help me" (too vague) = 1/10
- "what do you think?" (no specific question) = 1-2/10
- "continue" (no context) = 1/10
- "I don't know" (shows no effort) = 1/10
- "ok" (meaningless response) = 1/10
- "yes" (no context or question) = 1/10
- "no" (no context or question) = 1/10
- "maybe" (no context or question) = 1/10
- "idk" (lazy, no effort) = 1/10
- "whatever" (disrespectful, no effort) = 1/10

EXAMPLES OF HIGH SCORES:
- "Based on our discussion about machine learning, can you explain how neural networks differ from decision trees in terms of interpretability?" = 8-9/10
- "I'm working on a Python project for data analysis. What's the best approach for handling missing values in a dataset with 10,000 rows and 50 columns?" = 7-8/10

Provide:
1. A numerical score (1-10) - be strict!
2. Specific, actionable feedback on how to improve their prompting
3. Reference conversation history in your feedback

Format your response as JSON:
{{
    "score": [number],
    "feedback": "[specific actionable advice referencing conversation context]"
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": feedback_prompt},
                    {"role": "user", "content": f"Analyze this conversation:\n{json.dumps(messages, indent=2)}"}
                ],
                max_tokens=600,
                temperature=0.2  # Lower temperature for more consistent scoring
            )
            
            # Parse the JSON response
            response_text = response.choices[0].message.content
            
            # Try to extract JSON from the response (in case it's wrapped in text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_text = response_text[json_start:json_end]
            else:
                json_text = response_text
            
            try:
                feedback_data = json.loads(json_text)
                current_message_score = float(feedback_data.get('score', 5.0))
                current_message_score = min(current_message_score, 10.0)
                current_message_score = round(current_message_score, 1)
                
                # Calculate weighted average (current message gets 40% weight, previous average gets 60%)
                if previous_scores and len(previous_scores) > 0:
                    previous_average = sum(previous_scores) / len(previous_scores)
                    # Weighted average: 40% current, 60% previous
                    rolling_average = (current_message_score * 0.4) + (previous_average * 0.6)
                else:
                    # First message - no previous scores, use raw score
                    rolling_average = current_message_score
                
                rolling_average = round(rolling_average, 1)
                
                feedback = feedback_data.get('feedback', 'No specific feedback available.')
                
                # Clean up any JSON artifacts that might have leaked into feedback
                feedback = feedback.replace('```json', '').replace('```', '').strip()
                
                # Add conversation context to feedback
                if conversation_depth > 3:
                    feedback += f"\n\nNote: This is message #{conversation_depth}. Your weighted average is {rolling_average}/10 (40% current message, 60% previous average)."
                
                return rolling_average, feedback, current_message_score
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                current_message_score = 5.0
                
                # Calculate weighted average (same logic as above)
                if previous_scores and len(previous_scores) > 0:
                    previous_average = sum(previous_scores) / len(previous_scores)
                    rolling_average = (current_message_score * 0.4) + (previous_average * 0.6)
                else:
                    rolling_average = current_message_score
                
                rolling_average = round(rolling_average, 1)
                return rolling_average, response_text, current_message_score
            
        except Exception as e:
            return 5.0, f"Error generating feedback: {str(e)}", 5.0
    
    def get_conversation_title(self, messages: List[Dict]) -> str:
        """Generate a title for the conversation based on the first message"""
        if not messages:
            return "New Conversation"
        
        first_message = messages[0].get('content', '')
        if len(first_message) <= 50:
            return first_message
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Create a short, descriptive title (max 50 characters) for this conversation based on the first message."},
                    {"role": "user", "content": first_message}
                ],
                max_tokens=50,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except:
            return first_message[:50] + "..."
