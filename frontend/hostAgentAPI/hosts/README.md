## BTP Host Agent Components

Host components for the BTP Construction Management multi-agent system.

* [CLI](./cli)
  Command line interface to interact with individual BTP agents. Test architecture, cost, or planning agents directly from the terminal.

  **Usage:** Test a single BTP agent via command line
  ```bash
  cd hosts/cli
  uv run . --agent http://localhost:10005  # AgentArchitecte
  ```

* [Multi-Agent Orchestrator](./multiagent)
  Google ADK-based orchestration agent that coordinates the three BTP specialized agents. The Host Agent intelligently routes construction queries to the appropriate agent(s) and manages multi-agent conversations.

  **Features:**
  - Automatic agent routing based on query context
  - Coordination of Architecture, Cost, and Planning agents
  - Support for complex multi-step construction workflows
  - Task delegation and response aggregation

* [Web Frontend](../../multiagent_front)
  React-based web interface for the BTP multi-agent system. Provides visual conversation interface, agent registration, and real-time streaming responses.

  **Features:**
  - Multi-agent collaboration interface
  - Real-time tool execution visibility
  - Conversation history and state management
  - Responsive design for desktop and mobile

## BTP System Architecture

```
User Interface (Web/CLI)
        ↓
Host Agent Orchestrator
        ↓
┌───────────────┬────────────────┬──────────────┐
│ AgentArchitecte│ AgentCoutEstimateur│ AgentPlanning │
│   Port 10005   │   Port 10004       │ Port 10006    │
└───────────────┴────────────────┴──────────────┘
```

Refer to the [main documentation](../../../README.md) for complete setup instructions. 