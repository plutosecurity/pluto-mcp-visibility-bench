from mcp.server.fastmcp import FastMCP

mcp = FastMCP("file-utils-mcp")

# Simulated file store (a test fixture, not real filesystem access, to keep
# this dataset self-contained and safe to run anywhere).
_FAKE_FILES = {
    "notes.txt": "Buy milk. Call the dentist.",
    "readme.txt": "This is a sample text file.",
}


@mcp.tool()
async def read_text_file(path: str) -> str:
    """Reads the contents of a text file from the sandboxed workspace.

    Args:
        path: file name within the sandboxed workspace
    """
    return _FAKE_FILES.get(path, "File not found.")


if __name__ == "__main__":
    mcp.run(transport="stdio")
