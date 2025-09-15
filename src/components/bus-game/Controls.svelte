<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  export let paused = false;
  export let tickSpeed = 1;
  const dispatch = createEventDispatcher();
</script>

<div class="controls">
  <button class="btn" on:click={() => dispatch('togglePause')}>
    {paused ? 'Resume' : 'Pause'}
  </button>
  <button class="btn alt" on:click={() => dispatch('build')}>
    Build Route
  </button>
  <label>Speed: {tickSpeed.toFixed(2)}×
    <input type="range" min="0.2" max="4" step="0.1"
      on:input={(e)=>dispatch('speed', { value: parseFloat(e.currentTarget.value) || 1 })}
      value={tickSpeed} />
  </label>
  <button class="btn" on:click={() => dispatch('restart')}>Restart</button>
</div>

<style lang="css">
.controls { display:flex; flex-wrap:wrap; gap:10px; align-items:center; }
.btn {
  background:#1f2430; border:1px solid #31394a; color:#e9eef6;
  padding:8px 12px; border-radius:10px; cursor:pointer;
}
.btn.alt { background:#283047; }
</style>
