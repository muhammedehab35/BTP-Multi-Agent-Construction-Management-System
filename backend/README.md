# 🏗️ BTP Construction Management - Backend Agents

This guide explains the backend architecture for the BTP (Construction Project Management) multi-agent system.

---

## 📂 Project Structure

```
backend
├── A2AServer              # Core A2A Server framework
├── AgentArchitecte        # Architecture Agent (Port 10005)
├── AgentCoutEstimateur    # Cost Estimation Agent (Port 10004)
└── AgentPlanning          # Planning Agent (Port 10006)
```

---

## 🤖 BTP Agents Overview

### 1. AgentArchitecte (Port 10005)
**Expert in architecture and building design**

**MCP Tools:**
- `validateBlueprintCompliance` - Validate project compliance with building codes
- `calculate3DVolume` - Calculate volumes and material estimates
- `suggestMaterialsOptimization` - Suggest optimized materials
- `analyzeBuildingLoad` - Analyze structural loads
- `checkEnergyEfficiency` - Check energy efficiency compliance

**Directory Structure:**
```
AgentArchitecte
├── .env                # API keys for LLM providers
├── main.py             # Agent entry point
├── mcp_config.json     # MCP tools configuration
├── mcpserver/          # MCP Server implementation
│   └── architecture_tools.py  # 5 architecture tools
└── prompt.txt          # Agent system prompt
```

### 2. AgentCoutEstimateur (Port 10004)
**Expert in construction cost estimation**

**MCP Tools:**
- `estimateMaterialCost` - Estimate material costs with market variability
- `calculateLaborHours` - Calculate labor hours and costs
- `trackBudgetStatus` - Track budget vs actual spending
- `compareSupplierPrices` - Compare prices from multiple suppliers
- `generateCostReport` - Generate detailed cost reports

### 3. AgentPlanning (Port 10006)
**Expert in project planning and scheduling**

**MCP Tools:**
- `createGanttChart` - Create Gantt charts with dependencies
- `detectCriticalPath` - Identify critical path using CPM
- `optimizeResourceAllocation` - Optimize resource allocation
- `generateWeeklySchedule` - Generate weekly work schedules
- `analyzeProjectDelay` - Analyze delays and mitigation strategies

---

## 🛠️ Developing Your Own Agent

Follow these steps to create a custom Agent for the BTP system:

### 1. Copy an Existing Agent Directory
Use any of the three agents as a template:

```bash
cp -r AgentArchitecte MyNewAgent
cd MyNewAgent
```

### 2. Customize Your Agent
- **Update `.env`**: Add your API keys (DeepSeek, OpenAI, etc.)
- **Modify `main.py`**: Change agent name, port, and description
- **Configure `mcp_config.json`**: Define your MCP tools
- **Create Tools in `mcpserver/`**: Implement your specialized tools
- **Edit `prompt.txt`**: Customize the agent's role and behavior

### 3. Start Your Agent
```bash
python main.py --port 10007 --model deepseek-chat --provider deepseek
```

---

## 🧪 Testing Agents

### Option 1: Frontend Testing
1. Start all agents using the startup script:
   ```bash
   ./start_system.sh  # Linux/Mac
   start_system.bat   # Windows
   ```
2. Open browser to `http://localhost:5174`
3. Test agent interactions through the UI

### Option 2: Individual Agent Testing
Test a single agent using the frontend:
```bash
cd frontend/single_agent
npm install
npm run dev
```

---

## ⚠️ Important Notes

- **Tool Naming**: Use camelCase or PascalCase (e.g., `validateCompliance`, not `validate_compliance`)
- **Port Configuration**: Each agent must run on a unique port
- **API Keys**: Configure `.env` files for each agent before starting
- **MCP Tools**: All tools must be defined in `mcp_config.json` and implemented in `mcpserver/`

---

## 💡 Next Steps
- Explore the three BTP agents to understand implementation patterns
- Extend agents by adding more specialized MCP tools
- Integrate with the Host Agent for multi-agent orchestration
- Refer to [API_REFERENCE.md](../API_REFERENCE.md) for complete tool documentation