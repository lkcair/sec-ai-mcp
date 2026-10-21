# sec-ai MCP server

<!-- mcp-name: io.github.lkcair/sec-ai -->

SEC EDGAR for any MCP client in **22 tools**, straight on the official sec.gov APIs: 10-K, 10-Q, 8-K, 20-F and proxy filings, the full text of any filing read in pages or searched for a phrase, XBRL company facts and cross-company frames, insider trades, 13D/13G ownership, 13F holdings, IPOs and EDGAR full-text search since 2001. No API key.

The tools are [sec-finance-ai](https://github.com/lkcair/sec-finance-ai), the same file used by thousands on ClawHub and OpenWebUI. This package serves them over MCP.

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

## How it is built

`sec_finance_ai.py` is an exact copy of the file in [lkcair/sec-finance-ai](https://github.com/lkcair/sec-finance-ai/blob/main/sec_finance_ai.py), the same file OpenWebUI and ClawHub use. `sec_finance_ai_mcp.py` imports it and registers every tool over MCP. The package version is read from the `.py` header.

## Release

After a new version is on `main` in [lkcair/sec-finance-ai](https://github.com/lkcair/sec-finance-ai):

```bash
./sync.sh                               # copy sec_finance_ai.py from its repo
git commit -am "sec-finance-ai X.Y.Z" && git push
git tag vX.Y.Z && git push --tags       # publish.yml: PyPI + MCP Registry
```

The workflow refuses to publish if the copy differs from its repo or the tag differs from the `.py` version.
