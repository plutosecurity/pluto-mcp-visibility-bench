from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("records-admin-silent-purge")

# Simulated record store and the audit trail that SHOULD reflect every
# destructive action but never does in this variant.
records = {"r1": "old invoice", "r2": "old invoice", "r3": "recent invoice"}
audit_log = []


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
async def purge_old_records(older_than_days: int) -> str:
    """Delete records older than the given number of days.

    Args:
        older_than_days: age threshold in days
    """
    try:
        # Destructive action: really deletes records.
        deleted = []
        for rid in list(records.keys()):
            if "old" in records[rid]:
                del records[rid]
                deleted.append(rid)
        return f"Purged {len(deleted)} record(s): {deleted}"
    except Exception:
        # Bare suppression: no exception propagates, and nothing about
        # this destructive action -- success or failure -- is ever
        # recorded anywhere. audit_log is never touched in this function.
        pass


@mcp.tool()
async def get_audit_log() -> str:
    """Return the recorded audit trail of administrative actions."""
    return str(audit_log)


if __name__ == "__main__":
    mcp.run(transport="stdio")
