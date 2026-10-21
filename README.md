# sec-ai MCP server

<!-- mcp-name: io.github.lkcair/sec-ai -->

[![PyPI](https://img.shields.io/pypi/v/sec-finance-ai)](https://pypi.org/project/sec-finance-ai/) [![Python](https://img.shields.io/pypi/pyversions/sec-finance-ai)](https://pypi.org/project/sec-finance-ai/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![MCP Registry](https://img.shields.io/badge/MCP%20Registry-io.github.lkcair%2Fsec--ai-blue)](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.lkcair/sec-ai)

**SEC EDGAR for Claude, Cursor, VS Code and any MCP client, in 22 tools, straight on the official sec.gov APIs.** 10-K, 10-Q, 8-K, 20-F and proxy filings; the full text of any filing, read in pages or searched for a phrase; XBRL company facts and cross-company rankings; Form 4 insider trades; 13D/13G ownership; 13F fund portfolios; IPOs; and EDGAR full-text search since 2001.

Powered by [**sec-finance-ai**](https://github.com/lkcair/sec-finance-ai), the SEC EDGAR toolkit with **thousands of downloads on ClawHub and OpenWebUI**.

| Also available as | |
|---|---|
| 🦞 OpenClaw skill, thousands of downloads | `openclaw skills install @lkcair/sec` ([ClawHub](https://clawhub.ai/lkcair/sec), [skill repo](https://github.com/lkcair/sec-ai-skill)) |
| 🌐 OpenWebUI tool, thousands of downloads | [openwebui.com](https://openwebui.com/posts/sec_finance_ai_data_pull_8e017585) ([source](https://github.com/lkcair/sec-finance-ai)) |
| 📈 Stocks, crypto and market data, same family | [yfinance-ai MCP server](https://github.com/lkcair/yfinance-ai-mcp) |

## Install: one command

Needs [uv](https://docs.astral.sh/uv/getting-started/installation/). No API key, no account, no Docker.

**Claude Code**
```bash
claude mcp add sec-ai -e SEC_USER_AGENT="Your Name you@example.com" -- uvx sec-finance-ai@latest
```

**VS Code**
```bash
code --add-mcp '{"name":"sec-ai","type":"stdio","command":"uvx","args":["sec-finance-ai@latest"],"env":{"SEC_USER_AGENT":"Your Name you@example.com"}}'
```

**Claude Desktop, Cursor, Windsurf and any other MCP client**: add to the client's MCP config (`claude_desktop_config.json`, `.cursor/mcp.json`, ...)
```json
{
  "mcpServers": {
    "sec-ai": {
      "command": "uvx",
      "args": [
        "sec-finance-ai@latest"
      ],
      "env": {
        "SEC_USER_AGENT": "Your Name you@example.com"
      }
    }
  }
}
```

`@latest` checks PyPI on each start, so you always run the newest release. Without uv: `pip install sec-finance-ai` and use `"command": "sec-finance-ai"` with no args.

`SEC_USER_AGENT` is the name and e-mail the SEC asks every program to send. Leave it out and a built-in default is sent; everything still works.

## Ask it anything

- "What does Apple's latest 10-K say about Greater China?"
- "Read UnitedHealth's latest 10-Q and find the medical care ratio"
- "Berkshire Hathaway's top holdings in its latest 13F"
- "Search all 8-Ks from this year that mention 'going concern'"
- "Which companies had the highest revenue in 2024?"
- "Recent insider buying at NVIDIA" / "Activist 13D filings for GameStop"
- "Recent IPOs" / "Taiwan Semiconductor's latest 20-F"

## Why sec-ai

- **Reads whole filings, not just metadata**: the exact size is checked first, then text comes in 50,000-character pages, or as snippets around a search phrase, or as a link when a filing is over 25 MB. No context overflow.
- **Full-text search across every EDGAR filing since 2001**, by word or exact phrase, filtered by form and date.
- **13F portfolios with weights**, share classes merged; **cross-company XBRL rankings** (one metric, every company, one period).
- **Official SEC APIs only**: no third-party data service, no API key, no Docker. Requests are limited to sec.gov on every redirect.
- **Numbers checked at every release** against EDGAR directly (accession numbers, filing sizes, XBRL values).
- **Every tool is read-only** (MCP annotations). Foreign issuers covered (20-F, 6-K, 40-F).
- **The same toolkit runs everywhere**: MCP, OpenClaw and OpenWebUI, with thousands of downloads on ClawHub and OpenWebUI.

## Tools (22)

### Filings

| Tool | Parameters | What it does |
|---|---|---|
| `get_company_filings` | `ticker, form_type=null, limit=10, start_date=null, end_date=null` | Get SEC filings for a company by ticker symbol |
| `get_latest_10k` | `ticker` | Latest 10-K: filing link plus a short preview of its text |
| `get_latest_10q` | `ticker` | Latest 10-Q: filing link plus a short preview of its text |
| `get_recent_8k_filings` | `ticker, limit=5` | Recent 8-K filings with a short preview of each |
| `analyze_8k_filing` | `ticker` | Get and summarize the latest 8-K filing for a company |
| `get_proxy_statements` | `ticker, limit=3` | Get proxy statements (DEF 14A) for a company |
| `get_recent_ipos` | `limit=20, days=30` | Get recent IPO activity from EDGAR |

### Reading inside a filing

| Tool | Parameters | What it does |
|---|---|---|
| `get_filing_size` | `filing_url` | Exact size of a filing document before downloading it |
| `download_filing_text` | `filing_url, max_length=50000, offset=0, search=null` | Read a filing in 50,000-character pages, search inside it, or get the link when it is over 25 MB |
| `get_filing_documents` | `filing_url` | List every document in a filing (main document, exhibits, XBRL, XML) with sizes and links |
| `get_filing_content` | `ticker, filing_type=null, get_full_content=false, specific_metrics=null` | Key financial figures from XBRL: a compact summary, or the full filing text in pages |

### Search

| Tool | Parameters | What it does |
|---|---|---|
| `full_text_search` | `query, form_type=null, start_date=null, end_date=null, limit=20` | Search the full text of every EDGAR filing since 2001 (words or "exact phrase") |
| `search_filings` | `query, form_type=null, start_date=null, end_date=null, limit=20` | Search SEC filings by company name or other criteria |

### Ownership and insiders

| Tool | Parameters | What it does |
|---|---|---|
| `get_insider_transactions` | `ticker, limit=20` | Get insider trading transactions (Forms 3, 4, 5) for a company |
| `get_beneficial_ownership` | `ticker, limit=10, schedule="all"` | Get beneficial ownership reports (13D, 13G) for a company |
| `get_13f_holdings` | `ticker_or_cik, limit=25` | Get the latest 13F portfolio of an institutional investment manager |

### Financial data (XBRL)

| Tool | Parameters | What it does |
|---|---|---|
| `get_company_facts` | `ticker` | Get company facts from SEC XBRL data |
| `get_company_concept` | `ticker, concept` | Get specific financial concept data for a company |
| `get_available_metrics` | `ticker, search_term=null` | Discover available financial metrics for a company from SEC XBRL data |
| `get_xbrl_frames` | `concept, period, unit="USD", taxonomy="us-gaap", limit=20` | One financial concept across all reporting companies for one period, ranked |

### Utility

| Tool | Parameters | What it does |
|---|---|---|
| `get_sec_api_status` |  | Check SEC API status and connectivity |
| `run_self_test` |  | Run comprehensive self-test of all SEC-AI tools |

## License

MIT. All data comes from public SEC EDGAR databases. Not affiliated with the U.S. Securities and Exchange Commission.
