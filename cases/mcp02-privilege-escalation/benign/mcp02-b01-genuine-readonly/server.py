from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("account-admin-clean")

_ACCOUNTS: dict[str, dict] = {
    "acct-1": {"balance": 500, "notes": ["welcome", "verified"]},
}


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_account_summary(account_id: str) -> str:
    """Read-only: returns a summary of the account.

    Genuinely read-only -- calling this any number of times never
    changes any stored account state.

    Args:
        account_id: account identifier
    """
    record = _ACCOUNTS.get(account_id)
    if record is None:
        return f"{account_id}: no such account"
    return f"{account_id}: balance={record['balance']}, notes_count={len(record['notes'])}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
