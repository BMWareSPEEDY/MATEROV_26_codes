// ============================================================
// ROV Motor Mixer — ESP32 (Clean Signal Version)
// ============================================================
#include <ESP32Servo.h>

// ===================== PIN DEFINITIONS =====================
const int RC_CH1_PIN = 34;  // Crab (lateral) — Right stick X
const int RC_CH2_PIN = 35;  // Forward/Back   — Right stick Y
const int RC_CH3_PIN = 32;  // Vertical       — Left stick Y
const int RC_CH4_PIN = 33;  // Yaw (turn)     — Left stick X

const int MOTOR1_PIN = 13;  // Front-Left
const int MOTOR2_PIN = 12;  // Front-Right
const int MOTOR3_PIN = 14;  // Back-Left
const int MOTOR4_PIN = 27;  // Back-Right
const int MOTOR5_PIN = 26;  // Vertical Left
const int MOTOR6_PIN = 25;  // Vertical Right

// ===================== CONFIGURATION =======================
const int RC_MID   = 1500;
const int DEADZONE = 50;
const int ESC_MID  = 1500;

// ===================== OBJECTS ==============================
Servo motor[6];
const int motorPins[6] = {MOTOR1_PIN, MOTOR2_PIN, MOTOR3_PIN,
                          MOTOR4_PIN, MOTOR5_PIN, MOTOR6_PIN};

volatile unsigned long chRiseTime[4] = {0, 0, 0, 0};
volatile unsigned long chPulseWidth[4] = {1500, 1500, 1500, 1500};

// ===================== ISRs =================================
void IRAM_ATTR ch1ISR() {
  if (digitalRead(RC_CH1_PIN) == HIGH) chRiseTime[0] = micros();
  else { unsigned long pw = micros() - chRiseTime[0]; if (pw >= 800 && pw <= 2200) chPulseWidth[0] = pw; }
}
void IRAM_ATTR ch2ISR() {
  if (digitalRead(RC_CH2_PIN) == HIGH) chRiseTime[1] = micros();
  else { unsigned long pw = micros() - chRiseTime[1]; if (pw >= 800 && pw <= 2200) chPulseWidth[1] = pw; }
}
void IRAM_ATTR ch3ISR() {
  if (digitalRead(RC_CH3_PIN) == HIGH) chRiseTime[2] = micros();
  else { unsigned long pw = micros() - chRiseTime[2]; if (pw >= 800 && pw <= 2200) chPulseWidth[2] = pw; }
}
void IRAM_ATTR ch4ISR() {
  if (digitalRead(RC_CH4_PIN) == HIGH) chRiseTime[3] = micros();
  else { unsigned long pw = micros() - chRiseTime[3]; if (pw >= 800 && pw <= 2200) chPulseWidth[3] = pw; }
}

// ===================== HELPERS ==============================
float normalizeRC(unsigned long pulseWidth) {
  int pw = constrain((int)pulseWidth, 1000, 2000);
  int diff = pw - RC_MID;
  if (abs(diff) < DEADZONE) return 0.0f;
  float sign = (diff > 0) ? 1.0f : -1.0f;
  float magnitude = (float)(abs(diff) - DEADZONE) / (float)(500 - DEADZONE);
  return constrain(sign * magnitude, -1.0f, 1.0f);
}

int mixToESC(float value) {
  if (value == 0.0f) return ESC_MID;
  value = constrain(value, -1.0f, 1.0f);
  return ESC_MID + (int)(value * 500.0f);
}

void writeAllMotors(int us) {
  for (int i = 0; i < 6; i++) motor[i].writeMicroseconds(us);
}

// ===================== SETUP ================================
void setup() {
  Serial.begin(115200);
  Serial.println("ROV Motor Mixer Starting...");

  pinMode(RC_CH1_PIN, INPUT);
  pinMode(RC_CH2_PIN, INPUT);
  pinMode(RC_CH3_PIN, INPUT);
  pinMode(RC_CH4_PIN, INPUT);

  attachInterrupt(digitalPinToInterrupt(RC_CH1_PIN), ch1ISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(RC_CH2_PIN), ch2ISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(RC_CH3_PIN), ch3ISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(RC_CH4_PIN), ch4ISR, CHANGE);

  for (int i = 0; i < 6; i++) {
    motor[i].attach(motorPins[i], 1000, 2000);
    motor[i].writeMicroseconds(1500);
  }

  Serial.println("Arming ESCs... hold 1500us for 5 seconds");
  for (int i = 0; i < 50; i++) { writeAllMotors(1500); delay(100); }
  Serial.println("ESCs armed. Ready to go.");
}

// ===================== MAIN LOOP ============================
void loop() {
  float lateral  = normalizeRC(chPulseWidth[0]);  // CH1: Crab
  float forward  = normalizeRC(chPulseWidth[1]);  // CH2: Forward/back
  float vertical = normalizeRC(chPulseWidth[2]);  // CH3: Vertical
  float yaw      = normalizeRC(chPulseWidth[3]);  // CH4: Yaw

  // Motor mixing:
  //   Crab:    M1=M4 (same direction), M2=M3 (opposite direction)
  //   Forward: all same
  //   Yaw:     M1=M3 (same), M2=M4 (opposite)
  //
  //          Forward  Lateral  Yaw
  //   M1:     +1       +1      +1
  //   M2:     +1       -1      -1
  //   M3:     +1       -1      +1
  //   M4:     +1       +1      -1

  float m1 =  forward - lateral + yaw;   // Front-Left
  float m2 =  forward + lateral - yaw;   // Front-Right
  float m3 =  forward + lateral + yaw;   // Back-Left
  float m4 =  forward - lateral - yaw;   // Back-Right
  float m5 =  vertical;
  float m6 =  vertical;

  float maxVal = max(max(abs(m1), abs(m2)), max(abs(m3), abs(m4)));
  if (maxVal > 1.0f) { m1 /= maxVal; m2 /= maxVal; m3 /= maxVal; m4 /= maxVal; }

  m5 = constrain(m5, -1.0f, 1.0f);
  m6 = constrain(m6, -1.0f, 1.0f);

  if (lateral == 0.0f && forward == 0.0f && vertical == 0.0f && yaw == 0.0f) {
    writeAllMotors(1500);
  } else {
    motor[0].writeMicroseconds(mixToESC(m1));
    motor[1].writeMicroseconds(mixToESC(m2));
    motor[2].writeMicroseconds(mixToESC(m3));
    motor[3].writeMicroseconds(mixToESC(m4));
    motor[4].writeMicroseconds(mixToESC(m5));
    motor[5].writeMicroseconds(mixToESC(m6));
  }

  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 200) {
    lastPrint = millis();
    Serial.printf("RC: L=%.2f F=%.2f V=%.2f Y=%.2f | "
                  "M1=%d M2=%d M3=%d M4=%d M5=%d M6=%d\n",
                  lateral, forward, vertical, yaw,
                  mixToESC(m1), mixToESC(m2), mixToESC(m3),
                  mixToESC(m4), mixToESC(m5), mixToESC(m6));
  }

  delay(20);
}
