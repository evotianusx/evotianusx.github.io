<script lang="ts">
  import Button from "./Button.svelte";
  interface ParticipantSummary {
    name: string;
    items: ReceiptItem[];
    subtotal: number;
    tax: number;
    service: number;
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
  let taxRate = $state<number>(11); // 10% tax
  let serviceRate = $state<number>(0.0);

  // Derived state
  const summary = $derived<ParticipantSummary[]>(
    calculateSummary(participants, items),
  );
  const subtotal = $derived<number>(
    items.reduce((sum, item) => sum + item.price, 0),
  );
  const taxTotal = $derived<number>((subtotal * taxRate) / 100);
  const serviceTotal = $derived<number>((subtotal * serviceRate) / 100);
  const grandTotal = $derived<number>(subtotal + taxTotal + serviceTotal);
  const calculatedTotal = $derived<number>(
    summary.reduce((sum, participant) => sum + participant.total, 0),
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
    value: string | number,
  ): void {
    items = items.map((item) =>
      item.id === id
        ? {
            ...item,
            [field]:
              field === "price" ? parseFloat(value as string) || 0 : value,
          }
        : item,
    );
  }

  function calculateSummary(
    participants: string[],
    items: ReceiptItem[],
  ): ParticipantSummary[] {
    return participants.map((participant) => {
      const participantItems = items.filter((item) =>
        item.owners.includes(participant),
      );
      const subtotal = participantItems.reduce((sum, item) => {
        const share =
          item.owners.length > 0 ? item.price / item.owners.length : 0;
        return sum + share;
      }, 0);

      // Calculate participant's share of tax (proportional to their subtotal)
      const taxShare = (subtotal * taxRate) / 100;
      const serviceShare = (subtotal * serviceRate) / 100;

      const total = subtotal + taxShare;

      return {
        name: participant,
        items: participantItems,
        subtotal: parseFloat(subtotal.toFixed(2)),
        tax: parseFloat(taxShare.toFixed(2)),
        service: parseFloat(serviceShare.toFixed(2)),
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
  import { onMount } from "svelte";
  import domtoimage from "dom-to-image";

  let captureElement: HTMLElement;
  let downloadLink = "";

  async function captureDiv() {
    if (!captureElement) return;

    try {
      const image = await domtoimage.toPng(captureElement);

      // // Convert canvas to image and create download link
      // const image = canvas.toDataURL("image/png");
      downloadLink = image;

      // Optional: Automatically download the image
      const link = document.createElement("a");
      link.download = "Receipt.png";
      link.href = image;
      link.click();
    } catch (error) {
      console.error("Error capturing div:", error);
    }
  }
</script>

<div class="receipt-splitter">
  <!-- Participants Section -->
  <div class="section">
    <h3>Participants</h3>
    <div class="participant-list">
      {#each participants as participant}
        <div class="participant-tag">
          {participant}
          <Button
            variant="secondary"
            class="btn"
            onclick={() => removeParticipant(participant)}>X</Button
          >
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
      <Button variant="secondary" onclick={addParticipant}>Add</Button>
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
              <Button variant="secondary" onclick={() => removeItem(item.id)}
                >Remove</Button
              >
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
    <Button variant="secondary" onclick={addItem}>Add Item</Button>
  </div>
  <div class="section">
    <h3>Settings</h3>
    <br />
    <span>Tax</span>
    <input type="number" bind:value={taxRate} max="100" min="0" />
    <br />
    <span>Service Charge</span>
    <input
      type="number"
      bind:value={serviceRate}
      max="100"
      min="0"
      onclick={() => {
        serviceRate = null;
      }}
    />
  </div>
  <!-- Summary Section -->

  <div class="section" bind:this={captureElement}>
    <h3>Payment Summary</h3>

    <div class="table-wrapper">
      <div class="summary-grid">
        <!-- Header Row -->
        <div class="summary-header">Participant</div>
        <div class="summary-header">Items</div>
        <div class="summary-header text-right">Subtotal</div>
        <div class="summary-header text-right">Tax</div>

        <div class="summary-header text-right">Service Charge</div>
        <div class="summary-header text-right">Total</div>

        {#each summary as participantSummary}
          <div class="participant-cell">
            <div class="participant-avatar">
              {participantSummary.name.charAt(0)}
            </div>
            {participantSummary.name}
          </div>

          <div class="items-cell">
            {#each participantSummary.items as item}
              <div class="item-row">
                <h4>{item.name}</h4>
              </div>
            {/each}
          </div>

          <div class="amount-cell text-right">
            Items - Rp {formatCurrency(participantSummary.subtotal)}
          </div>

          <div class="amount-cell text-right">
            Tax - Rp {formatCurrency(participantSummary.tax)}
          </div>

          <div class="amount-cell text-right">
            Service - Rp {formatCurrency(participantSummary.service)}
          </div>

          <div class="amount-cell text-right font-medium">
            Total - Rp {formatCurrency(participantSummary.total)}
          </div>
        {/each}

        <!-- Totals Row -->
        <div class="summary-total-label">Subtotal:</div>
        <div></div>
        <div></div>
        <div></div>
        <div class="amount-cell text-right">
          Rp {formatCurrency(subtotal)}
        </div>
        <div></div>
        <div></div>

        <div class="summary-total-label">Tax ({taxRate}%):</div>
        <div></div>
        <div></div>
        <div></div>
        <div class="amount-cell text-right">
          Rp {formatCurrency(taxTotal)}
        </div>
        <div></div>

        <div class="summary-total-label">Service ({serviceRate}%):</div>
        <div></div>
        <div></div>
        <div></div>
        <div class="amount-cell text-right">
          Rp {formatCurrency(serviceTotal)}
        </div>
        <div></div>

        <div class="summary-total-label grand-total">Grand Total:</div>
        <div></div>
        <div></div>
        <div></div>
        <div class="amount-cell text-right grand-total">
          Rp {formatCurrency(grandTotal)}
        </div>
      </div>
    </div>

    <div class="Button-container">
      <Button variant="secondary" onclick={captureDiv}>Save Receipt</Button>
    </div>
  </div>
</div>

<style>
  .receipt-splitter {
    max-width: 90%;
    margin: 0 auto;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    padding: 1rem;
    box-sizing: border-box;
  }

  .section {
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--section-bg);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  h3 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    color: var(--text-color);
    font-size: 1.5rem;
  }

  .table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    margin-bottom: 1.5rem;
  }

  .summary-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .summary-header {
    font-weight: bold;
    padding: 0.75rem 0.5rem;
    border-bottom: 1px solid var(--border-color);
    color: var(--text-color);
    background-color: var(--table-header-bg);
    display: none;
  }

  .participant-cell {
    display: flex;
    align-items: center;
    padding: 0.75rem 0.5rem;
    border-bottom: 1px solid var(--border-color);
    font-weight: 500;
    color: var(--text-color);
  }

  .participant-avatar {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background-color: var(--Button-bg);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 0.75rem;
    font-weight: bold;
  }

  .participant-name {
    color: var(--text-color);
  }

  .items-cell {
    padding: 0.75rem 0.5rem;
    border-bottom: 1px solid var(--border-color);
  }

  .item-row {
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    display: flex;
    flex-direction: column;
  }

  .item-name {
    color: var(--text-color);
    font-weight: 500;
  }

  .item-details {
    color: var(--text-color);
    opacity: 0.8;
    font-size: 0.8rem;
    margin-top: 0.2rem;
  }

  .amount-cell {
    padding: 0.75rem 0.5rem;
    border-bottom: 1px solid var(--border-color);
    color: var(--text-color);
  }

  .total-cell {
    font-weight: bold;
    color: var(--text-color);
  }

  .text-right {
    text-align: right;
  }

  .summary-total-label {
    font-weight: bold;
    padding: 0.75rem 0.5rem;
    grid-column: 1;
    color: var(--text-color);
  }

  .grand-total {
    color: var(--Button-bg);
    font-weight: bold;
    font-size: 1.1rem;
  }

  .Button-container {
    display: flex;
    justify-content: flex-end;
    margin-top: 1.5rem;
  }

  .confirm-Button {
    padding: 0.75rem 1.5rem;
    background: var(--Button-bg);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
  }

  .confirm-Button:hover {
    background: var(--Button-hover);
  }

  /* Dark mode specific adjustments */
  :global(.dark-mode) .section {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  :global(.dark-mode) .item-details {
    opacity: 0.7;
  }

  /* Medium screens (tablets) */
  @media (min-width: 600px) {
    .receipt-splitter {
      max-width: 768px;
      padding: 1.5rem;
    }

    .section {
      padding: 1.5rem;
    }

    .summary-grid {
      grid-template-columns: 2fr 3fr 1fr 1fr 1fr 1fr;
    }

    .summary-header {
      display: block;
    }

    .summary-total-label {
      grid-column: 1 / 3;
    }

    .item-row {
      flex-direction: row;
      justify-content: space-between;
    }

    .item-details {
      margin-top: 0;
      margin-left: 0.5rem;
    }
  }

  /* Large screens (desktops) */
  @media (min-width: 1024px) {
    .receipt-splitter {
      max-width: 1000px;
      padding: 2rem;
    }

    .section {
      padding: 2rem;
    }
  }

  :root {
    /* Light mode colors */
    --bg-color: #ffffff;
    --text-color: #333333;
    --section-bg: #f5f5f5;
    --tag-bg: #e0e0e0;
    --border-color: #dddddd;
    --Button-bg: #4caf50;
    --Button-hover: #45a049;
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
      --Button-bg: #388e3c;
      --Button-hover: #2e7d32;
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
    --Button-bg: #388e3c;
    --Button-hover: #2e7d32;
    --table-header-bg: #3d3d3d;
    --input-bg: #2d2d2d;
    --input-text: #f0f0f0;
  }
</style>
