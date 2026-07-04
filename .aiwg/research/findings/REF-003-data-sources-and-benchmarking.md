---
ref_id: "REF-003"
title: "Data Sources, Indexers & Benchmarking Layer"
year: 2026
source_type: technical_report
authors:
  - name: "aflack project (internal research)"
quality_assessment:
  grade: moderate
  note: "Internal web-research synthesis; third-party figures directional"
---

# Data Sources, Indexers & Benchmarking Layer — Affiliate Content Pipeline

**Created**: 2026-07-03
**Purpose**: Catalog the top APIs, indexers, and aggregators for winning products and winning videos, so the pipeline can continuously benchmark our AI-generated content against the best creators ("crème de la crème") and validate before/after publishing. Research-first; verify pricing/access live before committing.

> Sources: web research 2026-07-03 (industry comparison articles + official TikTok surfaces). Treat all third-party GMV/sales numbers as estimates, not truth.

## Key structural insight (design constraint)

Most third-party market-intelligence tools (Kalodata, FastMoss, Shoplus, EchoTik, Pipiads, Gloda) do **not** have official TikTok API access — they run on web scraping, so their data and access can break when TikTok changes its frontend. Only profit trackers and campaign tools with a Seller Center connection read *your own* store data via official integration. Implication: our benchmarking layer should (a) prefer official first-party surfaces where possible, (b) treat third-party APIs as swappable adapters, and (c) build resilient ingestion (Aside logged-in browsing as fallback when APIs break).

## Tier 0 — Official / first-party (free or near-free, most durable)

| Source | What it gives | Access | Use in pipeline |
|---|---|---|---|
| **TikTok Creative Center** (`ads.tiktok.com/business/creativecenter`) | Top Ads, Top Products (trending SKUs/categories by region + growth rate), Trend Discovery (hashtags/songs/creators/videos), Keyword Insights, Creative Codes | Free forever; general browsing needs no login; product insights/advanced filters unlock with a (free) TikTok Ads Manager account | Primary trend + product discovery, hook research, category CTR/CVR/CPA benchmarks |
| **TikTok Creative Center — Top Products** | Popularity (ad-creative count), CTR, CVR, CPA, cost, impressions, 6s view rate per product/category | Same as above; desktop only | Niche/product shortlisting + benchmark targets |
| **TikTok Ads Manager (TTAM) benchmark overlays** | Your CTR/CVR/6s-view-rate plotted vs industry benchmarks; reach/CPM estimator; higher Symphony AI quotas | Free account; some features need a small test spend (~$50) | Validate our creatives against industry benchmark bands |
| **TikTok Commercial Content Library (CCL)** (`library.tiktok.com`) | Raw ad transparency (comprehensive, uncurated) | EEA, UK, Switzerland only as of Apr 2026 | Deep ad reconnaissance if we run EU |
| **TikTok Research API** | Programmatic content/commercial data; Feb 2026 expansion added Playlist Info + deeper commercial access | Restricted to academics/vetted journalists; broader/global access "in the works," no ETA | Watch item; not available to us yet |
| **TikTok Creator Marketplace (TTCM)** | Official creator discovery + performance metrics | Business access | Real-creator style benchmarking, later creator sourcing |

**Benchmark targets extracted from Creative Center data (industry reporting, verify live):**
- Hook: retain **55%+ of viewers at second 3** = strong hook by top-performer standards.
- Retention curve pattern: sec0–1 100%→75–85%; sec1–3 →50–60% (hook quality); sec3–6 →40–50%; sec6–15 →25–35%.
- Duration: top-CTR ads cluster **15–25s**, not sub-10s (contradicts "shorter is always better").
- E-commerce CTR: ~0.5% ≈ mid-pack of the *best* ads; ~0.3% = optimization headroom.
- Trust-sensitive verticals (health, finance): real-person/Spark Ads still outperform branded/AI-source content — "authenticity of format, not source." Relevant to our health/beauty compliance + persona strategy.

## Tier 1 — Third-party market intelligence (scraped; swappable adapters)

