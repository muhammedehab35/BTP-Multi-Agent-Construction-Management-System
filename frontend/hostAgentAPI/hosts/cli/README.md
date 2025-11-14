## BTP CLI Client

Command-line interface for testing individual BTP agents. This tool demonstrates A2AClient capabilities with text-based collaboration and streaming support.

## Features

- Reads agent's AgentCard for capabilities discovery
- Text-based conversation with BTP agents
- Streaming responses (if supported by agent)
- Direct tool testing and debugging

## Prerequisites

- Python 3.12 or higher
- UV package manager
- At least one running BTP agent

## Running the CLI

### Test AgentArchitecte (Architecture)
```bash
cd frontend/hostAgentAPI/hosts/cli
uv run . --agent http://localhost:10005
```

**Example queries:**
- "Validate compliance for a 3-story residential building"
- "Calculate concrete volume for 20m x 15m x 0.5m foundation"
- "Suggest sustainable materials for office building"

### Test AgentCoutEstimateur (Cost Estimation)
```bash
uv run . --agent http://localhost:10004
```

**Example queries:**
- "Estimate material costs for 150m³ concrete"
- "Calculate labor hours for masonry on 300m²"
- "Track budget: allocated $200k, spent $150k"

### Test AgentPlanning (Planning)
```bash
uv run . --agent http://localhost:10006
```

**Example queries:**
- "Create Gantt chart for foundation, framing, roofing"
- "Detect critical path with excavation 5d, foundation 10d"
- "Generate weekly schedule for construction crew"

## Usage Tips

- Use streaming for real-time responses
- Check agent card to see available tools
- Test individual MCP tools before multi-agent scenarios
- View detailed command line options in source code

## Documentation

For more information:
- [Backend Development](../../../../backend/README.md)
- [API Reference](../../../../API_REFERENCE.md)
- [Single Agent Testing](../../../single_agent/README.md) 
