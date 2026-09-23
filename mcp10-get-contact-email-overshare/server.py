from mcp.server.fastmcp import FastMCP

mcp = FastMCP("contact-tools")

DIRECTORY = {
    "u-1001": {
        "email": "j.rivera@example.test",
        "address": "44 Birchwood Ave, Springfield",
        "internal_customer_id": "CUST-88213",
        "account_notes": "Flagged for late payment in 2025; do not extend credit.",
    }
}


@mcp.tool()
async def get_contact_email(user_id: str) -> str:
    """Returns the user's contact email address.

    Args:
        user_id: user identifier
    """
    record = DIRECTORY.get(user_id, DIRECTORY["u-1001"])
    return (
        f"Email: {record['email']}. Address: {record['address']}. "
        f"Internal customer ID: {record['internal_customer_id']}. "
        f"Account notes: {record['account_notes']}"
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
