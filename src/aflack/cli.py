"""CLI for local Day-1 pipeline operations."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from .analytics import (
    AnalyticsSnapshot,
    current_analytics_rollup,
    record_snapshot,
    snapshot_from_postiz_payload,
)
from .aside_scan import import_aside_scan
from .compliance import check_publish_item
from .daemon import get_daemon_status, run_improvement_cycle
from .db import connect, exec_sql
from .economics import current_rollup
from .learning import (
    active_insights,
    dedupe_open_proposals,
    distill_insight,
    open_proposals,
    set_creator_proof,
    upsert_creator,
)
from .memory import consolidate_insights_to_lessons
from .prompt_quality import check_short_asset_prompt
from .publishing import PostizPublisher, PublishIntent
from .tracing import trace_events

app = typer.Typer(help="aflack local affiliate content pipeline")


@app.command()
def migrate() -> None:
    """Apply local SQL migrations."""

    for migration in sorted(Path("db/migrations").glob("*.sql")):
        typer.echo(f"Applying {migration}...")
        exec_sql(migration.read_text())
    typer.echo("Migrations applied.")


@app.command()
def db_status() -> None:
    """Show database extension and table status."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT extname, extversion
            FROM pg_extension
            WHERE extname IN ('graph','pg_cron','vector')
            ORDER BY extname
            """
        )
        typer.echo("Extensions:")
        for name, version in cur.fetchall():
            typer.echo(f"  - {name}: {version}")

        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
        )
        tables = [row[0] for row in cur.fetchall()]
        typer.echo("Tables:")
        for table in tables:
            typer.echo(f"  - {table}")


@app.command()
def seed_smoke() -> None:
    """Insert a tiny Product→Creative→Result graph and query it."""

    sql = """
    INSERT INTO niches (name, notes)
    VALUES ('smoke-beauty-tools', 'Smoke-test niche')
    ON CONFLICT (name) DO UPDATE SET updated_at = now()
    RETURNING id;
    """
    with connect() as conn, conn.cursor() as cur:
        cur.execute(sql)
        niche_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO products (niche_id, title, source_url)
            VALUES (%s, 'Ceramic Hair Curler', 'https://example.invalid/product')
            RETURNING id
            """,
            (niche_id,),
        )
        product_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO personas (name, ethics_policy)
            VALUES ('Maya Local Smoke', 'Synthetic persona; no impersonation; disclose affiliate relationship and AI usage where required.')
            ON CONFLICT (name) DO UPDATE SET ethics_policy = EXCLUDED.ethics_policy
            RETURNING id
            """
        )
        persona_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO hooks (niche_id, text, benchmark_metrics)
            VALUES (%s, 'POV: your hair in 30 seconds', '{"source":"smoke"}')
            RETURNING id
            """,
            (niche_id,),
        )
        hook_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO scripts (product_id, persona_id, hook_id, body, claim_flags)
            VALUES (%s, %s, %s, 'Affiliate disclosure: I may earn commission. Quick visual demo of a ceramic curler without medical claims.', '[]')
            RETURNING id
            """,
            (product_id, persona_id, hook_id),
        )
        script_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO creatives (script_id, higgsfield_job_id, media_path, duration_seconds, cost_credits, validation_metrics)
            VALUES (%s, 'smoke-job', 'artifacts/smoke.mp4', 15, 1, '{"virality_score": 50}')
            RETURNING id
            """,
            (script_id,),
        )
        creative_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO results (creative_id, views, ctr, conversions, revenue)
            VALUES (%s, 52000, 0.005, 26, 180.50)
            RETURNING id
            """,
            (creative_id,),
        )
        result_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO cost_ledger (ref_type, ref_id, cost_type, amount, unit, metadata)
            VALUES ('creative', %s, 'higgsfield', 1, 'credit', '{"source":"smoke"}')
            """,
            (creative_id,),
        )

        cur.execute("SELECT * FROM graph.auto_discover('public', NULL, true);")

        cur.execute(
            """
            SELECT depth, node_table_name, node_id, readable_path
            FROM graph.expand('products'::regclass::oid, %s, 4)
            ORDER BY depth, node_table_name, node_id
            LIMIT 20
            """,
            (str(product_id),),
        )
        rows = cur.fetchall()
        conn.commit()

    typer.echo(f"Seeded smoke graph: product={product_id}, creative={creative_id}, result={result_id}")
    typer.echo("Graph traversal:")
    for depth, table, node_id, path in rows:
        typer.echo(f"  depth={depth} table={table} id={node_id} path={path}")


