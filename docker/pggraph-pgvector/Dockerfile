# Local dev image: pgGraph + pgvector (all-in-Postgres memory substrate).
# pgGraph is early alpha — this image is for LOCAL/DEV use only, not production.
FROM ghcr.io/evokoa/pggraph:0.1.8

# Add pgvector for embeddings alongside the graph + pg_cron extensions.
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-17-pgvector \
    && rm -rf /var/lib/apt/lists/*

# Auto-create the vector extension on first init (graph/pg_cron already handled by base image).
RUN printf 'CREATE EXTENSION IF NOT EXISTS vector;\n' > /docker-entrypoint-initdb.d/20-pgvector.sql

# Inherit the base image's entrypoint/CMD (Postgres).
