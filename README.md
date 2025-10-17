# Prompt.ly v2

A three-column AI chatbot webapp with real-time feedback and quality scoring.

## Features

- **Left Column**: Table of contents for past conversations
- **Middle Column**: Main chat interface with AI chatbot
- **Right Column**: Real-time feedback and quality scoring (1-10 scale)
- **Adaptive Responses**: Chatbot becomes terser when user quality score drops below 3
- **Database Integration**: SQLite database for storing users and conversations

## Quick Start

### Option 1: Using Startup Scripts (Recommended)

1. **Set your OpenAI API key:**

   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Start the backend:**

   ```bash
   ./start_backend.sh
   ```

3. **In a new terminal, start the frontend:**

   ```bash
   ./start_frontend.sh
   ```

4. **Open your browser to:** `http://localhost:3000`

### Option 2: Manual Setup

#### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API Key

#### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your OpenAI API key:

   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

   Or create a `.env` file in the backend directory with:

   ```
   OPENAI_API_KEY=your-api-key-here
   ```

5. Run the Flask server:
   ```bash
   python app.py
   ```

#### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   ```

3. Start the React development server:

   ```bash
   npm start
   ```

4. Open your browser to `http://localhost:3000`

## Database

The SQLite database will be automatically created when you first run the backend. It includes:

- `users` table: stores user information and conversation IDs
- `conversations` table: stores conversation history

## Configuration

- **OpenAI Model**: Currently set to GPT-4o, easily modifiable in `backend/ai_service.py`
- **Quality Threshold**: Responses become terse when user score drops below 3
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/conversations` - Get all conversations for a user
- `POST /api/conversations` - Create a new conversation
- `POST /api/conversations/{id}/messages` - Send a message to a conversation
- `GET /api/conversations/{id}` - Get conversation history

## Project Structure

```
prompt.ly v2/
├── backend/
│   ├── app.py              # Flask application
│   ├── ai_service.py       # OpenAI integration
│   ├── database.py         # Database operations
│   ├── config.py           # Configuration
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service
│   │   └── App.js          # Main React app
│   └── package.json        # Node.js dependencies
├── start_backend.sh        # Backend startup script
├── start_frontend.sh       # Frontend startup script
└── README.md              # This file
```

## Troubleshooting

### Backend Issues

- Make sure your OpenAI API key is set correctly
- Check that Python 3.8+ is installed
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Frontend Issues

- Make sure Node.js 16+ is installed
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that the backend is running on port 5001

### Database Issues

- The SQLite database is created automatically
- If you need to reset: delete `backend/promptly.db` and restart the backend
