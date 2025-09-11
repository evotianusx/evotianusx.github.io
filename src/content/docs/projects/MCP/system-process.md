---
title: "System Process Monitor"
description: An MCP tool can trigger an external HTTP call (to your FastAPI service) and return structured results to an agent.
---

## 1) FastAPI backend (Process Explorer API)

This service snapshots running processes using `psutil`, supports filtering, server‑side sorting, and pagination.

**Requirements**

* Python 3.10+
* `fastapi`, `uvicorn[standard]`, `psutil`

```bash
pip install fastapi uvicorn[standard] psutil
# or
uv add fastapi uvicorn[standard] psutil
```

**Code — `main.py`**

```python
from typing import List, Optional, Literal
from math import ceil
from datetime import datetime

import psutil
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Process Explorer API", version="0.1.0")

# --- Models ------------------------------------------------------------------

class ProcessItem(BaseModel):
    pid: int
    name: Optional[str] = None
    username: Optional[str] = None
    status: Optional[str] = None
    create_time: Optional[float] = Field(
        None, description="Unix timestamp (seconds since epoch)"
    )
    memory_rss: Optional[int] = Field(
        None, description="Resident Set Size (bytes)"
    )
    memory_vms: Optional[int] = Field(
        None, description="Virtual Memory Size (bytes)"
    )
    cpu_percent: Optional[float] = Field(
        None, description="CPU percent (may be 0 on first read)"
    )
    cmdline: Optional[List[str]] = None

class PaginatedResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    items: List[ProcessItem]

# --- Helpers -----------------------------------------------------------------

SORTABLE_FIELDS = {
    "pid",
    "name",
    "username",
    "status",
    "create_time",
    "memory_rss",
    "memory_vms",
    "cpu_percent",
}

def safe_proc_info(p: psutil.Process) -> Optional[ProcessItem]:
    """
    Safely extract process info. Returns None if the process vanishes or is denied.
    Note on cpu_percent: psutil returns 0.0 on the first call unless previously primed.
    We keep it zero-cost & instantaneous for API responsiveness.
    """
    try:
        with p.oneshot():
            info = p.as_dict(attrs=[
                "pid", "name", "username", "status", "create_time", "cpu_percent", "cmdline"
            ])
            mem = p.memory_info()
            return ProcessItem(
                pid=info.get("pid"),
                name=info.get("name"),
                username=info.get("username"),
                status=info.get("status"),
                create_time=info.get("create_time"),
                cpu_percent=info.get("cpu_percent"),
                memory_rss=getattr(mem, "rss", None),
                memory_vms=getattr(mem, "vms", None),
                cmdline=info.get("cmdline"),
            )
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def paginate(items: List[ProcessItem], page: int, per_page: int) -> PaginatedResponse:
    total = len(items)
    total_pages = max(1, ceil(total / per_page)) if per_page > 0 else 1
    if page < 1 or page > total_pages:
        # Allow empty page if total == 0, else raise
        if total == 0 and page == 1:
            return PaginatedResponse(page=1, per_page=per_page, total=0, total_pages=1, items=[])
        raise HTTPException(status_code=400, detail=f"page must be between 1 and {total_pages}")
    start = (page - 1) * per_page
    end = start + per_page
    return PaginatedResponse(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        items=items[start:end],
    )

# --- Endpoint ----------------------------------------------------------------

@app.get("/processes", response_model=PaginatedResponse, summary="List running processes (paginated)")
def list_processes(
    page: int = Query(1, ge=1, description="1-based page index"),
    per_page: int = Query(25, ge=1, le=200, description="Items per page (max 200)"),
    sort_by: Optional[str] = Query(None, description=f"One of: {', '.join(sorted(SORTABLE_FIELDS))}"),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order"),
    q: Optional[str] = Query(None, description="Case-insensitive substring filter on process name"),
):
    # Snapshot all processes fast
    items: List[ProcessItem] = []
    for p in psutil.process_iter():
        item = safe_proc_info(p)
        if item:
            items.append(item)

    # Filter
    if q:
        q_lower = q.lower()
        items = [it for it in items if (it.name or "").lower().find(q_lower) != -1]

    # Sort
    if sort_by:
        if sort_by not in SORTABLE_FIELDS:
            raise HTTPException(status_code=400, detail=f"Invalid sort_by. Allowed: {', '.join(sorted(SORTABLE_FIELDS))}")
        reverse = (order == "desc")
        # Use a robust key function (None-safe)
        def key_fn(it: ProcessItem):
            val = getattr(it, sort_by, None)
            # Normalize lists (cmdline) and strings
            if isinstance(val, list):
                return " ".join(val) if val else ""
            return val if val is not None else -1 if sort_by in {"pid", "create_time", "cpu_percent", "memory_rss", "memory_vms"} else ""
        items.sort(key=key_fn, reverse=reverse)

    # Paginate
    return paginate(items, page, per_page)
```

