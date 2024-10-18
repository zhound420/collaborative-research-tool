from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import eventlet
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import PyPDF2
import openai
import anthropic
import ollama

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# File upload configuration
UPLOAD_FOLDER = '../uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# API keys configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL")

# Define a base agent class
class Agent:
    def act(self, task):
        raise NotImplementedError("Subclasses should implement this method")

# Define agents
class ResearchAgent(Agent):
    def act(self, task):
        response = f"Researching topic: {task}"
        socketio.emit('agent_update', {'agent': 'Research Specialist', 'message': response})
        return response

class PolicyAgent(Agent):
    def act(self, task):
        response = f"Evaluating policy impacts for: {task}"
        socketio.emit('agent_update', {'agent': 'Policy Analyst', 'message': response})
        return response

class TechnicalAgent(Agent):
    def act(self, task):
        response = f"Assessing technical feasibility for: {task}"
        socketio.emit('agent_update', {'agent': 'Technologist', 'message': response})
        return response

class CommunicationAgent(Agent):
    def act(self, task):
        response = f"Preparing communication materials for: {task}"
        socketio.emit('agent_update', {'agent': 'Communicator', 'message': response})
        return response

class WebBrowsingAgent(Agent):
    def act(self, task):
        response = f"Browsing the web for: {task}"
        socketio.emit('agent_update', {'agent': 'Web Browser', 'message': response})
        # Perform web browsing
        try:
            page = requests.get(task)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            response = f"Page title for {task}: {title}"
        except Exception as e:
            response = f"Error browsing the web for {task}: {e}"
        socketio.emit('agent_update', {'agent': 'Web Browser', 'message': response})
        return response

class DataProcessingAgent(Agent):
    def act(self, file_path):
        response = f"Processing file: {file_path}"
        socketio.emit('agent_update', {'agent': 'Data Processing', 'message': response})
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                summary = df.describe().to_string()
                response = f"Data summary: {summary}"
            elif file_path.endswith('.pdf'):
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = " ".join(page.extract_text() for page in reader.pages)
                    response = f"Extracted text from PDF: {text[:500]}..."
        except Exception as e:
            response = f"Error processing file {file_path}: {e}"
        socketio.emit('agent_update', {'agent': 'Data Processing', 'message': response})
        return response

class SentimentAnalysisAgent(Agent):
    def act(self, text):
        response = f"Analyzing sentiment for the provided text."
        socketio.emit('agent_update', {'agent': 'Sentiment Analysis', 'message': response})
        # Placeholder for sentiment analysis (e.g., using a pre-trained model)
        sentiment = "Positive" if "good" in text.lower() else "Neutral"
        response = f"Sentiment analysis result: {sentiment}"
        socketio.emit('agent_update', {'agent': 'Sentiment Analysis', 'message': response})
        return response

class RecommendationAgent(Agent):
    def act(self, context):
        response = f"Generating recommendations based on context: {context}"
        socketio.emit('agent_update', {'agent': 'Recommendation', 'message': response})
        # Placeholder recommendations
        recommendations = ["Read more on similar topics", "Consult a technical expert"]
        response = f"Recommendations: {', '.join(recommendations)}"
        socketio.emit('agent_update', {'agent': 'Recommendation', 'message': response})
        return response

class LLMIntegrationAgent(Agent):
    def act(self, task, llm_type="openai"):
        response = f"Processing task with LLM ({llm_type}): {task}"
        socketio.emit('agent_update', {'agent': 'LLM Integration', 'message': response})
        try:
            if llm_type == "openai":
                openai.api_key = OPENAI_API_KEY
                completion = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=task,
                    max_tokens=150
                )
                response = completion.choices[0].text.strip()
            elif llm_type == "claude":
                client = anthropic.Client(api_key=CLAUDE_API_KEY)
                response = client.completion(prompt=task, max_tokens_to_sample=150)
            elif llm_type == "ollama":
                response = ollama.ask(url=OLLAMA_URL, prompt=task)
        except Exception as e:
            response = f"Error processing task with {llm_type}: {e}"
        socketio.emit('agent_update', {'agent': 'LLM Integration', 'message': response})
        return response

# Initialize agents
research_agent = ResearchAgent()
policy_agent = PolicyAgent()
technical_agent = TechnicalAgent()
communication_agent = CommunicationAgent()
web_browsing_agent = WebBrowsingAgent()
data_processing_agent = DataProcessingAgent()
sentiment_analysis_agent = SentimentAnalysisAgent()
recommendation_agent = RecommendationAgent()
llm_integration_agent = LLMIntegrationAgent()

@app.route('/research', methods=['POST'])
def research():
    data = request.get_json()
    topic = data.get('topic')
    selected_agents = data.get('agents', [])
    llm_type = data.get('llm_type', 'openai')

    if 'Research Specialist' in selected_agents:
        research_agent.act(topic)
    if 'Policy Analyst' in selected_agents:
        policy_agent.act(topic)
    if 'Technologist' in selected_agents:
        technical_agent.act(topic)
    if 'Communicator' in selected_agents:
        communication_agent.act(topic)
    if 'Web Browser' in selected_agents:
        web_browsing_agent.act("https://en.wikipedia.org/wiki/" + topic)
    if 'Recommendation' in selected_agents:
        recommendation_agent.act(topic)
    if 'LLM Integration' in selected_agents:
        llm_integration_agent.act(topic, llm_type)

    return jsonify({'message': 'Agents have been activated for the task.'})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        socketio.emit('agent_update', {'agent': 'File Upload', 'message': f'File {filename} uploaded successfully'})
        data_processing_agent.act(file_path)
        return jsonify({'message': f'File {filename} uploaded successfully'}), 200

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
