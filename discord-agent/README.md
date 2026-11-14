# discord-agent

An AI agent that chats with, informs and manages a Discord server. Built with
[LangChain deepagents](https://github.com/langchain-ai/deepagents). In the
server, the bot goes by the name **Raider**.

Mention the bot or use `/ask` to ask it something. It uses tools to look up
the server (channels, roles, messages, server info) and to manage it (create
or delete channels and roles). Before it acts, it checks that the person
asking has the right Discord permissions.

## How it works

```
Discord message / slash command
        │
        ▼
   bot.py (RaiderClient) ── builds BotContext(guild, requester)
        │
        ▼
   agent.py (deep agent) ── LLM + tools + todo list + summarization
        │                      │
        │                      └─ tools/  (channels, roles, server)
        ▼
   Postgres checkpointer ── one conversation per user per channel
```

## Project layout

```
discord-agent/
├── src/discord_agent/
│   ├── __main__.py        # entry point: python -m discord_agent
│   ├── bot.py             # Discord client, slash commands
│   ├── agent.py           # builds the agent: prompt, tools, middleware
│   ├── llm.py             # picks the chat model from MODEL
│   ├── config.py          # reads settings from the environment
│   ├── context.py         # BotContext: who asked, in which server
│   ├── logging_config.py
│   └── tools/
│       ├── _common.py     # helpers shared by tools
│       ├── channels.py    # list / read / create / remove channels
│       ├── roles.py       # list / create / remove roles
│       └── server.py      # server info
├── tests/
├── Dockerfile
├── docker-compose.yml     # bot + Postgres
└── pyproject.toml
```

## Setup

1. Create a bot in the [Discord developer portal](https://discord.com/developers/applications).
   Enable the **Message Content** and **Server Members** intents, and invite
   it with the `Manage Roles` and `Manage Channels` permissions.
2. Copy the config and fill it in:
   ```bash
   cp .env.example .env
   ```

## Run

With Docker (bot + Postgres):
```bash
docker compose up -d
```

Locally, for development:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
docker compose up -d db      # Postgres only
python -m discord_agent
```

## Develop

```bash
pytest                       # tests (no Discord or LLM needed)
ruff check src tests         # lint
ruff format src tests        # format
```

## Releases

Use [conventional commits](https://www.conventionalcommits.org/) (`feat: ...`,
`fix: ...`). On every merge to `master`, CI works out the next version from
those messages, creates a `discord-agent-vX.Y.Z` GitHub Release, and pushes
the Docker image:

```bash
docker pull ghcr.io/jonathanbittan9-dotcom/discord-agent:latest
```
