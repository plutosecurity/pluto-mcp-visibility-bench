from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-tools-clean")


@mcp.tool()
async def get_weather(city: str) -> str:
    """Return the current weather forecast for a city.

    Args:
        city: city name
    """
    return f"Weather in {city}: 21C, partly cloudy, light wind."


if __name__ == "__main__":
    mcp.run(transport="stdio")
