"""Pydantic schemas for Google Forms Connector (C32. Surveys & Forms)."""
from __future__ import annotations
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameters model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Primary Google Forms.")
    access_token: str = Field(description="Google Forms OAuth 2.0 Access Token (forms.body, forms.responses).")
    base_url: str = Field(default="https://forms.googleapis.com/v1", description="Google Forms API base URL.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    success: bool
    message: str

class FormInfo(BaseModel):
    title: str
    document_title: Optional[str] = None
    description: Optional[str] = None

class FormRecord(BaseModel):
    form_id: str
    info: FormInfo
    responder_uri: Optional[str] = None
    revision_id: Optional[str] = None
    raw: Dict[str, Any] = Field(default_factory=dict)

class GetFormParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    form_id: str = Field(description="Google Form ID.")

class ListResponsesParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    form_id: str = Field(description="Google Form ID.")
    page_size: int = Field(default=20, ge=1, le=100, description="Max responses to return.")

class FormResponseRecord(BaseModel):
    response_id: str
    create_time: str
    last_submitted_time: str
    answers: Dict[str, Any] = Field(default_factory=dict)

class ResponseList(BaseModel):
    responses: list[FormResponseRecord]
    total: int

class AuditHealthRecord(BaseModel):
    status: str
    healthy: bool
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)
