#!/bin/bash
# BTP Multi-Agent System Shutdown Script
# Usage: ./stop_system.sh

echo "🛑 Stopping BTP Multi-Agent System"
echo "===================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Stop a service
stop_service() {
    local service_name=$1
    local pid_file="logs/${service_name}.pid"

    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${YELLOW}⏹️  Stopping ${service_name} (PID: $pid)...${NC}"
            kill $pid
            sleep 2

            if ps -p $pid > /dev/null 2>&1; then
                echo -e "${RED}❌ Force stopping ${service_name}${NC}"
                kill -9 $pid
            fi

            rm "$pid_file"
            echo -e "${GREEN}✅ ${service_name} stopped${NC}"
        else
            echo -e "${YELLOW}⚠️  ${service_name} was not running${NC}"
            rm "$pid_file"
        fi
    else
        echo -e "${YELLOW}⚠️  No PID file found for ${service_name}${NC}"
    fi
}

# Stop all services
stop_service "frontend"
stop_service "host_agent"
stop_service "AgentPlanning"
stop_service "AgentCostEstimator"
stop_service "AgentArchitect"

# Clean up remaining processes on ports
echo ""
echo "🧹 Cleaning up ports..."
for port in 10005 10004 10006 13000 5174; do
    pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        echo -e "${YELLOW}⏹️  Releasing port $port (PID: $pid)${NC}"
        kill -9 $pid 2>/dev/null
    fi
done

echo ""
echo -e "${GREEN}✅ All services stopped${NC}"
echo "===================================="
