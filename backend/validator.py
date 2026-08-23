import re
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

class ScrapeGuardValidator:
    def __init__(self, thresholds: Optional[Dict[str, float]] = None):
        self.thresholds = thresholds or {
            "min_completeness": 0.80,
            "max_missing_price": 0.15,
            "min_valid_records_pct": 85.0
        }

    def validate_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        field_errors = {}
        
        # 1. product_name: non-empty string
        name = record.get("product_name")
        if not name or not isinstance(name, str) or not name.strip():
            field_errors["product_name"] = "Missing or non-string product name"

        # 2. product_url: valid URL structure
        url = record.get("product_url")
        if not url or not self._is_valid_url(url):
            field_errors["product_url"] = "Invalid or missing product URL"

        # 3. price: numeric or explicit null
        price = record.get("price")
        if price is not None and not isinstance(price, (int, float)):
            field_errors["price"] = f"Price must be numeric or null, got {type(price).__name__}"

        # 4. currency: valid standard 3-letter code if price exists
        currency = record.get("currency")
        if price is not None and (not currency or not re.match(r"^[A-Z]{3}$", str(currency))):
            field_errors["currency"] = "Invalid currency code format"

        # 5. rating: float between 0.0 and 5.0
        rating = record.get("rating")
        if rating is not None:
            if not isinstance(rating, (int, float)) or not (0 <= rating <= 5.0):
                field_errors["rating"] = "Rating must be numeric between 0 and 5"

        # 6. review_count: non-negative integer
        reviews = record.get("review_count")
        if reviews is not None:
            if not isinstance(reviews, int) or reviews < 0:
                field_errors["review_count"] = "Review count must be a non-negative integer"

        # 7. availability: standard boolean/enum string or null
        availability = record.get("availability")
        valid_statuses = {"in_stock", "out_of_stock", "preorder", None}
        if availability not in valid_statuses and not isinstance(availability, bool):
            field_errors["availability"] = "Invalid availability status"

        # 8. image_url: valid URL or null
        img_url = record.get("image_url")
        if img_url is not None and not self._is_valid_url(img_url):
            field_errors["image_url"] = "Invalid image URL structure"

        return {
            "is_valid": len(field_errors) == 0,
            "errors": field_errors
        }

    def evaluate_dataset(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_records = len(dataset)
        if total_records == 0:
            return {"status": "FAIL", "reason": "Empty dataset received", "healthScore": 0}

        valid_count = 0
        field_health = {
            "product_name": 0, "product_url": 0, "price": 0, 
            "currency": 0, "rating": 0, "review_count": 0, 
            "availability": 0, "image_url": 0
        }

        failures = []

        for idx, rec in enumerate(dataset):
            result = self.validate_record(rec)
            if result["is_valid"]:
                valid_count += 1
            else:
                failures.append({"record_index": idx, "errors": result["errors"]})

            for key in field_health.keys():
                if rec.get(key) is not None and key not in result["errors"]:
                    field_health[key] += 1

        field_completeness = {k: round((v / total_records) * 100, 1) for k, v in field_health.items()}
        valid_pct = round((valid_count / total_records) * 100, 1)

        avg_completeness = sum(field_completeness.values()) / len(field_completeness)
        health_score = round(
            (avg_completeness * 0.40) +
            (valid_pct * 0.25) +
            (field_completeness["product_name"] * 0.20) +
            ((100 - (len(failures) / total_records * 100)) * 0.10) +
            (100 * 0.05)
        )

        status = "PASS" if valid_pct >= self.thresholds["min_valid_records_pct"] else "FAIL"

        return {
            "status": status,
            "healthScore": health_score,
            "totalRecords": total_records,
            "validRecords": valid_count,
            "invalidRecords": total_records - valid_count,
            "fieldHealth": field_completeness,
            "failures": failures[:10]
        }

    def _is_valid_url(self, url: str) -> bool:
        try:
            res = urlparse(url)
            return all([res.scheme in ["http", "https"], res.netloc])
        except Exception:
            return False
