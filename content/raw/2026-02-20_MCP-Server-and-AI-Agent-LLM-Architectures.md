# MCP Server and AI Agent-LLM Architectures

**Source:** https://saraswathilakshman.medium.com/mcp-server-and-ai-agent-llm-architectures-20fc1d3bc886
**Author:** 
**Published:** None
**Scraped:** 2026-02-20

---

MCP Server and AI Agent-LLM Architectures
Saraswathi Lakshman
10 min read
·
Apr 18, 2025

MCP (Multi-agent Conversational Protocol) represents an advancement in how AI agents communicate and collaborate. Let me explain what it is, how it differs from traditional AI agent-LLM connections, and its real-world applications.

What is MCP?

MCP is a standardised protocol designed to facilitate structured communication between multiple AI agents. Unlike simple agent-LLM connections, MCP establishes a formalised framework that enables:

Agent-to-agent communication with defined message formats
Structured conversation flows with clear roles and responsibilities
Metadata sharing and context management across multiple agents
Standardised interaction patterns for complex multi-agent systems
How MCP Differs from Traditional Agent-LLM Connections

Traditional agent-LLM connections typically feature:

A single agent querying an LLM directly
Simple request-response patterns
Limited contextual awareness between interactions
Direct integration where the agent controls all aspects of the interaction

MCP, by contrast, offers:

A mediating layer between multiple agents and LLMs
Standardised communication formats that all agents understand
Persistent conversation state management
Role-based interactions where different agents can have specialised functions
Built-in mechanisms for handling complex workflows across multiple agents
Advantages of MCP
Enhanced Collaboration: Agents can work together on complex tasks, sharing information and delegating subtasks.
Specialisation: Agents can focus on their core competencies while leveraging other agents’ capabilities.
Scalability: Systems can grow to include more agents without redesigning the entire architecture.
Reliability: Standardised message formats reduce errors in inter-agent communication.
Flexibility: New agents can be added to existing ecosystems without disrupting workflows.
Better Orchestration: Complex tasks can be broken down and distributed across specialised agents.
Real-World Use Cases
Enterprise Knowledge Management

An MCP system could connect specialised agents for document retrieval, summarisation, fact-checking, and query refinement. When an employee asks a complex question, these agents collaborate to provide accurate, comprehensive answers by accessing various information sources while maintaining conversation context.

Healthcare Diagnostics Support

Multiple agents specialising in different medical domains (radiology, pathology, patient history analysis) can collaborate via MCP to provide integrated diagnostic support. Each agent processes specialised information before contributing to a collective analysis that helps physicians make informed decisions.

Supply Chain Optimisation

MCP can coordinate agents that monitor inventory levels, predict demand, analyse logistics constraints, and optimise pricing. These agents work together to maintain optimal inventory levels, suggest reordering strategies, and adapt to changing market conditions in real-time.

Customer Service Enhancement

An MCP-based system could include agents for sentiment analysis, product knowledge, troubleshooting, and escalation management. When a customer inquiry comes in, these agents collaborate to understand the issue, provide accurate information, and ensure appropriate handling based on the customer’s emotional state and the complexity of the problem.

MCP represents a significant evolution in how we architect multi-agent AI systems, enabling more sophisticated collaboration patterns that better leverage the capabilities of individual agents and the underlying LLMS they might utilise.

Traditional Agent-LLM Connection

A traditional agent-LLM connection is a simpler architecture where a single AI agent interfaces directly with a large language model to perform tasks. In this setup, the agent acts as a wrapper or controller that sends prompts to the LLM, processes the responses, and potentially takes actions based on those responses.

Key Characteristics:
Direct 1:1 connection between the agent and LLM
Simple request-response interaction pattern
The agent manages all context and task state
Limited or no collaboration with other agents
The agent interprets LLM outputs and converts them to actions
Example: Customer Support Chatbot

Here’s a concrete example of a traditional agent-LLM setup:

