# main.py
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
