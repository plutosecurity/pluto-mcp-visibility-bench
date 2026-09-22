from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="filevault-storage-server")

files = {
    "report.pdf": "quarterly-report-contents",
    "notes.txt": "meeting-notes-contents",
}


@mcp.tool()
async def read_file(filename: str) -> str:
    """Read a file's contents by name.

    Args:
        filename: the file to read
    """
    return files.get(filename, "not found")


if __name__ == "__main__":
    mcp.run(transport="stdio")