Imagine a customer support chatbot for an e-commerce website. The architecture would work like this:

User Query: A customer asks, “When will my order #12345 be delivered?”

Agent Processing: The agent:

Recognises this as an order status query
Retrieves order #12345 data from the database
Formats this information into a prompt

LLM Interaction: The agent sends a prompt to the LLM like:

User has order #12345 with status "shipped" on 04/15/2025, current location "Denver distribution center", estimated delivery date 04/20/2025. Respond to their question about delivery timing in a helpful, friendly manner.
Response Processing: The LLM generates a response, which the agent may format or filter before presenting it to the user.
Action Taking: If the user asks to change delivery options, the agent interprets the LLM’s understanding of this request and executes the appropriate API calls to the order management system.

In this traditional setup, a single agent handles all aspects of the interaction — database queries, prompt construction, LLM response processing, and action execution. The agent doesn’t collaborate with other specialised agents, and all context management happens within this single agent.

Get Saraswathi Lakshman’s stories in your inbox

Join Medium for free to get updates from this writer.

This differs from MCP, where multiple specialised agents might collaborate (e.g., one for order lookup, another for delivery estimation, another for customer sentiment analysis) through a standardised protocol, sharing context and working together to provide a more sophisticated response.

End-to-End MCP Implementation Example: Smart Home Assistant System
Press enter or click to view image in full size
End-to-End MCP Implementation Example: Smart Home Assistant System

Let me walk you through a complete end-to-end example of implementing an MCP-based system for a smart home assistant that helps users manage their home environment, schedule, and entertainment needs.

Use Case Overview

Our system will allow users to interact with a main assistant that coordinates between specialized agents for:

Home device control (lights, temperature, etc.)
Media recommendations and playback
Calendar management and scheduling
System Architecture
Components Implementation
1. MCP Server

This is the central hub that facilitates communication between agents. Let’s implement it using Node.js with Express: This is a test code.

// mcp-server.js
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;
// Store active conversations
let conversations = {};
app.use(bodyParser.json());
// Initialize a new conversation
app.post('/conversations', (req, res) => {
  const conversationId = generateId();
  conversations[conversationId] = {
    messages: [],
    activeAgents: [],
    metadata: {}
  };
  res.json({ conversationId });
});
// Send a message in a conversation
app.post('/conversations/:id/messages', (req, res) => {
  const { id } = req.params;
  const { fromAgent, toAgent, content, type } = req.body;
  
  if (!conversations[id]) {
    return res.status(404).json({ error: 'Conversation not found' });
  }
  
  const message = {
    id: generateId(),
    timestamp: Date.now(),
    fromAgent,
    toAgent,
    content,
    type
  };
  
  conversations[id].messages.push(message);
  
  // Notify target agent (in a real system, this would use websockets or polling)
  res.json({ messageId: message.id });
});
// Get messages for a specific agent
app.get('/conversations/:id/messages/:agent', (req, res) => {
  const { id, agent } = req.params;
  
  if (!conversations[id]) {
    return res.status(404).json({ error: 'Conversation not found' });
  }
  
  const messages = conversations[id].messages.filter(
    m => m.toAgent === agent || m.toAgent === 'all'
  );
  
  res.json({ messages });
});
app.listen(port, () => {
  console.log(`MCP Server running on port ${port}`);
});
function generateId() {
  return Math.random().toString(36).substring(2, 15);
}
2. Agent Implementation

Let’s create a base agent class that all specialized agents will extend:

// base-agent.js
const axios = require('axios');
class BaseAgent {
  constructor(agentId, mcpServerUrl) {
    this.agentId = agentId;
    this.mcpServerUrl = mcpServerUrl;
    this.conversations = {};
    this.llmClient = axios.create({
      baseURL: 'https://api.llm-provider.com/v1',
      headers: { 'Authorization': `Bearer ${process.env.LLM_API_KEY}` }
    });
  }
  
