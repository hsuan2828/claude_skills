# Claude Code Skills — PM Job Search Automation

> 用 Claude Code 打造的 AI 輔助 PM 求職系統：自動搜尋職缺、追蹤應徵進度，每天早上 9 點自動更新報告。

## 系統架構

```
┌──────────────────────────────────────────────────────────┐
│              Claude Code Remote (CCR Cloud)              │
│                  每天 09:00 Asia/Taipei                  │
│                                                          │
│  WebSearch × 4 queries                                   │
│    → CakeResume / LinkedIn / 104 / Yourator              │
│  Extract snippets → Deduplicate → Write markdown table   │
│  git commit → push pm-jobs-report.md                     │
└──────────────────────┬───────────────────────────────────┘
                       │ 自動 commit
                       ▼
          pm-jobs-report.md (本 repo)
                       │ 使用者閱讀後
                       ▼
┌──────────────────────────────────────────────────────────┐
│                  本機 Claude Code CLI                     │
│                                                          │
│  /pm-jobs          → 即時搜尋（可加關鍵字過濾）           │
│  /jobs add         → 新增職缺到追蹤清單                   │
│  /jobs list        → 顯示所有職缺（依狀態分組）           │
│  /jobs update <id> → 更新進度                            │
└──────────────────────────────────────────────────────────┘
```

## 功能說明

### 自動搜尋（CCR 排程）

每天定時搜尋以下平台的 Product Manager 職缺，結果自動 commit 到本 repo：

| 平台 | 說明 |
|------|------|
| CakeResume | 台灣新創 PM 職缺為主 |
| LinkedIn | 外商與跨國企業 |
| 104人力銀行 | 台灣本土企業 |
| Yourator | 新創 / 科技公司 |

→ 最新報告：[pm-jobs-report.md](./pm-jobs-report.md)

### 本機職缺追蹤（job-tracker skill）

以自然語言管理應徵記錄，資料存在 `~/.claude/job-applications.json`：

```
新增職缺：Stripe，Product Manager，deadline 5/1
/jobs list
/jobs update 3 applied
mark job 2 as interview
```

應徵狀態追蹤：

```
🎯 想投遞 → 📤 已投遞 → 🗣️ 面試中 → 🎉 Offer / ❌ 拒絕
```

### 即時搜尋（pm-job-search skill）

```
/pm-jobs              # 搜尋所有平台
/pm-jobs fintech      # 只看 fintech 相關
/pm-jobs remote       # 只看遠端職缺
搜尋最新 senior PM 職缺
```

搜尋結果會與現有追蹤清單比對，避免重複，並提示你選擇要存哪幾筆。

## 技術設計

詳見 [auto_pm_agent.py](./auto_pm_agent.py)，包含：
- 資料 schema 定義
- 平台搜尋邏輯
- 排程架構說明
- 模擬執行輸出

## 安裝

```bash
# 複製 plugin 到 Claude Code
cp -r job-tracker-plugin \
  ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/job-tracker

# 重啟 Claude Code，Skill 自動載入
```

## 檔案結構

```
claude_skills/
├── README.md                              # 本文件
├── auto_pm_agent.py                       # 系統設計邏輯 + 資料 schema
├── pm-jobs-report.md                      # 每日自動更新的職缺報告
└── job-tracker-plugin/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── commands/
    │   ├── jobs.md                        # /jobs 指令
    │   └── pm-jobs.md                     # /pm-jobs 指令
    └── skills/
        ├── job-tracker/
        │   └── SKILL.md                   # 職缺追蹤邏輯
        └── pm-job-search/
            └── SKILL.md                   # 求職搜尋邏輯
```

## 排程資訊

| 項目 | 值 |
|------|-----|
| Trigger ID | `trig_01XCLpjkDMwQdFLqapnoiH5A` |
| 排程 | `0 1 * * *` UTC = 09:00 台北時間 |
| 模型 | claude-sonnet-4-6 |
| 管理頁面 | https://claude.ai/code/scheduled |

---

*Built with [Claude Code](https://claude.ai/code)*
