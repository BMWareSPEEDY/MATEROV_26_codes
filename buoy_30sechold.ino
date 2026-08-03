#include <Wire.h>
#include <MS5837.h>
#include "BluetoothSerial.h"

MS5837 sensor;
BluetoothSerial SerialBT;

#define SDA_PIN 21
#define SCL_PIN 22
#define THRUSTER_PIN 13

const float SURFACE_THRESHOLD = 0.5;

const float STAGE1_DEPTH = 1.0;
const float STAGE2_DEPTH = 0.4;
const float DEPTH_BAND = 0.05;
const unsigned long HOLD_TIME = 30000;
const unsigned long TRANSITION_TIMEOUT = 30000;

const int maxPackets = 20; // bumped up for 2 cycles
int logIndex = 0;

unsigned long lastLogTime = 0;
unsigned long stageHoldStart = 0;
unsigned long stageStartTime = 0;
bool thrusterOn = false;
bool missionStarted = false;
bool dataSent = false;

int missionStage = 0;
// 0  — sink  to 1.0m  (cycle 1)
// 1  — hold  at 1.0m  (cycle 1)
// 2  — rise  to 0.4m  (cycle 1)
// 3  — hold  at 0.4m  (cycle 1)
// 4  — sink  to 1.0m  (cycle 2)
// 5  — hold  at 1.0m  (cycle 2)
// 6  — rise  to 0.4m  (cycle 2)
// 7  — hold  at 0.4m  (cycle 2)
// 8  — resurface

float depthOffset = 0;

struct DepthPacket {
  unsigned long time;
  float depth;
};

DepthPacket depthLog[maxPackets];

// ── Helpers ───────────────────────────────────────────────────────────────────

float targetForStage(int stage) {
  // sink/hold stages target 1m; rise/hold stages target 0.4m
  return (stage == 0 || stage == 1 || stage == 4 || stage == 5)
         ? STAGE1_DEPTH : STAGE2_DEPTH;
}

void advanceTo(int nextStage, bool isHold) {
  digitalWrite(THRUSTER_PIN, LOW);
  thrusterOn = false;
  missionStage = nextStage;
  if (isHold) stageHoldStart = millis();
  else        stageStartTime = millis();
}

// ── Data tx (formatting untouched) ───────────────────────────────────────────

void sendData() {
  Serial.println("Sending data over Bluetooth...");
  SerialBT.println("=== Depth Log Start ===");
  for (int i = 0; i < logIndex; i++) {
    SerialBT.print("Time(ms): ");
    SerialBT.print(depthLog[i].time);
    SerialBT.print(" | Depth(m): ");
    SerialBT.println(depthLog[i].depth, 2);
  }
  SerialBT.println("=== Depth Log End ===");
  Serial.println("Data sent.");
  dataSent = true;
}

// ── Init ──────────────────────────────────────────────────────────────────────

void waitForBluetoothConnection() {
  Serial.println("Waiting for Bluetooth connection...");
  while (!SerialBT.hasClient()) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nBluetooth connected.");

  float sum = 0;
  for (int i = 0; i < 5; i++) {
    sensor.read();
    sum += sensor.depth();
    delay(300);
  }
  depthOffset = sum / 5.0;

  Serial.print("Depth zeroed at: ");
  Serial.println(depthOffset);
  Serial.println("Send 'start' to begin mission.");
}

void setup() {
  Serial.begin(115200);
  SerialBT.begin("BuoyLogger");

  pinMode(THRUSTER_PIN, OUTPUT);
  digitalWrite(THRUSTER_PIN, LOW);

  Wire.begin(SDA_PIN, SCL_PIN);

  if (!sensor.init()) {
    Serial.println("Sensor not found.");
    while (1);
  }

  sensor.setModel(MS5837::MS5837_30BA);
  sensor.setFluidDensity(997);

  waitForBluetoothConnection();
}

// ── Main loop ─────────────────────────────────────────────────────────────────

