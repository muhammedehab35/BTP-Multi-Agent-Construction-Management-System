## BTP Multi-Agent Orchestrator

Google ADK-based host agent that orchestrates the three BTP construction management agents over the A2A protocol.

## Overview

This orchestrator coordinates:
- **AgentArchitecte** (Port 10005): Architecture validation, calculations, materials
- **AgentCoutEstimateur** (Port 10004): Cost estimation, labor, budgets
- **AgentPlanning** (Port 10006): Scheduling, critical path, resources

## Prerequisites

- Python 3.12 or higher
- uv (Python package manager)
- All three BTP agents running

## Running the Orchestrator

1. **Start all BTP agents first:**
   ```bash
   # Terminal 1: AgentArchitecte
   cd backend/AgentArchitecte
   python main.py --port 10005

   # Terminal 2: AgentCoutEstimateur
   cd backend/AgentCoutEstimateur
   python main.py --port 10004

   # Terminal 3: AgentPlanning
   cd backend/AgentPlanning
   python main.py --port 10006
   ```

2. **Start the Host Agent orchestrator:**
   ```bash
   cd frontend/hostAgentAPI
   python api.py
   ```

3. **Register agents** (via API or web interface):
   ```bash
   curl -X POST http://localhost:13000/agent/register -H "Content-Type: application/json" -d '{"params": "http://localhost:10005"}'
   curl -X POST http://localhost:13000/agent/register -H "Content-Type: application/json" -d '{"params": "http://localhost:10004"}'
   curl -X POST http://localhost:13000/agent/register -H "Content-Type: application/json" -d '{"params": "http://localhost:10006"}'
   ```

## Intelligent Routing

The orchestrator automatically routes queries:
- **Architecture questions** → AgentArchitecte
- **Cost questions** → AgentCoutEstimateur
- **Planning questions** → AgentPlanning
- **Complex questions** → Multiple agents in sequence

## Documentation

For complete setup and usage, see:
- [Main README](../../../../README.md)
- [BTP Guide](../../../../README_BTP_EN.md)
- [Quick Start](../../../../QUICKSTART.md)