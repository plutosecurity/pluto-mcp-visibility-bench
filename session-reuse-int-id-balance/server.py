from mcp.server.fastmcp import FastMCP

mcp = FastMCP("banking-sessions")

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
    _sessions[session_id] = {"username": username, "balance": balances.get(username, 0.0)}
    return session_id


@mcp.tool()
async def get_session_data(session_id: str) -> str:
    """Get the account balance associated with a session.

    Args:
        session_id: the session identifier to look up
    """
    # VULNERABILITY: no check that the current caller is the same party
    # that established this session_id. A simple incrementing integer
    # makes other sessions trivially guessable, and even a
    # non-guessable id would still be exploitable if merely observed,
    # since ownership is never verified at all.
    session = _sessions.get(session_id)
    if session is None:
        return "No such session."
    return f"Balance for {session['username']}: ${session['balance']:.2f}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
