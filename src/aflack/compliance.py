"""Pre-publish compliance gate.

Blocks content that violates FTC disclosure, TikTok/YouTube reused-content and
medical-claim rules, AI-persona honesty, and Rockstar/Take-Two IP rules
(no pre-release footage, no same-seed remix of official footage).

This is a deterministic first-pass checklist. A human still approves before any
public publish. The director/LLM may add nuance, but these hard blocks stand.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Hard-blocked source provenance tags.
BLOCKED_SOURCES = {
    "rockstar_pre_release_footage",
    "leaked_footage",
    "official_trailer_footage_reupload",
    "same_seed_regeneration_of_official_footage",
}

# Phrases that indicate a prohibited medical/health claim for gaming-adjacent copy.
MEDICAL_CLAIM_MARKERS = (
    "cure",
    "treat",
    "diagnose",
    "clinically proven",
    "weight loss guaranteed",
)

# Phrases indicating false firsthand access.
FALSE_FIRSTHAND_MARKERS = (
    "i played the leaked",
    "i have the leaked build",
    "leaked copy i got",
)


@dataclass
class ComplianceResult:
    passed: bool
    blocks: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def check_publish_item(
    *,
    source_provenance: str | None,
    disclosure_text: str,
    script_body: str,
    persona_is_ai: bool = True,
) -> ComplianceResult:
    """Deterministic pre-publish check. Returns pass/blocks/warnings."""

    blocks: list[str] = []
    warnings: list[str] = []

    prov = (source_provenance or "").strip().lower()
    if prov in BLOCKED_SOURCES:
        blocks.append(f"blocked source provenance: {prov}")

    disclosure = (disclosure_text or "").lower()
    if "affiliate" not in disclosure and "commission" not in disclosure:
        blocks.append("missing affiliate disclosure")

    body = (script_body or "").lower()
    for marker in MEDICAL_CLAIM_MARKERS:
        if marker in body:
            blocks.append(f"possible prohibited medical/health claim: '{marker}'")
    for marker in FALSE_FIRSTHAND_MARKERS:
        if marker in body:
            blocks.append(f"false firsthand access claim: '{marker}'")

    if persona_is_ai and "ai" not in disclosure and "synthetic" not in disclosure:
        warnings.append("AI/synthetic persona: consider explicit AI disclosure per platform/FTC")

    return ComplianceResult(passed=len(blocks) == 0, blocks=blocks, warnings=warnings)
