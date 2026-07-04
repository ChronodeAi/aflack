# Long-Term Memory System — Research & Architecture Direction

**Created**: 2026-07-03
**Purpose**: Design a durable "company memory" for the content-creation + marketing pipeline: never forgets, de-duplicates, resists context rot, holds episodic + semantic + procedural memory, and injects only relevant memory on demand (not jammed into every context). Starting reference: agentmemory (coding-focused). Research-first; benchmark 2-3 candidates on our own data before committing.

> Sources: web research 2026-07-03 (multiple 2026 framework comparisons) + local agentmemory skills. Third-party benchmark numbers are directional, not gospel.

## Why agentmemory alone isn't the answer

agentmemory is a strong *reference implementation* and a good default for coding-session memory:
- Hybrid recall = BM25 keyword + vector similarity + graph expansion over linked concepts.
- Zero-LLM by default (on-device embeddings), so capture is cheap; LLM summaries + context injection are opt-in flags.
- Lifecycle: capture → compress → consolidate → forget (this is exactly the anti-rot loop we want).
- Automatic capture via lifecycle hooks (session start/end, tool-use, prompt-submit, pre-compact, post-commit).

But it's oriented around *coding sessions and commits*. Our memory is a **marketing/content domain memory**: products, niches, personas, hooks, scripts, creatives, variants, channels, disclosures, claims, and performance results — with a strong need for **temporal fact validity** (a product's GMV, a hook's win-rate, a compliance rule all change over time) and **dedup across near-identical creative ideas**. So: keep agentmemory's *design principles* (hybrid retrieval, capture hooks, consolidate/forget lifecycle, relevance-gated injection) and evaluate a domain-fit engine underneath.

## The three memory scopes have standardized (we want all three)

