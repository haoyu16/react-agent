# LangGraph ReAct Agent

A flexible AI agent that uses the ReAct (Reasoning + Acting) pattern to solve tasks through iterative thinking and tool use.

Based on [langchain-ai/react-agent](https://github.com/langchain-ai/react-agent).

This project implements a [ReAct agent](https://arxiv.org/abs/2210.03629) using [LangGraph](https://github.com/langchain-ai/langgraph). ReAct agents are uncomplicated, prototypical agents that can be flexibly extended to many tools.

The core logic, defined in `src/react_agent/graph.py`, demonstrates a flexible ReAct agent that iteratively reasons about user queries and executes actions, showcasing the power of this approach for complex problem-solving tasks.

## What it does

The ReAct agent:

1. Takes a user **query** as input
2. Reasons about the query and decides on an action
3. Executes the chosen action using available tools
4. Observes the result of the action
5. Repeats steps 2-4 until it can provide a final answer

By default, it's set up with a basic set of tools, but can be easily extended with custom tools to suit various use cases.

## Setup Python Environment

The project requires Python 3.11 or later. Here's how to set up your environment:

1. Create and activate a virtual environment:
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Unix/macOS
venv\\Scripts\\activate   # On Windows

# Or using conda
conda create -n react-agent python=3.11
conda activate react-agent
```

2. Install the project in development mode:
```bash
pip install -e .
```

This will install all required dependencies from `pyproject.toml`, including:
- langgraph
- langchain
- python-dotenv
- Required model libraries (openai, anthropic)

## Getting Started

To set up the project:

1. Create a `.env` file:
```bash
cp .env.example .env
```

2. Define required API keys in your `.env` file:

The primary [search tool](./src/react_agent/tools.py) [^1] used is [Tavily](https://tavily.com/). Create an API key [here](https://app.tavily.com/sign-in).

### Setup Model

The default model is:
```yaml
model: anthropic/claude-3-5-sonnet-20240620
```

Choose and set up your preferred model:

#### Anthropic
1. Sign up for an [Anthropic API key](https://console.anthropic.com/)
2. Add it to your `.env` file:
```
ANTHROPIC_API_KEY=your-api-key
```

#### OpenAI
1. Sign up for an [OpenAI API key](https://platform.openai.com/signup)
2. Add it to your `.env` file:
```
OPENAI_API_KEY=your-api-key
```

3. Run the agent:
```bash
python main.py
```

## Configuration

The agent can be configured through `config.yaml`. Here are the available options:

```yaml
# The language model to use (provider/model-name)
model: "anthropic/claude-3-5-sonnet-20240620"

# The system prompt that sets the agent's behavior
system_prompt: |
  You are a helpful AI assistant.
  
  System time: {system_time}

# Maximum number of search results to return
max_search_results: 10
```

To modify the agent's behavior:
1. Create or edit `config.yaml` in the project root
2. Adjust any of the following settings:
   - `model`: Change the LLM (e.g., "openai/gpt-4")
   - `system_prompt`: Customize how the agent behaves and responds
   - `max_search_results`: Control how many search results to return

The configuration will be automatically loaded when you run the agent.

## How to customize

1. **Add new tools**: Extend the agent's capabilities by adding new tools in [tools.py](./src/react_agent/tools.py). These can be any Python functions that perform specific tasks.

2. **Select a different model**: We default to Anthropic's Claude 3 Sonnet. You can select a compatible chat model using `provider/model-name` via configuration. Example: `openai/gpt-4-turbo-preview`.

3. **Customize the prompt**: We provide a default system prompt in [prompts.py](./src/react_agent/prompts.py). You can modify this to change how the agent behaves.

You can also extend this template by:
- Modifying the agent's reasoning process in [graph.py](./src/react_agent/graph.py)
- Adjusting the ReAct loop or adding additional steps to the agent's decision-making process

[^1]: https://python.langchain.com/docs/concepts/#tools