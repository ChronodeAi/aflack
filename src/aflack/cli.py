"""CLI for local Day-1 pipeline operations."""

from __future__ import annotations

from pathlib import Path

import typer

from .db import connect, exec_sql
from .compliance import check_publish_item
from .economics import current_rollup
from .publishing import PostizPublisher, PublishIntent

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


if __name__ == "__main__":
    app()
