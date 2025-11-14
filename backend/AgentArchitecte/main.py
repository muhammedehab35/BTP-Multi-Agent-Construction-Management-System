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


@click.command(help="Start the BTP Architecture Agent for construction project analysis")
@click.option("--host", "host", default="localhost", help="Server address (default: localhost)")
@click.option("--port", "port", default=10005, help="Listening port (default: 10005)")
@click.option("--prompt", "agent_prompt_file", default="prompt.txt", help="Agent prompt file")
@click.option("--model", "model_name", default="deepseek-chat", help="LLM model to use")
@click.option("--provider", "provider", default="deepseek", help="LLM provider (deepseek, openai, etc.)")
@click.option("--mcp_config", "mcp_config_path", default="mcp_config.json", help="MCP configuration file")
@click.option("--agent_url", "agent_url", default="", help="Public URL of the agent")
def main(host, port, agent_prompt_file, model_name, provider, mcp_config_path, agent_url=""):
    """Start the BTP Architecture Agent"""
    input_mode, output_mode = ["text", "text/plain"], ["text", "text/plain"]
    BasicAgent.SUPPORTED_CONTENT_TYPES = input_mode

    try:
        capabilities = AgentCapabilities(streaming=True)
        skill = AgentSkill(
            id="BTPArchitect",
            name="BTP Architecture Expert",
            description="Specialized agent for architectural analysis, regulatory compliance, structural calculations, and construction material optimization",
            tags=["btp", "architecture", "construction", "compliance", "calculations"],
            examples=[
                "Validate compliance for an 8-story building",
                "Calculate concrete volume needed for a foundation",
                "Optimize material choices for an eco-friendly house",
                "Calculate structural loads for an office floor"
            ]
        )

        if not agent_url:
            agent_url = f"http://{host}:{port}/"

        agent_card = AgentCard(
            name="AgentArchitecte",
            description="BTP Architecture Expert: compliance, structural calculations, material optimization, and technical analysis of construction projects",
            url=agent_url,
            version="1.0.0",
            defaultInputModes=input_mode,
            defaultOutputModes=output_mode,
            capabilities=capabilities,
            skills=[skill],
        )

        print(f"🏗️  Starting BTP Architecture Agent")
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

        logger.info(f"🚀 Architecture Agent started on {host}:{port}")
        server.start()

    except MissingAPIKeyError as e:
        logger.error(f"❌ Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
        exit(1)

if __name__ == "__main__":
    main()
