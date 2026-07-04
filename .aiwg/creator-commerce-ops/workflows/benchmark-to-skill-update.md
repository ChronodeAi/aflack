# Workflow: benchmark-to-skill-update

1. `aflack aside-scan-import <scan.json>`
2. `aflack improve-cycle`
3. `aflack insights-list --min-confidence 0.5`
4. `aflack proposals-list`
5. human reviews proposal
6. accepted proposal is encoded into a project-local skill/rule/workflow
7. test and record trace
