<script lang="ts">
  interface ParticipantSummary {
    name: string;
    items: ReceiptItem[];
    subtotal: number;
    tax: number;
    total: number;
  }
  interface ReceiptItem {
    id: number;
    name: string;
    price: number;
    owners: string[];
  }
  // State
  let items = $state<ReceiptItem[]>([
    { id: 1, name: "Pizza", price: 100000.0, owners: [] },
  ]);

  let participants = $state<string[]>(["Me"]);
  let newParticipant = $state<string>("");
  const taxRate = $state<number>(0.1); // 10% tax

  // Derived state
  const summary = $derived<ParticipantSummary[]>(
    calculateSummary(participants, items)
  );
  const subtotal = $derived<number>(
    items.reduce((sum, item) => sum + item.price, 0)
  );
  const taxTotal = $derived<number>(subtotal * taxRate);
  const grandTotal = $derived<number>(subtotal + taxTotal);
  const calculatedTotal = $derived<number>(
    summary.reduce((sum, participant) => sum + participant.total, 0)
  );

  // Methods
  function addParticipant(): void {
    if (
      newParticipant.trim() &&
      !participants.includes(newParticipant.trim())
    ) {
      participants = [...participants, newParticipant.trim()];
      newParticipant = "";
    }
  }

  function removeParticipant(name: string): void {
    participants = participants.filter((p) => p !== name);
    // Remove this participant from all items
    items = items.map((item) => ({
      ...item,
      owners: item.owners.filter((owner) => owner !== name),
    }));
  }

  function toggleOwnership(itemId: number, participant: string): void {
    items = items.map((item) => {
      if (item.id === itemId) {
        const owners = item.owners.includes(participant)
          ? item.owners.filter((owner) => owner !== participant)
          : [...item.owners, participant];
        return { ...item, owners };
      }
      return item;
    });
  }

  function addItem(): void {
    items = [
      ...items,
      {
        id: Math.max(0, ...items.map((i) => i.id)) + 1,
        name: "",
        price: 0,
        owners: [],
      },
    ];
  }

  function removeItem(id: number): void {
    items = items.filter((item) => item.id !== id);
  }

  function updateItem(
    id: number,
    field: keyof ReceiptItem,
    value: string | number
  ): void {
    items = items.map((item) =>
      item.id === id
        ? {
            ...item,
            [field]:
              field === "price" ? parseFloat(value as string) || 0 : value,
          }
        : item
    );
  }

  function calculateSummary(
    participants: string[],
    items: ReceiptItem[]
  ): ParticipantSummary[] {
    return participants.map((participant) => {
      const participantItems = items.filter((item) =>
        item.owners.includes(participant)
      );
      const subtotal = participantItems.reduce((sum, item) => {
        const share =
          item.owners.length > 0 ? item.price / item.owners.length : 0;
        return sum + share;
      }, 0);

      // Calculate participant's share of tax (proportional to their subtotal)
      const taxShare = subtotal * taxRate;
      const total = subtotal + taxShare;

      return {
        name: participant,
        items: participantItems,
        subtotal: parseFloat(subtotal.toFixed(2)),
        tax: parseFloat(taxShare.toFixed(2)),
        total: parseFloat(total.toFixed(2)),
      };
    });
  }

  function formatCurrency(amount: number, decimalPlaces = 2) {
    // Convert to number if it's a string
    const number = typeof amount === "string" ? parseFloat(amount) : amount;

    // Handle invalid numbers
    if (isNaN(number)) return "0.00";

    // Format the number
    return number.toLocaleString(undefined, {
      minimumFractionDigits: decimalPlaces,
      maximumFractionDigits: decimalPlaces,
      useGrouping: true, // This adds the commas
    });
  }
</script>

