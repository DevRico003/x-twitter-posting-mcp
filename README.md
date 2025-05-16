<h1 align="center">X-Twitter-Posting-MCP: Post to Twitter from AI Agents</h1>

<p align="center">
  <img src="public/TwitterAndMCP.png" alt="Twitter and MCP Integration" width="600">
</p>

A template implementation of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for posting tweets and threads to X (formerly Twitter).

## Overview

This project demonstrates how to build an MCP server that enables AI agents to post tweets and threads to X (Twitter). It serves as a practical template for creating your own Twitter-posting MCP servers.

The implementation follows the best practices laid out by Anthropic for building MCP servers, allowing seamless integration with any MCP-compatible client.

## Features

The server provides two essential Twitter posting tools:

1. **`post_tweet`**: Post a single tweet to X (Twitter)
2. **`post_thread`**: Post a thread of tweets to X (Twitter)

## Prerequisites

- Python 3.12+
- X (Twitter) API keys and tokens
- Docker if running the MCP server as a container (recommended)

## Installation

### Using uv

1. Install uv if you don't have it:
   ```bash
   pip install uv
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/DevRico003/x-twitter-posting-mcp.git
   cd x-twitter-posting-mcp
   ```

3. Install dependencies:
   ```bash
   uv pip install -e .
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Configure your environment variables in the `.env` file (see Configuration section)

### Using Docker (Recommended)

1. Build the Docker image:
   ```bash
   docker build -t mcp/x-twitter -t --build-arg PORT=8050 .
   ```

2. Create a `.env` file based on `.env.example` and configure your environment variables

## Configuration

The following environment variables can be configured in your `.env` file:

| Variable | Description | Example |
|----------|-------------|----------|
| `TRANSPORT` | Transport protocol (sse or stdio) | `sse` |
| `HOST` | Host to bind to when using SSE transport | `0.0.0.0` |
| `PORT` | Port to listen on when using SSE transport | `8050` |
| `TWITTER_API_KEY` | Your Twitter/X API key | `AbCdEfGhIjKlMnOpQrStUvWxYz` |
| `TWITTER_API_KEY_SECRET` | Your Twitter/X API key secret | `AbCdEfGhIjKlMnOpQrStUvWxYz` |
| `TWITTER_ACCESS_TOKEN` | Your Twitter/X access token | `123456789-AbCdEfGhIjKlMnOpQrStUvWxYz` |
| `TWITTER_ACCESS_TOKEN_SECRET` | Your Twitter/X access token secret | `AbCdEfGhIjKlMnOpQrStUvWxYz` |

## Running the Server

### Using uv

#### SSE Transport

```bash
# Set TRANSPORT=sse in .env then:
uv run src/main.py
```

The MCP server will be available as an API endpoint that you can connect to with the configuration shown below.

#### Stdio Transport

With stdio, the MCP client itself can spin up the MCP server, so nothing to run at this point.

### Using Docker

#### SSE Transport

```bash
docker run --env-file .env -p:8050:8050 mcp/x-twitter
```

The MCP server will be available as an API endpoint within the container that you can connect to with the configuration shown below.

#### Stdio Transport

With stdio, the MCP client itself can spin up the MCP server container, so nothing to run at this point.

## Integration with MCP Clients

### SSE Configuration

Once you have the server running with SSE transport, you can connect to it using this configuration:

```json
{
  "mcpServers": {
    "x-twitter": {
      "transport": "sse",
      "url": "http://localhost:8050/sse"
    }
  }
}
```

> **Note for Windsurf users**: Use `serverUrl` instead of `url` in your configuration:
> ```json
> {
>   "mcpServers": {
>     "x-twitter": {
>       "transport": "sse",
>       "serverUrl": "http://localhost:8050/sse"
>     }
>   }
> }
> ```

> **Note for n8n users**: Use host.docker.internal instead of localhost since n8n has to reach outside of it's own container to the host machine:
> 
> So the full URL in the MCP node would be: http://host.docker.internal:8050/sse

Make sure to update the port if you are using a value other than the default 8050.

### Python with Stdio Configuration

Add this server to your MCP configuration for Claude Desktop, Windsurf, or any other MCP client:

```json
{
  "mcpServers": {
    "x-twitter": {
      "command": "your/path/to/x-twitter-posting-mcp/.venv/Scripts/python.exe",
      "args": ["your/path/to/x-twitter-posting-mcp/src/main.py"],
      "env": {
        "TRANSPORT": "stdio",
        "TWITTER_API_KEY": "YOUR-API-KEY",
        "TWITTER_API_KEY_SECRET": "YOUR-API-KEY-SECRET",
        "TWITTER_ACCESS_TOKEN": "YOUR-ACCESS-TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET": "YOUR-ACCESS-TOKEN-SECRET"
      }
    }
  }
}
```

### Docker with Stdio Configuration

```json
{
  "mcpServers": {
    "x-twitter": {
      "command": "docker",
      "args": ["run", "--rm", "-i", 
               "-e", "TRANSPORT", 
               "-e", "TWITTER_API_KEY", 
               "-e", "TWITTER_API_KEY_SECRET", 
               "-e", "TWITTER_ACCESS_TOKEN", 
               "-e", "TWITTER_ACCESS_TOKEN_SECRET", 
               "mcp/x-twitter"],
      "env": {
        "TRANSPORT": "stdio",
        "TWITTER_API_KEY": "YOUR-API-KEY",
        "TWITTER_API_KEY_SECRET": "YOUR-API-KEY-SECRET",
        "TWITTER_ACCESS_TOKEN": "YOUR-ACCESS-TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET": "YOUR-ACCESS-TOKEN-SECRET"
      }
    }
  }
}
```

## Usage Examples

Here are some examples of how to use the MCP tools from an AI agent:

### Post a Single Tweet

```python
# Create and post a tweet
result = await mcp.invoke("x-twitter", "post_tweet", {"text": "Hello, Twitter! This is a tweet sent via MCP."})
print(result)
```

### Post a Thread

```python
# Create and post a thread
tweets = [
    "This is the first tweet in a thread posted via MCP.", 
    "This is the second tweet in the thread.", 
    "This is the final tweet in the thread."
]
result = await mcp.invoke("x-twitter", "post_thread", {"tweets": tweets})
print(result)
```