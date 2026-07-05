"""PII detection and handling for creator data.

The pipeline processes public creator data (social media handles, follower
counts, engagement rates). This module provides PII classification, masking,
and documentation to ensure responsible data handling.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

PII_PATTERNS = {
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "phone": re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    "ip_address": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
}

CREATOR_DATA_CLASSIFICATION = {
    "handle": "public",
    "display_name": "public",
    "followers": "public",
    "engagement_rate": "public",
    "monetization": "sensitive",
    "proof_notes": "sensitive",
    "source_url": "public",
    "platform": "public",
}


@dataclass(frozen=True)
class PIIDetectionResult:
    has_pii: bool
    detected_types: list[str]
    masked_content: str


def detect_pii(content: str) -> PIIDetectionResult:
    detected: list[str] = []
    masked = content
    for pii_type, pattern in PII_PATTERNS.items():
        if pattern.search(content):
            detected.append(pii_type)
            masked = pattern.sub(f"[{pii_type.upper()}_REDACTED]", masked)
    return PIIDetectionResult(
        has_pii=bool(detected),
        detected_types=detected,
        masked_content=masked,
    )


def mask_creator_data(data: dict[str, Any]) -> dict[str, Any]:
    result = dict(data)
    for key, classification in CREATOR_DATA_CLASSIFICATION.items():
        if key in result and classification == "sensitive":
            result[key] = "***MASKED***"
    return result


def classify_field(field_name: str) -> str:
    return CREATOR_DATA_CLASSIFICATION.get(field_name, "unknown")
