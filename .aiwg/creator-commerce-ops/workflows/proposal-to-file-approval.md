# Workflow: proposal-to-file-approval

**Purpose**: Convert daemon or insight-curator improvement proposals into file changes only after explicit human approval.

## Inputs

- `improvement_proposals` row with status `proposed`.
- Target type/name such as `skill:hook-authoring` or `rule:compliance-before-publish`.
- Human approval marker naming the proposal ID and allowed target file(s).

## Hard gates

1. No autonomous edits to skills, rules, workflows, agents, templates, or prompts.
2. No proposal application without a human approval marker.
3. No edits outside the approved file set.
4. No public publish, paid generation, account changes, or DM/comment automation as part of proposal application.
5. Every proposal application must record a trace event.

## Approval marker

A proposal is approved only when the operator writes or states an approval with:

```text
approve proposal <proposal_id> for files: <path1>, <path2>
```

The implementation session must preserve that approval text in the resulting report or trace payload.

## Steps

1. **List proposed changes**
   - Run/read `aflack proposals-list`.
   - Select exactly one proposal unless the operator approves a batch.
2. **Validate target scope**
   - Confirm `target_type` and `target_name` match the approved file(s).
   - Reject if the proposal tries to change unrelated files.
3. **Prepare patch**
   - Apply the smallest useful edit.
   - Keep existing safety rules intact.
   - Add or update tests when runtime code changes.
4. **Record trace**
   - Append a `pipeline_events` row or equivalent trace with:
     - proposal ID,
     - approved files,
     - applied files,
     - validation commands,
     - result.
5. **Update proposal status**
   - `approved` once approval is received.
   - `applied` only after the patch and validation pass.
   - `rejected` if the operator rejects the proposal.
6. **Validate**
   - Run the narrow relevant test first.
   - Then run the standard gate for code changes:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy src
uv run python -m compileall -q src
uv run python -m pytest tests/ --tb=short -q
```

## Output artifact

Write a short report under `.aiwg/reports/proposal-application-<proposal_id>-YYYY-MM-DD.md` containing:

- proposal ID,
- approval marker,
- files changed,
- validation results,
- any deferred follow-ups.
