"""Economics rollups for ROI/MMR gates."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .db import connect, fetchone_required


@dataclass(frozen=True)
class EconomicsRollup:
    total_cost: Decimal
    revenue: Decimal
    contribution_margin: Decimal
    generated_creatives: int
    cost_per_generated: Decimal | None


@dataclass(frozen=True)
class RoiScaleDecision:
    allowed: bool
    reason: str
    total_cost: Decimal
    revenue: Decimal
    contribution_margin: Decimal
    conversions: int
    snapshots: int
    min_conversions: int
    min_margin: Decimal


def current_rollup() -> EconomicsRollup:
    """Return a basic all-time economics rollup."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT COALESCE(SUM(amount), 0) FROM cost_ledger")
        total_cost = fetchone_required(cur)[0]
        cur.execute("SELECT COALESCE(SUM(revenue), 0) FROM results")
        revenue = fetchone_required(cur)[0]
        cur.execute("SELECT COUNT(*) FROM creatives")
        generated = int(fetchone_required(cur)[0])

    margin = revenue - total_cost
    cpg = (total_cost / generated) if generated else None
    return EconomicsRollup(
        total_cost=total_cost,
        revenue=revenue,
        contribution_margin=margin,
        generated_creatives=generated,
        cost_per_generated=cpg,
    )


def scale_gate_decision(*, min_conversions: int = 1, min_margin: Decimal | str = Decimal("0")) -> RoiScaleDecision:
    """Decide whether volume scale-up is allowed from measured analytics.

    The gate is deliberately conservative: no analytics snapshots means ROI is
    unmeasured, and a zero/negative contribution margin blocks scale-up.
    """

    if min_conversions < 0:
        raise ValueError("min_conversions must be non-negative")
    required_margin = Decimal(str(min_margin))

    with connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT COALESCE(SUM(amount), 0) FROM cost_ledger")
        total_cost = fetchone_required(cur)[0]
        cur.execute(
            """
            SELECT
              COUNT(*),
              COALESCE(SUM(revenue), 0),
              COALESCE(SUM(conversions), 0)
            FROM analytics_snapshots
            """
        )
        snapshots, revenue, conversions = fetchone_required(cur)

    snapshots = int(snapshots)
    conversions = int(conversions)
    margin = revenue - total_cost

    if snapshots == 0:
        allowed = False
        reason = "blocked: ROI unmeasured; no analytics snapshots captured"
    elif conversions < min_conversions:
        allowed = False
        reason = f"blocked: conversions {conversions} below required {min_conversions}"
    elif margin <= required_margin:
        allowed = False
        reason = f"blocked: contribution margin {margin} is not above required {required_margin}"
    else:
        allowed = True
        reason = "allowed: measured conversions and positive contribution margin"

    return RoiScaleDecision(
        allowed=allowed,
        reason=reason,
        total_cost=total_cost,
        revenue=revenue,
        contribution_margin=margin,
        conversions=conversions,
        snapshots=snapshots,
        min_conversions=min_conversions,
        min_margin=required_margin,
    )
