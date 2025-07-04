<script>
    let initialCount = 0;
    let count = $state(initialCount);

    function increment() {
        console.log("CLICKK")
        count += 1;
    }
</script>

<button onclick={increment}>
    Clicks: {count}
</button>

<style>
    button {
        font-family: inherit;
        font-size: inherit;
        padding: 1em 2em;
        color: #ff3e00;
        background-color: rgba(255, 62, 0, 0.1);
        border-radius: 2em;
        border: 2px solid #ff3e00;
        outline: none;
        width: 200px;
        font-variant-numeric: tabular-nums;
    }

    button:hover {
        border: 2px solid #ff3e00;
        background-color: rgba(255, 62, 0, 0.2);
    }
</style>