  async joinConversation(conversationId) {
    this.conversations[conversationId] = {
      lastMessageTimestamp: Date.now()
    };
    
    // Start polling for messages
    this.startPolling(conversationId);
  }
  
  async startPolling(conversationId) {
    setInterval(async () => {
      try {
        const response = await axios.get(
          `${this.mcpServerUrl}/conversations/${conversationId}/messages/${this.agentId}`
        );
        
        const messages = response.data.messages;
        const newMessages = messages.filter(
          m => m.timestamp > this.conversations[conversationId].lastMessageTimestamp
        );
        
        if (newMessages.length > 0) {
          this.conversations[conversationId].lastMessageTimestamp = 
            Math.max(...newMessages.map(m => m.timestamp));
          
          for (const message of newMessages) {
            await this.processMessage(conversationId, message);
          }
        }
      } catch (error) {
        console.error('Error polling for messages:', error);
      }
    }, 1000); // Poll every second
  }
  
  async sendMessage(conversationId, toAgent, content, type = 'text') {
    try {
      await axios.post(
        `${this.mcpServerUrl}/conversations/${conversationId}/messages`,
        {
          fromAgent: this.agentId,
          toAgent,
          content,
          type
        }
      );
    } catch (error) {
      console.error('Error sending message:', error);
    }
  }
  
  async queryLLM(prompt) {
    try {
      const response = await this.llmClient.post('/completions', {
        model: 'gpt-4',
        prompt,
        max_tokens: 500
      });
      return response.data.choices[0].text.trim();
    } catch (error) {
      console.error('Error querying LLM:', error);
      return 'I encountered an error processing your request.';
    }
  }
  
  async processMessage(conversationId, message) {
    // To be implemented by specialized agents
    console.log(`Received message: ${message.content}`);
  }
}
module.exports = BaseAgent;
3. Specialized Agent: Home Control Agent
// home-control-agent.js
const BaseAgent = require('./base-agent');
const smartHomeApi = require('./smart-home-api'); // Hypothetical API for smart home
class HomeControlAgent extends BaseAgent {
  constructor(mcpServerUrl) {
    super('home-control', mcpServerUrl);
    this.deviceStates = {};
  }
  
  async initialize() {
    // Get initial state of all devices
    this.deviceStates = await smartHomeApi.getAllDeviceStates();
  }
  
  async processMessage(conversationId, message) {
    if (message.type === 'query') {
      // Handle queries about device status
      if (message.content.includes('status')) {
        const deviceName = this.extractDeviceName(message.content);
        const status = await this.getDeviceStatus(deviceName);
        await this.sendMessage(conversationId, message.fromAgent, status);
      }
    } else if (message.type === 'command') {
      // Handle commands to control devices
      const { deviceName, action, parameters } = this.parseCommand(message.content);
      const result = await this.controlDevice(deviceName, action, parameters);
      await this.sendMessage(conversationId, message.fromAgent, result);
    }
  }
  
  extractDeviceName(content) {
    // Use LLM to extract device name from natural language
    const prompt = `Extract the device name from this query: "${content}"`;
    return this.queryLLM(prompt);
  }
  
  parseCommand(content) {
    // Parse a command using LLM
    const prompt = `
      Parse this command into JSON with deviceName, action, and parameters:
      "${content}"
      
      Example output:
      {
        "deviceName": "living room lights",
        "action": "dim",
        "parameters": {"level": 50}
      }
    `;
    
    const result = this.queryLLM(prompt);
    try {
      return JSON.parse(result);
    } catch (e) {
      return { error: "Could not parse command" };
    }
  }
  
  async getDeviceStatus(deviceName) {
    try {
      return await smartHomeApi.getDeviceStatus(deviceName);
    } catch (error) {
      return `Error getting status for ${deviceName}`;
    }
  }
  
