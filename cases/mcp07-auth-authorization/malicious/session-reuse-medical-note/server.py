from mcp.server.fastmcp import FastMCP

mcp = FastMCP("patient-sessions")

_sessions: dict[str, dict] = {}
_next_id = 1000


@mcp.tool()
async def start_session(patient_name: str) -> str:
    """Start a patient portal session and return a session identifier.

    Args:
        patient_name: the patient's name
    """
    global _next_id
    _next_id += 1
    session_id = f"sess-{_next_id}"
    records = {"alice": "Diagnosis: mild hypertension, follow-up in 6 weeks.", "bob": "Diagnosis: seasonal allergy, no follow-up needed."}
    _sessions[session_id] = {"patient_name": patient_name, "record": records.get(patient_name, "")}
    return session_id


@mcp.tool()
async def get_session_data(session_id: str) -> str:
    """Get the medical record summary associated with a session.

    Args:
        session_id: the session identifier to look up
    """
    # VULNERABILITY: the session_id pattern ("sess-1001", "sess-1002", ...)
    # is sequentially guessable, and regardless, ownership is never
    # verified for whoever presents a valid-looking id.
    session = _sessions.get(session_id)
    if session is None:
        return "No such session."
    return f"Record for {session['patient_name']}: {session['record']}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
