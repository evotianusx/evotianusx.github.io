<script>
    import { onMount } from "svelte";

    let folders = [];
    let targetFolder = null;
    let time = 0;
    let timerInterval;
    let found = false;
    let showHint = false;
    let folderCount = 5;
    const MAX_FOLDERS = 50;
    let lives = 3;
    let score = 0;
    let gameOver = false;
    let gameStarted = false;
    let isDragging = false;
    let dragItem = null;
    let startX, startY;
    let dropZone = {
        x: 0,
        y: 0,
        width: 100,
        height: 100,
        visible: false,
    };

    let container;

    function updatePosition() {
        if (container) {
            dropZone.x = container.clientWidth * 0.8 - dropZone.width;
            dropZone.y = container.clientHeight * 0.8 - dropZone.height;
        }
    }

    onMount(() => {
        updatePosition();

        const resizeObserver = new ResizeObserver(updatePosition);
        if (container) resizeObserver.observe(container);

        return () => resizeObserver.disconnect();
    });
    // Departments and labels
    const departments = ["HR", "Finance", "Engineering", "Marketing", "Legal"];
    const labels = [
        "CONFIDENTIAL",
        "Q4 REPORT",
        "INVOICE",
        "URGENT",
        "ARCHIVED",
    ];

    function generateFolders() {
        const newFolders = [];
        const colors = [
            "bg-blue-200",
            "bg-pink-200",
            "bg-green-200",
            "bg-yellow-200",
        ];

        // Scramble positions randomly
        for (let i = 0; i < folderCount; i++) {
            newFolders.push({
                id: i + 1,
                department:
                    departments[Math.floor(Math.random() * departments.length)],
                color: colors[Math.floor(Math.random() * colors.length)],
                label: labels[Math.floor(Math.random() * labels.length)],
                x: Math.random() * 80 + 5, // 5-85%
                y: Math.random() * 70 + 5, // 5-75%
            });
        }
        return newFolders;
    }

    function initGame() {
        gameStarted = true;
        clearInterval(timerInterval);
        found = false;
        showHint = false;
        time = 0;
        folders = generateFolders();
        targetFolder = folders[Math.floor(Math.random() * folders.length)];

        // Position drop zone in bottom-right
        dropZone = {
            x: 475, // 80% from left
            y: 480, // 80% from top
            width: 25,
            height: 15,
            visible: true,
        };

        timerInterval = setInterval(() => time++, 1000);
    }

    // Drag functions
    function startDrag(e, folder) {
        isDragging = true;
        dragItem = folder;

        // Handle both mouse and touch events
        const clientX = e.clientX ?? e.touches[0].clientX;
        const clientY = e.clientY ?? e.touches[0].clientY;

        startX = clientX - folder.x;
        startY = clientY - folder.y;

        // Add non-passive event listeners
        window.addEventListener("mousemove", drag, { passive: false });
        window.addEventListener("mouseup", stopDrag, { passive: true });
        window.addEventListener("touchmove", touchDrag, { passive: false });
        window.addEventListener("touchend", stopDrag, { passive: true });
    }

    function touchDrag(e) {
        if (!isDragging) return;

        // Now we can preventDefault since listener is non-passive
        e.preventDefault();

        drag({
            clientX: e.touches[0].clientX,
            clientY: e.touches[0].clientY,
        });
    }

    function drag(e) {
        if (!isDragging) return;
        dragItem.x = e.clientX - startX;
        dragItem.y = e.clientY - startY;
        folders = folders; // Trigger Svelte reactivity
    }

    function stopDrag() {
        if (!isDragging || !dragItem) return;
        // Get drop zone center and radius
        const dropZoneCenterX = dropZone.x + dropZone.width / 2;
        const dropZoneCenterY = dropZone.y + dropZone.height / 2;
        const dropZoneRadius = Math.min(dropZone.width, dropZone.height) / 2;

        // Get folder center position
        const folderCenterX = dragItem.x + 24; // Half of folder width (48px)
        const folderCenterY = dragItem.y + 28; // Half of folder height (56px)

        // Calculate distance between centers
        const distance = Math.sqrt(
            Math.pow(dropZoneCenterX - folderCenterX, 2) +
                Math.pow(dropZoneCenterY - folderCenterY, 2),
        );

        // Check if folder center is within the circular radius
        const inDropZone = distance <= 300;

        if (inDropZone) {
            if (dragItem.id === targetFolder.id) {
                found = true;
                score++;
                if (folderCount < MAX_FOLDERS) folderCount += 5;
                setTimeout(initGame, 1000);
            } else {
                lives--;
                if (lives <= 0) endGame();
            }
        }

        cleanupDrag();
    }

    function cleanupDrag() {
        isDragging = false;
        dragItem = null;

        // Remove all event listeners
        window.removeEventListener("mousemove", drag);
        window.removeEventListener("mouseup", stopDrag);
        window.removeEventListener("touchmove", touchDrag);
        window.removeEventListener("touchend", stopDrag);
    }

    function giveHint() {
        if (!gameOver) {
            showHint = true;
            time += 5;
            setTimeout(() => (showHint = false), 2000);
        }
    }

    function endGame() {
        gameOver = true;
        clearInterval(timerInterval);
    }

    function restartGame() {
        lives = 3;
        score = 0;
        folderCount = 5;
        gameOver = false;
        initGame();
    }

    onMount(initGame);
