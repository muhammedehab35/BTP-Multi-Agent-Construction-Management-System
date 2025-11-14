# 🏗️ BTP Multi-Agent Frontend
**Construction Project Management System Interface**

This application provides a user interface for the BTP (Construction Project Management) multi-agent system, enabling collaboration between three specialized agents: Architecture, Cost Estimation, and Planning.

## Quick Start

### Prerequisites

- Node.js (v18+) and npm installed
- Three BTP agents running on ports 10004, 10005, 10006
- Host Agent API running on port 13000

### Install Dependencies

```bash
npm install
```

### Configure Environment Variables

Check the `.env` file in the project's root directory:
```env
REACT_APP_HOSTAGENT_API=http://127.0.0.1:13000
```

If your HostAgentAPI is on a different port, modify the `.env` file accordingly.

### Start the Application

```bash
npm run dev
```

The application will open at `http://localhost:5174` (or the address shown in console).

## Using the BTP System

### 1. Register the Three BTP Agents

After opening the frontend, register each agent:

- **AgentArchitecte**: `http://localhost:10005`
  - Validates compliance, calculates volumes, suggests materials

- **AgentCoutEstimateur**: `http://localhost:10004`
  - Estimates costs, calculates labor, tracks budgets

- **AgentPlanning**: `http://localhost:10006`
  - Creates schedules, identifies critical paths, allocates resources

### 2. Ask Construction Questions

The system intelligently routes questions to the appropriate agent(s):

**Architecture Questions:**
- "Validate compliance for a 5-story residential building"
- "Calculate concrete volume needed for a 1000m² foundation"
- "Suggest sustainable materials for a commercial building"

**Cost Questions:**
- "Estimate material costs for 200m³ of concrete"
- "Calculate labor hours for electrical work on 500m²"
- "Compare supplier prices for steel reinforcement"

**Planning Questions:**
- "Create a Gantt chart for a 6-month construction project"
- "Identify the critical path for foundation and framing tasks"
- "Generate a weekly schedule for the construction crew"

### 3. Multi-Agent Collaboration

For complex questions, multiple agents work together:
- "I need to build a 3-story office building. Validate design, estimate costs, and create a schedule."

## Features

- **Real-time Streaming**: See agent responses as they're generated
- **Multi-Agent Coordination**: Intelligent routing between specialized agents
- **Tool Execution Visibility**: Watch MCP tools being called in real-time
- **Conversation History**: Track all interactions and decisions
- **Responsive Design**: Works on desktop and mobile devices

## 📚 Related Documentation

- [Main README](../../README.md) - Project overview
- [BTP System Guide](../../README_BTP_EN.md) - Detailed BTP documentation
- [API Reference](../../API_REFERENCE.md) - Complete tool documentation
- [Quick Start Guide](../../QUICKSTART.md) - 5-minute setup