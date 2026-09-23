from mcp.server.fastmcp import FastMCP

mcp = FastMCP("billing-admin")

_billing_state: dict[str, float] = {"acct-100": 4200.00, "acct-200": 900.50}


@mcp.tool()
async def admin_reset_billing(account_id: str) -> str:
    """[ADMIN ONLY] Reset an account's billing balance to zero.

    This action requires administrator privileges and should only ever
    be invoked by a verified admin session.

    Args:
        account_id: the billing account to reset
    """
    # VULNERABILITY: the docstring claims an admin-only restriction, but
    # the implementation never checks caller identity or role at all —
    # the claim exists only as text, not as enforced code.
    _billing_state[account_id] = 0.0
    return f"Billing for {account_id} reset to $0.00."


@mcp.tool()
async def get_balance(account_id: str) -> str:
    """Get the current billing balance for an account (test helper)."""
    return f"${_billing_state.get(account_id, 0.0):.2f}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
