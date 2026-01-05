# Troubleshooting Guide

## Issue: "Failed to get AI response" After Page Refresh During Generation

### Problem Description

If you refresh the page while an AI response is being generated, the streaming connection is interrupted. This can leave the application in a corrupted state where:

1. The in-memory message cache may have stale or missing entries
2. The database may have conversations where the last message is from the user (meaning the AI response was never completed)
3. Future message attempts may fail because the system expects cached data that doesn't exist

### Solution

We've implemented several fixes to handle this:

#### 1. Automatic Cache Cleanup

The message cache now:

- Automatically expires entries after 5 minutes
- Is cleaned up on server startup
- Handles missing cache entries gracefully by falling back to database messages

#### 2. Fix Corrupted Conversations Utility

A utility script has been created to detect and fix corrupted conversations:

```bash
python fix_corrupted_conversations.py
```

This script will:

- Scan all conversations for issues
- Detect conversations with incomplete AI responses
- Optionally fix them by removing the incomplete last user message

**Usage:**

1. Run the script: `python fix_corrupted_conversations.py`
2. Review the issues it finds
3. Choose option 1 to fix all conversations automatically

#### 3. Clear Cache Endpoint

A new admin endpoint is available to manually clear the cache:

```bash
POST /api/admin/clear-cache
```

This requires authentication and will clear all cached message data.

### Quick Fix Steps

If you're experiencing this issue right now:

1. **For Local Development:**

   ```bash
   # Stop your backend server
   # Run the fix utility
   python fix_corrupted_conversations.py
   # Choose option 1 to fix all conversations
   # Restart your backend server
   ```

2. **For Deployed Version:**

   - The cache will automatically expire after 5 minutes
   - Or restart the backend service to clear the cache
   - If issues persist, you may need to run the fix utility script on the server

3. **Reset Database (Nuclear Option):**
   ```bash
   ./reset_database.sh
   ```
   ⚠️ **Warning:** This will delete ALL conversations and data!

### Prevention

The fixes implemented will prevent this issue from recurring:

- Cache entries expire automatically
- Better error handling for missing cache
- Graceful fallback to database when cache is unavailable

## Debugging OpenAI API Issues

If you're experiencing issues with OpenAI API calls, you can test connectivity using:

### 1. Test Script

```bash
python test_openai_api.py
```

This script will:

- Check if your API key is configured
- Test a simple non-streaming API call
- Test a streaming API call
- Provide helpful error messages and suggestions

### 2. Debug Endpoint

You can also test via the API endpoint:

```bash
POST /api/debug/test-openai
```

This requires authentication and will return detailed information about the API test.

### 3. Check Server Logs

Look for DEBUG and ERROR messages in your backend server logs. The enhanced logging will show:

- Message formatting details
- API call parameters
- Response chunk counts
- Detailed error information

### Common Issues and Solutions

**Rate Limit Errors:**

- Wait a few moments and try again
- Check your OpenAI account usage limits
- Consider upgrading your OpenAI plan

**Authentication Errors:**

- Verify your API key is correct
- Check that the API key hasn't expired
- Ensure the key has proper permissions

**Connection Errors:**

- Check your internet connection
- Verify OpenAI API is accessible from your network
- Check for firewall/proxy issues

**Empty Responses:**

- Check server logs for detailed error messages
- Verify your API key has credits/quota remaining
- Try a simpler test message

### Technical Details

**Root Cause:**

- Messages with file attachments (images/PDFs) are stored in base64 format in an in-memory cache
- This cache is keyed by `conversation_id`
- When the AI response endpoint is called, it expects to find messages in this cache
- If the page refreshes during streaming, the cache entry may become stale or missing

**Fix:**

- Cache entries now have timestamps and expire after 5 minutes
- The system falls back to database messages if cache is unavailable (though file data will be missing)
- Conversations can be automatically repaired by removing incomplete user messages
- Enhanced error logging for OpenAI API calls with detailed context
- Fixed duplicate message formatting bug in streaming function
- Better error handling with user-friendly error messages
- Comprehensive debugging tools (test script and debug endpoint)
