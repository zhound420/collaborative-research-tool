# Collaborative Research Tool

## Overview
The Collaborative Research Tool is a local application that allows users to visualize real-time interactions between different research agents. These agents collaborate to perform research tasks, analyze data, and communicate findings. The backend is built using Flask and Python, while the frontend is developed using React and D3.js.

## Features
- Multiple agents performing tasks such as research, policy evaluation, technical assessment, and sentiment analysis.
- Real-time visualization of agent interactions using D3.js.
- Integration with various LLMs, including OpenAI, Anthropic, and Ollama.
- File processing capabilities for CSV and PDF documents.

## Prerequisites
- **Backend**: Python 3.10+
- **Frontend**: Node.js and npm

## Installation

### Backend Setup
1. Clone the repository and navigate to the **backend** folder:
   ```sh
   git clone <repository-url>
   cd collaborative_research_tool/backend
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
1. Navigate to the **frontend** folder and create the React app:
   ```sh
   cd ../frontend
   npx create-react-app .
   ```
2. Install additional dependencies:
   ```sh
   npm install socket.io-client d3
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
1. Enter a research topic in the search bar.
2. Select the agents you want to involve in the research task.
3. Upload files for analysis (optional).
4. Click on "Start Research" to see real-time agent interactions visualized.

## Project Structure
```
collaborative_research_tool/
|-- backend/
|   |-- main.py
|   |-- requirements.txt
|-- frontend/
|   |-- public/
|   |   |-- index.html
|   |-- src/
|   |   |-- App.js
|   |-- package.json
|-- uploads/ (Empty, used for uploaded files)
|-- .gitignore
|-- README.md
```

## Testing
- Use **Postman** or **CURL** to test backend endpoints.
- Verify real-time updates on the frontend when agents perform actions.

## License
MIT License.

## Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue for suggestions and improvements.

## Contact
For any inquiries or support, please reach out via the repository's issue tracker.
