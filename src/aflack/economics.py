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
