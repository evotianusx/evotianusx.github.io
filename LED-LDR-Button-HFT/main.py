import serial
import struct
import threading
import time
import math

"""
HFT PYTHON TRADING ENGINE - v2.0 (Safety Update)
-----------------------------------------------
Architecture: Producer-Consumer
Features:
- Deterministic binary parsing (struct.unpack)
- Mutex-locked shared memory (threading.Lock)
- Real-time Volatility tracking
- CIRCUIT BREAKER: Auto-locks system during extreme volatility (Darkness)
"""

# --- CONFIGURATION ---
SERIAL_PORT = "COM8"
BAUD_RATE = 2000000
VOLATILITY_THRESHOLD = 35.0  # Max allowed volatility before circuit breaker trips

# Shared state between threads
latest_data = {"price": 0, "seq": -1, "btn_signal": 0}
data_lock = threading.Lock()


class CircuitBreaker:
    """Safety mechanism to prevent trading during flash crashes/chaos."""

    def __init__(self, threshold):
        self.threshold = threshold
        self.is_locked = False
        self.lock_time = 0

    def check(self, current_vol):
        if current_vol > self.threshold:
            if not self.is_locked:
                print(
                    f"\n[!!!] CIRCUIT BREAKER TRIPPED: Volatility {current_vol:.2f} exceeds threshold!"
                )
            self.is_locked = True
            self.lock_time = time.time()

        # Auto-reset after 5 seconds of stability
        if self.is_locked and current_vol < (self.threshold * 0.5):
            if time.time() - self.lock_time > 5:
                print("\n[OK] Volatility stabilized. Circuit breaker reset.")
                self.is_locked = False

        return self.is_locked


def listener_thread(ser):
    """Handles high-throughput serial ingestion."""
    global latest_data
    print(f"[*] LISTENER: Ingesting data on {SERIAL_PORT}...")

    while True:
        try:
            if ser.in_waiting >= 6:
                raw = ser.read(6)
                if raw[0] == 0xAA:
                    header, seq, price, btn = struct.unpack("<BHHB", raw)
                    with data_lock:
                        latest_data["price"] = price
                        latest_data["seq"] = seq
                        if btn == 1:
                            latest_data["btn_signal"] = 1
                else:
                    ser.read(1)  # Re-aligning
        except Exception as e:
            print(f"\n[!] Listener Crash: {e}")
            break


def strategy_thread(ser):
    """Processes ticks and manages order execution with Safety Logic."""
    last_processed_seq = -1
    prices_history = []
    breaker = CircuitBreaker(VOLATILITY_THRESHOLD)

    print("[*] STRATEGY: Engine Initialized. Monitoring Market...")

    while True:
        with data_lock:
            curr_price = latest_data["price"]
            curr_seq = latest_data["seq"]
            curr_signal = latest_data["btn_signal"]
            latest_data["btn_signal"] = 0  # Acknowledge/Clear

        if curr_seq != -1 and curr_seq > last_processed_seq:
            # 1. ANALYTICS: Track Volatility
            prices_history.append(curr_price)
            if len(prices_history) > 100:
                prices_history.pop(0)

            vol = 0
            if len(prices_history) >= 20:
                recent = prices_history[-20:]
                avg_recent = sum(recent) / 20
                variance = sum((x - avg_recent) ** 2 for x in recent) / 20
                vol = math.sqrt(variance)

            # 2. SAFETY: Check Circuit Breaker
            system_locked = breaker.check(vol)

            # 3. FEEDBACK: Send Price + Lock Status to Arduino
            # Format: 'H' for price. We could add a 'B' for lock status if we update Arduino.
            try:
                ser.write(struct.pack("<H", curr_price))
            except:
                pass

            # 4. EXECUTION: Only if system is NOT locked
            if curr_signal == 1:
                if system_locked:
                    print(
                        f"\n[REJECTED] Seq {curr_seq} | Trade blocked by Circuit Breaker!"
                    )
                else:
                    print(
                        f"\n[EXECUTE] Seq {curr_seq} | Price: ${curr_price / 100:.2f}"
                    )
                    print(">>> ORDER FILLED | Position: LONG 0.1 BTC")

            # Dashboard
            status = (
                "!! LOCKED !!"
                if system_locked
                else ("VOLATILE" if vol > 15 else "STABLE")
            )
            print(
                f" TICK: {curr_seq:05} | PRICE: ${curr_price / 100:.2f} | VOL: {vol:.2f} [{status}] ",
                end="\r",
                flush=True,
            )

            last_processed_seq = curr_seq

        time.sleep(0.001)


if __name__ == "__main__":
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        ser.reset_input_buffer()
        print("[*] System initializing (waiting for hardware)...")
        time.sleep(2)

        t_listen = threading.Thread(target=listener_thread, args=(ser,), daemon=True)
        t_strat = threading.Thread(target=strategy_thread, args=(ser,), daemon=True)

        t_listen.start()
        t_strat.start()

        print("--- HFT SIMULATOR ACTIVE ---")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Emergency Stop: Shutting down engine.")
        if "ser" in locals():
            ser.close()
    except Exception as e:
        print(f"Connection Error: {str(e)}")
