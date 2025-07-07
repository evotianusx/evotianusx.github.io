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
        ? 'bg-indigo-600 text-white hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 focus-visible:ring-indigo-500'
        : variant === 'secondary'
          ? 'bg-gray-100 text-gray-900 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600 focus-visible:ring-gray-500'
          : 'text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 focus-visible:ring-gray-500'}"
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
</style>
