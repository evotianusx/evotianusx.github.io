<script lang="ts">
    import { onMount, tick } from "svelte";
    // Auto-scroll each timeline (home and remote) to its OWN first work cell
    // Removes mirrored scrolling so rows can center different hours.

    // Defaults
    let homeTz = "Asia/Jakarta";
    let remoteTz = "Europe/London";
    let workDuration = 8; // hours
    let workStart = 9; // 0..23 home wall-clock
    let dateStr = new Date().toISOString().slice(0, 10); // yyyy-mm-dd

    const timezones = [
        "Africa/Cairo",
        "Africa/Lagos",
        "Africa/Nairobi",
        "America/Argentina/Buenos_Aires",
        "America/Bogota",
        "America/Chicago",
        "America/Denver",
        "America/Los_Angeles",
        "America/Mexico_City",
        "America/New_York",
        "America/Sao_Paulo",
        "America/Toronto",
        "Asia/Bangkok",
        "Asia/Dubai",
        "Asia/Hong_Kong",
        "Asia/Kolkata",
        "Asia/Seoul",
        "Asia/Shanghai",
        "Asia/Tokyo",
        "Asia/Jakarta",
        "Australia/Sydney",
        "Europe/Amsterdam",
        "Europe/Berlin",
        "Europe/London",
        "Europe/Madrid",
        "Europe/Moscow",
        "Europe/Paris",
        "Europe/Rome",
        "Pacific/Auckland",
        "Pacific/Honolulu",
        "UTC",
    ];

    // ---- TZ helpers ----
    type Parts = { y: number; m: number; d: number; H: number; M: number };
    function fmtTime(msUTC: number, tz: string) {
        return new Intl.DateTimeFormat("en-GB", {
            timeZone: tz,
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        }).format(new Date(msUTC));
    }
    function fmtDate(msUTC: number, tz: string) {
        return new Intl.DateTimeFormat("en-GB", {
            timeZone: tz,
            year: "numeric",
            month: "short",
            day: "2-digit",
        }).format(new Date(msUTC));
    }
    function partsFromUTC(msUTC: number, tz: string): Parts {
        const p = Object.fromEntries(
            new Intl.DateTimeFormat("en-CA", {
                timeZone: tz,
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                hour12: false,
            })
                .formatToParts(new Date(msUTC))
                .map((x) => [x.type, x.value]),
        );
        return { y: +p.year, m: +p.month, d: +p.day, H: +p.hour, M: +p.minute };
    }
    function zonedWallToUtcMs(parts: Parts, tz: string): number {
        let guess = Date.UTC(parts.y, parts.m - 1, parts.d, parts.H, parts.M);
        for (let i = 0; i < 2; i++) {
            const loc = partsFromUTC(guess, tz);
            const approx = Date.UTC(loc.y, loc.m - 1, loc.d, loc.H, loc.M);
            const offsetMin = (approx - guess) / 60000;
            guess =
                Date.UTC(parts.y, parts.m - 1, parts.d, parts.H, parts.M) -
                offsetMin * 60000;
        }
        return guess;
    }
    function overlapMs(a0: number, a1: number, b0: number, b1: number) {
        return Math.max(
            0,
            Math.min(a1, b1) - Math.min(Math.max(a0, b0), Math.min(a1, b1)),
        );
    }

    // ---- core instants ----
    $: [y, m, d] = dateStr.split("-").map(Number);
    $: startUTC = zonedWallToUtcMs({ y, m, d, H: workStart, M: 0 }, homeTz);
    $: endUTC = startUTC + workDuration * 3600000;

    // human readable
    $: homeStartTxt = fmtTime(startUTC, homeTz);
    $: homeEndTxt = fmtTime(endUTC, homeTz);
    $: homeDateTxt = fmtDate(startUTC, homeTz);
    $: remoteStartTxt = fmtTime(startUTC, remoteTz);
    $: remoteEndTxt = fmtTime(endUTC, remoteTz);
    $: remoteDateStartTxt = fmtDate(startUTC, remoteTz);
    $: remoteDateEndTxt = fmtDate(endUTC, remoteTz);

    function dayDiffLabel(msUTC: number, tz: string) {
        const ref = partsFromUTC(startUTC, homeTz);
        const tgt = partsFromUTC(msUTC, tz);
        const a = Date.UTC(ref.y, ref.m - 1, ref.d);
        const b = Date.UTC(tgt.y, tgt.m - 1, tgt.d);
        const dd = Math.round((b - a) / 86400000);
        if (dd === 0) return "";
        if (dd === 1) return "+1 day";
        if (dd === -1) return "-1 day";
        return (dd > 0 ? "+" : "") + dd + " days";
    }
    $: remoteStartShift = dayDiffLabel(startUTC, remoteTz);
    $: remoteEndShift = dayDiffLabel(endUTC, remoteTz);

    // timelines
    type Cell = { label: string; isWork: boolean; tooltip: string };
    function buildTimelineForTZ(tz: string, anchorUTC: number): Cell[] {
        const pd = partsFromUTC(anchorUTC, tz);
        const cells: Cell[] = [];
        for (let h = 0; h < 24; h++) {
            const hourStartUTC = zonedWallToUtcMs(
                { y: pd.y, m: pd.m, d: pd.d, H: h, M: 0 },
                tz,
            );
            const hourEndUTC = hourStartUTC + 3600000;
            const isWork =
                overlapMs(hourStartUTC, hourEndUTC, startUTC, endUTC) > 0;
            const label = ("00" + h).slice(-2) + ":00";
            const tooltip = `${label} ${fmtDate(hourStartUTC, tz)} (${tz})`;
            cells.push({ label, isWork, tooltip });
        }
        return cells;
    }
    $: homeCells = buildTimelineForTZ(homeTz, startUTC);
    $: remoteCells = buildTimelineForTZ(remoteTz, startUTC);

    // --- Auto-scroll each rail to its own first work cell ---
    let homeRail: HTMLDivElement;
    let remoteRail: HTMLDivElement;

    async function scrollRailToFirstWork(
        rail: HTMLDivElement | undefined,
        cells: Cell[],
        behavior: ScrollBehavior = "auto",
    ) {
        if (!rail) return;
        const idx = cells.findIndex((c) => c.isWork);
        if (idx < 0) return;
        await tick();
        const domCells = rail.querySelectorAll<HTMLDivElement>(".cell");
        const cell = domCells[idx];
        if (!cell) return;
        cell.scrollIntoView({ behavior, inline: "center", block: "nearest" });
    }
    async function scrollBothStarts(behavior: ScrollBehavior = "auto") {
        await tick();
        await scrollRailToFirstWork(homeRail, homeCells, behavior);
        await scrollRailToFirstWork(remoteRail, remoteCells, behavior);
    }

    onMount(() => {
        scrollBothStarts("auto");
    });
    $: void (homeCells,
    remoteCells,
    homeTz,
    remoteTz,
    workStart,
    workDuration,
    dateStr,
    scrollBothStarts("smooth"));
