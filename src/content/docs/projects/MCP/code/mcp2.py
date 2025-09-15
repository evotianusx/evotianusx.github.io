#!/usr/bin/env python3
import json
import logging
from typing import Optional
import sys
import httpx
from fastmcp import FastMCP
from mcp.types import TextContent

API_BASE = "http://127.0.0.1:8000"

# ---- Logging setup ------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("process-mcp")

# ---- Server -------------------------------------------------------------------
mcp = FastMCP("process-mcp", port=8001)


@mcp.tool()
async def list_process(
    sort_by: str,
    order: str = "asc",
    page: int = 1,
    per_page: int = 25,
    q: Optional[str] = None,
):
    """
    Fetch a paginated list of processes from the API.

    Parameters:
        sort_by (str): Field name to sort results by. Allowed: cpu_percent, create_time, memory_rss, memory_vms, name, pid, status, username
        order (str, optional): Sort order, "asc" or "desc". Default is "asc".
        page (int, optional): Page number to fetch. Default is 1.
        per_page (int, optional): Number of results per page. Default is 25.
        q (str, optional): Optional search query to filter processes.

    Returns:
        List[TextContent]: The JSON response from the API as text, or error info.
    """
    params = {
        "page": page,
        "per_page": per_page,
        "order": order,
    }
    if sort_by:
        params["sort_by"] = sort_by
    if q:
        params["q"] = q

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
            r = await client.get(f"{API_BASE}/processes", params=params)
            r.raise_for_status()
            data = r.json()
            logger.debug("Fetched data: %s", data)
    except httpx.HTTPError as e:
        logger.error("HTTP error: %s", e)
        return [
            TextContent(
                type="text", text=json.dumps({"error": "http_error", "details": str(e)})
            )
        ]

    return [TextContent(type="text", text=json.dumps(data, separators=(",", ":")))]


# @mcp.tool()
# async def search(
#     query: str,
#     page: int = 1,
#     per_page: int = 25,
# ):
#     """
#     Search for processes using a query string.

#     Parameters:
#         query (str): The search term to filter processes.
#         page (int, optional): Page number to fetch. Default is 1.
#         per_page (int, optional): Number of results per page. Default is 25.

#     Returns:
#         List[TextContent]: The JSON response from the API as text, or error info.
#     """
#     params = {"q": query, "page": page, "per_page": per_page}

#     try:
#         async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
#             r = await client.get(f"{API_BASE}/processes/search", params=params)
#             r.raise_for_status()
#             data = r.json()
#             logger.debug("Search results: %s", data)
#     except httpx.HTTPError as e:
#         logger.error("HTTP error: %s", e)
#         return [
#             TextContent(
#                 type="text", text=json.dumps({"error": "http_error", "details": str(e)})
#             )
#         ]

#     return [TextContent(type="text", text=json.dumps(data, separators=(",", ":")))]


# @mcp.tool()
# async def fetch(id: str):
#     """
#     Fetch a process file by ID.

#     Parameters:
#         id (str): The identifier of the file to fetch.

#     Returns:
#         List[TextContent]: Currently returns an empty JSON object as a placeholder.
#     """
#     # Placeholder implementation: return an empty file response
#     logger.debug("Fetch called with file_id=%s, returning empty file.", id)
#     return [TextContent(type="text", text=json.dumps({}))]


if __name__ == "__main__":
    mcp.run(transport="http")