@app.command()
def set_beachhead() -> None:
    """Lock the chosen beachhead niche: GTA6 AI-persona gaming, YouTube-first."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO niches (name, status, scorecard, notes)
            VALUES (
              'gta6-ai-persona-gaming',
              'active',
              '{"intent":"audience-building","primary_platform":"youtube","format_strategy":"shorts_to_longform","affiliate_targets":["controllers","headsets","capture_cards","monitors","gift_cards","vpn"]}'::jsonb,
              'Beachhead A selected: GTA6 AI-persona gaming. YouTube-first funnel: Shorts for attention, long-form for RPM, gaming-adjacent affiliate/brand deals.'
            )
            ON CONFLICT (name) DO UPDATE
              SET status = EXCLUDED.status,
                  scorecard = EXCLUDED.scorecard,
                  notes = EXCLUDED.notes,
                  updated_at = now()
            RETURNING id
            """
        )
        niche_id = cur.fetchone()[0]
        conn.commit()
    typer.echo(f"Beachhead locked: gta6-ai-persona-gaming (niche_id={niche_id})")


@app.command()
def publish_smoke() -> None:
    """Create a safe YouTube/Postiz publish intent for the latest creative."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT id FROM creatives ORDER BY created_at DESC LIMIT 1")
        row = cur.fetchone()
        if not row:
            raise typer.BadParameter("No creatives found. Run `aflack seed-smoke` first.")
        creative_id = int(row[0])

    queue_id = PostizPublisher().enqueue(
        PublishIntent(
            creative_id=creative_id,
            platform="youtube",
            target_format="short",
            title="GTA 6 countdown: what we know so far",
            description="Synthetic persona content test. Affiliate disclosures and source provenance required before publish.",
            hashtags=["GTA6", "Gaming", "YouTubeShorts"],
            disclosure_text="Disclosure: synthetic/AI-assisted content; affiliate links may earn commission.",
        )
    )
    typer.echo(f"Created Postiz publish intent queue_id={queue_id} status=needs_auth")


@app.command()
def postiz_integrations() -> None:
    """List connected Postiz integrations (requires POSTIZ_API_KEY)."""

    try:
        integrations = PostizPublisher().list_integrations()
    except RuntimeError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=2) from exc
    for item in integrations:
        typer.echo(f"{item.get('id')} | {item.get('identifier')} | {item.get('name')}")


@app.command()
def postiz_submit(queue_id: int, integration_id: str, draft: bool = True) -> None:
    """Submit a queued item to Postiz (draft by default)."""

    try:
        response = PostizPublisher().submit_queue_item(queue_id, integration_id, as_draft=draft)
    except RuntimeError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=2) from exc
    typer.echo(response)


@app.command()
def postiz_preview(queue_id: int, integration_id: str, draft: bool = True) -> None:
    """Preview the Postiz payload for a queued item without submitting it."""

    try:
        payload = PostizPublisher().build_queue_payload(queue_id, integration_id, as_draft=draft)
    except RuntimeError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=2) from exc
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@app.command()
def compliance_smoke() -> None:
    """Run deterministic compliance smoke checks."""

    ok = check_publish_item(
        source_provenance="original_ai_visuals",
        disclosure_text="Disclosure: AI-assisted content; affiliate links may earn commission.",
        script_body="GTA6 countdown commentary with original visuals.",
    )
    blocked = check_publish_item(
        source_provenance="same_seed_regeneration_of_official_footage",
        disclosure_text="",
        script_body="I played the leaked build and this will cure your boredom.",
    )
    typer.echo(f"allowed_sample passed={ok.passed} blocks={ok.blocks} warnings={ok.warnings}")
    typer.echo(f"blocked_sample passed={blocked.passed} blocks={blocked.blocks} warnings={blocked.warnings}")
    if ok.passed is not True or blocked.passed is not False:
        raise typer.Exit(code=1)


@app.command()
def economics_status() -> None:
    """Print the current all-time economics rollup."""

    r = current_rollup()
    typer.echo(f"total_cost={r.total_cost}")
    typer.echo(f"revenue={r.revenue}")
    typer.echo(f"contribution_margin={r.contribution_margin}")
    typer.echo(f"generated_creatives={r.generated_creatives}")
    typer.echo(f"cost_per_generated={r.cost_per_generated}")


@app.command()
def cost_record(
    ref_type: str,
    ref_id: int,
    cost_type: str,
    amount: str,
    unit: str,
    metadata: str = "{}",
) -> None:
    """Record a generation/tool/operator cost in the local ledger."""

    try:
        parsed_metadata = json.loads(metadata)
    except json.JSONDecodeError as exc:
        typer.echo(f"metadata must be valid JSON: {exc}")
        raise typer.Exit(code=2) from exc
    if not isinstance(parsed_metadata, dict):
        raise typer.BadParameter("metadata must be a JSON object")

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO cost_ledger (ref_type, ref_id, cost_type, amount, unit, metadata)
            VALUES (%s, %s, %s, %s, %s, %s::jsonb)
            RETURNING id
            """,
            (ref_type, ref_id, cost_type, amount, unit, json.dumps(parsed_metadata)),
        )
        cost_id = int(cur.fetchone()[0])
        conn.commit()

    typer.echo(f"cost_ledger_id={cost_id}")


