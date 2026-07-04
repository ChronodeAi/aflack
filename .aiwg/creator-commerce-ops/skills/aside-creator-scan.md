# Skill: aside-creator-scan

Purpose: use logged-in Aside Browser sessions to observe Instagram/TikTok/YouTube creators and export structured benchmark observations.

Inputs:
- niche query,
- target platforms,
- number of creators/videos,
- proof criteria.

Output JSON contract: `.aiwg/creator-commerce-ops/templates/aside-scan.schema.json`.

Command path:
```bash
aside exec --effort ultrabrowse "<scan prompt>"
aflack aside-scan-import .aiwg/working/aside-scans/<file>.json
aflack improve-cycle
```

Safety:
- no private API scraping,
- no liking/commenting/following,
- no DM automation,
- read-only observation only.