The field has converged on three scopes — our schema must cover each:
- **Episodic** — specific past events/interactions (this video posted on this date got this retention curve).
- **Semantic** — durable facts/preferences (this niche's compliance rules; this persona's traits; this product's margin).
- **Procedural** — learned behaviors/rules (our winning hook templates; our "never make GLP-1 claims" rule; our publish checklist).

## Candidate engines (open source, 2026)

| Engine | Core model | Best at | Watch-outs | Fit for us |
|---|---|---|---|---|
| **Mem0** | Vector + optional graph + key-value; user/session/agent scopes; auto extraction + dedup; multi-signal retrieval | Fastest to integrate; product-ready personalization; largest community (~47k stars); free tier | Graph ("Mem0g") gated behind paid Pro (~$249/mo); mid-pack on temporal benchmark (~49% LongMemEval) | Strong default memory *API* for persona/user-facing memory; weak if we need heavy temporal reasoning |
| **Zep / Graphiti** | Temporal knowledge graph; facts stored with `valid_at`/`invalid_at` validity windows; hybrid semantic+BM25+graph retrieval | "What was true as of last Tuesday" — temporal correctness + clean invalidation (kills stale-fact rot) | Higher per-retrieval latency; graph adds ops; some features gated to Zep Cloud (Graphiti core is OSS, self-hostable) | Best for our benchmark/performance facts that change over time; strong anti-rot invalidation |
| **Cognee** | Graph+vector+relational hybrid; ECL (Extract→Cognify→Load) pipeline; 14 retrieval modes; self-improving "memify"; MCP + LangGraph native | Most complete graph-native "control plane"; 100% local (SQLite/LanceDB/KuzuDB) incl. Ollama; production proof (Bayer, etc.) | Heaviest/most complex; no SOC2/HIPAA certs (fine for us early) | Best if we want ONE self-hosted engine to remember + reason + improve; steeper setup |
| **Letta (MemGPT)** | OS-style tiered memory: small self-edited core + large archival/recall; agent curates its own working set via tool calls | Long-running stateful agents that own their memory | Opinionated runtime (a second orchestration layer); trades determinism for emergence — less control over exact capture/forget | Interesting for an autonomous "content operator" agent later; not the base memory store |
| **LangMem** | LangGraph-native hot-path + background memory | Teams already on LangGraph | Lock-in; limited value outside LangGraph | Only if we standardize on LangGraph |
| **Supermemory** | Universal memory + RAG, MCP integrations (Claude Code/OpenCode) | Coding-agent + cross-tool memory | Closed source; self-host needs enterprise deal | Not for an OSS "never forgets" build |
| **agentmemory** | BM25 + vector + concept-graph; zero-LLM default; capture hooks; consolidate/forget | Local coding-session memory; capture-hook pattern reference | Coding/commit-oriented schema | Keep as reference + possibly the coding-side memory; not the marketing-domain store |

## The failure modes we must design against (from the research)

1. **Context rot / stale facts** — flat vector stores retrieve the closest embedding, and a *stale* fact often embeds as close as the current one. **Invalidation over time is the thing almost nobody designs for** and separates the frameworks most. → Favor an engine with explicit fact validity windows (Zep/Graphiti) or a real consolidate/forget lifecycle (agentmemory/Cognee).
2. **Everything-in-context bloat** — the fix is relevance-gated retrieval: send only the relevant memories, not the whole history. Our system must *retrieve then inject*, never dump.
3. **Write-path LLM cost** — Mem0/Zep/Cognee run LLM calls on write to extract facts/build graph; at volume that bill rivals retrieval. → Pin a cheap extraction model (4o-mini class), batch writes, don't re-extract every message.
4. **Framework lock-in** — native data models differ; storing memory *only* inside a framework makes migration a salvage job. → **Keep the raw event stream (posts, results, ingests) in our own Postgres/S3 and treat the memory engine as an *index* over it.** Migration becomes a re-ingest.
5. **"Memory" is overloaded** — a truncating chat buffer ≠ a temporal knowledge graph. Match engine to requirement, not marketing label.

## Recommended architecture direction (to validate, not final)

A layered design that mirrors agentmemory's principles but is domain-fit and swappable:

```
                 ┌─────────────────────────────────────────┐
                 │  Raw event store (source of truth)         │  <- OWN THIS
                 │  Postgres + object storage (S3-compatible) │
                 │  posts, creatives, results, ingests, logs  │
                 └───────────────┬───────────────────────────┘
                                 │ (re-ingestable)
        ┌────────────────────────┼─────────────────────────┐
        │ Capture hooks           │                          │
        │ (what/when/why/how)     ▼                          │
   ┌────┴─────┐          ┌────────────────┐          ┌───────┴────────┐
   │ Episodic │          │   Semantic     │          │  Procedural    │
   │ events   │          │ facts + graph  │          │ rules/playbooks│
   └────┬─────┘          └───────┬────────┘          └───────┬────────┘
        └─────────── memory engine (swappable adapter) ──────┘
                                 │
                    hybrid retrieval: BM25 + vector + graph + temporal
                                 │  (relevance-gated)
                                 ▼
                 inject ONLY relevant memory into agent context
```

- **Engine choice (leaning):** start with **Mem0** (fastest to working memory, dedup + scopes) for persona/user + general memory, and **evaluate Zep/Graphiti** in parallel for the temporal performance-facts layer (product/hook/creative win-rates with validity windows). If we want a single self-hosted brain later, **Cognee** is the consolidation candidate. Keep **agentmemory** for the coding side of the build.
- **Capture policy (the "what/when/why/how"):** codify hooks like agentmemory —
  - *When*: end of each content experiment, each publish, each performance pull, each niche decision, each compliance ruling.
  - *What*: distilled facts, not raw logs ("hook A held 58% at 3s on beauty-tool X" not the whole transcript).
  - *Why*: so future generation is conditioned on proven winners and past failures/rejections.
  - *How*: cheap extraction model + dedup on write; link to the raw event in the source store.
- **Anti-rot lifecycle:** capture → compress → consolidate → forget/expire, plus temporal invalidation for facts that change. Dedup on write so near-identical creative ideas strengthen an existing memory instead of multiplying it.
- **Retrieval discipline:** every agent call does retrieve-then-inject with a token budget; nothing is permanently pinned except a tiny "core" (brand voice, non-negotiable compliance rules).

## Open questions to resolve with deeper research + a bake-off

- [ ] Run a 2-3 engine bake-off (Mem0 vs Zep/Graphiti vs Cognee) on OUR data: store real experiment results, re-run the generation agent, measure whether creative quality/hit-rate improves over time.
- [ ] Confirm current OSS vs paid boundaries live (Mem0 graph tier, Zep Cloud gates, Cognee local stack) — pricing/limits change.
- [ ] Decide self-host vs managed for v1 (favor self-host + local embeddings for "never forgets" + cost control; Cognee/Graphiti both run local).
- [ ] Define the marketing-domain schema (entities: Product, Niche, Persona, Hook, Script, Creative, Variant, Channel, Disclosure, Claim, Result, Lesson) and the capture-hook triggers.
- [ ] Decide the extraction model + batching policy to control write-path LLM cost.

## Immediate next actions

- [ ] Draft the marketing-domain memory schema + capture-hook trigger list as a spec artifact.
- [ ] Stand up a throwaway Mem0 local instance and a Graphiti local instance; ingest 20 sample results; compare retrieval quality + invalidation behavior.
- [ ] Document the "own the raw event store" decision as an ADR (avoids lock-in).