| Tool | Strength | Notable | API? | Est. entry price |
|---|---|---|---|---|
| **Kalodata** | Deepest product + creator + video + livestream research; strongest for research-first product/market reading | Insider-team credibility; can miss private-livestream "shadow sales" (~12–15% under EchoTik on live GMV) | Not official TikTok API | ~$49–50/mo, 7-day trial |
| **FastMoss** | Real-time trend/creator discovery; agency/operator workflows; ad monitoring; long historical depth | Tracks *intent* (flags rising early; may over-count vs settled sales); offers a dedicated **API plan** | Own API (scraped data) | ~$54/mo; API tier extra |
| **Shoplus** | Budget product research + creator discovery; trend following | ~800k users; reviewers flag bugs/accuracy; ~90-day history cap; no AI features | Not official | ~$15–49/mo, limited free tier |
| **EchoTik** | Strong free tier; product/creator/shop/livestream data; best live-GMV/"actual revenue" accuracy of the group; Chrome+Firefox extension | Tracks *settled* sales (more conservative than FastMoss intent); "Identity Osmosis" multi-platform influence score | Not official | ~$9.90–19/mo; real free plan |
| **Pipiads** | TikTok **ad-spy** — hooks, creatives, AI creative-performance prediction | Credit system gets expensive; reputational red flags (low Trustpilot) — vet carefully | Not official | ~$49–99/mo |
| **SmartScout (TikTok)** | Category-level market sizing, revenue estimates, market share, white-space | Category/white-space focus | — | mid |
| **Gloda** | Multimodal AI (video+audio+image) product insight — deeper than text-only | New/unproven at scale (~50k sellers) — watch | — | freemium |
| **Pentos** | Content analytics: viral patterns, hashtag performance, creator benchmarking | Content-first | — | — |
| **SimpTok** | Free, beginner worksheets/trend visibility | Shallow depth | — | free |

**Profit/operations (official Seller Center connections, our own data only):** Dashboardly, Kixmon (profit trackers); SFN AI, Euka, Reacher, Hubfluence, Cruva (campaign/creator mgmt, verified TikTok Shop App Store partners). Use later for margin truth + creator ops, not market discovery.

## Tier 2 — Creative validation / scoring (benchmark our own output)

| Source | Role |
|---|---|
| **Higgsfield Virality Predictor** (`brain_activity`) | Score a finished video's hook/attention/retention/virality before publishing; iterate creatives until they clear a threshold. Our in-house pre-publish gate. |
| **TikTok Creative Center Top Ads (same niche)** | Human/statistical benchmark set to compare structure, hook, pacing, CTA against real winners. |
| **Post-publish platform analytics** | Retention curve, CTR, CVR, GMV — the ground-truth loop that overrides all estimates. |

## Adapter/access strategy (build notes)

1. **Official-first**: Creative Center (Top Products, Top Ads, Trends, Keyword Insights) is the durable spine — free, first-party. Requires a free TTAM account for full filters; a ~$50 test spend unlocks benchmark overlays.
2. **Third-party as pluggable adapters**: wrap each tool (start with 1 research tool — Kalodata *or* FastMoss, they overlap ~80% — plus EchoTik free for settled-sales cross-check) behind a common interface so we can swap when one breaks or when pricing changes.
3. **Aside fallback for logged-in/scrape-fragile surfaces**: when an API breaks or a tool has no API, drive the logged-in web UI through Aside; if a site isn't signed in, prompt the user to sign in via Aside, then build a reusable Aside skill for that site.
4. **Cross-validate estimates**: FastMoss ≈ intent (early/optimistic), EchoTik ≈ settled (conservative). Never trust a single tool's GMV; reconcile against Seller Center once we transact.
5. **Benchmark dataset**: for each niche, pull 15–50 top ads/videos + top products, tag them (hook, retention proxy, format, duration, persona, proof, CTA, disclosure, claim-risk), and store as the "gold set" our AI content is scored against.

## Open questions to resolve with live research (before committing spend)

- Current exact pricing + API availability/limits for FastMoss API and Kalodata (verify live; do not trust cached numbers).
- Whether we qualify for any expanded TikTok Research API access.
- Which single research tool best covers beauty/wellness product + creator depth for our chosen beachhead.
- Rate limits / ToS constraints for automated ingestion (scraping legality/ToS risk per tool).

## Immediate next research actions

- [ ] Live-verify Kalodata vs FastMoss beauty/wellness coverage + current pricing/API (Firecrawl + Aside logged-in trial).
- [ ] Stand up a free TTAM account to unlock Creative Center Top Products filters + benchmark overlays (needs user login via Aside).
- [ ] Pull a first "gold set" of top beauty/wellness ads + products and define numeric benchmark thresholds.
- [ ] Prototype Higgsfield Virality Predictor scoring on 3 sample generated clips to calibrate a pass/fail gate.
