# Workflow: daemon-sdlc-loop

Cadence: every 6 hours by launchd/cron.

Steps:
1. scan or wait for Aside scan exports,
2. import benchmark observations,
3. distill/reinforce insights,
4. write improvement proposals,
5. record every event trace,
6. surface proposals for human approval.

Command:
```bash
scripts/aflack-improve-daemon.sh
```
