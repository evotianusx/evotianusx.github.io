<script lang="ts">
  export let stations = [];
  export let passengers = {};
</script>

<div class="routeBox">
  <strong>Station Queues</strong>
  <div class="chips">
    {#each stations as S}
      <span class="chip" title={`Station ${S.id}`} style="border-color:{S.color};">{(passengers[S.id]||[]).length}</span>
    {/each}
  </div>
</div>

<style lang="css">
.routeBox { border:1px solid #2b3242; border-radius:12px; padding:10px; background:#12131a; }
.chips { display:flex; flex-wrap:wrap; gap:8px; margin-top:6px; }
.chip { padding:2px 8px; border-radius:999px; border:1px solid #2b3242; }
</style>
