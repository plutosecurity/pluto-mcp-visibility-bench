from mcp.server.fastmcp import FastMCP

mcp = FastMCP("access-admin")

_admins: set[str] = {"alice"}


@mcp.tool()
async def admin_grant_admin_access(target_account: str, requester_role: str) -> str:
    """Grant admin access to another account. Admin role required to invoke.

    Args:
        target_account: the account to promote to admin
        requester_role: the role of the caller
    """
    # VULNERABILITY: a real-looking check exists, but a logic bug means
    # denial never actually stops execution — the "if" branch below logs
    # a warning but does not return, so control falls through to the
    # grant regardless of the check's outcome.
    if requester_role != "admin":
        _log_warning = f"non-admin role '{requester_role}' attempted grant"
    _admins.add(target_account)
    return f"{target_account} granted admin access."


@mcp.tool()
async def is_admin(account: str) -> str:
    """Check whether an account currently has admin access (test helper)."""
    return "yes" if account in _admins else "no"


if __name__ == "__main__":
    mcp.run(transport="stdio")
