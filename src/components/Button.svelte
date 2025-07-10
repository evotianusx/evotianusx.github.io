<script lang="ts">
    export let type: "button" | "submit" | "reset" = "button";
    export let disabled = false;
    export let variant: "primary" | "secondary" | "ghost" = "primary";
</script>

<button
    {type}
    {disabled}
    class="rounded-md px-4 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none
  {variant === 'primary'
        ? 'bg-[var(--sl-color-accent)] text-[var(--sl-color-white)] hover:bg-[var(--sl-color-accent-high)] dark:hover:bg-[var(--sl-color-accent-low)] focus-visible:ring-[var(--sl-color-accent)]'
        : variant === 'secondary'
          ? 'bg-[var(--sl-color-gray-6)] text-[var(--sl-color-white)] hover:bg-[var(--sl-color-gray-5)] dark:bg-[var(--sl-color-gray-1)] dark:text-[var(--sl-color-black)] dark:hover:bg-[var(--sl-color-gray-2)] focus-visible:ring-[var(--sl-color-gray-4)]'
          : 'text-[var(--sl-color-black)] hover:bg-[var(--sl-color-gray-6)] dark:text-[var(--sl-color-white)] dark:hover:bg-[var(--sl-color-gray-5)] focus-visible:ring-[var(--sl-color-gray-4)]'}"
    {...$$restProps}
>
    <slot />
</button>

<style global>
    /* This ensures dark mode transitions are smooth */
    :root {
        color-scheme: light dark;
        transition:
            background-color 0.2s ease,
            color 0.2s ease;
    }
    
    /* Add ring offset color that matches the background */
    :root, :root[data-theme='light'] {
        --tw-ring-offset-color: var(--sl-color-gray-7);
    }
    :root[data-theme='dark'] {
        --tw-ring-offset-color: var(--sl-color-gray-6);
    }
</style>