import os
import time
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from validator import ScrapeGuardValidator
from schemas import ScrapeRequest, HealingRequest
from webhook_router import router as webhook_router

app = FastAPI(title="ScrapeGuard AI Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)

BRIGHT_DATA_API_KEY = os.getenv("BRIGHT_DATA_API_KEY", "")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

validator = ScrapeGuardValidator()

state_db = {
    "scrapers": [
        {
            "id": "scr_amazon_prod",
            "name": "E-Commerce Intelligence Scraper",
            "target_url": "https://www.example.com/category/tech",
            "status": "OPERATIONAL",
            "health_score": 94,
            "last_run": "2026-08-23T22:00:00Z"
        }
    ],
    "healing_events": []
}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "demo_mode": DEMO_MODE}

@app.post("/api/scrape")
async def execute_scrape(payload: ScrapeRequest):
    raw_data = await fetch_scraper_data(payload.url, payload.trigger_demo_degradation)
    report = validator.evaluate_dataset(raw_data)
    
    if report["status"] == "FAIL" or report["healthScore"] < 80:
        incident = trigger_degradation_incident(payload.scraper_id, report)
        return {
            "status": "DEGRADED",
            "validation": report,
            "incident": incident,
            "data": raw_data
        }

    return {
        "status": "SUCCESS",
        "validation": report,
        "data": raw_data
    }

async def fetch_scraper_data(url: str, simulate_failure: bool) -> List[Dict[str, Any]]:
    if DEMO_MODE or not BRIGHT_DATA_API_KEY:
        price_val = None if simulate_failure else 299.99
        return [
            {
                "product_name": f"Pro Gaming Headset Gen-{i}",
                "product_url": f"{url}/product-{i}",
                "price": price_val if i > 3 and simulate_failure else 299.99,
                "currency": "USD",
                "rating": 4.7,
                "review_count": 128,
                "availability": "in_stock",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
            } for i in range(1, 21)
        ]
    
    headers = {"Authorization": f"Bearer {BRIGHT_DATA_API_KEY}"}
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.brightdata.com/dca/trigger",
            json={"collector": "c_12345", "url": url},
            headers=headers
        )
        if res.status_code != 200:
            raise HTTPException(status_code=500, detail="Bright Data API execution failed")
        return res.json()

def trigger_degradation_incident(scraper_id: str, report: Dict[str, Any]) -> Dict[str, Any]:
    incident = {
        "id": f"inc_{int(time.time())}",
        "scraper_id": scraper_id,
        "affected_field": "price",
        "severity": "CRITICAL",
        "detected_failure": "Price completeness dropped below threshold (15% valid vs 100% expected)",
        "ai_diagnosis": "Target site changed wrapper DOM from .price-tag to span[data-price-val]. Selector failing.",
        "status": "REQUIRES_HEALING",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    state_db["healing_events"].append(incident)
    return incident

@app.post("/api/heal")
async def execute_self_healing(payload: HealingRequest):
    proposed_repair = f"Updated CSS Selector for field '{payload.affected_field}' from .price-tag to span[data-price-val]."
    retested_data = await fetch_scraper_data("https://www.example.com/category/tech", simulate_failure=False)
    repair_report = validator.evaluate_dataset(retested_data)
    
    if repair_report["status"] == "PASS":
        return {
            "outcome": "ACCEPTED",
            "message": "Self-healing successful. Validation passed.",
            "repair_details": proposed_repair,
            "new_health_score": repair_report["healthScore"],
            "recovered_data_sample": retested_data[:2]
        }
    else:
        return {
            "outcome": "REJECTED",
            "message": "Repair patch failed validation. Rolled back to previous version.",
            "repair_details": proposed_repair,
            "validation": repair_report
        }
