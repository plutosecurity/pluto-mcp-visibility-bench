from mcp.server.fastmcp import FastMCP

mcp = FastMCP("session-tools")

SESSIONS = {
    "u-3003": {
        "last_login": "2026-09-20T08:15:00Z",
        "internal_host": "auth-node-07.internal.example",
        "internal_build": "auth-svc@3.4.1-rc2",
    }
}


@mcp.tool()
async def get_last_login_time(user_id: str) -> str:
    """Returns the timestamp of the user's most recent login.

    Args:
        user_id: user identifier
    """
    record = SESSIONS.get(user_id, SESSIONS["u-3003"])
    return (
        f"Last login: {record['last_login']}. "
        f"(handled by {record['internal_host']}, build {record['internal_build']})"
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
