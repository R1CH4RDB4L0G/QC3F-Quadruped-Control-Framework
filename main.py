"""
PROJECT NAME: ROBOT DOG
DESCRIPTION:inverse kinematis servo contoroll  
DATE:2025.02.17

HOW TO USE THIS CODE 

You have three options for moving the robot 

1. set_angle(servo,angle) moves servo desired anlge
2. move_leg(X,Y,Z,leg) moves endeffector to desired position aka leg
3. interpolate_legs(list,interpolation number aka t)
-> list: [element1,element2]
    ->element:[X,Y,Z,"frontLeft"], [X,Y,Z,"frontRight"], [X,Y,Z,"backLeft"],[X,Y,Z,"backRight"]

"""
import math
import sys
import time
import select
from machine import Pin
from config import *
import commands
import utils


###############
#START UP SEQUENCE
utils.set_position_together([commands.lie])
time.sleep(3)
utils.set_position_together([commands.stand])
time.sleep(1)

while True:
    # utils.interpolation_movement examples for all commands
    # Uncomment one line at a time to run that movement pattern.
    # Parameters: (command, d, delay_row, delay)
    # - command: one of the command lists from commands.py (e.g. commands.trot_ahead)
    # - d: number of interpolation steps (integer > 0)
    # - delay_row: which interpolation step to pause on (integer)
    # - delay: pause time in milliseconds when delay_row is hit

    # Gait / pose examples
    # utils.interpolation_movement(commands.push_up, 3, 1, 150)
    # utils.interpolation_movement(commands.sit, 2, 1, 100)
    # utils.interpolation_movement(commands.stand, 2, 1, 100)
    # utils.interpolation_movement(commands.stand2, 2, 1, 100)
    # utils.interpolation_movement(commands.lie, 2, 1, 100)
    # utils.interpolation_movement(commands.test, 5, 2, 100)

    # Trot / walking examples
    # utils.interpolation_movement(commands.trot_in_space, 4, 2, 50)
    utils.interpolation_movement(commands.trot_ahead,2,5,5)    
    # utils.interpolation_movement(commands.trot_rotate_right, 4, 2, 50)
    # utils.interpolation_movement(commands.trot_rotate_left, 4, 2, 50)
    # utils.interpolation_movement(commands.trot_side_left, 4, 2, 50)
    # utils.interpolation_movement(commands.trot_side_right, 4, 2, 50)

    pass

