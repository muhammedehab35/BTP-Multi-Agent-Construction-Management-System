#!/bin/bash
# BTP Multi-Agent System Startup Script
# Usage: ./start_system.sh

echo "🏗️  Starting BTP Multi-Agent System"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check port availability
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${RED}❌ Port $port already in use${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Port $port available${NC}"
        return 0
    fi
}

# Start an agent
start_agent() {
    local agent_name=$1
    local agent_dir=$2
    local port=$3
    local log_file="logs/${agent_name}.log"

    echo -e "${BLUE}🚀 Starting ${agent_name} on port ${port}...${NC}"
    mkdir -p logs

    cd "$agent_dir"
    nohup python main.py --port "$port" > "../../$log_file" 2>&1 &
    local pid=$!
    echo $pid > "../../logs/${agent_name}.pid"
    cd ../..
    sleep 2

    if ps -p $pid > /dev/null; then
        echo -e "${GREEN}✅ ${agent_name} started (PID: $pid)${NC}"
        echo -e "   📄 Logs: $log_file"
        return 0
    else
        echo -e "${RED}❌ Failed to start ${agent_name}${NC}"
        cat "$log_file"
        return 1
    fi
}

# Check prerequisites
echo ""
echo "🔍 Checking prerequisites..."
echo "=============================="

if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python not found. Install Python 3.10+${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python installed: $(python --version)${NC}"

if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}⚠️  uv not found. Installing...${NC}"
    pip install uv
fi
echo -e "${GREEN}✅ uv installed${NC}"

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm not found. Install Node.js 16+${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm installed: $(npm --version)${NC}"

# Check ports
echo ""
echo "🔌 Checking ports..."
echo "===================="
check_port 10005 || exit 1
check_port 10004 || exit 1
check_port 10006 || exit 1
check_port 13000 || exit 1
check_port 5174 || exit 1

# Start backend agents
echo ""
echo "🏗️  Starting backend agents..."
echo "=============================="

start_agent "AgentArchitect" "backend/AgentArchitecte" 10005
start_agent "AgentCostEstimator" "backend/AgentCoutEstimateur" 10004
start_agent "AgentPlanning" "backend/AgentPlanning" 10006

echo ""
echo "⏳ Waiting for agent initialization (10s)..."
sleep 10

# Start Host Agent
echo ""
echo "🎯 Starting Host Agent Orchestrator..."
echo "======================================"
cd frontend/hostAgentAPI
nohup python api.py > ../../logs/host_agent.log 2>&1 &
HOST_PID=$!
echo $HOST_PID > ../../logs/host_agent.pid
cd ../..
sleep 3

if ps -p $HOST_PID > /dev/null; then
    echo -e "${GREEN}✅ Host Agent started (PID: $HOST_PID)${NC}"
else
    echo -e "${RED}❌ Failed to start Host Agent${NC}"
    cat logs/host_agent.log
    exit 1
fi

# Start frontend
echo ""
echo "🎨 Starting React Frontend..."
echo "=============================="
cd frontend/multiagent_front

if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
fi

nohup npm run dev > ../../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../../logs/frontend.pid
cd ../..
sleep 5

if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
else
    echo -e "${RED}❌ Failed to start Frontend${NC}"
    cat logs/frontend.log
    exit 1
fi

# Summary
echo ""
echo "================================================================"
echo -e "${GREEN}✅ BTP Multi-Agent System started successfully!${NC}"
echo "================================================================"
echo ""
echo "📊 Active services:"
echo "  🏛️  AgentArchitect      : http://localhost:10005"
echo "  💰 AgentCostEstimator   : http://localhost:10004"
echo "  📅 AgentPlanning        : http://localhost:10006"
echo "  🎯 Host Agent           : http://localhost:13000"
echo "  🎨 Frontend             : http://localhost:5174"
echo ""
echo "📝 Log files:"
echo "  📄 logs/AgentArchitect.log"
echo "  📄 logs/AgentCostEstimator.log"
echo "  📄 logs/AgentPlanning.log"
echo "  📄 logs/host_agent.log"
echo "  📄 logs/frontend.log"
echo ""
echo "🛑 To stop all services: ./stop_system.sh"
echo ""
echo -e "${BLUE}🌐 Open your browser: http://localhost:5174${NC}"
echo "================================================================"