<div class="receipt-splitter">
  <h2>Receipt Splitter</h2>

  <!-- Participants Section -->
  <div class="section">
    <h3>Participants</h3>
    <div class="participant-list">
      {#each participants as participant}
        <div class="participant-tag">
          {participant}
          <button onclick={() => removeParticipant(participant)}>×</button>
        </div>
      {/each}
    </div>
    <div class="add-participant">
      <input
        type="text"
        bind:value={newParticipant}
        placeholder="Add participant"
        onkeydown={(e) => e.key === "Enter" && addParticipant()}
      />
      <button onclick={addParticipant}>Add</button>
    </div>
  </div>

  <!-- Items Section -->
  <div class="section">
    <h3>Receipt Items</h3>
    <table>
      <thead>
        <tr>
          <th>Item</th>
          <th>Price</th>
          {#each participants as participant}
            <th>{participant}</th>
          {/each}
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {#each items as item (item.id)}
          <tr>
            <td>
              <input
                type="text"
                bind:value={item.name}
                onchange={(e) => updateItem(item.id, "name", e.target.value)}
              />
            </td>
            <td>
              <input
                type="number"
                bind:value={item.price}
                onchange={(e) => updateItem(item.id, "price", e.target.value)}
                min="0"
                step="1000.00"
              />
      
            </td>
            {#each participants as participant}
              <td>
                <input
                  type="checkbox"
                  checked={item.owners.includes(participant)}
                  onchange={() => toggleOwnership(item.id, participant)}
                />
              </td>
            {/each}
            <td>
              <button onclick={() => removeItem(item.id)}>Remove</button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
    <button onclick={addItem}>Add Item</button>
  </div>

  <!-- Summary Section -->
  <div class="section">
    <h3>Summary</h3>
    <div class="summary-grid">
      <div class="summary-header">Participant</div>
      <div class="summary-header">Items</div>
      <div class="summary-header">Subtotal</div>
      <div class="summary-header">Tax</div>
      <div class="summary-header">Total</div>

      {#each summary as participantSummary}
        <div>{participantSummary.name}</div>
        <div>
          {#each participantSummary.items as item}
            <div>
              {item.name}
              ({item.owners.length > 1
                ? `Rp ${item.price.toFixed(2)} ÷ ${item.owners.length} = Rp ${(item.price / item.owners.length).toFixed(2)}`
                : `Rp ${item.price.toFixed(2)}`})
            </div>
          {/each}
        </div>
        <div>Rp {formatCurrency(participantSummary.subtotal)}</div>
        <div>Rp {formatCurrency(participantSummary.tax)}</div>
        <div>Rp {formatCurrency(participantSummary.total)}</div>
      {/each}

      <!-- Totals Row -->
      <div class="summary-total-label">Subtotal:</div>
      <div></div>
      <div>Rp {formatCurrency(subtotal)}</div>
      <div></div>
      <div></div>

      <div class="summary-total-label">Tax ({taxRate * 100}%):</div>
      <div></div>
      <div></div>
      <div>Rp {formatCurrency(taxTotal)}</div>
      <div></div>

      <div class="summary-total-label">Grand Total:</div>
      <div></div>
      <div></div>
      <div></div>
      <div>Rp {formatCurrency(grandTotal)}</div>
    </div>
  </div>
</div>
<style>
  :root {
    /* Light mode colors */
    --bg-color: #ffffff;
    --text-color: #333333;
    --section-bg: #f5f5f5;
    --tag-bg: #e0e0e0;
    --border-color: #dddddd;
    --button-bg: #4caf50;
    --button-hover: #45a049;
    --table-header-bg: #e0e0e0;
    --input-bg: #ffffff;
    --input-text: #333333;
  }

  @media (prefers-color-scheme: dark) {
    :root {
      /* Dark mode colors */
      --bg-color: #1a1a1a;
      --text-color: #f0f0f0;
      --section-bg: #2d2d2d;
      --tag-bg: #3d3d3d;
      --border-color: #444444;
      --button-bg: #388e3c;
      --button-hover: #2e7d32;
      --table-header-bg: #3d3d3d;
      --input-bg: #2d2d2d;
      --input-text: #f0f0f0;
    }
  }

  .dark-mode {
    /* Dark mode colors (for manual toggle) */
    --bg-color: #1a1a1a;
    --text-color: #f0f0f0;
    --section-bg: #2d2d2d;
    --tag-bg: #3d3d3d;
    --border-color: #444444;
    --button-bg: #388e3c;
    --button-hover: #2e7d32;
    --table-header-bg: #3d3d3d;
    --input-bg: #2d2d2d;
    --input-text: #f0f0f0;
  }

  .receipt-splitter {
    max-width: 1000px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    padding: 1rem;
  }

  .section {
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--section-bg);
    border-radius: 8px;
  }

  h3 {
    margin-top: 0;
    color: var(--text-color);
  }

  .participant-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .participant-tag {
    background: var(--tag-bg);
    padding: 0.3rem 0.6rem;
    border-radius: 16px;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    color: var(--text-color);
  }

  .participant-tag button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    font-size: 1.1rem;
    line-height: 1;
    color: var(--text-color);
  }

  .add-participant {
    display: flex;
    gap: 0.5rem;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1rem;
  }

  th,
  td {
    padding: 0.5rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
    color: var(--text-color);
  }

  th {
    background: var(--table-header-bg);
  }

  input[type="text"],
  input[type="number"] {
    padding: 0.3rem;
    width: 100%;
    box-sizing: border-box;
    background-color: var(--input-bg);
    color: var(--input-text);
    border: 1px solid var(--border-color);
  }

  .summary-grid {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr 1fr 1fr;
    gap: 0.5rem;
  }

  .summary-header {
    font-weight: bold;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 0.5rem;
  }

  .summary-total-label {
    font-weight: bold;
    grid-column: 1 / 3;
  }

  button {
    padding: 0.3rem 0.6rem;
    background: var(--button-bg);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background: var(--button-hover);
  }

  /* Dark mode toggle button */
  .dark-mode-toggle {
    position: fixed;
    top: 1rem;
    right: 1rem;
    background: var(--button-bg);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.5rem;
    cursor: pointer;
    z-index: 1000;
  }
</style>