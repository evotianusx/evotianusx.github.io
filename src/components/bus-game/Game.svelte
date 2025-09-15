<script>
  import { onMount } from "svelte";
  import Controls from "./Controls.svelte";
  import RouteList from "./RouteList.svelte";
  import StationQueues from "./StationQueues.svelte";

  // ===== Config =====
  const INITIAL_STATIONS = 5;
  const PASSENGER_OVERFLOW_LIMIT = 20;
  const MIN_DIST_RATIO = 0.2;
  const NEW_STATION_EVERY_SEC = 45;
  const STATION_RADIUS = 10;
  const DEPOT_SIZE = 18;
  const BOARDING_DWELL_SEC = 1;
  const DEPOT_DWELL_SEC = 3;
  const ASPECT = 16 / 9;

  export let className = "";

  const BUS_TYPES = [
    { id: "standard", label: "Standard", cap: 10, speed: 110 },
    { id: "fast", label: "Fast (low cap)", cap: 6, speed: 160 },
    { id: "large", label: "Large (slow)", cap: 18, speed: 80 },
  ];
  const PALETTE = [
    "#e74c3c",
    "#8e44ad",
    "#3498db",
    "#16a085",
    "#f39c12",
    "#e67e22",
    "#1abc9c",
    "#d35400",
    "#9b59b6",
    "#2ecc71",
    "#c0392b",
    "#2980b9",
    "#27ae60",
    "#f1c40f",
    "#7f8c8d",
  ];

  // ===== State =====
  let containerEl;
  let gameEl;
  let width = 1280;
  let height = Math.floor(width / ASPECT);

  let depot = { x: 0.5, y: 0.5 }; // normalized coords
  let stations = [];
  let routes = [];
  let buses = {};
  let passengers = {};
  let gameOver = false;
  let tickSpeed = 1;
  let paused = false;

  let buildMode = false;
  let building = { active: false, started: false, stopIds: [], error: null };

  // Ticking (1 passenger per tick; no burst catch-up)
  let ticks = 0;
  let tickAccum = 0;
  let lastTime = 0;

  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const distPx = (ax, ay, bx, by) => Math.hypot(ax - bx, ay - by);
  function toPx(p) {
    return { x: p.x * width, y: p.y * height };
  }

  // Safe margins to keep stations inside the viewBox
  function getSafeMarginsPx() {
    const m = Math.max(DEPOT_SIZE / 2 + STATION_RADIUS + 8, 30);
    return { mx: m, my: m };
  }

  function isFarEnough(norm) {
    const minPx = MIN_DIST_RATIO * width;
    const dpx = toPx(depot);
    if (distPx(dpx.x, dpx.y, norm.x * width, norm.y * height) < minPx)
      return false;
    for (const s of stations) {
      const spx = toPx(s);
      if (distPx(spx.x, spx.y, norm.x * width, norm.y * height) < minPx)
        return false;
    }
    return true;
  }

  function createRandomStation() {
    let tries = 0;
    while (tries++ < 200) {
      const { mx, my } = getSafeMarginsPx();
      const nx = clamp(Math.random(), mx / width, 1 - mx / width);
      const ny = clamp(Math.random(), my / height, 1 - my / height);
      const n = { x: nx, y: ny };
      if (isFarEnough(n)) {
        const id = crypto.randomUUID();
        const color = PALETTE[stations.length % PALETTE.length];
        passengers[id] = [];
        stations = [...stations, { id, x: n.x, y: n.y, color }];
        return;
      }
    }
  }

  function resetGame() {
    gameOver = false;
    stations = [];
    routes = [];
    buses = {};
    passengers = {};
    buildMode = false;
    building = { active: false, started: false, stopIds: [], error: null };
    ticks = 0;
    tickAccum = 0;
    lastTime = 0;
    for (let i = 0; i < INITIAL_STATIONS; i++) createRandomStation();
  }

  function spawnPassengerOne() {
    if (stations.length === 0) return;
    const fromIdx = Math.floor(Math.random() * stations.length);
    const from = stations[fromIdx];
    let to = from;
    if (stations.length > 1) {
      while (to.id === from.id)
        to = stations[Math.floor(Math.random() * stations.length)];
    }
    (passengers[from.id] ||= []).push({
      id: crypto.randomUUID(),
      targetStationId: to.id,
      color: to.color,
    });
    if ((passengers[from.id] || []).length > PASSENGER_OVERFLOW_LIMIT)
      gameOver = true;
  }

  // Smooth path (Catmull-Rom -> Cubic Bézier)
  function smoothPathD(points) {
    if (points.length < 2) return "";
    const p = points.map(toPx);
    let d = `M ${p[0].x.toFixed(1)} ${p[0].y.toFixed(1)}`;
    for (let i = 0; i < p.length - 1; i++) {
      const p0 = p[i - 1] || p[i];
      const p1 = p[i];
      const p2 = p[i + 1];
      const p3 = p[i + 2] || p[i + 1];
      const c1x = p1.x + (p2.x - p0.x) / 6;
      const c1y = p1.y + (p2.y - p0.y) / 6;
      const c2x = p2.x - (p3.x - p1.x) / 6;
      const c2y = p2.y - (p3.y - p1.y) / 6;
      d += ` C ${c1x.toFixed(1)} ${c1y.toFixed(1)}, ${c2x.toFixed(1)} ${c2y.toFixed(1)}, ${p2.x.toFixed(1)} ${p2.y.toFixed(1)}`;
    }
    return d;
  }

  function sampleSmooth(points, stepPx = 6) {
    const px = points.map(toPx);
    const sampled = [];
    for (let i = 0; i < px.length - 1; i++) {
      const a = px[i],
        b = px[i + 1];
      const segLen = Math.hypot(b.x - a.x, b.y - a.y);
      const steps = Math.max(2, Math.floor(segLen / stepPx));
      for (let s = 0; s < steps; s++) {
        const t = s / steps;
        sampled.push({
          x: a.x * (1 - t) + b.x * t,
          y: a.y * (1 - t) + b.y * t,
        });
      }
    }
    sampled.push(px[px.length - 1]);
    const sm = [];
    for (let i = 0; i < sampled.length; i++) {
      const a = sampled[i - 1] || sampled[i];
      const b = sampled[i];
      const c = sampled[i + 1] || sampled[i];
      sm.push({ x: (a.x + b.x + c.x) / 3, y: (a.y + b.y + c.y) / 3 });
    }
    return sm.map((p) => ({ x: p.x / width, y: p.y / height }));
  }

  function buildRouteFromStopIds(stopIds) {
    if (stopIds.length < 2) return null;
    const uniq = Array.from(new Set(stopIds));
    if (uniq.length !== stopIds.length) return null;
    const stops = stopIds
      .map((id) => stations.find((s) => s.id === id))
      .filter(Boolean);
    if (stops.length !== stopIds.length) return null;
    const pathPoints = [depot, ...stops, depot];
    const id = crypto.randomUUID();
    return {
      id,
      name: `Route ${routes.length + 1}`,
      stops: stopIds,
      pathPoints,
      buses: [],
      assignments: { standard: 0, fast: 0, large: 0 },
      sampled: sampleSmooth(pathPoints),
      seg: null,
      totalLen: 0,
    };
  }

  function deleteRouteById(routeId) {
    const r = routes.find((r) => r.id === routeId);
    if (!r) return;
    for (const busId of r.buses) delete buses[busId];
    routes = routes.filter((x) => x.id !== routeId);
  }

  function assignBuses(routeId, typeId, count) {
    const route = routes.find((r) => r.id === routeId);
    if (!route) return;

    if (!route.seg) {
      route.seg = [];
      route.totalLen = 0;
      const path = route.sampled;
      for (let i = 0; i < path.length; i++) {
        const a = toPx(path[i]);
        const b = toPx(path[(i + 1) % path.length]);
        const L = Math.hypot(b.x - a.x, b.y - a.y);
        route.seg.push(L);
        route.totalLen += L;
      }
    }

    const keep = [];
    for (const id of route.buses) {
      if (buses[id]?.typeId === typeId) delete buses[id];
      else keep.push(id);
    }
    route.buses = keep;

    for (let i = 0; i < count; i++) {
      const busId = crypto.randomUUID();
      const type = BUS_TYPES.find((t) => t.id === typeId);
      buses[busId] = {
        id: busId,
        typeId,
        cap: type.cap,
        speed: type.speed,
        routeId: route.id,
        dwell: DEPOT_DWELL_SEC,
        state: "depot",
        carried: [],
        progress: (route.totalLen * (i / Math.max(count, 1))) % route.totalLen,
      };
      route.buses.push(busId);
    }
    route.assignments[typeId] = count;
    routes = [...routes];
  }

  function stationAtPoint(px, py, threshold = STATION_RADIUS + 6) {
    for (const s of stations) {
      const sp = toPx(s);
      if (Math.hypot(px - sp.x, py - sp.y) <= threshold) return s;
    }
    return null;
  }
  function atDepot(px, py) {
    const d = toPx(depot);
    const half = DEPOT_SIZE / 2 + 6;
    return Math.abs(px - d.x) <= half && Math.abs(py - d.y) <= half;
  }

  function unloadLoad(bus, stopStation) {
    bus.carried = bus.carried.filter(
      (p) => p.targetStationId !== stopStation.id,
    );
    const route = routes.find((r) => r.id === bus.routeId);
    const allowedTargets = new Set(route.stops);
    const queue = passengers[stopStation.id] || [];
    const remaining = bus.cap - bus.carried.length;
    let loaded = 0;
    if (remaining > 0 && queue.length) {
      const keep = [];
      for (const p of queue) {
        if (loaded >= remaining) {
          keep.push(p);
          continue;
        }
        if (allowedTargets.has(p.targetStationId)) {
          bus.carried.push(p);
          loaded++;
        } else keep.push(p);
      }
      passengers[stopStation.id] = keep;
    }
  }

  function updateBus(bus, dt) {
    const route = routes.find((r) => r.id === bus.routeId);
    if (!route) return;
    const path = route.sampled;
    if (path.length < 2) return;

    if (bus.dwell > 0) {
      bus.dwell -= dt;
      if (bus.dwell > 0) return;
    }

    const moveDist = bus.speed * dt;
    if (!route.seg || route.seg.length === 0) return;

    bus.progress = (bus.progress + moveDist) % route.totalLen;

    let acc = 0,
      segIdx = 0;
    while (
      segIdx < route.seg.length &&
      acc + route.seg[segIdx] < bus.progress
    ) {
      acc += route.seg[segIdx++];
    }
    const segLen = route.seg[segIdx] || 1;
    const t = (bus.progress - acc) / segLen;
    const aIdx = segIdx % path.length;
    const bIdx = (segIdx + 1) % path.length;
    const A = toPx(path[aIdx]);
    const B = toPx(path[bIdx]);
    const nx = A.x + (B.x - A.x) * t;
    const ny = A.y + (B.y - A.y) * t;

    if (atDepot(nx, ny)) {
      bus.state = "depot";
      bus.dwell = DEPOT_DWELL_SEC;
      return;
    }
    const st = stationAtPoint(nx, ny);
    if (st) {
      unloadLoad(bus, st);
      bus.state = "station";
      bus.dwell = BOARDING_DWELL_SEC;
      return;
    }
    bus.state = "moving";
  }

  // === Ticking and frame loop ===
  function tickOnce() {
    if (gameOver) return;
    ticks += 1;
    spawnPassengerOne();
    if (ticks % NEW_STATION_EVERY_SEC === 0) createRandomStation();
  }

  function updateFrame(dt) {
    tickAccum += dt * tickSpeed;
    if (!paused && tickAccum >= 1) {
      tickOnce();
      tickAccum -= 1;
      if (tickAccum > 1) tickAccum = 0; // drop extras to avoid burst after throttle
    }
    if (!paused) {
      for (const id of Object.keys(buses)) updateBus(buses[id], dt * tickSpeed);
    }
  }

  function loop(ts) {
    if (!lastTime) lastTime = ts;
    const ms = ts - lastTime;
    lastTime = ts;
    updateFrame(ms / 1000);
    requestAnimationFrame(loop);
  }

  // === Sizing ===
  function recalcSize() {
    if (!gameEl) return;
    const w = Math.max(320, Math.floor(gameEl.getBoundingClientRect().width));
    width = w;
    height = Math.floor(w / ASPECT);
    // depot remains at 0.5,0.5 (normalized), so it's centered visually
  }

  let resizeObs;
  onMount(() => {
    resetGame();
    recalcSize();
    resizeObs = new ResizeObserver(recalcSize);
    resizeObs.observe(containerEl);
    requestAnimationFrame(loop);
    return () => resizeObs?.disconnect();
  });

  // === Builder ===
  function toggleBuildMode() {
    building = { active: true, started: false, stopIds: [], error: null };
    buildMode = true;
  }

  // Robust SVG click → viewBox coords (fixes depot detection)
  function svgClickToViewBox(svg, e) {
    const rect = svg.getBoundingClientRect();
    const sx = width / rect.width;
    const sy = height / rect.height;
    const x = (e.clientX - rect.left) * sx;
    const y = (e.clientY - rect.top) * sy;
    return { x, y };
  }

  function clickSvg(e) {
    if (!buildMode) return;
    const svg = e.currentTarget;
    const clicked = svgClickToViewBox(svg, e);

    const dpx = toPx(depot);
    const depotHit =
      Math.abs(clicked.x - dpx.x) <= DEPOT_SIZE / 2 &&
      Math.abs(clicked.y - dpx.y) <= DEPOT_SIZE / 2;

    if (!building.started) {
      if (depotHit) {
        building.started = true;
        building.error = null;
      } else building.error = "Click the Depot to start the route.";
      return;
    }

    if (depotHit) {
      if (building.stopIds.length >= 2) {
        const r = buildRouteFromStopIds(building.stopIds);
        if (r) {
          routes = [...routes, r];
          building = {
            active: false,
            started: false,
            stopIds: [],
            error: null,
          };
          buildMode = false;
        } else
          building.error = "Invalid route. 2+ unique stations; no duplicates.";
      } else
        building.error = "Pick at least 2 unique stations before finishing.";
      return;
    }

    // station click
    let clickedStation = null;
    for (const s of stations) {
      const sp = toPx(s);
      if (
        Math.hypot(sp.x - clicked.x, sp.y - clicked.y) <=
        STATION_RADIUS + 6
      ) {
        clickedStation = s;
        break;
      }
    }
    if (clickedStation) {
      if (building.stopIds.includes(clickedStation.id)) {
        building.error = "A route can visit each station only once.";
        return;
      }
      building.stopIds = [...building.stopIds, clickedStation.id];
      building.error = null;
    }
  }

  $: buildingPathD =
    buildMode && building.started && building.stopIds.length
      ? smoothPathD([
          depot,
          ...building.stopIds.map((id) => stations.find((s) => s.id === id)),
          depot,
        ])
      : "";

  $: stationQueues = stations.map((s) => ({
    id: s.id,
    color: s.color,
    count: (passengers[s.id] || []).length,
  }));

  function handleControls(event) {
    const { type, detail } = event;
    if (type === "togglePause") paused = !paused;
    if (type === "build") toggleBuildMode();
    if (type === "speed") tickSpeed = detail.value;
    if (type === "restart") resetGame();
  }

  function deleteRoute(event) {
    deleteRouteById(event.detail.id);
  }
  function assignRoute(event) {
    assignBuses(event.detail.routeId, event.detail.typeId, event.detail.count);
  }
