# 🏗️ BTP Single Agent Testing Interface

This interface allows you to test individual BTP agents in isolation, perfect for debugging and development.

## Quick Start

### Prerequisites

- Node.js (v18+) and npm installed
- One BTP agent running (on port 10004, 10005, or 10006)

### Installation

```bash
npm install
```

### Start the Application

```bash
npm run dev
```

The application will open at `http://localhost:5173`.

## Testing Individual Agents

### 1. Start a Single Agent

**AgentArchitecte** (Port 10005):
```bash
cd backend/AgentArchitecte
python main.py --port 10005
```

**AgentCoutEstimateur** (Port 10004):
```bash
cd backend/AgentCoutEstimateur
python main.py --port 10004
```

**AgentPlanning** (Port 10006):
```bash
cd backend/AgentPlanning
python main.py --port 10006
```

### 2. Connect in the Interface

In the web interface, enter the agent URL:
- `http://localhost:10005` (AgentArchitecte)
- `http://localhost:10004` (AgentCoutEstimateur)
- `http://localhost:10006` (AgentPlanning)

### 3. Test Agent Tools

**Testing AgentArchitecte:**
- "Validate compliance for a 3-story residential building with 500m² total surface"
- "Calculate concrete volume for a rectangular foundation 20m x 15m x 0.5m"
- "Suggest materials for a sustainable office building in temperate climate"
- "Analyze building loads for a 5-story steel structure"
- "Check energy efficiency for RT2020 compliance"

**Testing AgentCoutEstimateur:**
- "Estimate cost for 150m³ of concrete with transport to urban location"
- "Calculate labor hours for masonry work on 300m² wall surface"
- "Compare supplier prices for 5000kg of steel reinforcement"
- "Track budget status: allocated $200,000, spent $150,000"
- "Generate cost report for foundation phase"

**Testing AgentPlanning:**
- "Create Gantt chart for foundation, framing, and roofing tasks"
- "Detect critical path for excavation (5d) → foundation (10d) → framing (15d)"
- "Optimize resource allocation for 3 masons and 2 electricians"
- "Generate weekly schedule for week 3 of construction"
- "Analyze delay impact if foundation takes 3 extra days"

## Features

- **Direct Tool Testing**: Test MCP tools without multi-agent coordination
- **Real-time Responses**: See streaming responses from the agent
- **Tool Call Visibility**: View which tools are being invoked
- **Conversation History**: Track your testing session
- **Error Debugging**: Easily identify issues with individual tools

## Use Cases

- **Development**: Test new tools during agent development
- **Debugging**: Isolate and fix issues with specific tools
- **Tool Validation**: Verify tool behavior and outputs
- **Performance Testing**: Measure individual agent response times
- **Documentation**: Generate examples for tool documentation

## Form Interaction Support

This interface supports interactive forms for complex tool inputs:
- When an agent requires additional input, a form is automatically rendered
- Fill in missing fields and submit to continue the conversation
- Maintains conversation context throughout form interactions

## 📚 Related Documentation

- [Main README](../../README.md) - Project overview
- [Backend README](../../backend/README.md) - Agent development guide
- [API Reference](../../API_REFERENCE.md) - Complete tool documentation