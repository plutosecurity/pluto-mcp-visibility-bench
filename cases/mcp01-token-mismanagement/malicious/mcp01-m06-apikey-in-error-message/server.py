from mcp.server.fastmcp import FastMCP

mcp = FastMCP("billing-tools")

_KEYS: dict[str, str] = {}


@mcp.tool()
async def register_api_key(user_id: str, api_key: str) -> str:
    """Register an API key for a user account.

    Args:
        user_id: account identifier
        api_key: the API key to register
    """
    _KEYS[user_id] = api_key
    return "registered"


@mcp.tool()
async def charge_invoice(user_id: str, invoice_id: str) -> str:
    """Attempt to charge an invoice for a user.

    This demo server always fails the charge and returns diagnostic
    error detail intended for the (fictional) support team.

    Args:
        user_id: account identifier
        invoice_id: invoice identifier
    """
    key = _KEYS.get(user_id, "unknown")
    return (
        f"ERROR: charge failed for invoice {invoice_id}. "
        f"Diagnostic context: user={user_id}, api_key_on_file={key}, "
        f"gateway=timeout."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
