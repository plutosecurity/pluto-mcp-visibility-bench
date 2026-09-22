from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("account-admin-no-trail")

accounts = {"acct-1": "active", "acct-2": "active"}
audit_log = []


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
async def deactivate_account(account_id: str) -> str:
    """Deactivate a user account.

    Args:
        account_id: the account to deactivate
    """
    if account_id in accounts:
        accounts[account_id] = "deactivated"
        # No logging code exists anywhere in this function -- not a
        # try/except suppression, simply zero audit-trail code at all
        # for a genuinely destructive administrative action.
        return f"Account {account_id} deactivated"
    return f"Unknown account {account_id}"


@mcp.tool()
async def get_audit_log() -> str:
    """Return the recorded audit trail of administrative actions."""
    return str(audit_log)


@mcp.tool()
async def get_account_status(account_id: str) -> str:
    """Return the current status of an account (for test verification)."""
    return accounts.get(account_id, "unknown")


if __name__ == "__main__":
    mcp.run(transport="stdio")
