from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-mcp")

_FORECASTS = {
    "london": "Overcast, 14C",
    "tokyo": "Clear, 22C",
    "cairo": "Sunny, 33C",
}


@mcp.tool()
async def get_forecast(city: str) -> str:
    """Returns the weather forecast for a city.

    Args:
        city: city name
    """
    return _FORECASTS.get(city.lower(), "No forecast available for that city.")


if __name__ == "__main__":
    mcp.run(transport="stdio")
