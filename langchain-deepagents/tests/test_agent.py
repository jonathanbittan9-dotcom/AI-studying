from discord_agent.agent import build_agent


def test_agent_builds(monkeypatch):
    # Fake settings so the agent can be built in CI (no .env there). Nothing is sent anywhere.
    monkeypatch.setenv("DISCORD_TOKEN", "fake-token")
    monkeypatch.setenv("MODEL", "groq:openai/gpt-oss-120b")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key")
    assert build_agent() is not None
