# 🏗️ BTP Host Agent API
**Multi-Agent Orchestration Service for Construction Project Management**

The Host Agent API coordinates the three BTP specialized agents (Architecture, Cost Estimation, and Planning) to provide intelligent routing and multi-agent collaboration.

# Getting Started

**Project Overview:**

This service provides the orchestration layer for the BTP multi-agent system. It:
- Registers and manages the three BTP agents
- Routes user queries to the appropriate agent(s)
- Coordinates multi-agent conversations
- Manages conversation state and message history
- Provides API endpoints for the frontend interface

**Quick Start:**

1.  **Environment Setup:**
    * Ensure you have Python 3.12+ installed
    * Install required dependencies:
        ```bash
        pip install -r requirements.txt
        ```

2.  **Configure API Keys:**
    * Set up your LLM provider API keys in environment variables or `.env` file
    * The Host Agent uses LLM for intelligent routing decisions

3.  **Start the API Service:**
    ```bash
    python api.py
    ```
    * The service starts on `http://localhost:13000` by default 

**API Interface Testing:**

The project includes a `test_api.py` script to test the functionality of each API endpoint. This script utilizes the `unittest` framework to send requests to each endpoint and verify the responses.

1.  **Run the Test Script:**
    * Ensure the API service is running successfully (see the "Start the API Service" step above).
    * In the project's root directory, execute the test script:
        ```bash
        python test_api.py
        ```
    * The test script will automatically run all test cases and output the test results for each endpoint, including status codes, response content, and execution time, helping you verify the API's usability.

**API Endpoint Documentation:**

The following are the API endpoints and their functionalities, analyzed from the `test_api.py` file:

* **`/ping` (GET)**
    * **Functionality:** Tests if the API service is running and healthy.
    * **Request Example:** `GET http://127.0.0.1:13000/ping`
    * **Response Example:** `"Pong"`

* **`/conversation/create` (POST)**
    * **Functionality:** Creates a new conversation.
    * **Request Body:** None
    * **Response Example:**
        ```json
        {
          "result": {
            "conversation_id": "unique_conversation_id_generated"
          }
        }
        ```

* **`/conversation/list` (POST)**
    * **Functionality:** Lists all current conversations.
    * **Request Body:** None
    * **Response Example:**
        ```json
        {
          "result": [
            "conversation_id_1",
            "conversation_id_2",
            ...
          ]
        }
        ```

* **`/message/send` (POST)**
    * **Functionality:** Sends a message to a specified conversation.
    * **Request Body (application/json):**
        ```json
        {
          "params": {
            "role": "user",
            "parts": [{"type": "text", "text": "Message content to send"}],
            "metadata": {"conversation_id": "target_conversation_id"}
          }
        }
        ```
    * **Response Example:**
        ```json
        {
          "result": {
            "message_id": "generated_message_id",
            "conversation_id": "corresponding_conversation_id"
          }
        }
        ```

* **`/message/list` (POST)**
    * **Functionality:** Lists all messages within a specified conversation.
    * **Request Body (application/json):**
        ```json
        {
          "params": "target_conversation_id"
        }
        ```
    * **Response Example:**
        ```json
        {
          "result": [
            {
              "metadata": {"message_id": "message_id_1", ...},
              "role": "user",
              "parts": [{"type": "text", "text": "message_content_1"}]
            },
            {
              "metadata": {"message_id": "message_id_2", ...},
              "role": "assistant",
              "parts": [{"type": "text", "text": "reply_content_1"}]
            },
            ...
          ]
        }
        ```

* **`/message/pending` (POST)**
    * **Functionality:** Retrieves messages that are currently being processed (pending).
    * **Request Body:** None
    * **Response Example:**
        ```json
        {
          "result": [
            ["conversation_id_1", "message_id_1"],
            ["conversation_id_2", "message_id_2"],
            ...
          ]
        }
        ```
        *Note: An empty `result` array indicates that there are no messages currently pending.*

* **`/events/get` (POST)**
    * **Functionality:** Retrieves a list of events that have occurred (e.g., new message events).
    * **Request Body:** None
    * **Response Example:**
        ```json
        {
          "result": [
            {"event_type": "new_message", "data": {...}},
            ...
          ]
        }
        ```
        *Note: The `result` may contain event information when new questions or interactions occur.*

* **`/task/list` (POST)**
    * **Functionality:** Lists the current tasks.
    * **Request Body:** None
    * **Response Example:**
        ```json
        {
          "result": [
            {"task_id": "task_id_1", "status": "running", ...},
            ...
          ]
        }
        ```

* **`/agent/register` (POST)**
    * **Functionality:** Registers a BTP agent with the Host Agent.
    * **Request Body (application/json):**
        ```json
        {
          "params": "http://localhost:10005"
        }
        ```
    * **BTP Agent Registration:**
        ```bash
        # Register AgentArchitecte
        curl -X POST http://localhost:13000/agent/register \
          -H "Content-Type: application/json" \
          -d '{"params": "http://localhost:10005"}'

        # Register AgentCoutEstimateur
        curl -X POST http://localhost:13000/agent/register \
          -H "Content-Type: application/json" \
          -d '{"params": "http://localhost:10004"}'

        # Register AgentPlanning
        curl -X POST http://localhost:13000/agent/register \
          -H "Content-Type: application/json" \
          -d '{"params": "http://localhost:10006"}'
        ```
    * **Response Example:**
        ```json
        {
          "result": "registration_result_information"
        }
        ```

* **`/agent/list` (POST)**
    * **Functionality:** Lists all registered BTP agents.
    * **Request Body:** None
    * **Response Example:**
        ```json
        {
          "result": [
            "http://localhost:10005",
            "http://localhost:10004",
            "http://localhost:10006"
          ]
        }
        ```

* **`/api_key/update` (POST)**
    * **Functionality:** Updates the API Key.
    * **Request Body (application/json):**
        ```json
        {
          "api_key": "new_api_key"
        }
        ```
    * **Response Example:**
        ```json
        {
          "status": "success"
        }
        ```
