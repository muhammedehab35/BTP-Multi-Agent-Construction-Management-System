# 🚀 Quick Start Guide - BTP Multi-Agent System

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (2 min)

```bash
# Install Python dependencies
cd backend/A2AServer
pip install .

# Install uv (MCP tool manager)
pip install uv

# Install frontend dependencies
cd ../../frontend/multiagent_front
npm install
```

### Step 2: Configure API Keys (1 min)

Create `.env` file in each agent directory:

```bash
# AgentArchitect
echo "DEEPSEEK_API_KEY=your_key_here" > backend/AgentArchitect/.env

# AgentCostEstimator
echo "DEEPSEEK_API_KEY=your_key_here" > backend/AgentCostEstimator/.env

# AgentPlanning
echo "DEEPSEEK_API_KEY=your_key_here" > backend/AgentPlanning/.env

# Host Agent
echo "DEEPSEEK_API_KEY=your_key_here" > frontend/hostAgentAPI/.env
```

### Step 3: Start All Services (2 min)

**Option A: Manual Start (5 terminals)**

```bash
# Terminal 1 - AgentArchitect
cd backend/AgentArchitect && python main.py --port 10005

# Terminal 2 - AgentCostEstimator
cd backend/AgentCostEstimator && python main.py --port 10004

# Terminal 3 - AgentPlanning
cd backend/AgentPlanning && python main.py --port 10006

# Terminal 4 - Host Agent
cd frontend/hostAgentAPI && python api.py

# Terminal 5 - Frontend
cd frontend/multiagent_front && npm run dev
```

**Option B: Automated Script (Linux/Mac)**

```bash
chmod +x start_btp_system.sh
./start_btp_system.sh
```

**Option C: Windows Batch**

```cmd
start_btp_system.bat
```

### Step 4: Access the System

Open your browser: **http://localhost:5174**

## 🎯 First Test

### Test 1: Simple Question
```
Calculate the volume of concrete needed for a rectangular foundation:
Length: 20m, Width: 15m, Height: 1.5m
```

### Test 2: Multi-Agent Collaboration
```
I need to build a commercial building:
- 5 floors, 800m² total
- Budget: €350,000
- Start date: 2025-06-01

Validate compliance, estimate costs, and create a timeline.
```

## 📊 System Status Check

Verify all services are running:

```bash
# Check if ports are listening
curl http://localhost:10005/.well-known/agent.json  # AgentArchitect
curl http://localhost:10004/.well-known/agent.json  # AgentCostEstimator
curl http://localhost:10006/.well-known/agent.json  # AgentPlanning
curl http://localhost:13000/ping                     # Host Agent
curl http://localhost:5174                            # Frontend
```

## 🛑 Stop All Services

```bash
# Linux/Mac
./stop_btp_system.sh

# Manual (any OS)
# Find and kill processes on ports
lsof -ti:10005,10004,10006,13000,5174 | xargs kill
```

## 🔧 Common Issues

### Issue: Port already in use
```bash
# Find what's using the port
lsof -i :10005

# Kill the process
kill -9 <PID>
```

### Issue: API Key not working
```bash
# Verify .env file exists
cat backend/AgentArchitect/.env

# Test API key
curl -H "Authorization: Bearer YOUR_KEY" https://api.deepseek.com/v1/models
```

### Issue: Frontend can't connect to agents
```bash
# Check all agents are running
ps aux | grep python | grep main.py

# Check Host Agent is running
ps aux | grep python | grep api.py
```

## 📚 Next Steps

1. **Read full documentation**: [README_BTP_EN.md](README_BTP_EN.md)
2. **Explore agent capabilities**: Test each agent individually
3. **Customize prompts**: Edit `prompt.txt` files
4. **Add custom tools**: Extend MCP tools in `mcpserver/` directories

## 💡 Pro Tips

- **Use DeepSeek for cost-effectiveness**: `--provider deepseek --model deepseek-chat`
- **Test agents individually first**: Use single-agent mode before multi-agent
- **Monitor logs**: Check `logs/` directory for debugging
- **Customize prompts**: Adapt agent behavior to your needs

## 🎓 Learning Path

1. ✅ **Day 1**: Setup and basic queries
2. 📊 **Day 2**: Understand agent specializations
3. 🔧 **Day 3**: Add custom MCP tools
4. 🚀 **Day 4**: Deploy for real projects

## 🆘 Need Help?

- 📖 [Full Documentation](README_BTP_EN.md)
- 🐛 [Report Issues](https://github.com/your-repo/issues)
- 💬 [Ask Questions](https://github.com/your-repo/discussions)

---

**Ready to revolutionize construction management? Let's build! 🏗️**
