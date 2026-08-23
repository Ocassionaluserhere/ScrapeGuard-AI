from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ScrapeRequest(BaseModel):
    url: str
    scraper_id: str
    trigger_demo_degradation: bool = False

class HealingRequest(BaseModel):
    incident_id: str
    affected_field: str
    repair_instruction: str

class BrightDataWebhookPayload(BaseModel):
    snapshot_id: str = Field(..., description="Unique Bright Data execution snapshot ID")
    collector_id: str = Field(..., description="Scraper Studio collector identifier")
    status: str = Field(..., description="Execution status: 'completed', 'failed', 'running'")
    url: Optional[str] = Field(None, description="Target webpage URL processed")
    total_records: int = Field(default=0, description="Total items extracted in snapshot")
    data: Optional[List[Dict[str, Any]]] = Field(default=None, description="Extracted dataset array")
    error: Optional[str] = Field(None, description="Bright Data execution error message if failed")

class WebhookResponse(BaseModel):
    success: bool
    snapshot_id: str
    status: str
    processed_records: int
    validation_status: str
