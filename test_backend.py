#!/usr/bin/env python3

import requests
import json

def test_backend():
    base_url = "http://localhost:5001/api"
    
    print("🧪 Testing backend...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Get conversations
    try:
        response = requests.get(f"{base_url}/conversations")
        print(f"✅ Get conversations: {response.status_code}")
        conversations = response.json()
        print(f"   Found {len(conversations)} conversations")
    except Exception as e:
        print(f"❌ Get conversations failed: {e}")
        return
    
    # Test 3: Create conversation
    try:
        response = requests.post(f"{base_url}/conversations")
        print(f"✅ Create conversation: {response.status_code}")
        conv_data = response.json()
        conv_id = conv_data.get('conversation_id')
        print(f"   Created conversation: {conv_id}")
    except Exception as e:
        print(f"❌ Create conversation failed: {e}")
        return
    
    # Test 4: Send message
    if conv_id:
        try:
            message_data = {"message": "Hello, this is a test message"}
            response = requests.post(
                f"{base_url}/conversations/{conv_id}/messages",
                json=message_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"✅ Send message: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   AI Response: {result.get('ai_response', 'No response')[:100]}...")
                print(f"   Quality Score: {result.get('quality_score', 'No score')}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Send message failed: {e}")

if __name__ == "__main__":
    test_backend()
