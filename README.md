# Claude Code Skills — Job Search Automation

A Claude Code plugin that automates Product Manager job hunting in Taiwan — searches multiple job boards daily and tracks applications.

## What This Does

```
每天早上 9 點自動執行
         │
         ▼
┌─────────────────────┐
│  PM Job Search      │  WebSearch on CakeResume, LinkedIn,
│  Agent (CCR Cloud)  │  104人力銀行, Yourator
└────────┬────────────┘
         │ commit
         ▼
┌─────────────────────┐
│  pm-jobs-report.md  │  Daily job listings table
│  (this repo)        │
└─────────────────────┘
         │ user reviews
         ▼
┌─────────────────────┐
│  /jobs add          │  Save interesting jobs to local tracker
│  (Claude Code CLI)  │  ~/.claude/job-applications.json
└─────────────────────┘
```

## Skills

### `job-tracker`
Track job applications locally. Triggered by natural language:

```
新增職缺：Stripe，Product Manager，deadline 5/1
/jobs list
/jobs update 3 applied
```

Stores data in `~/.claude/job-applications.json`. Supports status tracking: 🎯 want-to-apply → 📤 applied → 🗣️ interview → 🎉 offer / ❌ rejected.

### `pm-job-search`
Search multiple job platforms for PM openings. Triggered by:

```
搜尋最新PM職缺
/pm-jobs
/pm-jobs fintech
/pm-jobs remote
```

Searches: CakeResume · LinkedIn · 104人力銀行 · Yourator · 1111人力銀行

## Automation

A scheduled Claude Code Remote (CCR) agent runs daily at 9:00 AM (Taipei time) and commits search results to [`pm-jobs-report.md`](./pm-jobs-report.md).

**Schedule:** `0 1 * * *` (UTC) = 09:00 Asia/Taipei  
**Model:** claude-sonnet-4-6  
**Managed at:** https://claude.ai/code/scheduled

## Installation

```bash
# Copy plugin to Claude Code plugins directory
cp -r job-tracker-plugin ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/job-tracker

# Restart Claude Code — skills activate automatically
```

## File Structure

```
claude_skills/
├── README.md
├── pm-jobs-report.md              # Auto-updated daily by scheduled agent
└── job-tracker-plugin/
    ├── .claude-plugin/
    │   └── plugin.json            # Plugin manifest
    ├── commands/
    │   ├── jobs.md                # /jobs slash command
    │   └── pm-jobs.md             # /pm-jobs slash command
    └── skills/
        ├── job-tracker/
        │   └── SKILL.md           # Application tracking logic
        └── pm-job-search/
            └── SKILL.md           # Job board search logic
```

## Tech Stack

- **Claude Code** — CLI with plugin/skill system
- **Claude Code Remote (CCR)** — Cloud-hosted scheduled agents
- **WebSearch / WebFetch** — Job board scraping
- **GitHub** — Result storage and portfolio

---
*Built with [Claude Code](https://claude.ai/code)*
