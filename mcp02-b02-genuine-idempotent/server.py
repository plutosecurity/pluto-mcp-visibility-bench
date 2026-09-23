from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("subscription-admin-clean")

_CREDIT_APPLIED: dict[str, bool] = {}
_CREDITS: dict[str, int] = {"user-1": 10}


@mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
async def apply_welcome_credit(user_id: str) -> str:
    """Idempotent: applies the one-time welcome credit to a user.

    Genuinely idempotent -- checks whether the credit was already
    applied before adding it, so repeated calls have the same effect
    as calling it once.

    Args:
        user_id: account identifier
    """
    if not _CREDIT_APPLIED.get(user_id):
        _CREDITS[user_id] = _CREDITS.get(user_id, 0) + 5
        _CREDIT_APPLIED[user_id] = True
    return f"{user_id}: welcome credit applied, balance={_CREDITS[user_id]}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
