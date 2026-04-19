"""
auto_pm_agent.py
----------------
PM Job Search Automation Agent — powered by Claude Code + CCR

Product Description
-------------------
This module documents the design logic of an automated Product Manager job
search system built on top of Claude Code's skill and scheduling infrastructure.

Architecture Overview
---------------------

    [Claude Code Remote (CCR)]
         Runs daily at 09:00 Asia/Taipei (cron: 0 1 * * *)
         Model: claude-sonnet-4-6
         │
         ├── WebSearch (x4 queries, no site: operators)
         │       "product manager jobs Taiwan 2026"
         │       "product manager Taiwan CakeResume"
         │       "product manager Taiwan Yourator"
         │       "104 product manager Taiwan"
         │
         ├── Extract job listings from search snippets
         │       Fields: company, title, location, salary, url, source
         │
         ├── Deduplicate (company + title)
         │
         └── Commit pm-jobs-report.md → GitHub (hsuan2828/claude_skills)

    [Local Claude Code CLI]
         Skills auto-triggered by natural language
         │
         ├── pm-job-search skill  →  /pm-jobs
         │       On-demand search with optional keyword filter
         │       Cross-checks against existing job-applications.json
         │
         └── job-tracker skill    →  /jobs
                 CRUD for ~/.claude/job-applications.json
                 Status lifecycle: want-to-apply → applied → interview → offer/rejected

Data Schema
-----------
Each job entry in ~/.claude/job-applications.json:

    {
        "id":         int,           # auto-increment
        "company":    str,
        "title":      str,
        "url":        str | None,
        "status":     Literal["want-to-apply", "applied", "interview",
                               "offer", "rejected"],
        "deadline":   str | None,    # YYYY-MM-DD
        "salary":     str | None,    # e.g. "60K-80K"
        "location":   str | None,    # e.g. "Remote", "Taipei"
        "notes":      str,
        "added_at":   str,           # YYYY-MM-DD
        "updated_at": str            # YYYY-MM-DD
    }

Supported Platforms
-------------------
- CakeResume       https://www.cakeresume.com
- LinkedIn         https://www.linkedin.com/jobs
- 104人力銀行      https://www.104.com.tw
- Yourator         https://www.yourator.co
- 1111人力銀行     https://www.1111.com.tw

Skill Files
-----------
- job-tracker-plugin/skills/job-tracker/SKILL.md
- job-tracker-plugin/skills/pm-job-search/SKILL.md
- job-tracker-plugin/commands/jobs.md
- job-tracker-plugin/commands/pm-jobs.md

Usage Examples
--------------
# Search for PM jobs now (local, interactive)
# > /pm-jobs
# > /pm-jobs fintech
# > /pm-jobs remote

# Manage tracked applications
# > /jobs list
# > /jobs add
# > 新增職缺：Stripe，Product Manager，deadline 5/1
# > mark job 3 as applied

Scheduled Trigger
-----------------
Trigger ID : trig_01XCLpjkDMwQdFLqapnoiH5A
Schedule   : 0 1 * * * UTC  (09:00 Asia/Taipei)
Output     : pm-jobs-report.md (auto-committed to this repo)
Manage at  : https://claude.ai/code/scheduled
"""

# ── Simulated run (for portfolio demonstration) ──────────────────────────────

import json
from datetime import date


SAMPLE_JOBS = [
    {
        "id": 1,
        "company": "Canva",
        "title": "Product Manager, Growth",
        "url": "https://www.cakeresume.com/jobs/canva-pm-growth",
        "status": "want-to-apply",
        "deadline": None,
        "salary": "NT$2M+",
        "location": "Remote / Taipei",
        "notes": "Found via CakeResume daily search",
        "added_at": str(date.today()),
        "updated_at": str(date.today()),
    },
    {
        "id": 2,
        "company": "Appier",
        "title": "Senior Product Manager",
        "url": "https://www.linkedin.com/jobs/view/appier-senior-pm",
        "status": "applied",
        "deadline": "2026-05-01",
        "salary": "NT$1.8M–2.2M",
        "location": "Taipei",
        "notes": "Applied via LinkedIn. Referral from Alice.",
        "added_at": str(date.today()),
        "updated_at": str(date.today()),
    },
]


def display_jobs(jobs: list[dict]) -> None:
    """Print job list grouped by status (mirrors the /jobs list skill output)."""
    status_emoji = {
        "want-to-apply": "🎯",
        "applied":        "📤",
        "interview":      "🗣️",
        "offer":          "🎉",
        "rejected":       "❌",
    }
    grouped: dict[str, list] = {}
    for job in jobs:
        grouped.setdefault(job["status"], []).append(job)

    for status, group in grouped.items():
        emoji = status_emoji.get(status, "•")
        print(f"\n### {emoji} {status.replace('-', ' ').title()} ({len(group)})")
        print(f"{'ID':<4} {'Company':<20} {'Title':<30} {'Location':<15} {'Deadline'}")
        print("-" * 80)
        for j in group:
            print(f"{j['id']:<4} {j['company']:<20} {j['title']:<30} "
                  f"{j.get('location') or '':<15} {j.get('deadline') or '—'}")


if __name__ == "__main__":
    print("=== PM Job Tracker — Sample Output ===")
    display_jobs(SAMPLE_JOBS)
    print(f"\nData schema:\n{json.dumps(SAMPLE_JOBS[0], indent=2, ensure_ascii=False)}")
