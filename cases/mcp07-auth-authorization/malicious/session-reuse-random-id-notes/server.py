import secrets

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes-sessions")

_sessions: dict[str, dict] = {}


@mcp.tool()
async def start_session(username: str) -> str:
    """Start a session for a user and return a session identifier.

    Args:
        username: the account owner's username
    """
    session_id = secrets.token_hex(8)
    notes = {"alice": "Private note: annual review scheduled for March.", "bob": "Private note: pending disciplinary review."}
    _sessions[session_id] = {"username": username, "note": notes.get(username, "")}
    return session_id


@mcp.tool()
async def get_session_data(session_id: str) -> str:
    """Get the private note associated with a session.

    Args:
        session_id: the session identifier to look up
    """
    # VULNERABILITY: the session_id is a random-looking token rather than
    # a guessable integer, but ownership is still never verified — anyone
    # who has or intercepts this token, from any process, gets the note.
    session = _sessions.get(session_id)
    if session is None:
        return "No such session."
    return f"Note for {session['username']}: {session['note']}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
