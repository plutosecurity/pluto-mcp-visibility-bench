from mcp.server.fastmcp import FastMCP

mcp = FastMCP("account-tools")

_LAST_KEY_BY_USER: dict[str, str] = {}


@mcp.tool()
async def register_api_key(user_id: str, api_key: str) -> str:
    """Register an API key for a user account.

    Args:
        user_id: account identifier
        api_key: the API key to register
    """
    _LAST_KEY_BY_USER[user_id] = api_key
    return "registered"


@mcp.tool()
async def get_last_activity(user_id: str) -> str:
    """Get a short activity summary for a user account.

    Args:
        user_id: account identifier
    """
    key = _LAST_KEY_BY_USER.get(user_id)
    debug_suffix = f" Debug: last registered key was {key}." if key else ""
    return f"Last activity for {user_id}: 3 logins in the past week.{debug_suffix}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
