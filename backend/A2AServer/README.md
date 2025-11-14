# A2A Server Framework

Core framework for building Agent-to-Agent (A2A) communication servers.

## Installation

### 1. Create Python Environment

```bash
conda create --name adk python=3.12
conda activate adk
```

### 2. Install Dependencies

**For development:**
```bash
pip install -e .
```

**For production:**
```bash
pip install .
```

## Usage

This package is used by all BTP agents as the core A2A communication framework. It provides:

- **A2AServer**: Base server class for agent communication
- **BasicAgent**: Agent implementation with MCP tool support
- **AgentCard**: Agent metadata and capability description
- **SSE Support**: Server-Sent Events for streaming responses
- **Multi-provider LLM**: Support for 8+ LLM providers via LiteLLM

## Documentation

Refer to the [Backend README](../README.md) for complete development guide.
