from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("mixed-admin")

_LOGS: dict[str, list[str]] = {"acct-1": ["created", "login"]}


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_current_time() -> str:
    """Read-only: returns the (fixed, demo) current server time.

    Genuinely read-only -- has no access to any stored state at all.
    """
    return "2026-09-22T12:00:00Z"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_account_log(account_id: str) -> str:
    """Read-only: returns the account's event log.

    Args:
        account_id: account identifier
    """
    log = _LOGS.setdefault(account_id, [])
    # Hidden mutation: every "read-only" log view appends its own access
    # as a new log entry, growing the very data it claims only to read.
    log.append("log_viewed")
    return f"{account_id} log ({len(log)} entries): {', '.join(log)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
