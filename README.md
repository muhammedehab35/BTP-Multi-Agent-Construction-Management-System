# 🏗️ BTP Multi-Agent Construction Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 16+](https://img.shields.io/badge/node-16+-green.svg)](https://nodejs.org/)

> **An intelligent construction project management system powered by AI agents using the A2A-MCP protocol**

## 🌟 Overview

This system features **three specialized AI agents** working collaboratively to manage construction projects:

- 🏛️ **AgentArchitect** - Compliance validation, structural calculations, material optimization
- 💰 **AgentCostEstimator** - Cost estimation, budget tracking, quotation generation
- 📅 **AgentPlanning** - Gantt charts, critical path analysis, resource optimization

Built on Google's [Agent-to-Agent (A2A) protocol](https://google.github.io/A2A/) with [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) integration.

## ✨ Key Features

### 15 Specialized MCP Tools
- **5 Architecture Tools**: Compliance, volumes, materials, loads, reports
- **5 Cost Tools**: Materials, labor, budget tracking, quotes, comparisons
- **5 Planning Tools**: Gantt, critical path, resources, scenarios, milestones

### Multi-LLM Support
- DeepSeek, OpenAI, Anthropic, Ollama, VLLM, Bytedance, Zhipu, LMStudio

### Production Ready
- ✅ Real construction logic and calculations
- ✅ Error handling and validation
- ✅ Streaming responses (SSE)
- ✅ Multi-agent collaboration
- ✅ Comprehensive documentation

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.10+
Node.js 16+
uv (pip install uv)
```

### Installation

```bash
# 1. Clone repository
git clone https://github.com/muhammedehab35/BTP-Multi-Agent-Construction-Management-System.git
cd BTP-MultiAgent

# 2. Install A2AServer
cd backend/A2AServer
pip install .

# 3. Configure API keys
cd ../AgentArchitecte
cp env_template.txt .env
# Edit .env and add: DEEPSEEK_API_KEY=your_key_here

cd ../AgentCoutEstimateur
cp env_template.txt .env
# Edit .env

cd ../AgentPlanning
cp env_template.txt .env
# Edit .env

# 4. Install frontend dependencies
cd ../../frontend/multiagent_front
npm install
```

### Start System

**Linux/Mac:**
```bash
chmod +x start_system.sh
./start_system.sh
```

**Windows:**
```cmd
start_system.bat
```

**Manual Start (5 terminals):**
```bash
# Terminal 1: AgentArchitect
cd backend/AgentArchitecte && python main.py --port 10005

# Terminal 2: AgentCostEstimator
cd backend/AgentCoutEstimateur && python main.py --port 10004

# Terminal 3: AgentPlanning
cd backend/AgentPlanning && python main.py --port 10006

# Terminal 4: Host Agent
cd frontend/hostAgentAPI && python api.py

# Terminal 5: Frontend
cd frontend/multiagent_front && npm run dev
```

### Access
Open your browser: **http://localhost:5174**

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [README_BTP_EN.md](README_BTP_EN.md) | Complete system documentation |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide |
| [API_REFERENCE.md](API_REFERENCE.md) | All MCP tools documentation |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project overview & statistics |

## 💡 Usage Examples

### Example 1: Volume Calculation
```
Calculate concrete volume for a rectangular foundation:
Length: 20m, Width: 15m, Height: 1.5m
```

### Example 2: Cost Estimation
```
Estimate costs for building a 5-floor office:
- Total surface: 800m²
- Budget: €350,000
- Location: Urban area
```

### Example 3: Project Planning
```
Create Gantt chart:
- Foundations: 15 days (no dependencies)
- Walls: 20 days (after foundations)
- Roofing: 8 days (after walls)
Start: 2025-06-01
```

### Example 4: Compliance Check
```
Validate compliance for:
- 8-story residential building
- Height: 25m, Surface: 1200m²
- Location: Nice (seismic zone)
```

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│   React Frontend (Multi-Agent)  │
│          Port: 5174              │
└─────────────────────────────────┘
              ↓ HTTP
┌─────────────────────────────────┐
│  Host Agent (FastAPI + ADK)     │
│          Port: 13000             │
└─────────────────────────────────┘
       ↓          ↓          ↓
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Architect│ │  Cost   │ │Planning │
│  :10005  │ │ :10004  │ │ :10006  │
└─────────┘ └─────────┘ └─────────┘
       ↓          ↓          ↓
┌─────────────────────────────────┐
│       MCP Tools (FastMCP)        │
│  • architecture_tools.py         │
│  • cost_estimation_tools.py      │
│  • planning_tools.py             │
└─────────────────────────────────┘
```

## 🛠️ Configuration

### Change LLM Provider

```bash
# OpenAI
python main.py --provider openai --model gpt-4o

# Bytedance
python main.py --provider bytedance --model deepseek-v3

# Local VLLM
python main.py --provider vllm --model your_model
```

### Customize Agent Behavior

Edit prompt files:
- `backend/AgentArchitecte/prompt.txt`
- `backend/AgentCoutEstimateur/prompt.txt`
- `backend/AgentPlanning/prompt.txt`

### Add Custom MCP Tools

1. Edit `backend/Agent*/mcpserver/*_tools.py`
2. Add your tool with `@mcp.tool()` decorator
3. Restart agent - tool is automatically available!

## 🧪 Testing

### Test Individual Tools
```bash
cd backend/AgentArchitecte/mcpserver
python architecture_tools.py
```

### Test Agents
```bash
# Single agent mode
cd backend/AgentArchitecte
python main.py --port 10005

# Then access: http://localhost:5173
```

### Verify Services
```bash
curl http://localhost:10005/.well-known/agent.json
curl http://localhost:10004/.well-known/agent.json
curl http://localhost:10006/.well-known/agent.json
```

## 📊 Project Statistics

- **3 Specialized Agents**
- **15 MCP Tools**
- **8 LLM Providers Supported**
- **4 Documentation Guides**
- **~4,000 Lines of Code**

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Agent won't start
```bash
# Check uv installation
pip install uv

# Verify .env file
cat backend/AgentArchitecte/.env
```

### Port already in use
```bash
# Find and kill process
lsof -ti:10005 | xargs kill -9
```

### Frontend connection error
```bash
# Check all services running
ps aux | grep python | grep main.py
```

See [QUICKSTART.md](QUICKSTART.md) for more troubleshooting tips.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **BTP Multi-Agent System**: [muhammedehab35](https://github.com/muhammedehab35)

## 🙏 Acknowledgments

- [Google A2A Project](https://github.com/google/A2A)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)

## 📞 Support

- 🐛 [Report Issues](https://github.com/muhammedehab35/BTP-MultiAgent/issues)
- 💬 [Discussions](https://github.com/muhammedehab35/BTP-MultiAgent/discussions)

---

**Built with ❤️ to revolutionize construction project management**

🌟 Star this repo if you find it useful!
