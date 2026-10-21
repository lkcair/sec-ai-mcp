# sec-finance-ai MCP server

<!-- mcp-name: io.github.lkcair/sec-ai -->

[![PyPI](https://img.shields.io/pypi/v/sec-finance-ai)](https://pypi.org/project/sec-finance-ai/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI-powered SEC EDGAR integration: 23 tools on the official sec.gov APIs, in one Python file.

🚀 **Thousands of downloads on ClawHub and OpenWebUI**

10-K, 10-Q, 8-K, 20-F and proxy filings, the full text of any filing read in pages or searched, XBRL company facts and cross-company rankings, Form 4 insider trades, 13D/13G ownership, 13F fund portfolios, IPOs, and full-text search of every filing since 2001.

| Use it in | Install | Repo |
|---|---|---|
| Claude, Cursor, VS Code, [LangChain](https://docs.langchain.com/oss/python/langchain/mcp), [Google ADK](https://google.github.io/adk-docs/tools-custom/mcp-tools/), [Strands Agents](https://strandsagents.com/docs/user-guide/sdk/tools/mcp-tools/) and other MCP clients | `uvx sec-finance-ai@latest` | [sec-ai-mcp](https://github.com/lkcair/sec-ai-mcp) |
| ClawHub skill for OpenClaw 🚀 Thousands of downloads | `openclaw skills install @lkcair/sec` | [sec-ai-skill](https://github.com/lkcair/sec-ai-skill) |
| OpenWebUI tool 🚀 Thousands of downloads | [Get it on openwebui.com](https://openwebui.com/posts/sec_finance_ai_data_pull_8e017585) | [sec-finance-ai](https://github.com/lkcair/sec-finance-ai) |
| Python | `from sec_finance_ai import Tools` | [sec-finance-ai](https://github.com/lkcair/sec-finance-ai) |


## Install

Needs [uv](https://docs.astral.sh/uv/getting-started/installation/). No API key.

Claude Code:
```bash
claude mcp add sec-ai -e SEC_USER_AGENT="Your Name you@example.com" -- uvx sec-finance-ai@latest
```

VS Code:
```bash
code --add-mcp '{"name":"sec-ai","type":"stdio","command":"uvx","args":["sec-finance-ai@latest"],"env":{"SEC_USER_AGENT":"Your Name you@example.com"}}'
```

Claude Desktop, Cursor, Windsurf and other clients, in the client's MCP config file:
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

`@latest` picks up new releases when the client starts. Without uv: `pip install sec-finance-ai`, then use `"command": "sec-finance-ai"` with no args.

`SEC_USER_AGENT` is the name and e-mail the SEC asks programs to send. If it is not set, a default is sent.

Listed in the [MCP Registry](https://registry.modelcontextprotocol.io) as `io.github.lkcair/sec-ai`. Every tool is read-only.

## Agent frameworks

The server runs over stdio with `uvx sec-finance-ai@latest`, so any framework with MCP support can load all its tools.

`SEC_USER_AGENT` is optional. MCP starts the server with a minimal environment, so pass it as shown; `**os.environ` keeps `PATH`, so `uvx` is found.

[LangChain](https://docs.langchain.com/oss/python/langchain/mcp): `pip install "langchain[mcp]" langchain-anthropic`
```python
import asyncio
import os
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

async def main():
    config = {"mcpServers": {"sec-ai": {
        "command": "uvx", "args": ["sec-finance-ai@latest"],
        "env": {**os.environ, "SEC_USER_AGENT": "Your Name you@example.com"},  # optional
    }}}
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        result = await agent.ainvoke({"messages": [{"role": "user", "content": "What does Apple's latest 10-K say about Greater China?"}]})
        print(result["messages"][-1].content)

asyncio.run(main())
```

[Google ADK](https://google.github.io/adk-docs/tools-custom/mcp-tools/): `pip install "google-adk[mcp]"`
```python
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="sec_ai",
    instruction="Answer with the sec-ai tools.",
    tools=[McpToolset(connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx", args=["sec-finance-ai@latest"],
            env={**os.environ, "SEC_USER_AGENT": "Your Name you@example.com"},  # optional
        ),
        timeout=60,
    ))],
)
```

[Strands Agents](https://strandsagents.com/docs/user-guide/sdk/tools/mcp-tools/): `pip install strands-agents`
```python
import os
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

sec_ai = MCPClient(lambda: stdio_client(StdioServerParameters(
    command="uvx", args=["sec-finance-ai@latest"],
    env={**os.environ, "SEC_USER_AGENT": "Your Name you@example.com"},  # optional
)))
agent = Agent(tools=[sec_ai])
agent("What does Apple's latest 10-K say about Greater China?")
```

## Example questions

- What does Apple's latest 10-K say about Greater China?
- What are Berkshire Hathaway's top holdings in its latest 13F?
- Find every 8-K this year that mentions 'going concern'.
- Which companies had the highest revenue in 2024?

## MCP tools (22)

### Filings

| Tool | Parameters | Description |
|---|---|---|
| `get_company_filings` | `ticker, form_type=null, limit=10, start_date=null, end_date=null` | Get SEC filings for a company by ticker symbol |
| `get_latest_10k` | `ticker` | Latest 10-K with a short preview of its text |
| `get_latest_10q` | `ticker` | Latest 10-Q with a short preview of its text |
| `get_recent_8k_filings` | `ticker, limit=5` | Recent 8-K filings with a short preview of each |
| `analyze_8k_filing` | `ticker` | Get and summarize the latest 8-K filing for a company |
| `get_proxy_statements` | `ticker, limit=3` | Get proxy statements (DEF 14A) for a company |
| `get_recent_ipos` | `limit=20, days=30` | Get recent IPO activity from EDGAR |

### Reading inside a filing

| Tool | Parameters | Description |
|---|---|---|
| `get_filing_size` | `filing_url` | Exact size of a filing document before downloading it |
| `download_filing_text` | `filing_url, max_length=50000, offset=0, search=null` | Read a filing in 50,000-character pages, search inside it, or get the link when it is over 25 MB |
| `get_filing_documents` | `filing_url` | List every document in a filing (main document, exhibits, XBRL, XML) with sizes and links |
| `get_filing_content` | `ticker, filing_type=null, get_full_content=false, specific_metrics=null` | Key financial figures from XBRL, or the full filing text in pages |

### Search

| Tool | Parameters | Description |
|---|---|---|
| `full_text_search` | `query, form_type=null, start_date=null, end_date=null, limit=20` | Search the full text of every EDGAR filing since 2001 (words or "exact phrase") |
| `search_filings` | `query, form_type=null, start_date=null, end_date=null, limit=20` | Search SEC filings by company name or other criteria |

### Ownership and insiders

| Tool | Parameters | Description |
|---|---|---|
| `get_insider_transactions` | `ticker, limit=20` | Get insider trading transactions (Forms 3, 4, 5) for a company |
| `get_beneficial_ownership` | `ticker, limit=10, schedule="all"` | Get beneficial ownership reports (13D, 13G) for a company |
| `get_13f_holdings` | `ticker_or_cik, limit=25` | Get the latest 13F portfolio of an institutional investment manager |

### Financial data (XBRL)

| Tool | Parameters | Description |
|---|---|---|
| `get_company_facts` | `ticker` | Get company facts from SEC XBRL data |
| `get_company_concept` | `ticker, concept` | Get specific financial concept data for a company |
| `get_available_metrics` | `ticker, search_term=null` | Discover available financial metrics for a company from SEC XBRL data |
| `get_xbrl_frames` | `concept, period, unit="USD", taxonomy="us-gaap", limit=20` | One financial concept across all reporting companies for one period, ranked |

### Utility

| Tool | Parameters | Description |
|---|---|---|
| `get_sec_api_status` |  | Check SEC API status and connectivity |
| `run_self_test` |  | Run comprehensive self-test of all SEC-AI tools |

## License

MIT. All data comes from public SEC EDGAR databases. Not affiliated with the U.S. Securities and Exchange Commission.
