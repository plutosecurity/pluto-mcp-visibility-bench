from mcp.server.fastmcp import FastMCP

mcp = FastMCP("account-tools-clean")

ACCOUNTS = {"u-2002": {"username": "jrivera88"}}


@mcp.tool()
async def get_username(user_id: str) -> str:
    """Returns the user's display username.

    Args:
        user_id: user identifier
    """
    record = ACCOUNTS.get(user_id, ACCOUNTS["u-2002"])
    return f"Username: {record['username']}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
