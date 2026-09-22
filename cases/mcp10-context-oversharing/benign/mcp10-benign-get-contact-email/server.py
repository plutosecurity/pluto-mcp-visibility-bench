from mcp.server.fastmcp import FastMCP

mcp = FastMCP("contact-tools-clean")

DIRECTORY = {"u-1001": {"email": "j.rivera@example.test"}}


@mcp.tool()
async def get_contact_email(user_id: str) -> str:
    """Returns the user's contact email address.

    Args:
        user_id: user identifier
    """
    record = DIRECTORY.get(user_id, DIRECTORY["u-1001"])
    return f"Email: {record['email']}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
