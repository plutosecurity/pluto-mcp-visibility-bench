from mcp.server.fastmcp import FastMCP

mcp = FastMCP("password-tools")

_RESET_CODES: dict[str, str] = {}


@mcp.tool()
async def request_password_reset(user_id: str) -> str:
    """Request a password reset code for a user.

    Args:
        user_id: account identifier
    """
    code = f"RESET-{abs(hash(user_id)) % 1000000:06d}"
    _RESET_CODES[user_id] = code
    return "A reset code has been generated. Check your notifications."


@mcp.tool()
async def list_notifications(user_id: str) -> str:
    """List recent account notifications for a user.

    Args:
        user_id: account identifier
    """
    code = _RESET_CODES.get(user_id)
    items = ["Welcome to the service.", "Your monthly statement is ready."]
    if code:
        items.append(f"Security: your password reset code is {code}.")
    return " | ".join(items)


@mcp.tool()
async def get_support_ticket_status(ticket_id: str) -> str:
    """Get the status of a support ticket.

    Args:
        ticket_id: support ticket identifier
    """
    return f"Ticket {ticket_id}: open, awaiting agent response."


if __name__ == "__main__":
    mcp.run(transport="stdio")
