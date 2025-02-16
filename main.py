"""Main entry point for running the ReAct agent."""

import asyncio
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain_core.messages import HumanMessage
from react_agent.configuration import Configuration
from react_agent.graph import graph
from react_agent.logging import get_logger, setup_logging
from react_agent.state import InputState

# Set up logging
setup_logging()
logger = get_logger(__name__)


def load_config(config_path: Optional[str] = None) -> Configuration:
    """Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file. If None, uses default config.yaml

    Returns:
        Configuration object with the loaded settings
    """
    if config_path is None:
        config_path = str(Path(__file__).parent / "config.yaml")

    try:
        with open(config_path) as f:
            config_dict = yaml.safe_load(f)
        logger.info("Successfully loaded configuration from %s", config_path)
        return Configuration(**config_dict)
    except FileNotFoundError:
        logger.error("Config file not found at %s. Using default configuration.", config_path)
        return Configuration()
    except Exception as e:
        logger.error("Error loading config file: %s", e, exc_info=True)
        return Configuration()


async def run_agent(
    user_input: str,
    config: Optional[Configuration] = None,
) -> None:
    """Run the ReAct agent with the given input.

    Args:
        user_input: The user's input message to process
        config: Optional configuration overrides for the agent
    """
    # Create input state with the user's message using proper message type
    input_state = InputState(messages=[HumanMessage(content=user_input)])
    logger.debug("Created input state: %s", input_state)
    
    try:
        # Run the graph with the input state and configuration
        config_dict = vars(config) if config else {}
        logger.debug("Running graph with config: %s", config_dict)
        
        result = await graph.ainvoke(input_state, {"configurable": config_dict})
        logger.debug("Received result: %s", result)
        
        # Print the final response
        # The result is a State object with a messages attribute
        if result and result["messages"]:
            final_message = result["messages"][-1]
            if hasattr(final_message, "content"):
                response = final_message.content
                logger.info("Agent response: %s", response)
                print(f"\nAgent response: {response}")
            else:
                logger.warning("Final message has no content attribute")
                print("\nAgent response: Unable to get message content")
        else:
            logger.warning("No messages in result")
            print("\nAgent response: No response generated")
    except Exception as e:
        logger.error("Error running agent: %s", e, exc_info=True)
        print(f"\nError running agent: {e}")


async def main():
    """Main function to run the agent interactively."""
    logger.info("Starting ReAct Agent Interactive Mode")
    
    # Load configuration from YAML file
    config = load_config()
    
    print("ReAct Agent Interactive Mode")
    print("Type 'quit' to exit")
    print("-" * 50)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "quit":
            logger.info("User requested to quit")
            break
            
        logger.info("Processing user input: %s", user_input)
        await run_agent(user_input, config)

    logger.info("ReAct Agent shutting down")


if __name__ == "__main__":
    asyncio.run(main()) 