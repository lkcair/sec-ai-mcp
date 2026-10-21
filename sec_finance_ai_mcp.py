"""
MCP server for sec-finance-ai (registry name sec-ai).

Imports sec_finance_ai.py as is and registers every public async method of its
Tools class as an MCP tool, with the schema built from its type hints and
docstring. sec_finance_ai.py is not modified; OpenWebUI and ClawHub keep using it.

Run: uvx sec-finance-ai
SEC_USER_AGENT="Name email" identifies you to the SEC; the built-in default is used otherwise.
"""

import inspect
import logging
import re
import sys
import typing

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

import sec_finance_ai

logger = logging.getLogger(__name__)

# OpenWebUI injects these at call time; an MCP client cannot send them.
HIDDEN_PARAMS = {"__event_emitter__", "__user__", "__metadata__"}

VERSION = re.search(r"^version:\s*(\S+)", sec_finance_ai.__doc__ or "", re.M)
VERSION = VERSION.group(1) if VERSION else ""


def _adapt(method):
    """Wrap a bound tool method so its MCP schema hides the OpenWebUI-only params."""
    sig = inspect.signature(method)
    hints = typing.get_type_hints(method)
    params = [
        p.replace(annotation=hints.get(p.name, p.annotation))
        for p in sig.parameters.values() if p.name not in HIDDEN_PARAMS
    ]

    async def call(**kwargs):
        logger.info("tool %s called with %s", method.__name__, sorted(kwargs))
        try:
            return await method(**kwargs)
        except Exception:
            logger.error("tool %s failed", method.__name__, exc_info=True)
            raise

    call.__name__ = method.__name__
    call.__doc__ = method.__doc__
    call.__signature__ = sig.replace(parameters=params, return_annotation=hints.get("return", sig.return_annotation))
    call.__annotations__ = {p.name: p.annotation for p in params}
    return call


def build_server():
    """Create the MCP server with every tool registered."""
    tools = sec_finance_ai.Tools()
    names = sorted(
        n for n, _ in inspect.getmembers(tools, inspect.iscoroutinefunction) if not n.startswith("_")
    )
    server = MCPServer(
        name="sec-finance-ai",
        version=VERSION,
        instructions=(
            "SEC EDGAR data from the official sec.gov APIs: filings (10-K, 10-Q, 8-K, proxy), "
            "full text of any filing read in pages or searched, XBRL facts and frames, insider "
            "trades, 13D/G and 13F holdings, IPOs and EDGAR full-text search."
        ),
        website_url="https://github.com/lkcair/sec-finance-ai",
    )
    for name in names:
        fn = _adapt(getattr(tools, name))
        server.add_tool(
            fn,
            name=name,
            description=inspect.cleandoc(fn.__doc__ or name),
            annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                        idempotentHint=True, openWorldHint=True),
        )
    logger.info("sec-finance-ai MCP %s: %d tools registered", VERSION, len(names))
    return server


def main():
    """Entry point for the `sec-finance-ai` console script (stdio transport)."""
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    build_server().run("stdio")


if __name__ == "__main__":
    main()
