# 📁 Project Structure

## Clean BTP Multi-Agent System Structure

```
BTP-MultiAgent/
├── 📄 README.md                    # Main documentation
├── 📄 README_BTP_EN.md             # Detailed BTP guide
├── 📄 QUICKSTART.md                # 5-minute setup
├── 📄 API_REFERENCE.md             # MCP tools documentation
├── 📄 PROJECT_SUMMARY.md           # Project overview
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📄 LICENSE                      # MIT License
│
├── 🔧 start_system.sh              # Startup script (Linux/Mac)
├── 🔧 stop_system.sh               # Shutdown script (Linux/Mac)
├── 🔧 start_system.bat             # Startup script (Windows)
│
├── 📁 backend/
│   ├── 📁 A2AServer/               # Core A2A framework
│   │   └── src/A2AServer/
│   │       ├── agent.py            # BasicAgent class
│   │       ├── task_manager.py    # AgentTaskManager
│   │       ├── common/
│   │       │   ├── server/        # A2A server implementation
│   │       │   ├── client/        # A2A client
│   │       │   └── A2Atypes.py    # Pydantic models
│   │       └── mcp_client/
│   │           ├── client.py      # MCP client (stdio/SSE)
│   │           └── providers/     # LLM providers
│   │               ├── openai.py
│   │               ├── deepseek.py
│   │               ├── anthropic.py
│   │               └── ... (8 providers)
│   │
│   ├── 📁 AgentArchitecte/         # ⭐ Architecture Agent
│   │   ├── main.py                 # Agent entry point
│   │   ├── prompt.txt              # Agent instructions
│   │   ├── mcp_config.json         # MCP configuration
│   │   ├── env_template.txt        # Environment template
│   │   └── mcpserver/
│   │       └── architecture_tools.py  # 5 MCP tools:
│   │           • validateBlueprintCompliance
│   │           • calculate3DVolume
│   │           • suggestMaterialsOptimization
│   │           • calculateStructuralLoad
│   │           • generateTechnicalReport
│   │
│   ├── 📁 AgentCoutEstimateur/     # ⭐ Cost Estimator Agent
│   │   ├── main.py
│   │   ├── prompt.txt
│   │   ├── mcp_config.json
│   │   ├── env_template.txt
│   │   └── mcpserver/
│   │       └── cost_estimation_tools.py  # 5 MCP tools:
│   │           • estimateMaterialCost
│   │           • calculateLaborHours
│   │           • trackBudgetDeviation
│   │           • generateCostBreakdown
│   │           • comparePriceAlternatives
│   │
│   └── 📁 AgentPlanning/           # ⭐ Planning Agent
│       ├── main.py
│       ├── prompt.txt
│       ├── mcp_config.json
│       ├── env_template.txt
│       └── mcpserver/
│           └── planning_tools.py        # 5 MCP tools:
│               • createGanttChart
│               • detectCriticalPath
│               • optimizeResourceAllocation
│               • simulateScenario
│               • generateMilestoneReport
│
├── 📁 frontend/
│   ├── 📁 hostAgentAPI/            # Multi-agent orchestrator
│   │   ├── api.py                  # FastAPI server
│   │   ├── server.py               # ConversationServer
│   │   ├── adk_host_manager.py    # ADK integration
│   │   ├── requirements.txt
│   │   └── hosts/
│   │       └── multiagent/
│   │           ├── host_agent.py   # Google ADK agent
│   │           └── remote_agent_connection.py
│   │
│   ├── 📁 multiagent_front/        # ⭐ React Multi-Agent UI
│   │   ├── package.json
│   │   ├── vite.config.js
│   │   └── src/
│   │       ├── App.jsx
│   │       ├── main.jsx
│   │       ├── components/
│   │       │   ├── ChatBubble.jsx
│   │       │   ├── Conversation.jsx
│   │       │   ├── AgentsTable.jsx
│   │       │   └── ... (10+ components)
│   │       ├── pages/
│   │       │   ├── Home.jsx
│   │       │   ├── ConversationPage.jsx
│   │       │   ├── AgentListPage.jsx
│   │       │   └── ... (7 pages)
│   │       ├── api/
│   │       │   └── api.js
│   │       └── store/
│   │           └── recoilState.js
│   │
│   └── 📁 single_agent/            # Single Agent UI (optional)
│       ├── package.json
│       └── src/
│           ├── App.jsx
│           ├── components/
│           └── services/
│               └── a2aApiService.js
│
└── 📁 logs/                         # Runtime logs (auto-created)
    ├── AgentArchitect.log
    ├── AgentCostEstimator.log
    ├── AgentPlanning.log
    ├── host_agent.log
    └── frontend.log
```

## 🎯 Key Components

### Backend Agents (Python)
- **Port 10005**: AgentArchitect - Building compliance & structure
- **Port 10004**: AgentCostEstimator - Budget & cost management
- **Port 10006**: AgentPlanning - Timeline & resource planning

### Frontend (React + Node.js)
- **Port 13000**: Host Agent API - Multi-agent orchestration
- **Port 5174**: React UI - User interface

### MCP Tools (FastMCP)
- **15 specialized tools** across 3 domains
- Python-based with FastMCP framework
- Automatically exposed to LLMs

## 📦 Dependencies

### Backend
- `A2AServer` - Core framework
- `fastmcp` - MCP tool framework
- `starlette` + `uvicorn` - ASGI server
- `pydantic` - Data validation
- `google-genai` - ADK support
- LLM clients: `openai`, `anthropic`, etc.

### Frontend
- `react` + `react-dom` - UI framework
- `@mui/material` - Component library
- `recoil` - State management
- `react-router-dom` - Routing
- `vite` - Build tool

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `.env` | API keys (per agent) |
| `prompt.txt` | Agent instructions |
| `mcp_config.json` | MCP tool configuration |
| `package.json` | Node.js dependencies |
| `requirements.txt` | Python dependencies |

## 🚀 Execution Flow

1. **User Query** → Frontend (Port 5174)
2. **Frontend** → Host Agent API (Port 13000)
3. **Host Agent** analyzes query → Routes to appropriate agent(s)
4. **Agent(s)** process via LLM → Call MCP tools
5. **MCP Tools** execute calculations → Return results
6. **Agent(s)** format response → Return to Host Agent
7. **Host Agent** → Frontend → User

## 📊 File Count Summary

- **Python files**: ~30
- **JavaScript/JSX files**: ~25
- **Configuration files**: ~15
- **Documentation files**: 6
- **MCP tools**: 15 functions
- **Total lines of code**: ~4,000+

## 🔒 .gitignore Recommendations

```gitignore
# Environment
.env
*.env

# Python
__pycache__/
*.pyc
*.egg-info/
dist/
build/

# Node
node_modules/
dist/
.vite/

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

**Last Updated**: January 2025
**Version**: 1.0.0
