import click
import os
import sys
import logging
from A2AServer.common.server import A2AServer
from A2AServer.common.A2Atypes import AgentCard, AgentCapabilities, AgentSkill, MissingAPIKeyError
from A2AServer.task_manager import AgentTaskManager
from A2AServer.agent import BasicAgent
from dotenv import load_dotenv

load_dotenv()

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@click.command(help="Start the BTP Planning Agent for project planning and optimization")
@click.option("--host", "host", default="localhost", help="Server address")
@click.option("--port", "port", default=10006, help="Listening port (default: 10006)")
@click.option("--prompt", "agent_prompt_file", default="prompt.txt", help="Prompt file")
@click.option("--model", "model_name", default="deepseek-chat", help="LLM model")
@click.option("--provider", "provider", default="deepseek", help="LLM provider")
@click.option("--mcp_config", "mcp_config_path", default="mcp_config.json", help="MCP config")
@click.option("--agent_url", "agent_url", default="", help="Public URL")
def main(host, port, agent_prompt_file, model_name, provider, mcp_config_path, agent_url=""):
    """Start the BTP Planning Agent"""
    input_mode, output_mode = ["text", "text/plain"], ["text", "text/plain"]
    BasicAgent.SUPPORTED_CONTENT_TYPES = input_mode

    try:
        capabilities = AgentCapabilities(streaming=True)
        skill = AgentSkill(
            id="BTPPlanning",
            name="BTP Planning Expert",
            description="Specialized agent for project planning: Gantt diagrams, critical paths, resource optimization, and schedule management",
            tags=["btp", "planning", "gantt", "resources", "deadlines"],
            examples=[
                "Create a Gantt diagram for a construction project",
                "Identify the critical path in a construction schedule",
                "Optimize resource allocation on a construction site",
                "Simulate the impact of a delivery delay on the schedule"
            ]
        )

        if not agent_url:
            agent_url = f"http://{host}:{port}/"

        agent_card = AgentCard(
            name="AgentPlanning",
            description="BTP Planning Expert: Gantt charts, critical paths, resource optimization, scenario simulation, and milestone tracking",
            url=agent_url,
            version="1.0.0",
            defaultInputModes=input_mode,
            defaultOutputModes=output_mode,
            capabilities=capabilities,
            skills=[skill],
        )

        print(f"📅 Starting BTP Planning Agent")
        print(f"📋 AgentCard: {agent_card}")

        agent = BasicAgent(
            config_path=mcp_config_path,
            model_name=model_name,
            prompt_file=agent_prompt_file,
            provider=provider
        )

        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=agent),
            host=host,
            port=port,
        )

        logger.info(f"🚀 Planning Agent started on {host}:{port}")
        server.start()

    except MissingAPIKeyError as e:
        logger.error(f"❌ Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
        exit(1)

if __name__ == "__main__":
    main()
