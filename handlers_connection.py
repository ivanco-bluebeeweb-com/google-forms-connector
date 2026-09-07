"""Connection management for Google Forms Connector."""
from __future__ import annotations
import uuid
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import NoParams, ConnectParams, ConnectionIdParams, ConnectionRecord, ConnectionList, DeleteResult
from google_forms_client import GoogleFormsClient

async def resolve_client(ctx, connection_id: str = "") -> GoogleFormsClient:
    connections = await ctx.store.get("connections", [])
    if not connections:
        raise ValueError("No Google Forms connections configured. Use connect_google_forms first.")
    conn = None
    if connection_id:
        for c in connections:
            if c.get("id") == connection_id:
                conn = c
                break
        if not conn:
            raise ValueError(f"Connection {connection_id} not found.")
    else:
        conn = connections[0]
    return GoogleFormsClient(access_token=conn["access_token"], base_url=conn.get("base_url", ""))

@chat.function(
    "connect_google_forms",
    "Connect Google Forms account via OAuth 2.0 Access Token.",
    action_type="write",
    chain_callable=True,
    event="google-forms-connector.connect_google_forms",
    effects=["create:connection"],
    data_model=ConnectionRecord
)
async def connect_google_forms(params: ConnectParams, ctx) -> ActionResult:
    """Connect Google Forms account."""
    client = GoogleFormsClient(access_token=params.access_token, base_url=params.base_url)
    res = await client.verify_auth()
    if res.get("status") == "error":
        return ActionResult.error(f"Failed to authenticate with Google Forms: {res.get('error')}")

    connections = await ctx.store.get("connections", [])
    masked = params.access_token[:6] + "..." if len(params.access_token) > 6 else "***"
    record = {
        "id": f"conn_{uuid.uuid4().hex[:8]}",
        "label": params.label or "Primary Google Forms",
        "access_token": params.access_token,
        "masked_key": masked,
        "base_url": params.base_url,
        "is_active": True
    }
    for c in connections:
        c["is_active"] = False
    connections.append(record)
    await ctx.store.set("connections", connections)
    return ActionResult.success(ConnectionRecord(**record), summary=f"Connected Google Forms account '{record['label']}'.")

@chat.function(
    "list_connections",
    "List configured Google Forms connections.",
    action_type="read",
    chain_callable=True,
    event="google-forms-connector.list_connections",
    effects=["read:connections"],
    data_model=ConnectionList
)
async def list_connections(params: NoParams, ctx) -> ActionResult:
    """List Google Forms connections."""
    connections = await ctx.store.get("connections", [])
    recs = [ConnectionRecord(**c) for c in connections]
    return ActionResult.success(ConnectionList(connections=recs, total=len(recs)), summary=f"Found {len(recs)} connection(s).")

@chat.function(
    "disconnect_google_forms",
    "Disconnect Google Forms account and delete stored credentials.",
    action_type="destructive",
    chain_callable=True,
    event="google-forms-connector.disconnect_google_forms",
    effects=["delete:connection"],
    data_model=DeleteResult
)
async def disconnect_google_forms(params: ConnectionIdParams, ctx) -> ActionResult:
    """Disconnect Google Forms account."""
    connections = await ctx.store.get("connections", [])
    if not connections:
        return ActionResult.error("No connections to remove.")
    target_id = params.connection_id or connections[0]["id"]
    new_conns = [c for c in connections if c.get("id") != target_id]
    if len(new_conns) == len(connections):
        return ActionResult.error(f"Connection {target_id} not found.")
    if new_conns and not any(c.get("is_active") for c in new_conns):
        new_conns[0]["is_active"] = True
    await ctx.store.set("connections", new_conns)
    return ActionResult.success(DeleteResult(success=True, message=f"Disconnected {target_id}"), summary=f"Disconnected {target_id}.")
