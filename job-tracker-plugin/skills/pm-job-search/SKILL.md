---
name: pm-job-search
description: This skill should be used when the user wants to "search for PM jobs", "find product manager positions", "look for job openings", "search job boards", "crawl job sites", "show me PM vacancies", "find product manager jobs in Taiwan", or anything related to automatically searching public job boards for Product Manager / 產品經理 openings. Also activates for: "搜尋PM職缺", "找產品經理工作", "爬職缺", "求職搜尋", "最新PM職缺".
version: 1.0.0
---

# PM Job Search

Automatically search public job boards for Product Manager openings and optionally save them to the job tracker.

## Platforms to Search

Search ALL of these in parallel using WebSearch:

| Platform | Search Query |
|----------|-------------|
| CakeResume | `site:cakeresume.com "product manager" OR "產品經理"` |
| LinkedIn | `site:linkedin.com/jobs "product manager" Taiwan` |
| 104人力銀行 | `site:104.com.tw "產品經理" OR "product manager"` |
| Yourator | `site:yourator.co "product manager" OR "產品經理"` |
| 1111人力銀行 | `site:1111.com.tw "產品經理"` |

Also do a general search: `"product manager" OR "產品經理" 職缺 台灣 2026`

## Steps

1. **Run searches in parallel** — Use WebSearch for each platform above. Use today's date context to prioritize recent postings.

2. **Fetch job details** — For each search result URL that looks like an actual job posting (not a search results page), use WebFetch to get:
   - Company name
   - Job title
   - Location (Remote / 台北 / 新竹 etc.)
   - Salary range (if shown)
   - Application deadline (if shown)
   - Brief description (2-3 lines max)
   - Direct URL

   Limit to the top 3-5 most promising results per platform to avoid excessive fetches.

3. **Deduplicate** — Remove duplicate jobs (same company + same title). Keep the one with more complete info.

4. **Cross-check with existing tracker** — Read `~/.claude/job-applications.json`. Mark any found jobs that are already tracked (show ✅ Already tracked). Do not add duplicates automatically.

5. **Present results** — Show results in this format:

```
## 🔍 PM Job Search Results — {today's date}

Found {N} new openings across {M} platforms.

### CakeResume ({n} found)
| # | Company | Title | Location | Salary | URL |
|---|---------|-------|----------|--------|-----|
| 1 | Stripe | Senior PM | Remote | NT$2M+ | https://... |

### LinkedIn ({n} found)
...

### Already in your tracker (skipped)
- Company X — Title Y
```

6. **Ask to save** — After showing results, ask:
   > 要把哪幾筆加入職缺清單？請輸入編號（例如：1, 3, 5）或輸入 `all` 全部加入，或 `skip` 略過。

7. **Save selected jobs** — For each selected job, add it to `~/.claude/job-applications.json` using the job-tracker format with `status: "want-to-apply"`. Confirm what was saved.

## Handling Failures

- If a platform search returns no results or errors, note it and continue with others.
- If WebFetch for a job URL fails (paywall / bot block), use what's available from the search snippet.
- If 104.com.tw or 1111.com.tw block direct fetch, fall back to search snippet data only.
- Always complete the search even if some platforms fail — partial results are better than none.

## Filtering Options

If the user specifies filters, apply them:
- **Keyword**: e.g. "找 fintech PM" → filter titles/descriptions containing fintech
- **Location**: e.g. "只要遠端" → filter for Remote only
- **Seniority**: e.g. "senior PM" → filter for senior/lead/principal roles
- **Language**: respond in the same language the user used (Chinese default)

## Notes

- Be concise in descriptions — the goal is a quick scan, not a full job description
- Prefer direct job listing URLs over search result pages
- If salary is not shown, omit the column rather than showing "N/A" everywhere
- Jobs posted more than 60 days ago should be deprioritized or flagged as potentially expired
