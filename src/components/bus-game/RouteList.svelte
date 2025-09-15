<script lang="ts">
  import { createEventDispatcher } from "svelte";
  export let routes = [];
  export let stations = [];
  export let BUS_TYPES = [];
  const dispatch = createEventDispatcher();

  const stationById = (id) => stations.find((s) => s.id === id);
</script>

<div class="routes">
  {#each routes as r (r.id)}
    <div class="routeBox">
      <div class="row">
        <div style="display:flex; gap:8px; align-items:center;">
          <strong>{r.name}</strong>
          {#if (r.buses?.length || 0) === 0}
            <span class="badge">No buses assigned</span>
          {/if}
        </div>
        <button
          class="btn danger"
          on:click={() => dispatch("delete", { id: r.id })}>Delete</button
        >
      </div>
      <div class="routeStops">
        <span class="chip">Depot</span>
        {#each r.stops as sid}
          {#if stationById(sid) as S}
            <span class="chip" style="border-color:{S.color}; color:{S.color}"
              >{sid.slice(0, 4)}</span
            >
          {/if}
        {/each}
        <span class="chip">Depot</span>
      </div>
      <div class="assignRow">
        {#each BUS_TYPES as T}
          <label
            >{T.label}
            <input
              type="number"
              min="0"
              value={r.assignments[T.id] ?? 0}
              on:change={(e) =>
                dispatch("assign", {
                  routeId: r.id,
                  typeId: T.id,
                  count: Math.max(
                    0,
                    parseInt(e.currentTarget.value || "0", 10),
                  ),
                })}
            />
          </label>
        {/each}
      </div>
    </div>
  {/each}
</div>

<style lang="css">
  .routes {
    display: grid;
    gap: 8px;
  }
  .routeBox {
    border: 1px solid #2b3242;
    border-radius: 12px;
    padding: 10px;
    background: #12131a;
  }
  .row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }
  .routeStops {
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
    margin-top: 6px;
  }
  .assignRow {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
    margin-top: 8px;
  }
  .assignRow input {
    width: 64px;
    background: #0f1118;
    border: 1px solid #2b3242;
    color: #e9eef6;
    padding: 4px 6px;
    border-radius: 8px;
  }
  .btn {
    background: #1f2430;
    border: 1px solid #31394a;
    color: #e9eef6;
    padding: 6px 10px;
    border-radius: 10px;
    cursor: pointer;
  }
  .btn.danger {
    background: #5a2230;
    border-color: #7d2a3b;
  }
  .chip {
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid #2b3242;
  }
  .badge {
    font-size: 12px;
    opacity: 0.8;
  }
</style>