</script>

<div class="min-h-screen flex flex-col items-center relative">
    {#if !gameStarted}
        <p class="text-lg">Loading game...</p>
    {:else}
        <!-- Game Over Popup -->
        {#if gameOver}
            <div
                class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
            >
                <div
                    class="bg-white p-8 rounded-lg shadow-xl text-center max-w-md"
                >
                    <h2 class="text-2xl font-bold text-red-600 mb-4">
                        Game Over!
                    </h2>
                    <p class="text-xl mb-2">
                        Your score: <span class="font-bold">{score}</span> correct
                        finds
                    </p>
                    <p class="text-gray-600 mb-6">
                        Max folders reached: {folderCount}
                    </p>
                    <button
                        on:click={restartGame}
                        class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg transition-colors"
                    >
                        Play Again
                    </button>
                </div>
            </div>
        {/if}

        <h1 class="text-3xl font-bold text-gray-800 mb-2">
            Find the Department File!
        </h1>

        <!-- Target -->

        <!-- Scrollable Cabinet Container -->
        <div
            class="min-h-screen bg-gray-100 flex flex-col items-center py-8 relative"
            bind:this={container}
        >
            {#if targetFolder}
                <div class="mb-2 text-center bg-white p-4 rounded-lg shadow">
                    <p class="text-lg">
                        Find:
                        <span class="font-semibold text-indigo-600">
                            {targetFolder.color
                                .replace("bg-", "")
                                .replace("-200", "")}
                            {targetFolder.department} file labeled '{targetFolder.label}'
                        </span>
                    </p>

                    <p class="text-gray-600">
                        Lives:
                        {#each Array(3) as _, i}
                            <span
                                class={`inline-block w-4 h-4 ml-1 rounded-full ${i < lives ? "bg-red-500" : "bg-gray-300"}`}
                            />
                        {/each}
                    </p>
                    {#if found}
                        <div class="mt-6 animate-bounce">
                            <p class="text-2xl font-bold text-green-600">
                                ✓ Found! (+1 point) 🏆 {score}
                            </p>
                        </div>
                    {/if}
                </div>
            {/if}
            <!-- Cabinet Container -->
            <div
                class="relative w-[90vw] max-w-4xl h-[60vh] bg-gray-200 border-2 border-gray-400 rounded-lg mb-6 overflow-hidden"
            >
                <!-- Drop Zone -->
                <div
                    class="absolute rounded-full border-2 border-dashed border-amber-500 bg-amber-100 bg-opacity-30 flex items-center justify-center transition-all drop-zone {isDragging
                        ? 'is-dragging'
                        : ''}"
                    class:bg-amber-200={isDragging}
                    style={`
        left:40%;
        top: 40%;
        width: 15%;
        height: 15%;
        aspect-ratio: 1/1;
      `}
                >
                    <span class="text-xs font-bold text-amber-700"
                        >DROP HERE</span
                    >
                </div>
                <!-- Folders -->
                {#each folders as folder}
                    <!-- svelte-ignore a11y_no_static_element_interactions -->
                    <div
                        class="absolute w-24 h-28 flex flex-col items-center justify-center text-xs font-medium rounded-sm shadow-md transition-transform cursor-move touch-none {folder.color}"
                        style={`left: ${folder.x}px; top: ${folder.y}px`}
                        on:mousedown={(e) => startDrag(e, folder)}
                        on:touchstart={(e) => {
                            e.preventDefault();
                            startDrag(e, folder);
                        }}
                        touch-action="none"
                    >
                        <span class="font-bold">{folder.department}</span>
                        <span class="text-[0.6rem] mt-1 px-1 text-center"
                            >{folder.label}</span
                        >
                    </div>
                {/each}
            </div>
        </div>

        <!-- Game UI -->
    {/if}
</div>

<style>
    /* Base styles */
    .drop-zone {
        position: absolute;
        transition: all 0.3s ease;
        transform: scale(1);
    }

    /* Mobile styles (applied by default) */
    .drop-zone {
        left: 80% !important;
        top: 80% !important;
    }

    /* Desktop override (applies on screens ≥ 768px) */
    @media (min-width: 768px) {
        .drop-zone {
            left: 40% !important;
            top: 40% !important;
        }
    }

    /* Dragging state - grow and pulse animation */
    .drop-zone.is-dragging {
        transform: scale(1.1);
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% {
            transform: scale(1.1);
        }
        50% {
            transform: scale(1.15);
        }
        100% {
            transform: scale(1.1);
        }
    }
</style>