void loop() {

  // ── Command handling ────────────────────────────────────────────────────────
  if (SerialBT.available()) {
    String cmd = SerialBT.readStringUntil('\n');
    cmd.trim();
    cmd.toLowerCase();

    if (cmd == "start" && !missionStarted) {
      Serial.println("START received. Mission beginning...");
      SerialBT.println("Mission started.");

      logIndex    = 0;
      dataSent    = false;
      thrusterOn  = false;
      missionStage = 0;
      stageStartTime = millis();
      lastLogTime    = millis();
      missionStarted = true;

    } else if (cmd == "stop" && missionStarted) {
      Serial.println("STOP received. Halting thruster and sending data...");
      SerialBT.println("Mission stopped. Sending data...");

      digitalWrite(THRUSTER_PIN, LOW);
      thrusterOn     = false;
      missionStarted = false;
      missionStage   = 0;
      sendData();
    }
  }

  if (!missionStarted) return;

  sensor.read();
  float currentDepth = sensor.depth() - depthOffset;

  // ── Data logging every 5 s (stages 0–7 only) ───────────────────────────────
  if (missionStage < 8 && (millis() - lastLogTime >= 5000) && logIndex < maxPackets) {
    depthLog[logIndex].time  = millis();
    depthLog[logIndex].depth = currentDepth;
    Serial.print("Logged ["); Serial.print(logIndex);
    Serial.print("] Depth: "); Serial.println(currentDepth);
    logIndex++;
    lastLogTime = millis();
  }

  // ── State machine ───────────────────────────────────────────────────────────
  switch (missionStage) {

    // ── SINK stages (0, 4) ────────────────────────────────────────────────────
    case 0:
    case 4: {
      bool timedOut = (millis() - stageStartTime >= TRANSITION_TIMEOUT);

      if (currentDepth < STAGE1_DEPTH - DEPTH_BAND && !timedOut) {
        if (!thrusterOn) {
          digitalWrite(THRUSTER_PIN, HIGH);
          thrusterOn = true;
          Serial.print("Stage "); Serial.print(missionStage);
          Serial.println(": Thruster ON — sinking to 1m");
        }
      } else {
        if (timedOut) {
          Serial.print("Stage "); Serial.print(missionStage);
          Serial.print(": TIMEOUT at "); Serial.print(currentDepth); Serial.println("m — advancing.");
          SerialBT.print("Timeout at "); SerialBT.print(currentDepth); SerialBT.println("m. Holding here.");
        } else {
          Serial.print("Stage "); Serial.print(missionStage + 1);
          Serial.println(": Reached 1m. Holding...");
          SerialBT.println("Reached 1m depth. Holding.");
        }
        advanceTo(missionStage + 1, true); // → hold stage
      }
      break;
    }

    // ── HOLD-AT-1m stages (1, 5) ──────────────────────────────────────────────
    case 1:
    case 5: {
      if (currentDepth > STAGE1_DEPTH + DEPTH_BAND && thrusterOn) {
        digitalWrite(THRUSTER_PIN, LOW);
        thrusterOn = false;
        Serial.print("Stage "); Serial.print(missionStage); Serial.println(": Thruster OFF — too deep");
      } else if (currentDepth < STAGE1_DEPTH - DEPTH_BAND && !thrusterOn) {
        digitalWrite(THRUSTER_PIN, HIGH);
        thrusterOn = true;
        Serial.print("Stage "); Serial.print(missionStage); Serial.println(": Thruster ON — too shallow");
      }

      if (millis() - stageHoldStart >= HOLD_TIME) {
        Serial.print("Stage "); Serial.print(missionStage);
        Serial.println(": Hold complete. Rising to 0.4m...");
        SerialBT.println("Rising to 0.4m depth.");
        advanceTo(missionStage + 1, false); // → rise stage
      }
      break;
    }

    // ── RISE stages (2, 6) ────────────────────────────────────────────────────
    case 2:
    case 6: {
      if (thrusterOn) { digitalWrite(THRUSTER_PIN, LOW); thrusterOn = false; }

      bool timedOut = (millis() - stageStartTime >= TRANSITION_TIMEOUT);

      if (currentDepth <= STAGE2_DEPTH + DEPTH_BAND || timedOut) {
        if (timedOut) {
          Serial.print("Stage "); Serial.print(missionStage);
          Serial.print(": TIMEOUT at "); Serial.print(currentDepth); Serial.println("m — advancing.");
          SerialBT.print("Timeout at "); SerialBT.print(currentDepth); SerialBT.println("m. Holding here.");
        } else {
          Serial.print("Stage "); Serial.print(missionStage + 1);
          Serial.println(": Reached 0.4m. Holding...");
          SerialBT.println("Reached 0.4m depth. Holding.");
        }
        advanceTo(missionStage + 1, true); // → hold stage
      }
      break;
    }

    // ── HOLD-AT-0.4m stages (3, 7) ────────────────────────────────────────────
    case 3:
    case 7: {
      if (currentDepth > STAGE2_DEPTH + DEPTH_BAND && thrusterOn) {
        digitalWrite(THRUSTER_PIN, LOW);
        thrusterOn = false;
        Serial.print("Stage "); Serial.print(missionStage); Serial.println(": Thruster OFF — too deep");
      } else if (currentDepth < STAGE2_DEPTH - DEPTH_BAND && !thrusterOn) {
        digitalWrite(THRUSTER_PIN, HIGH);
        thrusterOn = true;
        Serial.print("Stage "); Serial.print(missionStage); Serial.println(": Thruster ON — too shallow");
      }

      if (millis() - stageHoldStart >= HOLD_TIME) {
        Serial.print("Stage "); Serial.print(missionStage); Serial.println(": Hold complete.");
        if (missionStage == 3) {
          // End of cycle 1 — start cycle 2
          Serial.println("Starting cycle 2. Sinking to 1m...");
          SerialBT.println("Cycle 1 complete. Starting cycle 2.");
          advanceTo(4, false); // → sink stage cycle 2
        } else {
          // End of cycle 2 — resurface
          Serial.println("Stage 8: Resurfacing...");
          SerialBT.println("Resurfacing...");
          advanceTo(8, false);
        }
      }
      break;
    }

    // ── RESURFACE (8) ─────────────────────────────────────────────────────────
    case 8: {
      if (thrusterOn) { digitalWrite(THRUSTER_PIN, LOW); thrusterOn = false; }

      if (currentDepth < SURFACE_THRESHOLD && !dataSent) {
        Serial.println("Buoy resurfaced.");
        SerialBT.println("Buoy resurfaced. Sending data...");

        if (!SerialBT.hasClient()) {
          Serial.println("Waiting for Bluetooth reconnection...");
          while (!SerialBT.hasClient()) { delay(500); Serial.print("."); }
          Serial.println("\nReconnected.");
        }

        sendData();
        missionStarted = false;
        missionStage   = 0;

        Serial.println("Mission complete. Send 'start' to run again.");
        SerialBT.println("Mission complete. Send 'start' to run again.");
      }
      break;
    }
  }

  delay(100);
}