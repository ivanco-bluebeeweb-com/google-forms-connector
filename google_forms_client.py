"""HTTP client for Google Forms API v1."""
from __future__ import annotations
import httpx
from typing import Any, Optional

DEFAULT_BASE = "https://forms.googleapis.com/v1"

class GoogleFormsClient:
    def __init__(self, access_token: str, base_url: str = ""):
        self.access_token = access_token.strip()
        self.base_url = (base_url.strip() if base_url else DEFAULT_BASE).rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "User-Agent": "Imperal-GoogleForms-Connector/1.0.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def verify_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/forms/invalid_probe_id", headers=self.headers)
                if resp.status_code == 404:
                    return {"status": "ok", "message": "Authenticated"}
                if resp.status_code == 401:
                    return {"status": "error", "error": "Invalid or expired OAuth token (HTTP 401)"}
                return {"status": "ok", "message": f"HTTP {resp.status_code}"}
            except Exception as e:
                return {"status": "error", "error": str(e)}

    async def get_form(self, form_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/forms/{form_id}", headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            raise ValueError(f"Google Forms API error ({resp.status_code}): {resp.text}")

    async def list_responses(self, form_id: str, page_size: int = 20) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/forms/{form_id}/responses", headers=self.headers, params={"pageSize": page_size})
            if resp.status_code == 200:
                data = resp.json()
                return data.get("responses", [])
            raise ValueError(f"Google Forms API error ({resp.status_code}): {resp.text}")
