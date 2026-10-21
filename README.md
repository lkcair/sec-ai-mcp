# sec-ai MCP server

<!-- mcp-name: io.github.lkcair/sec-ai -->

SEC EDGAR for any MCP client in **22 tools**, straight on the official sec.gov APIs: 10-K, 10-Q, 8-K, 20-F and proxy filings, the full text of any filing read in pages or searched for a phrase, XBRL company facts and cross-company frames, insider trades, 13D/13G ownership, 13F holdings, IPOs and EDGAR full-text search since 2001. No API key.

Powered by [sec-finance-ai](https://github.com/lkcair/sec-finance-ai), our SEC EDGAR toolkit with thousands of downloads on ClawHub and OpenWebUI.

## Install

**Claude Code**
```bash
claude mcp add sec-ai -e SEC_USER_AGENT="Your Name you@example.com" -- uvx sec-finance-ai
```

**Claude Desktop, Cursor, VS Code and other clients**
```json
{
  "mcpServers": {
    "sec-ai": {
      "command": "uvx",
      "args": ["sec-finance-ai"],
      "env": { "SEC_USER_AGENT": "Your Name you@example.com" }
    }
  }
}
```

Without [uv](https://docs.astral.sh/uv/): `pip install sec-finance-ai` and use `"command": "sec-finance-ai"`.

`SEC_USER_AGENT` is the name and e-mail the SEC asks every program to send. If you leave it out, a built-in default is sent and everything still works.

## Try

- "What does Apple's latest 10-K say about Greater China?"
- "Berkshire Hathaway's top holdings in its latest 13F"
- "Search all 8-Ks from this year that mention \"going concern\""
- "Which companies had the highest revenue in 2024?"

Every tool is read-only. Full tool list: [sec-finance-ai README](https://github.com/lkcair/sec-finance-ai#%EF%B8%8F-available-tools-22).

MIT. Not affiliated with the U.S. Securities and Exchange Commission.
