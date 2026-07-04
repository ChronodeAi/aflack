# Aside MCP Triage — 2026-07-04

## Summary

The Codex-exposed `mcp__aside__repl` tool initially returned `Transport closed`.

## Backend checks

- `aside --version`: 1.26.626.1517
- `aside account status`: signed in as `tech@chronode.ai` on `u0`, Profile 0
- `aside repl "console.log(...)"`: PASS
- `aside mcp` process startup: PASS
- direct JSON-RPC `initialize` handshake to `aside mcp`: PASS
- configured command in `~/.codex/config.toml`: `/Users/ace/.local/bin/aside`, args `["mcp"]`

## Diagnosis

Aside itself and the stdio MCP server are healthy. The failing piece is the already-attached Codex MCP transport wrapper for this running session. Since the CLI and MCP backend are healthy, the safe fallback is the Aside CLI (`aside repl` for deterministic browser tooling, `aside exec` for autonomous browser research).

## Policy for this run

Use read-only Aside CLI sessions for Instagram/TikTok research. Do not like, comment, follow, DM, post, or change settings.

## Final status for this run

- Codex MCP tool wrapper: still returned `Transport closed` when invoked from this session.
- Aside backend/CLI/MCP server: healthy and verified.
- Resolution used for this run: safe fallback to `aside exec` / `aside repl` CLI, which successfully accessed logged-in Instagram and TikTok browser sessions.
- Scan policy observed: read-only. No likes, comments, follows, DMs, saves, posts, uploads, or settings changes.
- Output imported: `.aiwg/working/aside-scans/live-ig-tiktok-gta6-2026-07-04.json`.
- Import command: `aflack aside-scan-import .aiwg/working/aside-scans/live-ig-tiktok-gta6-2026-07-04.json`.

To restore the Codex-exposed MCP wrapper specifically, a fresh Codex/MCP session reload may be required; the underlying `aside mcp` server itself initializes correctly.