@app.command()
def publish_queue_status(limit: int = 20) -> None:
    """List recent publish queue items and external IDs."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, creative_id, platform, target_format, status,
                   COALESCE(postiz_post_id, ''), COALESCE(platform_post_id, ''),
                   COALESCE(platform_url, '')
            FROM publish_queue
            ORDER BY id DESC
            LIMIT %s
            """,
            (limit,),
        )
        rows = cur.fetchall()

    if not rows:
        typer.echo("(no publish queue items)")
        return
    for row in rows:
        queue_id, creative_id, platform, target_format, status, postiz_id, platform_id, url = row
        typer.echo(
            " | ".join(
                [
                    f"id={queue_id}",
                    f"creative_id={creative_id}",
                    f"platform={platform}",
                    f"format={target_format}",
                    f"status={status}",
                    f"postiz_post_id={postiz_id or '-'}",
                    f"platform_post_id={platform_id or '-'}",
                    f"url={url or '-'}",
                ]
            )
        )


@app.command()
def analytics_record_manual(
    platform: str,
    source_post_id: str = "",
    publish_queue_id: int = 0,
    creative_id: int = 0,
    channel_id: int = 0,
    platform_url: str = "",
    views: int = 0,
    likes: int = 0,
    comments: int = 0,
    shares: int = 0,
    saves: int = 0,
    clicks: int = 0,
    conversions: int = 0,
    ctr: str = "",
    revenue: str = "0",
) -> None:
    """Record a manual analytics snapshot from any video platform."""

    try:
        snapshot = AnalyticsSnapshot.normalized(
            platform=platform,
            source="manual",
            publish_queue_id=publish_queue_id or None,
            creative_id=creative_id or None,
            channel_id=channel_id or None,
            source_post_id=source_post_id or None,
            platform_url=platform_url or None,
            views=views,
            likes=likes,
            comments=comments,
            shares=shares,
            saves=saves,
            clicks=clicks,
            conversions=conversions,
            ctr=ctr or None,
            revenue=revenue,
            raw={"entry": "manual_cli"},
        )
        snapshot_id = record_snapshot(snapshot)
    except ValueError as exc:
        typer.echo(f"analytics snapshot rejected: {exc}")
        raise typer.Exit(code=2) from exc

    typer.echo(f"analytics_snapshot_id={snapshot_id}")
    typer.echo(f"platform={snapshot.platform}")
    typer.echo(f"views={snapshot.views}")
    typer.echo(f"conversions={snapshot.conversions}")
    typer.echo(f"revenue={snapshot.revenue}")


@app.command()
def analytics_status(platform: str = "") -> None:
    """Print aggregate analytics captured in the local event store."""

    rollup = current_analytics_rollup(platform or None)
    typer.echo(f"snapshots={rollup.snapshots}")
    typer.echo(f"total_views={rollup.total_views}")
    typer.echo(f"total_likes={rollup.total_likes}")
    typer.echo(f"total_comments={rollup.total_comments}")
    typer.echo(f"total_shares={rollup.total_shares}")
    typer.echo(f"total_saves={rollup.total_saves}")
    typer.echo(f"total_clicks={rollup.total_clicks}")
    typer.echo(f"total_conversions={rollup.total_conversions}")
    typer.echo(f"total_revenue={rollup.total_revenue}")


