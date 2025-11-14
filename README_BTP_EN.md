# 🏗️ Construction Project Management System - Multi-Agent BTP

## 📋 Overview

An intelligent construction project management system based on A2A-MCP architecture with three specialized collaborative agents:

- **🏛️ AgentArchitect**: Compliance validation, structural calculations, material optimization
- **💰 AgentCostEstimator**: Cost estimation, budget tracking, quotations
- **📅 AgentPlanning**: Planning, Gantt charts, resource management, timeline control

## ✨ Key Features

### Agent Architect
- ✅ Regulatory compliance validation (Building codes, Eurocodes, Accessibility)
- 📐 3D volume calculations (rectangular, cylindrical, pyramidal)
- 🧱 Material choice optimization (budget, ecology, climate)
- ⚖️ Structural load calculations
- 📄 Technical report generation

### Agent Cost Estimator
- 💵 Material cost estimation with market variability
- 👷 Labor hours calculation with social charges
- 📊 Real-time budget deviation tracking
- 📋 Detailed quotation generation
- 🔍 Price alternative comparison

### Agent Planning
- 📅 Automatic Gantt chart creation
- 🎯 Critical path detection
- 👥 Resource allocation optimization
- 🌦️ Scenario simulation (weather, delays)
- 🎉 Milestone tracking and alerts

## 🚀 Installation

### Prerequisites
```bash
- Python 3.10+
- Node.js 16+
- uv (Python package manager)
```

### 1. Backend Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/A2AServer-BTP.git
cd A2AServer-BTP

# Install A2AServer package
cd backend/A2AServer
pip install .

# Create .env files for each agent
cd ../AgentArchitect
cp env_template.txt .env
# Edit .env and add your API key

cd ../AgentCostEstimator
cp env_template.txt .env
# Edit .env

cd ../AgentPlanning
cp env_template.txt .env
# Edit .env
```

### 2. Frontend Installation

```bash
# Host Agent Orchestrator
cd frontend/hostAgentAPI
pip install -r requirements.txt

# Multi-Agent Interface
cd ../multiagent_front
npm install

# Single Agent Interface (optional)
cd ../single_agent
npm install
```

## 🎯 Quick Start

### Multi-Agent Mode (Recommended)

#### Terminal 1: Agent Architect
```bash
cd backend/AgentArchitect
python main.py --host localhost --port 10005 \
               --provider deepseek --model deepseek-chat
```

#### Terminal 2: Agent Cost Estimator
```bash
cd backend/AgentCostEstimator
python main.py --host localhost --port 10004 \
               --provider deepseek --model deepseek-chat
```

#### Terminal 3: Agent Planning
```bash
cd backend/AgentPlanning
python main.py --host localhost --port 10006 \
               --provider deepseek --model deepseek-chat
```

#### Terminal 4: Host Agent Orchestrator
```bash
cd frontend/hostAgentAPI
python api.py
# Accessible at http://localhost:13000
```

#### Terminal 5: React Frontend
```bash
cd frontend/multiagent_front
npm run dev
# Accessible at http://localhost:5174
```

### Single Agent Mode

To test a single agent:

```bash
# Terminal 1: Start an agent (e.g., Architect)
cd backend/AgentArchitect
python main.py --port 10005

# Terminal 2: Single Agent Frontend
cd frontend/single_agent
npm run dev
# Accessible at http://localhost:5173
```

## 📖 Usage Examples

### Example 1: Residential Project Validation

**Question to the multi-agent system:**
```
I want to build an 8-story residential building in Nice, France.
Total surface: 1200m², height: 25m.
Is it compliant? What budget should I expect? How long will it take?
```

**The system will:**
1. **AgentArchitect** validates compliance (seismic zone, height, accessibility)
2. **AgentCostEstimator** estimates materials + labor
3. **AgentPlanning** creates Gantt chart with project duration

### Example 2: House Material Optimization

**Question:**
```
Single-family house 150m², temperate climate, standard budget,
environmental priority. What materials for the walls?
```

**AgentArchitect Response:**
- Recommended material: Autoclaved aerated concrete
- Energy performance: Class B
- Climate adaptation: Insulation R≥4

### Example 3: Budget Deviation Analysis

**Question to AgentCostEstimator:**
```
Initial budget: €250,000
Spent to date: €180,000
Completion: 60%
Remaining estimate: €90,000
Analyze the budget deviation
```

**Response:**
- Projected final cost: €270,000
- Overrun: 8% (WARNING)
- Recommendations: Optimize remaining items

### Example 4: Complete Planning

**Question to AgentPlanning:**
```
Create a Gantt chart for:
- Foundations: 15 days (no dependencies)
- Load-bearing walls: 20 days (after foundations)
- Framework: 10 days (after walls)
- Roofing: 8 days (after framework)
Start date: 2025-04-01
```

**Response:**
- Total duration: 53 working days (76 calendar days)
- End date: 2025-06-16
- Critical path: Foundations → Walls → Framework → Roofing

## 🛠️ Advanced Configuration

### Changing LLM Model

**For OpenAI:**
```bash
python main.py --provider openai --model gpt-4o
```

**For Bytedance:**
```bash
python main.py --provider bytedance --model deepseek-v3
```

**For local VLLM server:**
```bash
# In .env
VLLM_API_KEY=your_key
VLLM_BASE_URL=http://localhost:8000/v1

