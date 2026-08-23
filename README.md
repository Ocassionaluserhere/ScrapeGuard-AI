# ScrapeGuard AI — Master Project Specification

ScrapeGuard AI is an AI-assisted, self-healing web scraping framework powered by Bright Data Scraper Studio and a deterministic Python validation engine. It continuously monitors web scraping pipelines, detects field-level data extraction degradations, and automatically triggers an AI-assisted re-parsing and re-validation loop before accepting fixes.

![ScrapeGuard AI System Architecture](https://raw.githubusercontent.com/your-username/scrapecguard-ai/main/docs/architecture.png)

## Core Architecture & Workflow

1. **Trigger & Scrape:** Initiates a web scraping run via Bright Data Scraper Studio or localized execution engine.
2. **Deterministic Data Validation:** Output records are instantly parsed through `ScrapeGuardValidator` without relying on slow or non-deterministic LLM calls for standard data integrity rules.
3. **Failure Detection:** Detects structural schema breaks, sudden null-value explosions, missing required fields, or degraded formatting.
4. **Self-Healing Loop:** Upon validation failure, an incident report and failure diagnosis are dispatched to trigger selector repair or logic patching.
5. **Retest & Validation Check:** Proposed repairs are automatically executed against a test batch. 
6. **Accept / Rollback:** The repaired logic is accepted **only** if the retest achieves passing validation metrics; otherwise, the repair is rejected and rolled back to preserve system stability.

---

## Folder Structure

```text
scrapecguard-ai/
├── backend/
│   ├── main.py
│   ├── validator.py
│   ├── schemas.py
│   ├── webhook_router.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
