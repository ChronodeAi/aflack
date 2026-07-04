"""Heuristic quality gates for short-form asset-generation prompts."""

from __future__ import annotations

from dataclasses import dataclass

POSITIVE_GTA_ANCHORS = (
    "gta6 day-one",
    "gta6 launch",
    "launch night",
    "day-one setup",
    "vice",
    "wanted-level",
    "open-world",
    "game launch",
)

NARRATIVE_TENSION_MARKERS = (
    "not ready",
    "fails",
    "before you buy",
    "wrong",
    "mistake",
    "fix first",
    "secret",
    "hidden",
    "three checks",
    "audit",
    "caught",
)

PAYOFF_MARKERS = (
    "wait for",
    "final frame",
    "reveals",
    "reveal",
    "payoff",
    "twist",
    "turns into",
    "loop",
    "ends with",
)

MOTION_MARKERS = (
    "push-in",
    "dolly",
    "orbital",
    "whip-pan",
    "crash zoom",
    "macro",
    "cut",
    "camera",
    "animate",
    "snaps",
    "drifts",
)

COMPLIANCE_NEGATIVES = (
    "no real brand logos",
    "no rockstar",
    "take-two",
    "no gta footage",
    "no trailer frames",
    "no real-person likeness",
)


@dataclass(frozen=True)
class PromptQualityResult:
    passed: bool
    blocks: list[str]
    warnings: list[str]


def _has_any(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


def check_short_asset_prompt(prompt: str) -> PromptQualityResult:
    """Reject prompts that are compliant but too generic for short-form assets."""

    blocks: list[str] = []
    warnings: list[str] = []
    lowered = prompt.lower()

    if not _has_any(lowered, POSITIVE_GTA_ANCHORS):
        blocks.append("missing positive GTA6/day-one/Vice relevance anchor")
    if not _has_any(lowered, NARRATIVE_TENSION_MARKERS):
        blocks.append("missing narrative tension or buyer/viewer problem")
    if not _has_any(lowered, PAYOFF_MARKERS):
        blocks.append("missing visible payoff or end-state reveal")
    if not _has_any(lowered, MOTION_MARKERS):
        blocks.append("missing camera/motion/edit direction")

    missing_negatives = [marker for marker in COMPLIANCE_NEGATIVES if marker not in lowered]
    if missing_negatives:
        warnings.append(f"missing explicit compliance negatives: {', '.join(missing_negatives)}")

    if "mood:" in lowered and not ("first second" in lowered or "0:" in lowered or "opening frame" in lowered):
        warnings.append("mood is specified but the first-frame hook is not")

    return PromptQualityResult(passed=not blocks, blocks=blocks, warnings=warnings)