# Startup
python main.py --provider vllm --model your_model
```

### Modifying Prompts

Agent prompts are located in:
```
backend/AgentArchitect/prompt.txt
backend/AgentCostEstimator/prompt.txt
backend/AgentPlanning/prompt.txt
```

Edit these files to adapt agent behavior.

### Adding MCP Tools

**Example: New tool for AgentArchitect**

1. Edit `backend/AgentArchitect/mcpserver/architecture_tools.py`

```python
@mcp.tool()
def checkEnergyCompliance(
    insulation_r_value: float,
    heating_system: str
) -> dict:
    """Check energy compliance RE2020"""
    # Your logic here
    return {"compliant": True, "class": "A"}
```

2. Restart the agent

The tool will be automatically available to the LLM!

## 📊 Technical Architecture

```
┌─────────────────────────────────────────┐
│      React Frontend (Multi-Agent)       │
│         Port: 5174                       │
└─────────────────────────────────────────┘
                  ↓ HTTP
┌─────────────────────────────────────────┐
│      Host Agent (FastAPI + ADK)         │
│         Port: 13000                      │
│  - Intelligent agent selection          │
│  - Multi-agent coordination             │
└─────────────────────────────────────────┘
          ↓              ↓              ↓
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ AgentArchi    │ │ AgentCost     │ │ AgentPlan     │
│ Port: 10005   │ │ Port: 10004   │ │ Port: 10006   │
│               │ │               │ │               │
│ • Compliance  │ │ • Materials   │ │ • Gantt       │
│ • Calculations│ │ • Labor       │ │ • Critical    │
│ • Materials   │ │ • Budget      │ │ • Resources   │
└───────────────┘ └───────────────┘ └───────────────┘
        ↓                  ↓                  ↓
┌───────────────────────────────────────────────────┐
│              MCP Tools (FastMCP)                   │
│  • architecture_tools.py                          │
│  • cost_estimation_tools.py                       │
│  • planning_tools.py                              │
└───────────────────────────────────────────────────┘
```

## 🧪 Testing MCP Tools

Each tool can be tested individually:

```bash
# Test AgentArchitect
cd backend/AgentArchitect/mcpserver
python architecture_tools.py

# Test AgentCostEstimator
cd backend/AgentCostEstimator/mcpserver
python cost_estimation_tools.py

# Test AgentPlanning
cd backend/AgentPlanning/mcpserver
python planning_tools.py
```

## 🐛 Troubleshooting

### Issue: Agent won't start
**Solution:** Check that `uv` is installed
```bash
pip install uv
```

### Issue: MCP tools not found
**Solution:** Verify MCP configuration
```bash
cd backend/AgentXXX
cat mcp_config.json
# Verify the script path is correct
```

### Issue: Frontend connection error
**Solution:** Verify all services are running
```bash
# Check ports
netstat -an | grep 10005  # AgentArchitect
netstat -an | grep 10004  # AgentCostEstimator
netstat -an | grep 10006  # AgentPlanning
netstat -an | grep 13000  # Host Agent
```

### Issue: Invalid API keys
**Solution:** Check .env files
```bash
cd backend/AgentXXX
cat .env
# Ensure DEEPSEEK_API_KEY (or other) is set
```

## 📈 Future Improvements

- [ ] Database integration for project history
- [ ] PDF export for quotes and reports
- [ ] Interactive Gantt visualization in frontend
- [ ] Public REST API for ERP integration
- [ ] Document management module (plans, photos)
- [ ] Advanced structural calculations (FEM analysis)
- [ ] BIM 3D modeling tool integration
- [ ] Project performance analytics dashboard

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create a branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is under MIT license. See [LICENSE](LICENSE) for details.

## 👥 Authors

- **Original A2A-MCP System**: [johnson7788](https://github.com/johnson7788/A2AServer)
- **BTP Adaptation**: Your Team

## 📞 Support

- 🐛 [GitHub Issues](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)
- 📧 Email: support@your-domain.com

---

**🏗️ Built with ❤️ to revolutionize construction project management**
