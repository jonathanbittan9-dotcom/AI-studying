from discord_agent.bot import create_client
from discord_agent.config import load_settings
from discord_agent.logging_config import setup_logging


def main() -> None:
    setup_logging()
    settings = load_settings()
    client = create_client(settings)
    # log_handler=None: we already configured logging, don't let discord.py add a second handler.
    client.run(settings.discord_token, log_handler=None)


if __name__ == "__main__":
    main()


