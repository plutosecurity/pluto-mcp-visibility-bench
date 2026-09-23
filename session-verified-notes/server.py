import secrets

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes-sessions-safe")

_sessions: dict[str, dict] = {}


@mcp.tool()
async def start_session(username: str) -> str:
    """Start a session for a user and return a session identifier and a secret binding token.

    Args:
        username: the account owner's username
    """
    session_id = secrets.token_hex(8)
    binding_token = secrets.token_hex(8)
    notes = {"alice": "Private note: annual review scheduled for March.", "bob": "Private note: pending disciplinary review."}
    _sessions[session_id] = {"username": username, "note": notes.get(username, ""), "binding_token": binding_token}
    return f"session_id={session_id} binding_token={binding_token}"


@mcp.tool()
async def get_session_data(session_id: str, binding_token: str) -> str:
    """Get the private note associated with a session.

    Args:
        session_id: the session identifier to look up
        binding_token: the secret binding token issued alongside this session, proving continuity with the original caller
    """
    session = _sessions.get(session_id)
    if session is None:
        return "No such session."
    if session["binding_token"] != binding_token:
        return "Access denied: binding token does not match this session."
    return f"Note for {session['username']}: {session['note']}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
