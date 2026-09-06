"""Extension declaration, capabilities, health check for Google Forms Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "google-forms-connector",
    version="0.1.0",
    display_name="Google Forms",
    icon="icon.svg",
    capabilities=["google_forms:manage"],
    description="Official Imperal connector for Google Forms (C30. Email Marketing & Newsletter). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("google_forms_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} Google Forms connection(s) configured." if count else "Not connected yet."
    }
