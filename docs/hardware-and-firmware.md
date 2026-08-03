# Hardware & Firmware Specification

This document details the embedded software architecture, pin configurations, and motor mixing algorithms running on ESP32 microcontrollers.

---

## 1. ROV Motor Mixer (`code.ino`)

The primary ROV flight firmware receives 4-channel PWM input from an RC receiver, normalizes the inputs with deadband rejection, and mixes the signals into 6 independent electronic speed controller (ESC) outputs.

### Pinout Mapping

| Subsystem | Function | ESP32 GPIO Pin | Channel / Notes |
| :--- | :--- | :--- | :--- |
| **RC In** | Crab (Lateral / Strafe) | `GPIO 34` | Right stick X (CH1) |
| **RC In** | Forward / Reverse | `GPIO 35` | Right stick Y (CH2) |
| **RC In** | Vertical (Heave) | `GPIO 32` | Left stick Y (CH3) |
| **RC In** | Yaw (Turn) | `GPIO 33` | Left stick X (CH4) |
| **ESC Out** | Front-Left Thruster | `GPIO 13` | Motor 1 (Vectored) |
| **ESC Out** | Front-Right Thruster | `GPIO 12` | Motor 2 (Vectored) |
| **ESC Out** | Back-Left Thruster | `GPIO 14` | Motor 3 (Vectored) |
| **ESC Out** | Back-Right Thruster | `GPIO 27` | Motor 4 (Vectored) |
| **ESC Out** | Vertical Left Thruster | `GPIO 26` | Motor 5 (Heave) |
| **ESC Out** | Vertical Right Thruster | `GPIO 25` | Motor 6 (Heave) |

### Control Loop & Mixing Matrix

- **Interrupt-Driven Pulse Capture:** RC channel inputs are captured using `IRAM_ATTR` pin change interrupts with microsecond precision (`800 µs – 2200 µs` valid band, `1500 µs` neutral).
- **Deadband Normalization:** A `±50 µs` deadband around center suppresses stick jitter, normalizing output to `[-1.0, 1.0]`.
- **Planar Vector Mixing:**
  ```text
  FL = Forward + Crab + Yaw
  FR = Forward - Crab - Yaw
  BL = Forward - Crab + Yaw
  BR = Forward + Crab - Yaw
  ```
- **Scale Clamping:** Vector outputs exceeding unit magnitude are dynamically rescaled to prevent actuator clipping and preserve directional priority.
- **Vertical Drive:** Symmetrically assigns vertical axis stick input directly to Motor 5 and Motor 6.

---

## 2. Autonomous Profiling Float (`buoy_30sechold.ino`)

Firmware for an autonomous vertical profiling buoy designed to collect water column depth profiles and transmit telemetry upon surfacing.

### Hardware Interfaces
- **Pressure & Depth Sensor:** MS5837 high-resolution digital pressure sensor on I2C (`SDA: GPIO 21`, `SCL: GPIO 22`).
- **Thruster Control:** Low-side switch or single ESC on `GPIO 13`.
- **Wireless Telemetry:** Dual-mode Bluetooth Serial (`SerialBT`) with automatic reconnect.

### Mission State Machine

The profiling cycle executes through an autonomous 9-stage sequence:

| Stage | Mode | Target Depth | Hold Duration | Thruster Behavior |
| :---: | :--- | :---: | :---: | :--- |
| `0` | Cycle 1 Sink | 1.0 m | — | Thruster active until threshold reached |
| `1` | Cycle 1 Hold | 1.0 m | 30 s | Closed-loop depth stabilization (`±0.05 m` band) |
| `2` | Cycle 1 Ascend | 0.4 m | — | Buoyant passive/active rise |
| `3` | Cycle 1 Hold | 0.4 m | 30 s | Closed-loop depth stabilization |
| `4` | Cycle 2 Sink | 1.0 m | — | Repeat profile cycle 2 |
| `5` | Cycle 2 Hold | 1.0 m | 30 s | Closed-loop depth stabilization |
| `6` | Cycle 2 Ascend | 0.4 m | — | Buoyant passive/active rise |
| `7` | Cycle 2 Hold | 0.4 m | 30 s | Closed-loop depth stabilization |
| `8` | Resurface | Surface (`< 0.5 m`) | — | Shut down thruster; initiate Bluetooth telemetry upload |

### Data Logging
Records periodic timestamped depth samples into a circular memory buffer and streams comma-separated telemetry (`timestamp_ms, depth_m`) over Bluetooth upon task completion.