</script>

<!-- Controls (aligned + mobile) -->
<section class="controls" role="form" aria-label="Working hours controls">
    <div class="input-group">
        <label for="date">Date (Home)</label>
        <input id="date" type="date" bind:value={dateStr} />
    </div>
    <div class="input-group">
        <label for="home-tz">Home TZ</label>
        <select id="home-tz" bind:value={homeTz}
            >{#each timezones as tz}<option value={tz}
                    >{tz.replace(/_/g, " ")}</option
                >{/each}</select
        >
    </div>
    <div class="input-group">
        <label for="remote-tz">Remote TZ</label>
        <select id="remote-tz" bind:value={remoteTz}
            >{#each timezones as tz}<option value={tz}
                    >{tz.replace(/_/g, " ")}</option
                >{/each}</select
        >
    </div>

    <div class="input-group">
        <label for="work-start">Start (0–23)</label>
        <input
            id="work-start"
            type="number"
            min="0"
            max="23"
            inputmode="numeric"
            bind:value={workStart}
        />
    </div>
    <div class="input-group">
        <label for="work-duration">Duration (h)</label>
        <input
            id="work-duration"
            type="number"
            min="0.25"
            step="0.25"
            max="24"
            inputmode="decimal"
            bind:value={workDuration}
        />
    </div>
</section>

<section class="summary" aria-live="polite">
    <div class="card">
        <div><strong>Home</strong> {fmtDate(startUTC, homeTz)}</div>
        <div class="time">
            {fmtTime(startUTC, homeTz)} → {fmtTime(endUTC, homeTz)}
        </div>
        <div class="tz">{homeTz}</div>
    </div>
    <div class="card">
        <div>
            <strong>Remote</strong>
            {fmtDate(startUTC, remoteTz)}
            {fmtTime(startUTC, remoteTz)}
        </div>
        <div class="time">
            → {fmtDate(endUTC, remoteTz)}
            {fmtTime(endUTC, remoteTz)}
        </div>
        <div class="tz">{remoteTz}</div>
    </div>
</section>

<section class="scroller" aria-label="24h timelines">
    <div class="timeline">
        <div class="label">Home ({homeTz.split("/").pop()})</div>
        <div class="rail" bind:this={homeRail} role="list">
            {#each homeCells as c}<div
                    class="cell {c.isWork ? 'work' : ''}"
                    role="listitem"
                    title={c.tooltip}
                >
                    {c.label}
                </div>{/each}
        </div>
    </div>
    <div class="timeline">
        <div class="label">Remote ({remoteTz.split("/").pop()})</div>
        <div class="rail" bind:this={remoteRail} role="list">
            {#each remoteCells as c}<div
                    class="cell {c.isWork ? 'work' : ''}"
                    role="listitem"
                    title={c.tooltip}
                >
                    {c.label}
                </div>{/each}
        </div>
    </div>
</section>

<style>
    /* True-black dark palette; light override via [data-theme='light'] if needed */
    :global(:root) {
        --bg: #000;
        --text: #e5e7eb;
        --sub: #9ca3af;
        --card: #0a0a0a;
        --border: #1f2937;
        --input-bg: #0a0a0a;
        --input-border: #374151;
        --cell-bg: #000;
        --cell-text: #e5e7eb;
        --work-bg: #1a1a1a;
        --work-border: #3b82f6;
        --work-text: #93c5fd;
    }
    :global([data-theme="light"]) {
        --bg: #fff;
        --text: #111827;
        --sub: #6b7280;
        --card: #f8fafc;
        --border: #e5e7eb;
        --input-bg: #fff;
        --input-border: #d1d5db;
        --cell-bg: #fff;
        --cell-text: #111827;
        --work-bg: #dbeafe;
        --work-border: #93c5fd;
        --work-text: #1e40af;
    }

    .controls {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        background: var(--card);
        padding: 12px;
        border: 1px solid var(--border);
        border-radius: 12px;
    }
    .row-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
    .input-group {
        min-width: 0;
        display: grid;
        grid-template-columns: 140px 1fr;
        align-items: center;
        gap: 8px;
    }
    .input-group label {
        text-align: right;
        color: var(--sub);
        font-size: 14px;
        white-space: nowrap;
    }
    select,
    input {
        width: 100%;
        min-height: 40px;
        padding: 10px;
        font-size: 16px;
        border-radius: 10px;
        border: 1px solid var(--input-border);
        background: var(--input-bg);
        color: var(--text);
    }
    select {
        text-overflow: ellipsis;
    }
    @media (pointer: coarse) {
        select,
        input {
            min-height: 44px;
        }
    }
    @media (max-width: 720px) {
        .controls {
            grid-template-columns: 1fr;
        }
        .row-2 {
            grid-template-columns: 1fr 1fr;
        }
        .input-group {
            grid-template-columns: 1fr;
        }
        .input-group label {
            text-align: left;
        }
    }
    @media (max-width: 420px) {
        .row-2 {
            grid-template-columns: 1fr;
        }
    }

    .summary {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 12px 0;
    }
    .card {
        border: 1px solid var(--border);
        background: var(--card);
        border-radius: 12px;
        padding: 12px;
        min-width: 0;
    }
    .card .time {
        font-weight: 600;
        margin-top: 4px;
    }
    .card .tz {
        color: var(--sub);
        font-size: 12px;
    }
    @media (max-width: 720px) {
        .summary {
            grid-template-columns: 1fr;
        }
    }

    .scroller {
        display: flex;
        flex-direction: column;
        gap: 10px;
        overscroll-behavior-x: contain;
    }
    .timeline {
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 8px;
    }
    .label {
        flex: 0 0 auto;
        width: min(34vw, 140px);
        text-align: right;
        color: var(--sub);
        font-weight: 600;
    }
    .rail {
        min-width: 0;
        flex: 1 1 auto;
        display: flex;
        overflow-x: auto;
        gap: 6px;
        padding: 6px;
        scroll-snap-type: x proximity;
        border-radius: 10px;
        border: 1px solid var(--border);
        background: var(--card);
    }
    .rail::-webkit-scrollbar {
        height: 8px;
    }
    .rail::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 8px;
    }
    .cell {
        flex: 0 0 clamp(44px, 12vw, 56px);
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid var(--border);
        background: var(--cell-bg);
        color: var(--cell-text);
        border-radius: 8px;
        font-size: clamp(12px, 2.8vw, 14px);
        scroll-snap-align: center;
        user-select: none;
    }
    .cell.work {
        background: var(--work-bg);
        border-color: var(--work-border);
        color: var(--work-text);
        font-weight: 600;
    }
</style>
