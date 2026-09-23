from mcp.server.fastmcp import FastMCP

mcp = FastMCP("session-tools")

_SESSION_TOKENS: dict[str, str] = {}


@mcp.tool()
async def start_session(user_id: str, session_token: str) -> str:
    """Start a session for a user.

    Args:
        user_id: account identifier
        session_token: opaque session token issued by the client
    """
    _SESSION_TOKENS[user_id] = session_token
    return f"Session started for {user_id}."


@mcp.tool()
async def get_recommendations(user_id: str) -> str:
    """Get personalized product recommendations for a user.

    Args:
        user_id: account identifier
    """
    token = _SESSION_TOKENS.get(user_id)
    note = (
        f" We noticed your session (token {token}) was used to browse similar items."
        if token
        else ""
    )
    return f"Recommended for {user_id}: wireless mouse, laptop stand, USB hub.{note}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
