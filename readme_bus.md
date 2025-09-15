✅ Finalized Requirements (as implemented)

Rendering: Simple SVG only; responsive, mobile-friendly.

Stations: Start with 5 stations, each has a unique color. More stations spawn over time.

Minimum spacing: Each new station is at least ~20% of screen width away from other stations & depot.

Depot: Exactly one depot, rendered as a square in the visual center; all routes start & end here.

Route building: Click Depot → 2+ unique stations → Depot to create a route.

No edit, only delete: You can delete a route; to change it, recreate it.

Single-visit rule: A route can visit each station at most once.

Route configuration: Per-route assignment of multiple bus types & counts.

Bus types (3):

Standard: medium capacity, medium speed

Fast (low cap): high speed, low capacity

Large (slow): high capacity, lower speed

Passengers: Spawn at stations, rendered as triangles; triangle color = destination station color.

Spawn cadence: Exactly 1 passenger per tick (tick = 1 second at 1× speed).

Distribution: Uniform random station selection (configurable later).

Loading/unloading: Buses unload at their passenger’s destination; load only passengers whose destination is on that bus’s route.

Bus loop behavior: Buses loop along the route; when reaching the depot they refuel (dwell) then continue.

Overflow lose condition: If any station’s queue exceeds 20, it’s Game Over.

Collisions: Ignored; buses can pass through each other.

Controls: Pause/Resume, speed slider (default 1×), Restart.

Curves: Routes are drawn as smooth curves (Catmull-Rom → cubic Bézier).

Performance: Responsive SVG with a fixed 16:9 aspect; depot click and station clicks are mapped precisely to the viewBox.

Storage: None; levels are randomly generated each play.

🧭 Current Behavior & Key Implementation Notes

Responsive board: SVG uses aspect-ratio: 16/9; width: 100%; height: auto; with viewBox driven by the container width. This keeps the depot truly centered at normalized (0.5, 0.5) and prevents container “creep” height.

Station clamping: Stations spawn fully inside the visible area with a safe margin so no nodes are clipped.

Route builder UX: Requires clicking Depot to start, then 2+ unique stations, then Depot again to finish. Live dashed preview curve while building.

Precise clicks: Depot & station hits are detected using a viewBox-mapped coordinate conversion (no CTM issues), so clicking works across devices and DPI.

Ticking: We process at most 1 tick per animation frame. If a tab lags, extra ticks are dropped rather than processed in a burst → ensures 1 spawn per tick visually & logically.

Buses:

Move by distance along a cached polyline (evenly spaced), not by index hops.

Can mix multiple bus types per route (assign counts in the route panel).

Dwell times at stations (boarding) and at depot (refuel) are respected.

HUD: Top-right overlay shows Ticks, Stations, Routes, and Total passengers waiting.

Delete route: Removes its buses and path; you can rebuild any time.

🧩 Config Knobs (in Game.svelte)
const INITIAL_STATIONS = 5;
const PASSENGER_OVERFLOW_LIMIT = 20; // lose when any station > this
const MIN_DIST_RATIO = 0.20;         // station spacing ~20% of screen width
const NEW_STATION_EVERY_SEC = 45;    // add a station every 45 ticks
const STATION_RADIUS = 10;
const DEPOT_SIZE = 18;
const BOARDING_DWELL_SEC = 1;        // station dwell
const DEPOT_DWELL_SEC = 3;           // refuel dwell
const ASPECT = 16 / 9;               // board aspect ratio


Bus types:

Type	id	Capacity	Speed (px/s baseline)
Standard	standard	10	110
Fast (low cap)	fast	6	160
Large (slow)	large	18	80

Speeds are tuned for smooth motion at typical container sizes; tweak as desired.

🗂️ Project Structure (current)
src/
  components/
    bus-game/
      Controls.svelte        # Pause/Resume, Build, Speed slider, Restart
      RouteList.svelte       # Per-route bus assignments & Delete
      StationQueues.svelte   # Queue counts per station (chips)
      Game.svelte            # Main game logic + SVG rendering (this is the page UI)
  pages/
    bus-game.astro           # Example Astro page that mounts <Game />


Each Svelte file uses <style lang="css">.

Game.svelte owns the simulation loop, state, route building, tick logic, bus movement, and HUD.

RouteList dispatches assign and delete events to Game.svelte.

▶️ How to Run (Astro)

Enable Svelte in Astro:

npm i -D @astrojs/svelte svelte


astro.config.mjs:

import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
export default defineConfig({ integrations: [svelte()] });


Place files as per the structure above.

Start dev server:

npm run dev


Open /bus-game.

🕹️ How to Play

Click Build Route.

Click the Depot square to start.

Click 2 or more station circles (each only once).

Click Depot again to finish.

In the route’s card, assign buses (any mix of the 3 types).

Watch buses loop, loading/unloading passengers.

Don’t let any station’s queue exceed 20!

Controls: Pause/Resume, speed slider (default 1×), and Restart.

🛠️ Notable Fixes Included

Depot click detection fixed using viewBox-based coordinate mapping.

1 passenger per tick guaranteed (no burst catch-up after throttling).

Station clamping so nodes never spawn off-screen.

Centered depot regardless of container size; 16:9 SVG aspect prevents container expansion.

Removed invalid export const usage in Svelte scripts (props export-only rule).

🧭 Nice-to-Haves / Future Tweaks

Spawn queue with catch-up: If you want time-accurate simulation after tab throttling, we can queue missed spawns but still release 1 per tick visually.

Dynamic difficulty: Increase spawn rate/overflow limit over time.

Multiple depots: Support advanced routing constraints.

Scoring/metrics: Deliveries per minute, average wait time, etc.

Touch affordances: Larger hit areas/tap highlights for mobile.