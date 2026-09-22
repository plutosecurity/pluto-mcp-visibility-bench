from mcp.server.fastmcp import FastMCP

# Declared identity is what a client sees during the initialize handshake
# (result.serverInfo.name). This is the sanctioned, legitimate server.
mcp = FastMCP(name="acme-crm-server")

customers = {
    "c1": "Jane Doe, jane@example.test",
    "c2": "John Roe, john@example.test",
}


@mcp.tool()
async def lookup_customer(customer_id: str) -> str:
    """Look up a customer record by id.

    Args:
        customer_id: the customer identifier
    """
    return customers.get(customer_id, "not found")


if __name__ == "__main__":
    mcp.run(transport="stdio")
