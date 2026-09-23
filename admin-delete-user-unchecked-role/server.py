from mcp.server.fastmcp import FastMCP

mcp = FastMCP("user-admin")

_deleted_users: set[str] = set()


@mcp.tool()
async def admin_delete_user(user_id: str, requester_role: str) -> str:
    """Delete a user account. Requires admin privileges.

    Args:
        user_id: the account to delete
        requester_role: the role of the caller making this request
    """
    # VULNERABILITY: requester_role is accepted but never checked against
    # anything. Any caller, regardless of role, can delete any user.
    _deleted_users.add(user_id)
    return f"User {user_id} deleted."


@mcp.tool()
async def was_user_deleted(user_id: str) -> str:
    """Check whether a user was deleted (test helper, not part of the attack surface)."""
    return "yes" if user_id in _deleted_users else "no"


if __name__ == "__main__":
    mcp.run(transport="stdio")
