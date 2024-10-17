# Collaborative Research Tool

## Overview
This tool provides a collaborative platform for real-time agent-based research visualization. The backend is built with Flask, while the frontend uses React and D3.js for visualization.

## Features
- Multiple agents (Research Specialist, Policy Analyst, etc.) to perform different research-related tasks.
- Real-time visualization of agent activities.
- API integrations (OpenAI, Anthropic, Ollama).
- File processing for CSV and PDF documents.

## Prerequisites
- **Backend**: Python 3.10+
- **Frontend**: Node.js and npm

## Installation

### Backend Setup
1. Navigate to the **backend** folder:
   ```sh
   cd backend
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set environment variables for API keys:
   - **OPENAI_API_KEY**: Your OpenAI API key.
   - **CLAUDE_API_KEY**: Your Anthropic API key.
   - **OLLAMA_URL**: URL for Ollama integration.

### Frontend Setup
1. Navigate to the **frontend** folder:
   ```sh
   cd ../frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```

## Running the Application

### Start Backend Server
Navigate to the **backend** folder and run the Flask server:
```sh
python main.py
```

### Start Frontend Application
Navigate to the **frontend** folder and start the React application:
```sh
npm start
```

Access the application by opening your browser at `http://localhost:3000`.

## Usage
- Enter a topic in the search bar.
- Select the agents you want to involve in the research task.
- Upload files for analysis (optional).
- Click on "Start Research" to see real-time agent interactions visualized.

## Testing
- Use **Postman** or **CURL** to test backend endpoints.
- Verify real-time updates on the frontend.

## License
MIT License.
