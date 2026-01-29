# Tribu IA: Purple Code Agent (BigCodeBench)

This agent is an expert Python developer optimized for the [BigCodeBench](https://github.com/bigcodebench/BigCodeBench) benchmark. It is built using the [A2A (Agent-to-Agent)](https://a2a-protocol.org/) protocol and designed to be evaluated by Green Agents (evaluators) on the AgentBeats platform.

## Features

- **Expert Code Generation**: Specialized in solving complex Python coding tasks.
- **A2A Protocol Ready**: Implements the standard A2A interface for seamless integration.
- **CI/CD Integrated**: Automatically builds and publishes Docker images to GitHub Container Registry (GHCR).

## Project Structure

```
.
├── src/
│   ├── server.py      # A2A Server setup and Agent Card configuration
│   ├── executor.py    # Request handling and task management
│   └── agent.py       # Core expert coding logic
├── .github/workflows/
│   └── publish.yml    # CI/CD pipeline for GHCR publishing
├── Dockerfile         # Standalone container configuration
├── pyproject.toml     # Python dependencies
└── uv.lock            # Locked dependencies
```

## Getting Started

### 1. Local Development

Install dependencies using `uv`:
```bash
uv sync
```

Set your API key in a `.env` file:
```bash
AGENT_LLM=openai/gpt-4o
OPENAI_API_KEY=your-api-key-here
```

Run the agent:
```bash
uv run src/server.py
```

### 2. Running with Docker

Build and run locally:
```bash
docker build -t purple-agent .
docker run -p 9019:9019 --env-file .env purple-agent
```

## CI/CD and Publishing

This repository includes a GitHub Actions workflow that automatically publishes a Docker image to GHCR on every push to `main` or new tag.

1. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Your update"
   git push origin main
   ```
2. **Track Progress**: Check the **Actions** tab in your GitHub repository.
3. **Usage**: The image will be available at `ghcr.io/<your-username>/tribu-ia-purple-agent:latest`.

## Evaluation

To evaluate this agent, use the **Tribu IA Green Agent** or register it with the **AgentBeats Leaderboard** by pointing to its endpoint (default port 9019).

For more details, see the [PURPLE_AGENT_GUIDE.md](PURPLE_AGENT_GUIDE.md).
