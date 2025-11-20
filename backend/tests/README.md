# Test Suite Documentation

## Overview

This test suite provides comprehensive testing for the prompt.ly backend application, including unit tests and integration tests.

## Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── test_database.py         # Unit tests for database operations
├── test_ai_service.py       # Unit tests for AI service (with OpenAI mocking)
├── test_auth_service.py     # Unit tests for authentication (with Auth0 mocking)
├── test_app_integration.py  # Integration tests for API endpoints
└── README.md               # This file
```

## Test Coverage

### Unit Tests

1. **Database Tests** (`test_database.py`)

   - User creation and retrieval
   - Conversation creation and management
   - Message and score updates
   - Conversation summaries

2. **AI Service Tests** (`test_ai_service.py`)

   - Feedback generation with mocked OpenAI API
   - Chat response generation for different quality scores
   - JSON parsing error handling
   - Response length based on quality score

3. **Auth Service Tests** (`test_auth_service.py`)
   - JWT token verification
   - Public key retrieval from Auth0
   - Authentication decorator functionality

### Integration Tests

4. **API Endpoint Tests** (`test_app_integration.py`)
   - Health check endpoint
   - User profile endpoint
   - Conversation creation and retrieval
   - Message sending and AI response generation
   - Authentication requirements

## Running Tests

### Prerequisites

Install test dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### Run All Tests

```bash
# From project root
pytest backend/tests/

# Or from backend directory
cd backend
pytest tests/
```

### Run Specific Test Files

```bash
# Run only database tests
pytest backend/tests/test_database.py

# Run only AI service tests
pytest backend/tests/test_ai_service.py

# Run only integration tests
pytest backend/tests/test_app_integration.py
```

### Run with Coverage Report

```bash
pytest backend/tests/ --cov=backend --cov-report=html --cov-report=term
```

This generates:

- Terminal coverage report
- HTML report in `htmlcov/` directory (open `htmlcov/index.html` in browser)

### Run with Verbose Output

```bash
pytest backend/tests/ -v
```

### Run Specific Test Function

```bash
pytest backend/tests/test_database.py::TestDatabase::test_create_user -v
```

## Test Behaviors Validated

### Database Operations

- ✅ User creation (new and duplicate)
- ✅ User retrieval by email
- ✅ Conversation creation
- ✅ Conversation retrieval
- ✅ Conversation updates (messages, scores, feedback)
- ✅ User conversation list retrieval
- ✅ Conversation summary generation

### AI Service

- ✅ Feedback generation from OpenAI API
- ✅ Quality score calculation
- ✅ Response generation based on quality score:
  - Low quality (≤3): Terse responses (20-30 words, max 100 tokens)
  - Medium quality (≤5): Brief responses (50-100 words, max 200 tokens)
  - High quality (>5): Normal responses (max 1000 tokens)
- ✅ JSON parsing error handling
- ✅ Previous scores integration

### Authentication

- ✅ JWT token verification
- ✅ Auth0 public key retrieval
- ✅ Authentication decorator enforcement
- ✅ Invalid token handling

### API Endpoints

- ✅ Health check (no auth required)
- ✅ User profile retrieval (auth required)
- ✅ Conversation creation (auth required)
- ✅ Message sending with feedback (auth required)
- ✅ AI response generation (auth required)
- ✅ Authentication requirement enforcement

## Test Fixtures

Common fixtures available in `conftest.py`:

- `test_db`: In-memory SQLite database for testing
- `sample_user_email`: Test user email
- `sample_conversation_id`: Test conversation ID
- `sample_messages`: Sample message array
- `mock_openai_response`: Mocked OpenAI API response
- `mock_auth0_token`: Mocked Auth0 JWT token payload

## Mocking Strategy

- **OpenAI API**: All OpenAI calls are mocked to avoid API costs and ensure fast, reliable tests
- **Auth0**: Auth0 API calls are mocked for token verification tests
- **Database**: Uses in-memory SQLite for fast, isolated tests
- **External Services**: All external HTTP requests are mocked

## Continuous Integration

These tests are designed to run in CI/CD pipelines. They:

- Don't require external services (OpenAI, Auth0)
- Use in-memory database (no setup/teardown needed)
- Complete in seconds
- Are deterministic and repeatable

## Adding New Tests

When adding new functionality:

1. **Unit Tests**: Add to appropriate test file or create new one
2. **Integration Tests**: Add to `test_app_integration.py`
3. **Fixtures**: Add shared fixtures to `conftest.py`
4. **Mocking**: Mock all external dependencies

Example:

```python
def test_new_feature(self, test_db, sample_user_email):
    """Test description"""
    # Arrange
    # Act
    result = test_db.new_method(sample_user_email)
    # Assert
    assert result is True
```

## Troubleshooting

### Tests fail with import errors

- Ensure you're in the correct directory
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Database errors

- Tests use in-memory database, so no cleanup needed
- If issues persist, check `conftest.py` fixture setup

### Mock errors

- Verify mocks are properly patched
- Check that mock return values match expected format
