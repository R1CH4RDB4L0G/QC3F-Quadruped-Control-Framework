# QC3F – Quadruped Control Framework

A quadruped robot dog with inverse kinematics servo control, built with MicroPython.

## Overview
This project implements a four‑legged robot‑dog control framework with multiple gaits and varios movements powered by inverse kinematics for example(gait,trot,sit,stand). It provides a modular control platform for a 4‑leg, 3‑DOF‑per‑leg setup, allowing users to operate the robot at different abstraction levels. The code is written in MicroPython and was tested on a Raspberry Pi Pico.

## Project Details

- **Project Name**: QC3F – Quadruped Control Framework
- **Description**: Inverse kinematics servo control for a quadruped robot
- **Date**: 2025.02.17
- **Platform**: MicroPython (Raspberry Pi Pico or similar)

## Hardware

- 4 legs with 3 servos each (12 servos total)
- UART controller interface
- PWM servo control

## Installation

1. Flash MicroPython to your microcontroller
2. Copy all Python files to the device:
   - `main.py` - Entry point
   - `config.py` - Configuration and constants
   - `commands.py` - Movement commands
   - `utils.py` - Utility functions

## Usage

### Basic Movement Functions

There are three primary ways to control the robot:

1. **Direct Servo Control**
   ```python
   set_angle(servo, angle)
   ```
   Moves a specific servo to the desired angle.

2. **Leg Position Control**
   ```python
   move_leg(X, Y, Z, leg)
   ```
   Moves the end effector of a leg to the desired 3D position.

3. **Interpolated Movement**
   ```python
   interpolate_legs(list, t)
   ```
   Smoothly interpolates between poses.
   - `list`: List of leg positions
   - `t`: Interpolation step number

### Available Commands

| Command | Description |
|---------|-------------|
| `push_up` | Robot performs a push-up motion |
| `sit` | Robot sits down |
| `stand` | Robot stands up |
| `stand2` | Alternative standing pose |
| `lie` | Robot lies down |
| `test` | Test sequence for debugging |
| `trot_in_space` | Trot gait in place |
| `trot_ahead` | Forward trot movement |
| `trot_rotate_right` | Rotate right while trotting |
| `trot_rotate_left` | Rotate left while trotting |
| `trot_side_left` | Side step left while trotting |
| `trot_side_right` | Side step right while trotting |

### Leg Configuration

```
   FRONT
+--------+
| FL  FR |  ^   
|        |  |  Moving 
| BL  BR |  |   direction 
+--------+
   BACK
```

- **FL**: Front Left
- **FR**: Front Right
- **BL**: Back Left
- **BR**: Back Right

### Running Movements

Uncomment desired movement in `main.py`:

```python
utils.interpolation_movement(commands.stand, 2, 1, 100)
```

Parameters:
- `command`: Command list from commands.py
- `d`: Number of interpolation steps (integer > 0)
- `delay_row`: Which step to pause on
- `delay`: Pause time in milliseconds

## Configuration

Edit `config.py` to customize:

- **Kinematic Parameters**: Leg segment lengths (L1-L9)
- **Servo Pins**: GPIO pin assignments
- **Safety Limits**: Joint angle limits
- **Per-servo Offsets**: Calibration values

### Units

- Lengths and coordinates: millimetres (mm)
- Angles: degrees

## File Structure

```
.
├── main.py      # Entry point and startup sequence
├── config.py    # Hardware configuration and constants
├── commands.py  # Pre-defined movement commands
└── utils.py     # Utility functions for movement control
```
