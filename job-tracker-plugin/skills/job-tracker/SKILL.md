---
name: job-tracker
description: This skill should be used when the user wants to "track a job", "add a job application", "list jobs I want to apply to", "update job status", "record a job posting", "manage job applications", "show my job list", "mark job as applied", "add notes to a job", "remove a job", or anything related to organizing job opportunities and applications. Also activates for phrases like "整理職缺", "新增職缺", "職缺清單", "求職追蹤", "應徵紀錄".
version: 1.0.0
---

# Job Application Tracker

Help the user manage job opportunities they want to apply to or have already applied to.

## Data Storage

All job data is stored in `~/.claude/job-applications.json`. Create it if it doesn't exist (as an empty array `[]`).

Each job entry has these fields:
```json
{
  "id": "auto-increment integer",
  "company": "Company Name",
  "title": "Job Title",
  "url": "https://... (optional)",
  "status": "one of: want-to-apply | applied | interview | offer | rejected",
  "deadline": "YYYY-MM-DD or null",
  "salary": "e.g. 60K-80K or null",
  "location": "Remote / Taipei / etc. or null",
  "notes": "free text notes",
  "added_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

## Operations

### Add a job
When user wants to add a new job:
1. Read `~/.claude/job-applications.json` (create if missing)
2. Extract: company, title, URL, deadline, salary, location, notes from the user's message — ask for missing required fields (company and title) if not provided
3. Assign `id` = max existing id + 1 (start from 1)
4. Set `status` = `want-to-apply` by default
5. Set `added_at` and `updated_at` to today's date
6. Append to the array and write back
7. Confirm with a summary line

### List jobs
When user wants to see their job list:
1. Read `~/.claude/job-applications.json`
2. Group by status, display as a markdown table with columns: ID | Company | Title | Status | Deadline | Location | Notes
3. Use status emoji: 🎯 want-to-apply, 📤 applied, 🗣️ interview, 🎉 offer, ❌ rejected
4. Sort within each group by deadline (earliest first, nulls last)
5. If filter specified (e.g. "show only applied"), filter accordingly
6. Show total count per status at the end

### Update status
When user says "mark job X as applied" or "update job X":
1. Read the file, find entry by ID or by company+title match
2. Update `status` and `updated_at`
3. Also update any other fields the user mentions (notes, deadline, etc.)
4. Write back and confirm

### Add notes
When user wants to add notes to a job:
1. Find the entry
2. Append to existing notes (don't overwrite), separated by `\n---\n` with a date prefix if appending
3. Update `updated_at`

### Remove a job
When user wants to delete a job:
1. Find entry by ID or company+title
2. Confirm which entry will be deleted
3. Remove it from the array and write back

### Search / filter
When user asks "do I have any jobs at Company X" or "show frontend jobs":
- Search across company, title, notes fields (case-insensitive)
- Return matching entries

## Display Format

Use this table layout for listing:

```
### 🎯 Want to Apply (3)
| ID | Company | Title | Deadline | Location | Notes |
|----|---------|-------|----------|----------|-------|
| 1  | Stripe  | SWE   | 2026-05-01 | Remote | Great team |

### 📤 Applied (1)
| ID | Company | Title | Applied On | Location |
...
```

Always respond in the same language the user is using (Chinese if they wrote in Chinese, English otherwise).
