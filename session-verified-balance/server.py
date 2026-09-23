from mcp.server.fastmcp import FastMCP

mcp = FastMCP("banking-sessions-safe")

_sessions: dict[str, dict] = {}
_next_id = 1


@mcp.tool()
async def start_session(username: str) -> str:
    """Start a session for a user and return a session identifier.

    Args:
        username: the account owner's username
    """
    global _next_id
    session_id = str(_next_id)
    _next_id += 1
    balances = {"alice": 15230.50, "bob": 402.10}
    # The session is bound to the exact username that established it, and
    # that binding is what get_session_data actually verifies below.
    _sessions[session_id] = {"owner": username, "balance": balances.get(username, 0.0)}
    return session_id


@mcp.tool()
async def get_session_data(session_id: str, caller_username: str) -> str:
    """Get the account balance associated with a session.

    Args:
        session_id: the session identifier to look up
        caller_username: the username claimed by the current caller, verified against the session owner
    """
    session = _sessions.get(session_id)
    if session is None:
        return "No such session."
    if session["owner"] != caller_username:
        return "Access denied: session does not belong to this caller."
    return f"Balance for {session['owner']}: ${session['balance']:.2f}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
