import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import * as d3 from 'd3';

const socket = io('http://localhost:5000');

function App() {
  const [updates, setUpdates] = useState([]);
  const [topic, setTopic] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedAgents, setSelectedAgents] = useState([]);
  const [llmType, setLlmType] = useState("openai");
  const [apiKeys, setApiKeys] = useState({ openai: "", claude: "", ollamaUrl: "" });

  useEffect(() => {
    socket.on('agent_update', (data) => {
      setUpdates((prevUpdates) => [...prevUpdates, data]);
      updateVisualization();
    });
  }, []);

  const handleResearch = () => {
    fetch('http://localhost:5000/research', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ topic, agents: selectedAgents, llm_type: llmType }),
    });
  };

  const handleFileUpload = () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    }).then((response) => response.json())
      .then((data) => {
        setUpdates((prevUpdates) => [...prevUpdates, { agent: 'File Upload', message: data.message }]);
        updateVisualization();
      });
  };

  const handleAgentSelection = (agent) => {
    setSelectedAgents((prevSelectedAgents) => {
      if (prevSelectedAgents.includes(agent)) {
        return prevSelectedAgents.filter((a) => a !== agent);
      } else {
        return [...prevSelectedAgents, agent];
      }
    });
  };

  const handleApiKeyChange = (e) => {
    const { name, value } = e.target;
    setApiKeys((prevKeys) => ({ ...prevKeys, [name]: value }));
  };

  const updateVisualization = () => {
    // Clear previous visualization
    d3.select("#d3-container").selectAll("svg").remove();

    // Visualization using D3.js
    const svg = d3.select("#d3-container").append("svg").attr("width", 800).attr("height", 400);
    const nodes = updates.map((update, index) => ({ id: index, agent: update.agent, message: update.message }));
    const links = nodes.map((node, index) => index > 0 ? { source: index - 1, target: index } : null).filter(link => link !== null);

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(400, 200));

    const link = svg.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(links)
      .enter().append("line")
      .attr("stroke-width", 2)
      .attr("stroke", "#999");

    const node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("circle")
      .data(nodes)
      .enter().append("circle")
      .attr("r", 20)
      .attr("fill", d => getNodeColor(d.agent))
      .call(d3.drag()
        .on("start", (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = event.x;
          d.fy = event.y;
        })
        .on("drag", (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on("end", (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }));

    node.append("title").text(d => `${d.agent}: ${d.message}`);

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    });
  };

  const getNodeColor = (agent) => {
    switch (agent) {
      case 'Research Specialist': return '#ff7f0e';
      case 'Policy Analyst': return '#2ca02c';
      case 'Technologist': return '#1f77b4';
      case 'Communicator': return '#d62728';
      case 'Web Browser': return '#9467bd';
      case 'Data Processing': return '#8c564b';
      case 'Sentiment Analysis': return '#e377c2';
      case 'Recommendation': return '#7f7f7f';
      case 'LLM Integration': return '#bcbd22';
      default: return '#17becf';
    }
  };

  return (
    <div className="App">
      <h1>Collaborative Research Assistant</h1>
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter research topic"
      />
      <div>
        <label>
          <input type="checkbox" value="Research Specialist" onChange={() => handleAgentSelection('Research Specialist')} /> Research Specialist
        </label>
        <label>
          <input type="checkbox" value="Policy Analyst" onChange={() => handleAgentSelection('Policy Analyst')} /> Policy Analyst
        </label>
        <label>
          <input type="checkbox" value="Technologist" onChange={() => handleAgentSelection('Technologist')} /> Technologist
        </label>
        <label>
          <input type="checkbox" value="Communicator" onChange={() => handleAgentSelection('Communicator')} /> Communicator
        </label>
        <label>
          <input type="checkbox" value="Web Browser" onChange={() => handleAgentSelection('Web Browser')} /> Web Browser
        </label>
        <label>
          <input type="checkbox" value="Recommendation" onChange={() => handleAgentSelection('Recommendation')} /> Recommendation
        </label>
        <label>
          <input type="checkbox" value="LLM Integration" onChange={() => handleAgentSelection('LLM Integration')} /> LLM Integration
        </label>
      </div>
      <div>
        <label>
          LLM Type:
          <select value={llmType} onChange={(e) => setLlmType(e.target.value)}>
            <option value="openai">OpenAI</option>
            <option value="claude">Claude</option>
            <option value="ollama">Ollama</option>
          </select>
        </label>
      </div>
      <button onClick={handleResearch}>Start Research</button>
      <br /><br />
      <input
        type="file"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />
      <button onClick={handleFileUpload}>Upload File</button>
      <div>
        {updates.map((update, index) => (
          <p key={index}><strong>{update.agent}:</strong> {update.message}</p>
        ))}
      </div>
      <div id="d3-container"></div>
    </div>
  );
}

export default App;
```