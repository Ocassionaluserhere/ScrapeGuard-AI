import os
import hmac
import hashlib
from fastapi import APIRouter, Header, HTTPException, BackgroundTasks, Request, status
from schemas import BrightDataWebhookPayload, WebhookResponse
from validator import ScrapeGuardValidator

router = APIRouter(prefix="/api/v1/webhooks", tags=["Webhooks"])

WEBHOOK_SECRET = os.getenv("BRIGHT_DATA_WEBHOOK_SECRET", "default_secret_key")
validator = ScrapeGuardValidator()

def verify_signature(raw_body: bytes, signature_header: str | None):
    if not signature_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing webhook signature header"
        )
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature verification"
        )

async def process_async_snapshot(payload: BrightDataWebhookPayload):
    if payload.status != "completed" or not payload.data:
        print(f"[ALERT] Snapshot {payload.snapshot_id} failed with status: {payload.status}")
        return

    report = validator.evaluate_dataset(payload.data)
    print(f"[INFO] Snapshot {payload.snapshot_id} Validated: {report['status']} (Health: {report['healthScore']}%)")

    if report["status"] == "FAIL" or report["healthScore"] < 80:
        print(f"[TRIGGER] Self-healing initiated for snapshot {payload.snapshot_id}")

@router.post("/brightdata", response_model=WebhookResponse)
async def bright_data_webhook(
    request: Request,
    payload: BrightDataWebhookPayload,
    background_tasks: BackgroundTasks,
    x_brightdata_signature: str | None = Header(None, alias="X-BrightData-Signature")
):
    raw_body = await request.body()
    
    if os.getenv("ENABLE_WEBHOOK_VERIFICATION", "false").lower() == "true":
        verify_signature(raw_body, x_brightdata_signature)

    background_tasks.add_task(process_async_snapshot, payload)

    return WebhookResponse(
        success=True,
        snapshot_id=payload.snapshot_id,
        status=payload.status,
        processed_records=len(payload.data) if payload.data else 0,
        validation_status="QUEUED"
    )
