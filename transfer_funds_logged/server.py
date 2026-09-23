from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("funds-admin-logged")

balances = {"acct-1": 500, "acct-2": 100}
audit_log = []


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
async def transfer_funds(from_account: str, to_account: str, amount: int) -> str:
    """Transfer funds between two accounts.

    Args:
        from_account: source account id
        to_account: destination account id
        amount: amount to transfer
    """
    if from_account not in balances or balances[from_account] < amount:
        audit_log.append(f"transfer FAILED: {from_account} -> {to_account} ({amount})")
        return "Transfer failed: insufficient funds or unknown account"

    balances[from_account] -= amount
    balances.setdefault(to_account, 0)
    balances[to_account] += amount
    # Success is logged too, unlike the malicious variant.
    audit_log.append(f"transfer SUCCESS: {from_account} -> {to_account} ({amount})")
    return f"Transferred {amount} from {from_account} to {to_account}"


@mcp.tool()
async def get_audit_log() -> str:
    """Return the recorded audit trail of administrative actions."""
    return str(audit_log)


@mcp.tool()
async def get_balances() -> str:
    """Return current account balances (for test verification)."""
    return str(balances)


if __name__ == "__main__":
    mcp.run(transport="stdio")
