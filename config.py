"""
PROJECT NAME: ROBOT DOG
DESCRIPTION: Configuration constants and hardware mapping for the robot dog.
DATE: 2025.02.17

Notes / conventions:
- Use snake_case for variable names.
- Global configuration constants are ALLCAPS-style where appropriate.
- Units: lengths and coordinates are in millimetres (mm); angles are in degrees.

This module contains hard-coded robot geometry, servo pin/PWM setup, safety
limits for joint angles and per-servo offsets. Tweak values here when you
calibrate the robot or change hardware wiring.

Data shapes expected by other modules:
- `servo_positions` : list of [servo_pwm_object, last_angle_degrees]
- `robot_memory` : [current_command, next_command] (both are command lists from `commands.py`)

"""
from machine import PWM,Pin




##############################################################################
##############################################################################
#GLOBAL CONSTANTS 

##############################################################################
#Constants for kinematics

# Length of leg segments (see kinematic drawing)
# Units: millimetres (mm)
L1 = 60
L2 = 110
L3 = 110

# values from model; change these to measured values after calibration
L4 = 30
L5 = 36.723  # corrected: use decimal point (float). Previously used a comma which creates a tuple.
L6 = 28.284
L7 = 24
L8 = 15  # servo arm length for our version (mm)
L9 = 20

# Angles placeholder for kinematic calculations (degrees)
theta1 = 0
theta2 = 0
theta3 = 0
theta4 = 0

# Desired coordinates for the end effector (foot) in mm
pos_X = 0
pos_Y = 0
pos_Z = 0

##############################################################################
#Constants for PWM 

#SERVO PINS
servo_pin0 = Pin(6)
servo_pin1 = Pin(7)
servo_pin2 = Pin(8)
servo_pin3 = Pin(0)
servo_pin4 = Pin(1)
servo_pin5 = Pin(2)
servo_pin6 = Pin(9)
servo_pin7 = Pin(10)
servo_pin8 = Pin(11)
servo_pin9 = Pin(3)
servo_pin10 = Pin(4)
servo_pin11 = Pin(5)

#SERVOS
servo_0 =  PWM(servo_pin0)
servo_1 =  PWM(servo_pin1)
servo_2 =  PWM(servo_pin2)
servo_3 =  PWM(servo_pin3)
servo_4 =  PWM(servo_pin4)
servo_5 =  PWM(servo_pin5)
servo_6 =  PWM(servo_pin6)
servo_7 =  PWM(servo_pin7)
servo_8 =  PWM(servo_pin8)
servo_9 =  PWM(servo_pin9)
servo_10 =  PWM(servo_pin10)
servo_11 =  PWM(servo_pin11)

#Set PWM frequency
frequency = 50

servo_0.freq(frequency)
servo_1.freq(frequency)
servo_2.freq(frequency)
servo_3.freq(frequency)
servo_4.freq(frequency)
servo_5.freq(frequency)
servo_6.freq(frequency)
servo_7.freq(frequency)
servo_8.freq(frequency)
servo_9.freq(frequency)
servo_10.freq(frequency)
servo_11.freq(frequency)

##############################################################################
#secure angles constans

#Adduction joint servos:S0 S3 S6 S9

ad_max=85
ad_min=-25

#Hip joint servos: S1 S4 S7 S10 

hip_max=120
hip_min=-20

#Ankle joint servos S2 S5 S8 S11  

ankle_max=135
ankle_min=90



##############################################################################
#offset constans

#FL
offset_s0=0
offset_s1=0
offset_s2=2

#FR
offset_s3=0
offset_s4=3
offset_s5=-5

#BL
offset_s6=0
offset_s7=0
offset_s8=-4

#BR
offset_s9=0
offset_s10=10
offset_s11=3



##############################################################################
##############################################################################


servo_positions=[
   #[servo_name,postion in degree]
    [servo_0,0],
    [servo_1,0],
    [servo_2,0],
    [servo_3,0],
    [servo_4,0],
    [servo_5,0],
    [servo_6,0],
    [servo_7,0],
    [servo_8,0],
    [servo_9,0],
    [servo_10,0],
    [servo_11,0],
]

robot_memory=["",""]