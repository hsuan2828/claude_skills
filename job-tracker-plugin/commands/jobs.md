---
name: jobs
description: Manage your job application list. Usage: /jobs [add|list|update|remove|search] [args]
---

Show or manage your job application tracker.

- `/jobs` or `/jobs list` — list all tracked jobs grouped by status
- `/jobs add` — add a new job (Claude will ask for details)
- `/jobs update <id>` — update a job's status or notes
- `/jobs remove <id>` — remove a job from the list
- `/jobs search <keyword>` — search across company/title/notes

The tracker stores data in `~/.claude/job-applications.json`.

Use the job-tracker skill to handle the actual operation based on the subcommand and any arguments provided.
