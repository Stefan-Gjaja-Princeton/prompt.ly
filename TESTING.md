# Testing Documentation

## Overview

This document describes the testing strategy, coverage, and execution instructions for the prompt.ly application.

## Test Suite Structure

### Backend Tests (Python)

Located in `backend/tests/`:

- **Unit Tests**: Test individual components in isolation
  - `test_database.py`: Database operations
  - `test_ai_service.py`: AI service with mocked OpenAI
  - `test_auth_service.py`: Authentication with mocked Auth0
- **Integration Tests**: Test API endpoints end-to-end
  - `test_app_integration.py`: Full request/response cycle

### Frontend Tests (JavaScript/React)

Located in `frontend/src/`:

- `App.test.js`: Basic component tests (starter file)

## Running Tests

### Backend Tests

#### Prerequisites

```bash
cd backend
pip install -r requirements.txt
```

#### Run All Backend Tests

```bash
# From project root
pytest backend/tests/

# Or from backend directory
cd backend
pytest tests/
```

#### Run with Coverage

```bash
pytest backend/tests/ --cov=backend --cov-report=html --cov-report=term
```

#### Run Specific Test Suite

```bash
# Database tests only
pytest backend/tests/test_database.py

# AI service tests only
pytest backend/tests/test_ai_service.py

# Integration tests only
pytest backend/tests/test_app_integration.py
```

### Frontend Tests

#### Prerequisites

```bash
cd frontend
npm install
```

#### Run Frontend Tests

```bash
cd frontend
npm test
```

## Test Coverage Summary

### Backend Coverage

**Database Operations** (test_database.py):

- ✅ User creation and retrieval
- ✅ Conversation creation and management
- ✅ Message and score updates
- ✅ Conversation summaries
- ✅ User conversation lists

**AI Service** (test_ai_service.py):

- ✅ Feedback generation (mocked OpenAI)
- ✅ Quality score calculation
- ✅ Response generation based on quality:
  - Low quality (≤3): Terse responses
  - Medium quality (≤5): Brief responses
  - High quality (>5): Normal responses
- ✅ Error handling

**Authentication** (test_auth_service.py):

- ✅ JWT token verification
- ✅ Auth0 integration (mocked)
- ✅ Authentication decorator

**API Endpoints** (test_app_integration.py):

- ✅ Health check
- ✅ User profile
- ✅ Conversation CRUD operations
- ✅ Message sending
- ✅ AI response generation
- ✅ Authentication enforcement

### Frontend Coverage

**Components** (App.test.js):

- ⚠️ Basic structure (needs expansion)
- ⚠️ Authentication flow
- ⚠️ Conversation management
- ⚠️ Message sending
- ⚠️ Feedback display

_Note: Frontend tests are minimal and should be expanded_

## Behaviors Validated

### Core Functionality

1. **User Management**

   - Users can be created and retrieved
   - Duplicate user creation is handled gracefully

2. **Conversation Management**

   - Conversations can be created for users
   - Conversations store messages, scores, and feedback
   - Users can retrieve their conversation lists

3. **Message Processing**

   - Messages trigger feedback generation
   - Quality scores are calculated
   - AI responses are generated based on quality
   - Two-phase response (feedback → AI response)

4. **Authentication**

   - Protected endpoints require valid JWT tokens
   - Token verification works correctly
   - Invalid tokens are rejected

5. **Error Handling**
   - Invalid requests return appropriate error codes
   - Missing data is handled gracefully
   - External API failures are caught

## Test Execution During Demo

To run tests during your presentation:

1. **Quick Test Run** (30 seconds):

   ```bash
   pytest backend/tests/ -v
   ```

2. **Show Coverage** (1 minute):

   ```bash
   pytest backend/tests/ --cov=backend --cov-report=term
   ```

3. **Run Specific Test** (10 seconds):
   ```bash
   pytest backend/tests/test_database.py::TestDatabase::test_create_user -v
   ```

## Test Data

- Tests use **in-memory SQLite database** (no setup needed)
- All external APIs are **mocked** (OpenAI, Auth0)
- Tests are **deterministic** and **repeatable**
- No cleanup required (database is in-memory)

## Continuous Integration

These tests are designed for CI/CD:

- ✅ Fast execution (< 10 seconds)
- ✅ No external dependencies
- ✅ Isolated test environment
- ✅ Repeatable results

## Future Improvements

1. **Frontend Tests**: Expand React component tests
2. **E2E Tests**: Add end-to-end tests with Cypress/Playwright
3. **Performance Tests**: Add load testing for API endpoints
4. **Security Tests**: Add tests for authentication edge cases

## Troubleshooting

### Common Issues

**Import Errors**

- Ensure you're in the correct directory
- Install dependencies: `pip install -r requirements.txt`

**Database Errors**

- Tests use in-memory database, no setup needed
- Check `conftest.py` if issues persist

**Mock Errors**

- Verify mocks match expected API responses
- Check that external services are properly mocked

**Frontend Test Errors**

- Ensure `npm install` has been run
- Check that test environment is configured
