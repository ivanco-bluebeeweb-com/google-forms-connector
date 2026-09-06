"""Resource handlers for Google Forms Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ConnectionIdParams,
    GetFormParams, FormRecord, FormInfo,
    ListResponsesParams, ResponseList, FormResponseRecord,
    AuditHealthRecord
)
from handlers_connection import resolve_client

@chat.function(
    "get_form",
    "Get details of one Google Form by form ID.",
    action_type="read",
    chain_callable=True,
    event="google-forms-connector.get_form",
    effects=["read:form"],
    data_model=FormRecord
)
async def get_form(params: GetFormParams, ctx) -> ActionResult:
    """Get Google Form details."""
    try:
        client = await resolve_client(ctx, params.connection_id)
        raw = await client.get_form(form_id=params.form_id)
        info_raw = raw.get("info", {})
        info = FormInfo(
            title=info_raw.get("title", "Untitled Form"),
            document_title=info_raw.get("documentTitle"),
            description=info_raw.get("description")
        )
        rec = FormRecord(
            form_id=raw.get("formId", params.form_id),
            info=info,
            responder_uri=raw.get("responderUri"),
            revision_id=raw.get("revisionId"),
            raw=raw
        )
        return ActionResult.ok(rec, summary=f"Retrieved form {params.form_id}: {info.title}")
    except Exception as e:
        return ActionResult.error(f"Error fetching Google Form: {e}")

@chat.function(
    "list_responses",
    "List submissions/responses for one Google Form.",
    action_type="read",
    chain_callable=True,
    event="google-forms-connector.list_responses",
    effects=["read:responses"],
    data_model=ResponseList
)
async def list_responses(params: ListResponsesParams, ctx) -> ActionResult:
    """List Google Form responses."""
    try:
        client = await resolve_client(ctx, params.connection_id)
        items = await client.list_responses(form_id=params.form_id, page_size=params.page_size)
        recs = [
            FormResponseRecord(
                response_id=r.get("responseId", ""),
                create_time=r.get("createTime", ""),
                last_submitted_time=r.get("lastSubmittedTime", ""),
                answers=r.get("answers", {})
            )
            for r in items
        ]
        return ActionResult.ok(ResponseList(responses=recs, total=len(recs)), summary=f"Found {len(recs)} response(s) for form {params.form_id}.")
    except Exception as e:
        return ActionResult.error(f"Error fetching form responses: {e}")

@chat.function(
    "audit_survey_health",
    "Audit active forms and submission volume in Google Forms.",
    action_type="read",
    chain_callable=True,
    event="google-forms-connector.audit_survey_health",
    effects=["read:survey_health"],
    data_model=AuditHealthRecord
)
async def audit_survey_health(params: ConnectionIdParams, ctx) -> ActionResult:
    """Audit Google Forms health."""
    try:
        client = await resolve_client(ctx, params.connection_id)
        auth_check = await client.verify_auth()
        is_ok = auth_check.get("status") == "ok"
        rec = AuditHealthRecord(
            status="healthy" if is_ok else "unhealthy",
            healthy=is_ok,
            message="Google Forms API connection verified." if is_ok else auth_check.get("error", "Unknown error"),
            details=auth_check
        )
        return ActionResult.ok(rec, summary=f"Survey health: {rec.status}")
    except Exception as e:
        return ActionResult.error(f"Error auditing survey health: {e}")
