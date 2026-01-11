### 1. The Main Power Bridge

- **5V Pin:** Connect a jumper wire from the Arduino **5V** pin to the **Red (+) Rail**.
- **GND Pin:** Connect a jumper wire from an Arduino **GND** pin to the **Blue (-) Rail**.

### 2. I2C LCD (via PCF8574 Backpack)

- **GND:** Connect to the **Blue (-) Rail**.
- **VCC:** Connect to the **Red (+) Rail**.
- **SDA:** Connect to Arduino Pin **A4**.
- **SCL:** Connect to Arduino Pin **A5**.

### 3. The Execution Button (Pin 2)

- **Placement:** Place the button spanning the center "trench" of the breadboard.
- **Leg 1:** Connect to the **Blue (-) Rail** (GND).
- **Leg 2:** Connect to Arduino Digital Pin **2**.
- _Note: We use `INPUT_PULLUP` in the code, so no external resistor is needed for the button._

### 4. The LDR Chaos Factor (Analog A0)

- **LDR Leg 1:** Connect to the **Red (+) Rail** (5V).
- **LDR Leg 2 / Signal:** Connect to Arduino Analog Pin **A0**.
- **1kΩ Resistor (Brown-Black-Red):** Connect one end to the same row as **A0** (the signal leg) and the other end to the **Blue (-) Rail** (GND).

### Quick Troubleshooting Check:

- **Horizontal vs. Vertical:** Remember that the numbered rows (1, 2, 3...) are connected horizontally across 5 holes, but the Power Rails (+ and -) run vertically along the entire side of the board.
- **The Gap:** Ensure your button and LDR signal wires are on the same side of the center divider as the pins they are connecting to.
- **LCD Contrast:** If the wiring is correct but the screen is blank, turn the small blue potentiometer on the back of the LCD module.