**Run the API**

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Quick test**

```bash
curl 'http://127.0.0.1:8000/processes?per_page=5&sort_by=pid&order=asc'
```

---

## 2) MCP server (stdio transport)

The MCP tool `list_process` calls the FastAPI endpoint over HTTP and returns a JSON payload to the client.

**Requirements**

* `httpx`
* `mcp` (the server library providing `FastMCP`)

```bash
pip install httpx mcp
# or
uv add httpx mcp
```

**Code — `mcp.py`**

```python
import asyncio
import json
import logging
from typing import Optional, Literal, Any, List
import sys
import httpx
from pydantic import BaseModel, Field, ValidationError

from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

API_BASE = "http://127.0.0.1:8000"

# ---- Logging setup ------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stderr,  # ensure logs don't corrupt stdout
)
logger = logging.getLogger("process-mcp")

# ---- Server -------------------------------------------------------------------
mcp = FastMCP("process-mcp")

@mcp.tool()
async def list_process(
    sort_by: str,
    order: Literal["asc", "desc"] = "asc",
    page: int = 1,
    per_page: int = 25,
    q: Optional[str] = None,
):

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

    return [TextContent(type="text", text=json.dumps(data, separators=(",", ":"))) ]

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**Run the MCP server (stdio)**

```bash
python mcp.py
# or with uv
uv run mcp.py
```

> The MCP server writes logs to **stderr** (safe for stdio). Tool results are written to **stdout**.

---

## 3) Testing with the OpenAI Agents SDK

This snippet launches the MCP server as a child process (stdio) and lists tools, then runs an agent that calls `list_process`.

**Requirements**

* `python-dotenv`
* `openai-agents` (or your Agents SDK distribution)

```bash
pip install python-dotenv openai-agents
# or
uv add python-dotenv openai-agents
```

**Code — `test_agent.py`**

```python
from dotenv import load_dotenv
from agents.mcp import MCPServerStdio
from agents import Agent, Runner, trace

load_dotenv(override=True)

fetch_params = {"command": "uv", "args": ["run", "mcp.py"], "env": {}}

async with MCPServerStdio(
    params=fetch_params, client_session_timeout_seconds=60, name='ha'
) as server:
    fetch_tools = await server.list_tools()

print(fetch_tools)

instructions = """
You are SysMon, an operations-savvy assistant that inspects local processes via an MCP tool.

Guidelines:
1) When the user asks “top N by memory/cpu”, call list_processes with per_page=N, page=1 and the right sort_by.
2) Prefer server-side sorting (sort_by + order) over client sorting.
3) Always include PID in summaries; report memory in MB and CPU% when available.
4) If more rows are needed, request subsequent pages.
5) If the user names an app (e.g., “chrome”), pass q="chrome".

Respond concisely with a short table and 1–2 bullet insights; include which sort key and page size you used.
"""

