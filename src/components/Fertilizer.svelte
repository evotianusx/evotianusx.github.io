<script lang="ts">
    import { onMount } from "svelte";
    import FertilizerData from "./fertilizer.json";

    interface Fertilizer {
        id: number;
        name: string;
        N?: number;
        P2O5?: number;
        K2O?: number;
        CaO?: number;
        B?: number;
        Mn?: number;
        Zn?: number;
        Fe?: number;
        note: string;
    }

    // User inputs
    let fruitYield = 100; // kg fruit per tree
    let applications = 4;

    // Fertilizer data
    let allFertilizers: Fertilizer[] = [];
    let selectedFertilizerIds: number[] = [];

    // Calculations
    let nutrientNeeds: Record<string, number> = {};
    let fertilizerDoses: Record<string, Record<string, number>> = {};
    let fertilizerTotalWeights: Record<string, number> = {}; // Total weight per fertilizer per year
    let fertilizerApplicationWeights: Record<string, number> = {}; // Weight per fertilizer per application
    let nutrientSupply: Record<string, number> = {};
    let insufficientNutrients: string[] = [];
    let suggestions: string[] = [];

    // Nutrient requirements (g/kg fruit)
    const nutrientRequirements = {
        N: 1.75,
        P2O5: 2.29,
        K2O: 3.615,
        CaO: 4.65,
        B: 0.075,
        Mn: 0.03,
        Zn: 0.0225,
        Fe: 0.035,
    };

    // Efficiency of nutrient uptake (%)
    const efficiency = {
        N: 0.4,
        P2O5: 0.2,
        K2O: 0.6,
        CaO: 0.6,
        B: 0.3,
        Mn: 0.3,
        Zn: 0.3,
        Fe: 0.3,
    };

    // Toggle fertilizer selection
    function toggleFertilizer(id: number) {
        if (selectedFertilizerIds.includes(id)) {
            selectedFertilizerIds = selectedFertilizerIds.filter(
                (fId) => fId !== id,
            );
        } else {
            selectedFertilizerIds = [...selectedFertilizerIds, id];
        }
        calculateFertilizerPlan();
    }

    // Calculate nutrient needs based on fruit yield
    function calculateNutrientNeeds(yieldKg: number): Record<string, number> {
        const needs: Record<string, number> = {};
        for (const nutrient in nutrientRequirements) {
            const req =
                nutrientRequirements[
                    nutrient as keyof typeof nutrientRequirements
                ];
            const eff = efficiency[nutrient as keyof typeof efficiency];
            needs[nutrient] = (req * yieldKg) / eff / 1000; // Convert g to kg
        }
        return needs;
    }

    // Calculate fertilizer doses and total nutrient supply
    function calculateFertilizerPlan() {
        // Reset previous calculations
        nutrientSupply = {};
        insufficientNutrients = [];
        suggestions = [];
        fertilizerTotalWeights = {};
        fertilizerApplicationWeights = {};

        // Calculate nutrient needs
        nutrientNeeds = calculateNutrientNeeds(fruitYield);

        // Get selected fertilizers
        const selectedFertilizers = allFertilizers.filter((f) =>
            selectedFertilizerIds.includes(f.id),
        );

        // Calculate doses
        fertilizerDoses = {};
        const tempSupply: Record<string, number> = {};

        selectedFertilizers.forEach((fert) => {
            fertilizerDoses[fert.name] = {};
            let totalWeightForThisFertilizer = 0; // kg per year

            for (const nutrient in nutrientNeeds) {
                const content = fert[nutrient as keyof Fertilizer];
                if (typeof content === "number" && content > 0) {
                    const doseKg = nutrientNeeds[nutrient] / (content / 100);
                    const dosePerApp = (doseKg * 1000) / applications;
                    fertilizerDoses[fert.name][nutrient] = parseFloat(
                        dosePerApp.toFixed(2),
                    );

                    // Add to total weight for this fertilizer
                    totalWeightForThisFertilizer += doseKg;

                    // Track total nutrient supply
                    if (!tempSupply[nutrient]) tempSupply[nutrient] = 0;
                    tempSupply[nutrient] += nutrientNeeds[nutrient];
                }
            }

            // Store total weight and per application weight
            fertilizerTotalWeights[fert.name] = parseFloat(
                totalWeightForThisFertilizer.toFixed(3),
            );
            fertilizerApplicationWeights[fert.name] = parseFloat(
                (totalWeightForThisFertilizer / applications).toFixed(3),
            );
        });

        nutrientSupply = tempSupply;

        // Check for insufficient nutrients
        for (const nutrient in nutrientNeeds) {
            const supplied = nutrientSupply[nutrient] || 0;
            const needed = nutrientNeeds[nutrient];

            if (supplied < needed * 0.9) {
                // Less than 90% of need
                insufficientNutrients.push(nutrient);
            }
        }

        // Generate suggestions
        if (insufficientNutrients.length > 0) {
            suggestions.push(
                `⚠️ Insufficient supply for: ${insufficientNutrients.join(", ")}`,
            );
            suggestions.push(
                "💡 Consider adding fertilizers containing these nutrients:",
            );

            // Suggest fertilizers that contain the missing nutrients
            const missingSet = new Set(insufficientNutrients);
            const suggestedFerts = allFertilizers.filter((fert) => {
                return (
                    !selectedFertilizerIds.includes(fert.id) &&
                    Object.keys(fert).some(
                        (key) =>
                            missingSet.has(key) &&
                            typeof fert[key as keyof Fertilizer] === "number" &&
                            (fert[key as keyof Fertilizer] as number) > 0,
                    )
                );
            });

            if (suggestedFerts.length > 0) {
                suggestedFerts.slice(0, 3).forEach((fert) => {
                    suggestions.push(
                        `  • ${fert.name} (contains: ${Object.keys(fert)
                            .filter(
                                (k) =>
                                    missingSet.has(k) &&
                                    typeof fert[k as keyof Fertilizer] ===
                                        "number" &&
                                    (fert[k as keyof Fertilizer] as number) > 0,
                            )
                            .join(", ")})`,
                    );
                });
            } else {
                suggestions.push(
                    "  • No specific fertilizers found. Consider custom NPK or micronutrient supplements.",
                );
            }
        }
    }

    // Initialize data
    onMount(() => {
        allFertilizers = FertilizerData.map((item: any) => ({
            id: item.id,
            name: item.name,
            N: parseFloat(item.N) || 0,
            P2O5: parseFloat(item.P2O5) || 0,
            K2O: parseFloat(item.K2O) || 0,
            CaO: parseFloat(item.CaO) || 0,
            B: parseFloat(item.B) || 0,
            Mn: parseFloat(item.Mn) || 0,
            Zn: parseFloat(item.Zn) || 0,
            Fe: parseFloat(item.Fe) || 0,
            note: item.note || "",
        }));

        // Select first 2 fertilizers by default
        selectedFertilizerIds = allFertilizers.slice(0, 2).map((f) => f.id);
        calculateFertilizerPlan();
    });
