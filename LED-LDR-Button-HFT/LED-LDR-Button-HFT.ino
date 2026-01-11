#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

/**
 * HFT HARDWARE TERMINAL FIRMWARE
 * -----------------------------
 * Features:
 * - 2Mbps Binary Serial Link (HFT Simulation)
 * - I2C LCD Dashboard (PCF8574)
 * - LDR Chaos Factor (Analog A0)
 * - Edge-Triggered Trade Button (Pin 2)
 */

// Initialize LCD (Standard I2C Address 0x27)
LiquidCrystal_I2C lcd(0x27, 16, 2); 

const int buttonPin = 2;
const int ldrPin = A0; 
uint16_t seqNum = 0;
uint16_t lastDisplayedPrice = 0;
int lastButtonState = HIGH; 

void setup() {
  Serial.begin(2000000); 
  
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("HFT TERMINAL");
  lcd.setCursor(0, 1);
  lcd.print("READY >>>>");
}

void loop() {
  // 1. READ SENSORS
  int ldrValue = analogRead(ldrPin);
  int currentButtonState = digitalRead(buttonPin);
  
  // 2. CALCULATE VOLATILITY (LDR Logic)
  // If covered (dark), market goes crazy. Adjust '300' if needed.
  int volatility = (ldrValue < 300) ? 50 : 5;
  uint16_t price = 15000 + random(-volatility, volatility);
  
  // 3. EDGE DETECTION (Button Logic)
  uint8_t tradeSignal = 0;
  if (currentButtonState == LOW && lastButtonState == HIGH) {
    tradeSignal = 1; 
    digitalWrite(LED_BUILTIN, HIGH);
    lcd.setCursor(0, 1);
    lcd.print(volatility > 5 ? "VOLATILE TRADE!" : "ORDER SENT!    ");
  } 
  
  if (currentButtonState == HIGH && lastButtonState == LOW) {
    digitalWrite(LED_BUILTIN, LOW);
    lcd.setCursor(0, 1);
    lcd.print(volatility > 5 ? "DANGER: DARK   " : "LISTENING...   ");
  }

  lastButtonState = currentButtonState;

  // 4. TRANSMIT TO PYTHON (6-byte binary packet)
  Serial.write(0xAA);             
  Serial.write((uint8_t*)&seqNum, 2); 
  Serial.write((uint8_t*)&price, 2);  
  Serial.write(tradeSignal); 

  // 5. RECEIVE FROM PYTHON (LCD Update)
  if (Serial.available() >= 2) {
    uint16_t rxPrice;
    Serial.readBytes((char*)&rxPrice, 2);
    
    if (rxPrice != lastDisplayedPrice) {
      lcd.setCursor(8, 0);
      lcd.print("$");
      lcd.print(rxPrice / 100.0);
      lastDisplayedPrice = rxPrice;
    }
  }

  seqNum++;
  delay(5); 
}