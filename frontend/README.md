# 🏗️ BTP Construction Management - Frontend Interface

This project provides user interfaces for the BTP (Construction Project Management) multi-agent system. It supports both single-agent testing and multi-agent collaboration modes.

## 📁 Project Structure
* **hostAgentAPI**: Central orchestration API coordinating the three BTP agents
* **multiagent_front**: Multi-agent collaboration interface for full BTP workflow
* **single_agent**: Single-agent testing interface for individual agent testing

## 🚀 Quick Start

### 1. Multi-Agent Mode (Full BTP System)

#### 1. Start the Three BTP Agents

Start AgentArchitecte:
```bash
cd backend/AgentArchitecte
python main.py --port 10005
```

Start AgentCoutEstimateur:
```bash
cd backend/AgentCoutEstimateur
python main.py --port 10004
```

Start AgentPlanning:
```bash
cd backend/AgentPlanning
python main.py --port 10006
```

#### 2. Start the Host Agent
The Host Agent coordinates all three BTP agents:
```bash
cd hostAgentAPI
pip install -r requirements.txt
python api.py
```

#### 3. Start the Frontend
```bash
cd multiagent_front
npm install
npm run dev
```

#### 4. Configure BTP Agents in the Web Interface
- Open the frontend at `http://localhost:5174`
- Register the three agents:
  - **AgentArchitecte**: `http://localhost:10005`
  - **AgentCoutEstimateur**: `http://localhost:10004`
  - **AgentPlanning**: `http://localhost:10006`
- Start asking construction-related questions

**Example Questions:**
- "I need to build a 3-story residential building. Can you validate compliance and estimate costs?"
- "Create a project schedule for a 500m² commercial building"
- "Suggest optimized materials for a sustainable housing project"

### 2. Single Agent Testing Mode

#### 1. Start One BTP Agent
Example with AgentArchitecte:
```bash
cd backend/AgentArchitecte
python main.py --port 10005
```

#### 2. Start the Frontend
```bash
cd single_agent
npm install
npm run dev
```

#### 3. Test Individual Agent
- Open the frontend page
- Enter agent URL: `http://localhost:10005`
- Test specific architecture tools and capabilities

## 💡 BTP System Features
- **Three Specialized Agents**: Architecture, Cost Estimation, and Planning
- **15 MCP Tools**: 5 tools per agent for construction management
- **Multi-Agent Orchestration**: Intelligent routing between agents
- **Real Construction Data**: Actual material prices, labor rates, and building codes
- **Comprehensive Workflow**: From design validation to cost estimation to project scheduling

## 📌 Important Notes
- Default ports: AgentArchitecte (10005), AgentCoutEstimateur (10004), AgentPlanning (10006)
- Ensure all ports are available before starting
- Configure API keys in each agent's `.env` file
- Use the automated startup scripts for quick deployment:
  - Linux/Mac: `./start_system.sh`
  - Windows: `start_system.bat`

## 📚 Documentation
- [Main README](../README.md) - Project overview
- [BTP Guide](../README_BTP_EN.md) - Detailed BTP system documentation
- [Quick Start](../QUICKSTART.md) - 5-minute setup guide
- [API Reference](../API_REFERENCE.md) - Complete tool documentation