# Dependency Update Policy

## Minimum Release Age

All dependency updates must wait **7 days** after the upstream release before
being merged. This mitigates supply chain attacks from malicious packages
published and quickly yanked.

## Implementation

- Dependabot is configured with weekly updates (see `.github/dependabot.yml`)
- Reviewers MUST verify the dependency was released at least 7 days ago before
  approving a Dependabot PR
- Emergency security fixes may bypass this policy with explicit operator approval

## Review Checklist

1. Check the release date of the new version on PyPI/GitHub
2. Verify at least 7 days have passed since release
3. Review the changelog for breaking changes
4. Run `uv sync --extra dev && uv run pytest tests/ -q` to verify tests pass
5. Check for any new transitive dependencies