async with MCPServerStdio(
    params=fetch_params, client_session_timeout_seconds=60, name="ha"
) as server:
    agent = Agent(
        name="investigator",
        instructions=instructions,
        model="gpt-4.1-mini",
        mcp_servers=[server],
    )
    with trace("SYS MONitor"):
        result = await Runner.run(
            agent,
            "Show my the current processes",
        )
        print(result.final_output)
```

**Example output**

```
[Tool(name='list_process', title=None, description='', inputSchema={'properties': {'sort_by': {'title': 'Sort By', 'type': 'string'}, 'order': {'default': 'asc', 'enum': ['asc', 'desc'], 'title': 'Order', 'type': 'string'}, 'page': {'default': 1, 'title': 'Page', 'type': 'integer'}, 'per_page': {'default': 25, 'title': 'Per Page', 'type': 'integer'}, 'q': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Q'}}, 'required': ['sort_by'], 'title': 'list_processArguments', 'type': 'object'}, outputSchema=None, annotations=None, meta=None)]
```

```
Here are the first 10 processes sorted by PID (page size 10):

| PID | Name             | User | Memory (MB) | CPU % | Status   |
| --- | ---------------- | ---- | ----------- | ----- | -------- |
| 1   | systemd          | root | 11.63       | 0.0   | sleeping |
| 2   | init-systemd(Ub) | root | 1.62        | 0.0   | sleeping |
| 6   | init             | root | 1.75        | 0.0   | sleeping |
| 60  | systemd-journald | root | 14.76       | 0.0   | sleeping |
| 81  | systemd-udevd    | root | 5.75        | 0.0   | sleeping |
| 97  | snapfuse         | root | 1.50        | 0.0   | sleeping |
| 100 | snapfuse         | root | 9.88        | 0.0   | sleeping |
| 102 | snapfuse         | root | 1.50        | 0.0   | sleeping |
| 113 | snapfuse         | root | 10.51       | 0.0   | sleeping |
| 118 | snapfuse         | root | 6.12        | 0.0   | sleeping |

- All these processes are currently sleeping with 0.0% CPU usage.
- The memory usage varies from about 1.5MB to 14.76MB.
```

---

## API Reference — `GET /processes`

**Query params**

* `page` (int, ≥1)
* `per_page` (int, 1–200)
* `sort_by` (one of: `pid`, `name`, `username`, `status`, `create_time`, `memory_rss`, `memory_vms`, `cpu_percent`)
* `order` (`asc` | `desc`)
* `q` (case-insensitive substring on `name`)

**Notes**

* `cpu_percent` may be 0.0 on first read unless `psutil` is primed; this design keeps the endpoint fast.
* Fields like `cmdline` may be empty for restricted/system processes.

## MCP Tool Reference — `list_process`

**Arguments**

* `sort_by: str` (required)
* `order: Literal["asc", "desc"] = "asc"`
* `page: int = 1`
* `per_page: int = 25`
* `q: Optional[str] = None`

**Behavior**

* Calls `GET {API_BASE}/processes` with provided params and returns JSON as a single `TextContent` payload.
* Logs are emitted to `stderr`; output is emitted to `stdout` (stdio‑safe for MCP).

---

## Troubleshooting

* **Permission errors / missing fields**: Some processes are inaccessible; they are skipped gracefully.
* **CPU% always 0.0**: `psutil` needs a second sampling to compute CPU%; for low overhead, this API returns the instantaneous (possibly 0.0) value.
* **Sorting pitfalls**: `None` values are normalized so sorting is stable.
* **Port conflicts**: Change `--port` or set `API_BASE` accordingly.

## Next steps (optional hardening)

* Add a `primed=true` flag to perform a short 0.1s CPU sampling loop when requested.
* Expose `fields` query to reduce payload size.
* Add auth (e.g., API key or local‑only binding) if you plan to bind beyond `127.0.0.1`.
* Stream results with Server‑Sent Events (SSE) or WebSockets for live updates.
