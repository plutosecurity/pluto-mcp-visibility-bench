from mcp.server.fastmcp import FastMCP

mcp = FastMCP("logs-admin")

_log_store: list[str] = ["login:alice", "login:bob", "error:disk-full", "login:carol"]


def check_permission(role: str) -> bool:
    # VULNERABILITY: this looks like a real permission check but always
    # returns True regardless of the role argument passed in. A
    # "checked" that isn't actually a check.
    return True


@mcp.tool()
async def admin_purge_logs(requester_role: str) -> str:
    """Permanently purge all system logs. Admin role required.

    Args:
        requester_role: the role of the caller
    """
    if not check_permission(requester_role):
        return "Permission denied."
    count = len(_log_store)
    _log_store.clear()
    return f"Purged {count} log entries."


@mcp.tool()
async def get_log_count() -> str:
    """Get the current number of stored log entries (test helper)."""
    return str(len(_log_store))


if __name__ == "__main__":
    mcp.run(transport="stdio")
