# Trello MCP Server for Grok

A Streamable HTTP MCP server for Trello, compatible with Grok (xAI) custom connectors.

## Features

- List boards, lists, and cards
- Create, move, archive cards
- Add comments
- Search
- Uses Trello REST API with API key + token

## Setup

1. Get a Trello API key and token from https://trello.com/app-key
2. Copy `.env.example` to `.env` and fill in credentials
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   python server.py
   ```

The server listens on `http://0.0.0.0:8000`.

## Docker

```bash
docker build -t trello-mcp .
docker run --env-file .env -p 8000:8000 trello-mcp
```

## Connecting to Grok

1. Expose the server publicly (ngrok, Cloudflare Tunnel, or a real domain):
   ```bash
   ngrok http 8000
   ```
2. In Grok: go to Connectors → New Connector → Custom
3. Paste the public HTTPS URL
4. Grok will discover the tools

## Environment Variables

- `TRELLO_API_KEY` (required)
- `TRELLO_TOKEN` (required)

## License

MIT