</script>

<div class={`wrap ${className}`} bind:this={containerEl}>
  <div class="game" bind:this={gameEl}>
    <svg
      viewBox={`0 0 ${width} ${height}`}
      on:click={clickSvg}
      preserveAspectRatio="xMidYMid meet"
      style="width:100%; height:auto; aspect-ratio: 16 / 9; background: radial-gradient(1200px 600px at 50% 40%, #10131c, #080a0f 70%);"
    >
      {#if buildMode && building.started && building.stopIds.length}
        <path
          d={buildingPathD}
          stroke="#5dade2"
          stroke-width="3"
          fill="none"
          stroke-dasharray="6 6"
          opacity="0.8"
        />
      {/if}

      {#each routes as r (r.id)}
        <path
          d={smoothPathD(r.pathPoints)}
          stroke="#6c7bd9"
          stroke-width="3.5"
          fill="none"
          opacity="0.9"
        />
      {/each}

      {#if depot}
        {@const d = toPx(depot)}
        <rect
          x={d.x - DEPOT_SIZE / 2}
          y={d.y - DEPOT_SIZE / 2}
          width={DEPOT_SIZE}
          height={DEPOT_SIZE}
          fill="#f7dc6f"
          stroke="#c39b09"
          stroke-width="2"
          rx="4"
          ry="4"
        />
      {/if}

      {#each stations as s (s.id)}
        {@const p = toPx(s)}
        <g>
          <circle
            cx={p.x}
            cy={p.y}
            r={STATION_RADIUS}
            fill={s.color}
            stroke="#1b1f2a"
            stroke-width="3"
          />
          {#if (passengers[s.id] || []).length}
            {#each passengers[s.id].slice(0, 12) as psg, i}
              <polygon
                points={`${p.x + 18 + (i % 6) * 8},${p.y - 20 - Math.floor(i / 6) * 14} ${p.x + 14 + (i % 6) * 8},${p.y - 12 - Math.floor(i / 6) * 14} ${p.x + 22 + (i % 6) * 8},${p.y - 12 - Math.floor(i / 6) * 14}`}
                fill={psg.color}
                stroke="#0b0c10"
                stroke-width="1.5"
                opacity="0.95"
              />
            {/each}
          {/if}
        </g>
      {/each}

      {#each Object.values(buses) as bus (bus.id)}
        {#if routes.find((r) => r.id === bus.routeId)}
          {@const path = R.sampled}
          {@const pos = (() => {
            if (!R.seg || R.seg.length === 0 || bus.progress == null)
              return toPx(path[0]);
            let acc = 0,
              segIdx = 0,
              progress = bus.progress % (R.totalLen || 1);
            while (segIdx < R.seg.length && acc + R.seg[segIdx] < progress)
              acc += R.seg[segIdx++];
            const segLen = R.seg[segIdx] || 1;
            const t = (progress - acc) / segLen;
            const aIdx = segIdx % path.length;
            const bIdx = (segIdx + 1) % path.length;
            const A = toPx(path[aIdx]);
            const B = toPx(path[bIdx]);
            return { x: A.x + (B.x - A.x) * t, y: A.y + (B.y - A.y) * t };
          })()}
          <g transform={`translate(${pos.x},${pos.y})`}>
            <rect
              x="-8"
              y="-6"
              width="16"
              height="12"
              fill={bus.typeId === "fast"
                ? "#48c9b0"
                : bus.typeId === "large"
                  ? "#af7ac5"
                  : "#85c1e9"}
              stroke="#11151f"
              stroke-width="2"
              rx="3"
              ry="3"
            />
            <text
              x="0"
              y="-10"
              text-anchor="middle"
              font-size="9"
              fill="#aab6d3"
            >
              {bus.carried.length}/{bus.cap}
            </text>
          </g>
        {/if}
      {/each}
    </svg>

    <div class="hud">
      <div><strong>Ticks:</strong> {ticks}</div>
      <div><strong>Stations:</strong> {stations.length}</div>
      <div><strong>Routes:</strong> {routes.length}</div>
      <div>
        <strong>Passengers waiting:</strong>
        {stationQueues.reduce((a, b) => a + b.count, 0)}
      </div>
    </div>

    {#if gameOver}
      <div class="gameover">
        <div class="card">
          <h3>Game Over</h3>
          <p>
            A station exceeded {PASSENGER_OVERFLOW_LIMIT} waiting passengers.
          </p>
          <button class="btn" on:click={resetGame}>Restart</button>
        </div>
      </div>
    {/if}
  </div>

  <div class="panel">
    <Controls
      {paused}
      {tickSpeed}
      on:togglePause={handleControls}
      on:build={handleControls}
      on:speed={handleControls}
      on:restart={handleControls}
    />
    {#if buildMode}
      <div class="routeBox">
        <strong>Build a Route</strong>
        <ol>
          <li><b>Click Depot</b> to start.</li>
          <li>Click <b>2+ unique stations</b>.</li>
          <li><b>Click Depot</b> again to finish.</li>
        </ol>
        <div style="opacity:.85">
          State: <b
            >{building.started
              ? "Selecting stations…"
              : "Waiting for Depot click"}</b
          >
        </div>
        {#if building.error}<div style="color:#f1948a">
            {building.error}
          </div>{/if}
      </div>
    {/if}
    <RouteList
      {routes}
      {stations}
      {BUS_TYPES}
      on:delete={deleteRoute}
      on:assign={assignRoute}
    />
    <StationQueues {stations} {passengers} />
  </div>
</div>

<style lang="css">
  .wrap {
    display: grid;
    grid-template-rows: 1fr auto;
    height: 100%;
  }
  .game {
    position: relative;
    width: 100%;
  }
  .panel {
    padding: 12px 16px;
    background: #0b0c10;
    border-top: 1px solid #1f2430;
    display: grid;
    gap: 10px;
  }
  svg {
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 16 / 9;
  }
  .hud {
    position: absolute;
    right: 10px;
    top: 10px;
    background: rgba(15, 18, 25, 0.65);
    border: 1px solid #2b3242;
    padding: 8px 10px;
    border-radius: 10px;
    font-size: 13px;
  }
  .btn {
    background: #1f2430;
    border: 1px solid #31394a;
    color: #e9eef6;
    padding: 8px 12px;
    border-radius: 10px;
    cursor: pointer;
  }
  .gameover {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    background: rgba(8, 10, 14, 0.6);
    backdrop-filter: blur(2px);
    z-index: 10;
  }
  .card {
    background: #141824;
    border: 1px solid #2b3242;
    border-radius: 16px;
    padding: 18px;
    min-width: 260px;
    text-align: center;
  }
  .routeBox {
    border: 1px solid #2b3242;
    border-radius: 12px;
    padding: 10px;
    background: #12131a;
  }
</style>