@app.command()
def prompt_quality(path: Path | None = None, text: str = "") -> None:
    """Check whether a short-form asset prompt is generation-worthy."""

    if path:
        prompt = path.read_text()
    else:
        prompt = text
    if not prompt.strip():
        raise typer.BadParameter("provide --text or a prompt file path")

    result = check_short_asset_prompt(prompt)
    typer.echo(f"passed={result.passed}")
    typer.echo(f"blocks={result.blocks}")
    typer.echo(f"warnings={result.warnings}")
    if not result.passed:
        raise typer.Exit(code=1)


@app.command()
def postiz_analytics_post(queue_id: int = 0, post_id: str = "", platform: str = "youtube", days: int = 7) -> None:
    """Fetch Postiz post analytics and store a local analytics snapshot."""

    creative_id = None
    channel_id = None
    platform_url = None
    if queue_id:
        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT creative_id, channel_id, platform, postiz_post_id, platform_url
                FROM publish_queue
                WHERE id = %s
                """,
                (queue_id,),
            )
            row = cur.fetchone()
        if not row:
            raise typer.BadParameter(f"publish_queue id={queue_id} not found")
        creative_id, channel_id, queue_platform, queue_postiz_id, platform_url = row
        platform = queue_platform or platform
        post_id = post_id or queue_postiz_id or ""

    if not post_id:
        raise typer.BadParameter("post_id is required when queue_id has no postiz_post_id")

    try:
        payload = PostizPublisher().get_post_analytics(post_id, days=days)
        snapshot = snapshot_from_postiz_payload(
            payload,
            platform=platform,
            publish_queue_id=queue_id or None,
            creative_id=creative_id,
            channel_id=channel_id,
            postiz_post_id=post_id,
            platform_url=platform_url,
        )
        snapshot_id = record_snapshot(snapshot)
    except (RuntimeError, ValueError) as exc:
        typer.echo(f"postiz analytics ingest failed: {exc}")
        raise typer.Exit(code=2) from exc

    typer.echo(f"analytics_snapshot_id={snapshot_id}")
    typer.echo(f"platform={snapshot.platform}")
    typer.echo(f"source_post_id={snapshot.source_post_id}")
    typer.echo(f"views={snapshot.views}")
    typer.echo(f"conversions={snapshot.conversions}")
    typer.echo(f"revenue={snapshot.revenue}")


@app.command()
def postiz_analytics_platform(integration_id: str, platform: str = "youtube", days: int = 7) -> None:
    """Fetch Postiz platform analytics and store a local analytics snapshot."""

    try:
        payload = PostizPublisher().get_platform_analytics(integration_id, days=days)
        snapshot = snapshot_from_postiz_payload(payload, platform=platform)
        snapshot_id = record_snapshot(snapshot)
    except (RuntimeError, ValueError) as exc:
        typer.echo(f"postiz platform analytics ingest failed: {exc}")
        raise typer.Exit(code=2) from exc

    typer.echo(f"analytics_snapshot_id={snapshot_id}")
    typer.echo(f"platform={snapshot.platform}")
    typer.echo(f"views={snapshot.views}")
    typer.echo(f"conversions={snapshot.conversions}")
    typer.echo(f"revenue={snapshot.revenue}")


@app.command()
def improve_cycle(niche: str = "gta6-ai-persona-gaming") -> None:
    """Run one autonomous improvement cycle (scan orchestration -> distill -> propose).

    Safe by design: never generates paid media, never publishes, never edits
    skill/rule files. It records insights + proposals and a full event trace.
    """

    result = run_improvement_cycle(niche=niche)
    typer.echo(f"trace_id={result.trace_id} run_id={result.run_id}")
    typer.echo(f"summary={result.summary}")
    typer.echo(f"blocked_actions={result.blocked_actions}")


@app.command()
def daemon_status(daemon: str = "improvement-daemon") -> None:
    """Show read-only daemon status, backlog, and blocked actions."""

    status = get_daemon_status(daemon)
    typer.echo(f"daemon={status.daemon}")
    if status.latest_run:
        run = status.latest_run
        typer.echo(f"latest_run_id={run['id']}")
        typer.echo(f"latest_trace_id={run['trace_id']}")
        typer.echo(f"latest_status={run['status']}")
        typer.echo(f"started_at={run['started_at']}")
        typer.echo(f"finished_at={run['finished_at']}")
        typer.echo(f"summary={run['summary']}")
        typer.echo(f"counts={json.dumps(run['counts'], sort_keys=True)}")
        if run["error"]:
            typer.echo(f"error={run['error']}")
    else:
        typer.echo("latest_run_id=None")
        typer.echo("latest_status=never_run")
    typer.echo(f"active_insights={status.active_insights}")
    typer.echo(f"open_proposals={status.open_proposals}")
    typer.echo(f"recent_events={status.recent_events}")
    typer.echo(f"blocked_actions={status.blocked_actions}")


@app.command()
def memory_consolidate(min_confidence: float = 0.6, limit: int = 20) -> None:
    """Promote high-confidence active insights into deduped procedural lessons."""

    result = consolidate_insights_to_lessons(min_confidence=min_confidence, limit=limit)
    typer.echo(f"scanned={result.scanned}")
    typer.echo(f"created={result.created}")
    typer.echo(f"skipped_existing={result.skipped_existing}")
    typer.echo(f"lesson_ids={result.lesson_ids}")


@app.command()
def insights_list(scope: str = "", limit: int = 20, min_confidence: float = 0.0) -> None:
    """List active, deduped insights (highest-confidence first)."""

    rows = active_insights(scope or None, limit=limit, min_confidence=min_confidence)
    for i in rows:
        typer.echo(f"[{i.id}] {i.scope} conf={i.confidence:.2f} support={i.support_count} :: {i.statement}")
    if not rows:
        typer.echo("(no active insights)")


@app.command()
def insight_add(scope: str, statement: str, confidence: float = 0.5) -> None:
    """Manually distill one insight (dedup-aware)."""

    insight_id, created = distill_insight(scope=scope, statement=statement, confidence=confidence)
    typer.echo(f"insight_id={insight_id} created={created}")


@app.command()
def proposals_list(limit: int = 50) -> None:
    """List open improvement proposals awaiting human decision."""

    rows = open_proposals(limit=limit)
    for p in rows:
        typer.echo(f"[{p['id']}] {p['target_type']}:{p['target_name']} ({p['status']}) :: {p['change_summary']}")
    if not rows:
        typer.echo("(no open proposals)")


@app.command()
def proposals_dedupe() -> None:
    """Supersede duplicate open improvement proposals, keeping one live copy."""

    count = dedupe_open_proposals()
    typer.echo(f"superseded={count}")


@app.command()
def creator_add(
    platform: str,
    handle: str,
    niche: str = "",
    followers: int = 0,
    display_name: str = "",
    source_url: str = "",
) -> None:
    """Register a benchmark creator candidate (proof of success added separately)."""

    creator_id = upsert_creator(
        platform=platform,
        handle=handle,
        display_name=display_name or None,
        niche=niche or None,
        followers=followers or None,
        source_url=source_url or None,
    )
    typer.echo(f"creator_id={creator_id}")


@app.command()
def creator_proof(
    creator_id: int,
    engagement_rate: float = 0.0,
    monetization: str = "",
    consistency_days: int = 0,
    notes: str = "",
) -> None:
    """Attach proof-of-real-success and compute credibility (not vanity metrics)."""

    credibility = set_creator_proof(
        creator_id,
        proof_engagement_rate=engagement_rate or None,
        proof_monetization=monetization or None,
        proof_consistency_days=consistency_days or None,
        proof_notes=notes or None,
    )
    typer.echo(f"creator_id={creator_id} credibility={credibility}")


@app.command()
def aside_scan_import(path: Path) -> None:
    """Import logged-in Aside Instagram/TikTok scan JSON into benchmark tables."""

    try:
        summary = import_aside_scan(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        typer.echo(f"scan import failed: {exc}")
        raise typer.Exit(code=2) from exc
    typer.echo(f"trace_id={summary.trace_id}")
    typer.echo(f"observations_seen={summary.observations_seen}")
    typer.echo(f"creators_upserted={summary.creators_upserted}")
    typer.echo(f"videos_inserted={summary.videos_inserted}")
    typer.echo(f"videos_duplicate={summary.videos_duplicate}")
    typer.echo(f"creators_verified_or_plausible={summary.creators_verified_or_plausible}")


@app.command()
def trace_show(trace_id: str) -> None:
    """Replay a full event trace ('every bullet tracer') for one run."""

    for e in trace_events(trace_id):
        typer.echo(f"{e['created_at']} | {e['stage']:8} | {e['actor']:18} | {e['event_type']:8} | {e['payload']}")


if __name__ == "__main__":
    app()
