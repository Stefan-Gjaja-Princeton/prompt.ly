# Testing Documentation

This document describes the comprehensive testing suite for Prompt.ly, including unit tests and system tests.

## Overview

The testing suite is organized into three main categories:

1. **Backend Unit Tests** - Test individual components and functions
2. **Frontend Unit Tests** - Test React components and utilities
3. **System Tests** - End-to-end tests for complete user flows

## Backend Unit Tests

Location: `backend/tests/`

### Test Files

- **`test_database.py`** - Tests database operations
  - User creation and retrieval
  - Conversation CRUD operations
  - Message count optimization
  - Conversation deletion with ownership verification
  - Pagination and limits

- **`test_ai_service.py`** - Tests AI service functionality
  - Chat response generation (normal and streaming)
  - Feedback generation with quality scoring
  - Conversation title generation
  - File attachment handling (images and PDFs)
  - Error handling and fallbacks

- **`test_auth_service.py`** - Tests authentication
  - JWT token verification
  - Public key retrieval from Auth0
  - User data extraction from tokens
  - Auth decorator functionality

- **`test_app_integration.py`** - Tests API endpoints
  - Health check endpoint
  - User profile endpoints
  - Conversation endpoints (GET, POST, DELETE)
  - Message sending with file validation
  - AI response streaming (SSE format)
  - Error responses (400, 401, 404, 500)

### Running Backend Tests

```bash
cd backend
pytest
```

With coverage:
```bash
cd backend
pytest --cov=. --cov-report=html
```

## Frontend Unit Tests

Location: `frontend/src/__tests__/`

### Test Files

- **`utils/markdown.test.js`** - Tests markdown rendering
  - Plain text rendering
  - Bold, italic, code blocks
  - Lists and links
  - Error handling

- **`services/apiService.test.js`** - Tests API service
  - Request/response handling
  - Authentication token injection
  - SSE streaming support
  - AbortController support
  - Error handling

- **`components/ConfirmationModal.test.js`** - Tests confirmation modal
  - Show/hide behavior
  - Button interactions
  - Event propagation
  - Custom props

- **`components/FeedbackPanel.test.js`** - Tests feedback panel
  - Quality score display
  - Feedback text rendering
  - Improvement tips
  - Loading states

- **`components/ConversationList.test.js`** - Tests conversation list
  - Empty state
  - Conversation rendering
  - Date formatting
  - Delete functionality
  - Active conversation highlighting

### Running Frontend Tests

```bash
cd frontend
npm test
```

With coverage:
```bash
cd frontend
npm run test:coverage
```

## System Tests

Location: `tests/system/`

### Test Files

- **`test_authentication_flow.js`** - End-to-end authentication
  - Login flow
  - Token storage
  - Logout flow
  - Unauthenticated redirects

- **`test_conversation_management.js`** - Conversation CRUD
  - Creating conversations
  - Loading conversations
  - Deleting conversations
  - UI updates after operations

- **`test_message_sending.js`** - Message sending flow
  - Text messages
  - File attachments (images, PDFs)
  - Feedback generation
  - AI response streaming
  - Message limit enforcement

- **`test_streaming_response.js`** - Streaming behavior
  - Chunk-by-chunk streaming
  - Typing indicators
  - Error handling during streaming
  - Abort on conversation delete
  - Page refresh handling

- **`test_error_handling.js`** - Error scenarios
  - Network errors
  - HTTP error codes (401, 404, 500)
  - Timeout handling
  - Invalid file types
  - Message limit errors

### Running System Tests

First, install Playwright:
```bash
npm install
npx playwright install
```

Run all system tests:
```bash
npm run test:system
```

Run with UI:
```bash
npm run test:system:ui
```

## Test Coverage Goals

- **Backend Unit Tests**: 80%+ code coverage
- **Frontend Unit Tests**: 70%+ code coverage for components
- **System Tests**: Cover all major user flows
- **Critical Paths**: 100% coverage (auth, message sending, streaming)

## Running All Tests

From the root directory:
```bash
npm run test:all
```

This runs:
1. Backend unit tests
2. Frontend unit tests
3. System tests

## Test Infrastructure

### Backend
- **Framework**: pytest
- **Mocking**: unittest.mock
- **Database**: In-memory SQLite for tests
- **Coverage**: pytest-cov

### Frontend
- **Framework**: Jest + React Testing Library
- **Mocking**: Jest mocks
- **Setup**: `frontend/src/setupTests.js`

### System Tests
- **Framework**: Playwright
- **Browsers**: Chromium (configurable for Firefox/WebKit)
- **Configuration**: `playwright.config.js`

## Notes

- Some system tests are skipped until Auth0 test credentials are configured
- System tests assume backend is running on default port
- Adjust selectors in system tests based on actual component class names
- Mock OpenAI API calls in backend tests to avoid API costs
- Use test database (in-memory SQLite) for backend tests

## Continuous Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Backend Tests
  run: cd backend && pytest

- name: Run Frontend Tests
  run: cd frontend && npm test -- --watchAll=false

- name: Run System Tests
  run: npm run test:system
```

