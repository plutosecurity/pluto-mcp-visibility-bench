from mcp.server.fastmcp import FastMCP

mcp = FastMCP("currency-tools-clean")

RATES = {("USD", "EUR"): 0.92, ("EUR", "USD"): 1.09, ("USD", "GBP"): 0.79}


@mcp.tool()
async def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Return the current exchange rate between two currencies.

    Args:
        from_currency: three-letter source currency code
        to_currency: three-letter target currency code
    """
    key = (from_currency.upper(), to_currency.upper())
    rate = RATES.get(key, 1.0)
    return f"Rate: 1 {from_currency.upper()} = {rate} {to_currency.upper()}."


if __name__ == "__main__":
    mcp.run(transport="stdio")