</script>

<div class="container">
    <h1>Fertilizer Calculator</h1>

    <!-- User Inputs -->
    <div class="input-section">
        <h2>Input Parameters</h2>
        <div class="input-group">
            <label>Fruit Yield (kg/tree/year):</label>
            <input type="number" bind:value={fruitYield} min="1" step="1" />
        </div>

        <div class="input-group">
            <label>Number of Applications per Year:</label>
            <input type="number" bind:value={applications} min="1" max="12" />
        </div>
    </div>

    <!-- Fertilizer Selection with Chips -->
    <div class="fertilizer-selection">
        <h2>Select Fertilizers</h2>
        <div class="chip-container">
            {#each allFertilizers as fert (fert.id)}
                <button
                    class="chip {selectedFertilizerIds.includes(fert.id)
                        ? 'selected'
                        : ''}"
                    on:click={() => toggleFertilizer(fert.id)}
                    title={fert.note || ""}
                >
                    {fert.name}
                    {#if fert.note}
                        <span class="chip-note"> ({fert.note})</span>
                    {/if}
                </button>
            {/each}
        </div>
    </div>

    <!-- Results -->
    <div class="results">
        <h2>Nutrient Needs (kg/tree/year)</h2>
        <div class="nutrient-grid">
            {#each Object.entries(nutrientNeeds) as [nutrient, need]}
                <div class="nutrient-item">
                    <strong>{nutrient}:</strong>
                    {(need * fruitYield).toFixed(3)} kg
                </div>
            {/each}
        </div>

        <h2>Fertilizer Plan</h2>
        {#if Object.keys(fertilizerDoses).length === 0}
            <p>No fertilizers selected</p>
        {:else}
            {#each Object.entries(fertilizerDoses) as [fertName, doses]}
                <div class="fertilizer-plan">
                    <h3>{fertName}</h3>
                    <div class="fertilizer-summary">
                        <div class="summary-item">
                            <strong>Total Weight Needed:</strong>
                            {fertilizerTotalWeights[fertName] || 0} kg/year
                        </div>
                        <div class="summary-item">
                            <strong>Per Application:</strong>
                            {fertilizerApplicationWeights[fertName] || 0} kg/application
                        </div>
                    </div>
                    <div class="dose-details">
                        <strong>Breakdown by Nutrient (g/application):</strong>
                        <div class="dose-grid">
                            {#each Object.entries(doses) as [nutrient, dose]}
                                <div class="dose-item">
                                    {nutrient}: {dose} g
                                </div>
                            {/each}
                        </div>
                    </div>
                </div>
            {/each}
        {/if}

        <!-- Warnings and Suggestions -->
        {#if insufficientNutrients.length > 0}
            <div class="warning">
                <h3>⚠️ Insufficient Nutrient Supply</h3>
                <ul>
                    {#each suggestions as suggestion}
                        <li>{suggestion}</li>
                    {/each}
                </ul>
            </div>
        {/if}
    </div>
</div>

<style>
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        font-family: Arial, sans-serif;
    }

    .input-section,
    .fertilizer-selection,
    .results {
        margin-bottom: 30px;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
    }

    .input-group {
        margin-bottom: 15px;
    }

    .input-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }

    .input-group input {
        width: 200px;
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 15px;
    }

    .chip {
        padding: 10px 15px;
        border: 2px solid #e0e0e0;
        border-radius: 20px;
        background-color: #f5f5f5;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 14px;
        text-align: left;
    }

    .chip:hover {
        border-color: #007bff;
        background-color: #e3f2fd;
    }

    .chip.selected {
        background-color: #007bff;
        color: white;
        border-color: #0056b3;
    }

    .chip-note {
        font-size: 12px;
        opacity: 0.8;
    }

    .nutrient-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 10px;
        margin-top: 10px;
    }

    .nutrient-item {
        padding: 12px;
        background-color: #e3f2fd;
        border-radius: 6px;
        font-size: 0.95em;
        border: 1px solid #bbdefb;
    }

    .fertilizer-plan {
        margin-bottom: 25px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #fafafa;
    }

    .fertilizer-summary {
        display: flex;
        gap: 20px;
        margin: 10px 0;
        flex-wrap: wrap;
    }

    .summary-item {
        background-color: #e8f5e9;
        padding: 8px 12px;
        border-radius: 4px;
        border: 1px solid #c8e6c9;
    }

    .dose-details {
        margin-top: 15px;
    }

    .dose-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 8px;
        margin-top: 8px;
    }

    .dose-item {
        padding: 6px 10px;
        background-color: #f5f5f5;
        border-radius: 4px;
        font-size: 0.9em;
        border: 1px solid #e0e0e0;
    }

    .warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 4px;
        padding: 15px;
        margin-top: 20px;
    }

    .warning h3 {
        margin-top: 0;
        color: #856404;
    }

    .warning ul {
        margin-bottom: 0;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .chip-container {
            gap: 8px;
        }

        .chip {
            padding: 8px 12px;
            font-size: 13px;
        }

        .nutrient-grid {
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        }

        .fertilizer-summary {
            flex-direction: column;
            gap: 8px;
        }

        .dose-grid {
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        }
    }
</style>
