from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("records-admin-logged")

records = {"r1": "old invoice", "r2": "old invoice", "r3": "recent invoice"}
audit_log = []


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
async def purge_old_records(older_than_days: int) -> str:
    """Delete records older than the given number of days.

    Args:
        older_than_days: age threshold in days
    """
    deleted = []
    for rid in list(records.keys()):
        if "old" in records[rid]:
            del records[rid]
            deleted.append(rid)
    # Genuine audit trail: every destructive call is recorded, success
    # or not, with what actually happened.
    audit_log.append(f"purge_old_records(older_than_days={older_than_days}) deleted {deleted}")
    return f"Purged {len(deleted)} record(s): {deleted}"


@mcp.tool()
async def get_audit_log() -> str:
    """Return the recorded audit trail of administrative actions."""
    return str(audit_log)


if __name__ == "__main__":
    mcp.run(transport="stdio")
