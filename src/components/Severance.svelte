<script>
    import { onMount } from "svelte";

    let income = 0;
    let displayedIncome = "";
    let taxBreakdown = [];
    let totalTax = 0;
    let effectiveRate = 0;
    let inputElement;

    const taxBrackets = [
        { min: 0, max: 50000000, rate: 0 },
        { min: 50000000, max: 100000000, rate: 0.05 },
        { min: 100000000, max: 500000000, rate: 0.15 },
        { min: 500000000, max: Infinity, rate: 0.25 },
    ];

    onMount(() => {
        updateDisplayedIncome();
    });

    function updateDisplayedIncome() {
        displayedIncome = formatCurrencyForInput(income);
    }

    function handleInput(event) {
        const rawValue = event.target.value.replace(/\D/g, "");
        income = rawValue ? parseInt(rawValue, 10) : 0;
        displayedIncome = formatCurrencyForInput(income);
        calculateTax();
    }

    function handleBlur() {
        updateDisplayedIncome();
    }

    function calculateTax() {
        let remainingIncome = income;
        totalTax = 0;
        taxBreakdown = [];

        for (let i = 0; i < taxBrackets.length; i++) {
            const bracket = taxBrackets[i];
            const bracketMax =
                bracket.max === Infinity ? Infinity : bracket.max;
            const taxableInBracket = Math.max(
                0,
                Math.min(remainingIncome, bracketMax - bracket.min),
            );

            if (taxableInBracket <= 0) continue;

            const taxInBracket = taxableInBracket * bracket.rate;
            totalTax += taxInBracket;

            taxBreakdown.push({
                range: formatRange(bracket.min, bracketMax),
                rate: bracket.rate * 100,
                taxableAmount: taxableInBracket,
                tax: taxInBracket,
            });

            if (bracket.max === Infinity) break;
            remainingIncome -= taxableInBracket;
        }

        effectiveRate = income > 0 ? (totalTax / income) * 100 : 0;
    }

    function formatRange(min, max) {
        const minStr = formatCurrency(min);
        if (max === Infinity) return `${minStr}+`;
        return `${minStr} – ${formatCurrency(max)}`;
    }

    function formatCurrency(value) {
        return new Intl.NumberFormat("id-ID", {
            style: "currency",
            currency: "IDR",
            minimumFractionDigits: 0,
            maximumFractionDigits: 0,
        }).format(value);
    }

    function formatCurrencyForInput(value) {
        return new Intl.NumberFormat("id-ID").format(value);
    }
</script>

<div class="tax-calculator">
    <h2>Indonesian Pesangon Tax Calculator</h2>

    <div class="input-group">
        <label for="income">Gross Pesangon (Rp):</label>
        <input
            id="income"
            type="text"
            bind:value={displayedIncome}
            on:input={handleInput}
            on:blur={handleBlur}
            placeholder="Enter total income"
            autocomplete="off"
        />
    </div>

    <div class="results">
        <h3>Tax Breakdown:</h3>
        {#each taxBreakdown as bracket, i}
            <div class="breakdown-item" class:even={i % 2 === 0}>
                <div class="range">{bracket.range} → {bracket.rate}% tax</div>
                <div class="calculation">
                    Tax: {bracket.rate}% × {formatCurrency(
                        bracket.taxableAmount,
                    )} =
                    <span class="tax-amount">{formatCurrency(bracket.tax)}</span
                    >
                </div>
            </div>
        {/each}

        <div class="summary">
            <div class="total-tax">
                <strong>Total Tax:</strong>
                {formatCurrency(totalTax)}
            </div>
            <div class="effective-rate">
                <strong>Effective Tax Rate:</strong>
                {effectiveRate.toFixed(2)}%
            </div>
        </div>
    </div>
</div>

<style>
    .tax-calculator {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        font-family: Arial, sans-serif;
    }

    .input-group {
        margin-bottom: 20px;
    }

    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }

    input {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }

    .breakdown-item {
        padding: 10px;
        border-bottom: 1px solid #eee;
    }

    .breakdown-item.even {
        background-color: #f9f9f9;
    }

    .range {
        font-weight: bold;
        margin-bottom: 5px;
    }

    .calculation {
        color: #555;
    }

    .tax-amount {
        color: #d32f2f;
        font-weight: bold;
    }

    .summary {
        margin-top: 20px;
        padding: 15px;
        background-color: #e3f2fd;
        border-radius: 4px;
    }

    .total-tax,
    .effective-rate {
        font-size: 18px;
        margin: 10px 0;
    }
</style>