  async controlDevice(deviceName, action, parameters) {
    try {
      await smartHomeApi.controlDevice(deviceName, action, parameters);
      this.deviceStates[deviceName] = await this.getDeviceStatus(deviceName);
      return `Successfully performed ${action} on ${deviceName}`;
    } catch (error) {
      return `Error controlling ${deviceName}`;
    }
  }
}
module.exports = HomeControlAgent;
4. Coordinator Agent

This agent is responsible for managing the conversation and delegating tasks to specialized agents:

// coordinator-agent.js
const BaseAgent = require('./base-agent');
class CoordinatorAgent extends BaseAgent {
  constructor(mcpServerUrl) {
    super('coordinator', mcpServerUrl);
    this.agentCapabilities = {
      'home-control': ['device status', 'control lights', 'adjust temperature'],
      'media': ['recommend movies', 'play music', 'search content'],
      'calendar': ['schedule events', 'check availability', 'set reminders']
    };
  }
  
  async processMessage(conversationId, message) {
    if (message.fromAgent === 'user') {
      // User messages need to be routed to appropriate agents
      const intent = await this.determineIntent(message.content);
      const targetAgent = this.determineTargetAgent(intent);
      
      if (targetAgent === 'multiple') {
        // Handle complex requests requiring multiple agents
        await this.handleComplexRequest(conversationId, message);
      } else if (targetAgent) {
        // Forward to appropriate specialized agent
        await this.sendMessage(
          conversationId, 
          targetAgent, 
          message.content, 
          intent.type
        );
      } else {
        // Handle directly if no specialized agent is needed
        const response = await this.generateResponse(message.content);
        await this.sendMessage(conversationId, 'user', response);
      }
    } else {
      // Handle responses from specialized agents
      if (message.toAgent === 'coordinator') {
        // Forward relevant information to user
        await this.sendMessage(conversationId, 'user', message.content);
      }
    }
  }
  
  async determineIntent(content) {
    const prompt = `
      Analyze this user request: "${content}"
      
      Respond with a JSON object containing:
      1. "intent": The primary user intent
      2. "type": Either "query" or "command"
      3. "requires": Array of required capabilities
      
      Example:
      {
        "intent": "turn on lights",
        "type": "command",
        "requires": ["control lights"]
      }
    `;
    
    const result = await this.queryLLM(prompt);
    try {
      return JSON.parse(result);
    } catch (e) {
      return { intent: "conversation", type: "query", requires: [] };
    }
  }
  
  determineTargetAgent(intent) {
    if (!intent.requires || intent.requires.length === 0) {
      return null; // Handle directly
    }
    
    // Find agents that can handle all required capabilities
    const capableAgents = Object.entries(this.agentCapabilities)
      .filter(([agent, capabilities]) => 
        intent.requires.every(req => capabilities.some(cap => cap.includes(req)))
      )
      .map(([agent]) => agent);
    
    if (capableAgents.length === 0) {
      return null;
    } else if (capableAgents.length === 1) {
      return capableAgents[0];
    } else {
      return 'multiple';
    }
  }
  
  async handleComplexRequest(conversationId, message) {
    // Break down complex requests that need multiple agents
    const plan = await this.createPlan(message.content);
    
    for (const step of plan) {
      await this.sendMessage(
        conversationId,
        step.agent,
        step.query,
        step.type
      );
    }
  }
  
  async createPlan(content) {
    const prompt = `
      Create a step-by-step plan to fulfill this request:
      "${content}"
      
      Return a JSON array of steps, where each step has:
      1. "agent": The agent to handle the step
      2. "query": The specific query for that agent
      3. "type": Either "query" or "command"
      
      Example:
      [
        {
          "agent": "calendar",
          "query": "Check if I'm free tomorrow at 8 PM",
          "type": "query"
        },
        {
          "agent": "media",
          "query": "Recommend a movie for tomorrow night",
          "type": "query"
        }
      ]
    `;
    
    const result = await this.queryLLM(prompt);
    try {
      return JSON.parse(result);
    } catch (e) {
      return [];
    }
  }
  
  async generateResponse(content) {
    const prompt = `
      Generate a helpful response to this user message:
      "${content}"
    `;
    return this.queryLLM(prompt);
  }
}
module.exports = CoordinatorAgent;
5. Main Application

Now, let’s create a main application file that ties everything together:

// main.js
const HomeControlAgent = require('./home-control-agent');
const MediaAgent = require('./media-agent'); // Implementation similar to HomeControlAgent
const CalendarAgent = require('./calendar-agent'); // Implementation similar to HomeControlAgent
const CoordinatorAgent = require('./coordinator-agent');
const MCP_SERVER_URL = 'http://localhost:3000';
async function startSystem() {
  // Initialize all agents
  const homeAgent = new HomeControlAgent(MCP_SERVER_URL);
  await homeAgent.initialize();
  
  const mediaAgent = new MediaAgent(MCP_SERVER_URL);
  await mediaAgent.initialize();
  
  const calendarAgent = new CalendarAgent(MCP_SERVER_URL);
  await calendarAgent.initialize();
  
  const coordinator = new CoordinatorAgent(MCP_SERVER_URL);
  
  console.log('All agents initialized and ready!');
}
startSystem().catch(console.error);
Message Flow Example

Let’s trace through a complete message flow for a user request: “Turn down the living room lights and play some relaxing music.”

User Request: The user’s request is sent from the UI to the MCP server.
MCP Routing: MCP routes the message to the Coordinator Agent.
Intent Analysis: The Coordinator Agent uses the LLM to analyze the intent:
{ "intent": "control home and play music", "type": "command", "requires": ["control lights", "play music"] }
Task Planning: The Coordinator identifies this requires multiple agents and creates a plan:
[ { "agent": "home-control", "query": "Turn down the living room lights", "type": "command" }, { "agent": "media", "query": "Play some relaxing music", "type": "command" } ]

Message Dispatching: The Coordinator sends messages to the respective agents through MCP.

Home Control Processing: The Home Control Agent:

Parses the command to identify device (“living room lights”), action (“dim”), and parameters (implicit low level)
Controls the smart home devices via the appropriate API
Sends a confirmation message back to the Coordinator

Media Agent Processing: The Media Agent:

Understands that relaxing music is requested
Selects an appropriate playlist or station
Activates the media system to play the content
Sends a confirmation to the Coordinator

Response Aggregation: The Coordinator collects responses from both agents and formulates a unified response to the user.

User Notification: The final response is sent to the user through the MCP server.

Implementation Considerations
Scaling and Deployment
Containerization: Each agent and the MCP server could be deployed as separate Docker containers.
Kubernetes: For larger implementations, use Kubernetes to manage container orchestration.
Serverless: For cost-efficiency, agents can be implemented as serverless functions triggered by MCP events.
Security
Authentication: Implement JWT-based authentication between agents and the MCP server.
Encryption: Encrypt all messages passing through the MCP server.
Rate Limiting: Add rate limiting to prevent abuse of the system.
Reliability
Message Persistence: Store messages in a durable database to survive service restarts.
Agent Health Monitoring: Implement health checks and automatic restarts for failed agents.
Idempotency: Ensure message processing is idempotent to handle potential duplicates.
Conclusion

This example demonstrates the core concepts of an MCP-based multi-agent system. The key advantages shown here include:

Separation of Concerns: Each agent focuses on its specific domain.
Flexible Communication: Agents can communicate directly through a standardised protocol.
Intelligent Coordination: The Coordinator Agent uses an LLM to determine the best approach to complex requests.
Extensibility: New agent types can be added without modifying existing agents.

While this is a simplified implementation, it illustrates the fundamental principles of MCP architecture that can be expanded to more complex and sophisticated real-world applications.

---
*Auto-collected for Prompt Engineering Course*
