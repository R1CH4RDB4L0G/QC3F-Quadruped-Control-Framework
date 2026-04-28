from machine import Pin

from config import *
import math
import sys
import time
import select



"""
PROJECT NAME: ROBOT DOG
DESCRIPTION:inverse kinematis servo contoroll  
DATE:2025.04.13
name convention: snake case, global variables allcaps

HOW TO USE THIS CODE 

You have three options for moving the robot 

1. set_angle(servo,angle) moves servo desired anlge
2. move_to_postion(X,Y,Z,leg) moves endeffector to desired position

  FRONT
+--------+
| FL  FR |  ^   
|        |  |  Moving 
| BL  BR |  |   direction 
+--------+
   BACK


"""

push_up=[
        [[20,60,163,"frontLeft"], [20,60,160,"frontRight"], [20,60,163,"backLeft"],[20,60,160,"backRight"]],
        [[20,60,100,"frontLeft"], [20,60,100,"frontRight"], [20,60,100,"backLeft"],[20,60,100,"backRight"]],
        [[20,60,163,"frontLeft"], [20,60,160,"frontRight"], [20,60,163,"backLeft"],[20,60,160,"backRight"]],
        ]



sit=[   
    [20,60,120,"frontLeft"], [20,60,120,"frontRight"], [20,60,80,"backLeft"],[20,60,80,"backRight"]
    ]


stand=[   
    [20,60,160,"frontLeft"], [20,60,160,"frontRight"], [20,60,160,"backLeft"],[20,60,160,"backRight"]
    ]

stand2=[   
    [20,60,160,"frontLeft"], [20,60,160,"frontRight"], [40,60,160,"backLeft"],[40,60,160,"backRight"]
    ]


lie=[   
    [20,60,80,"frontLeft"], [20,60,80,"frontRight"], [20,60,80,"backLeft"],[20,60,80,"backRight"]
    ]


test=[
    [[20,60,120,"frontLeft"], [20,60,120,"frontRight"], [20,60,80,"backLeft"],[20,60,80,"backRight"]],
    [ [20,60,160,"frontLeft"], [20,60,160,"frontRight"], [20,60,160,"backLeft"],[20,60,160,"backRight"]],
    ]




trot_in_space = [

    [[0,60,160,"frontRight"], [0,60,160,"backLeft"], [0,60,130,"frontLeft"], [0,60,130,"backRight"]],
    [[0,60,160,"frontRight"], [0,60,160,"backLeft"], [0,60,140,"frontLeft"], [0,60,140,"backRight"]],
    [[0,60,160,"frontRight"], [0,60,160,"backLeft"], [0,60,150,"frontLeft"], [0,60,150,"backRight"]],
    [[0,60,150,"frontRight"], [0,60,150,"backLeft"], [0,60,160,"frontLeft"], [0,60,160,"backRight"]],
    [[0,60,140,"frontRight"], [0,60,140,"backLeft"], [0,60,160,"frontLeft"], [0,60,160,"backRight"]],
    [[0,60,130,"frontRight"], [0,60,130,"backLeft"], [0,60,160,"frontLeft"], [0,60,160,"backRight"]],
    [[0,60,140,"frontRight"], [0,60,140,"backLeft"], [0,60,160,"frontLeft"], [0,60,160,"backRight"]],
    [[0,60,150,"frontRight"], [0,60,150,"backLeft"], [0,60,160,"frontLeft"], [0,60,160,"backRight"]],
    [[0,60,160,"frontRight"], [0,60,160,"backLeft"], [0,60,150,"frontLeft"], [0,60,150,"backRight"]],
    [[0,60,160,"frontRight"], [0,60,160,"backLeft"], [0,60,140,"frontLeft"], [0,60,140,"backRight"]],

]


trot_ahead= [

    [[0,60,160,"frontRight"],   [50,60,160,"backLeft"],  [0,60,130,"frontLeft"],     [50,60,130,"backRight"]],
    [[10,60,160,"frontRight"],  [60,60,160,"backLeft"], [-10,60,140,"frontLeft"],   [40,60,140,"backRight"]],
    [[20,60,160,"frontRight"],  [70,60,160,"backLeft"], [-20,60,150,"frontLeft"],   [30,60,150,"backRight"]],
    [[20,60,150,"frontRight"],  [70,60,150,"backLeft"], [-20,60,160,"frontLeft"],   [30,60,160,"backRight"]],
    [[10,60,140,"frontRight"],  [60,60,140,"backLeft"], [-10,60,160,"frontLeft"],   [40,60,160,"backRight"]],
    [[0,60,130,"frontRight"],   [50,60,130,"backLeft"],  [0,60,160,"frontLeft"],     [50,60,160,"backRight"]],
    [[-10,60,140,"frontRight"], [40,60,140,"backLeft"],[10,60,160,"frontLeft"],    [60,60,160,"backRight"]],
    [[-20,60,150,"frontRight"], [30,60,150,"backLeft"],[20,60,160,"frontLeft"],    [70,60,160,"backRight"]],
    [[-20,60,160,"frontRight"], [30,60,160,"backLeft"],[20,60,150,"frontLeft"],    [70,60,150,"backRight"]],
    [[-10,60,160,"frontRight"], [40,60,160,"backLeft"],[10,60,140,"frontLeft"],    [60,60,140,"backRight"]],

]

trot_rotate_right = [

    [[0,70,160,"frontRight"],   [10,70,160,"backLeft"],  [0,70,130,"frontLeft"], [10,70,130,"backRight"]],
    [[0,65,160,"frontRight"],   [10,65,160,"backLeft"],  [0,65,140,"frontLeft"], [10,65,140,"backRight"]],
    [[0,60,160,"frontRight"],   [10,60,160,"backLeft"],  [0,60,150,"frontLeft"], [10,60,150,"backRight"]],
    [[0,60,150,"frontRight"],   [10,60,150,"backLeft"],  [0,60,160,"frontLeft"], [10,60,160,"backRight"]],
    [[0,65,140,"frontRight"],   [10,65,140,"backLeft"],  [0,65,160,"frontLeft"], [10,65,160,"backRight"]],
    [[0,70,130,"frontRight"],   [10,70,130,"backLeft"],  [0,70,160,"frontLeft"], [10,70,160,"backRight"]],
    [[0,75,140,"frontRight"],   [10,75,140,"backLeft"],  [0,75,160,"frontLeft"], [10,75,160,"backRight"]],
    [[0,80,150,"frontRight"],   [10,80,150,"backLeft"],  [0,80,160,"frontLeft"], [10,80,160,"backRight"]],
    [[0,80,160,"frontRight"],   [10,80,160,"backLeft"],  [0,80,150,"frontLeft"], [10,80,150,"backRight"]],
    [[0,75,160,"frontRight"],   [10,75,160,"backLeft"],  [0,75,140,"frontLeft"], [10,75,140,"backRight"]],

]

trot_rotate_left = [
    [[0,70,160,"frontRight"], [10,70,160,"backLeft"], [0,70,130,"frontLeft"], [10,70,130,"backRight"]],
    [[0,75,160,"frontRight"], [10,75,160,"backLeft"], [0,75,140,"frontLeft"], [10,75,140,"backRight"]],
    [[0,80,160,"frontRight"], [10,80,160,"backLeft"], [0,80,150,"frontLeft"], [10,80,150,"backRight"]],
    [[0,80,150,"frontRight"], [10,80,150,"backLeft"], [0,80,160,"frontLeft"], [10,80,160,"backRight"]],
    [[0,75,140,"frontRight"], [10,75,140,"backLeft"], [0,75,160,"frontLeft"], [10,75,160,"backRight"]],
    [[0,70,130,"frontRight"], [10,70,130,"backLeft"], [0,70,160,"frontLeft"], [10,70,160,"backRight"]],
    [[0,65,140,"frontRight"], [10,65,140,"backLeft"], [0,65,160,"frontLeft"], [10,65,160,"backRight"]],
    [[0,60,150,"frontRight"], [10,60,150,"backLeft"], [0,60,160,"frontLeft"], [10,60,160,"backRight"]],
    [[0,60,160,"frontRight"], [10,60,160,"backLeft"], [0,60,150,"frontLeft"], [10,60,150,"backRight"]],
    [[0,65,160,"frontRight"], [10,65,160,"backLeft"], [0,65,140,"frontLeft"], [10,65,140,"backRight"]],
]

trot_side_left= [

    [[0,70,130,"frontRight"],   [20,70,130,"backLeft"],  [0,70,160,"frontLeft"], [20,70,160,"backRight"]],
    [[0,65,140,"frontRight"],   [20,75,140,"backLeft"],  [0,65,160,"frontLeft"], [20,75,160,"backRight"]],
    [[0,60,150,"frontRight"],   [20,80,150,"backLeft"],  [0,60,160,"frontLeft"], [20,80,160,"backRight"]],
    [[0,60,160,"frontRight"],   [20,80,160,"backLeft"],  [0,60,150,"frontLeft"], [20,80,150,"backRight"]],
    [[0,65,160,"frontRight"],   [20,75,160,"backLeft"],  [0,65,140,"frontLeft"], [20,75,140,"backRight"]],
    [[0,70,160,"frontRight"],   [20,70,160,"backLeft"],  [0,70,130,"frontLeft"], [20,70,130,"backRight"]],
    [[0,75,160,"frontRight"],   [20,65,160,"backLeft"],  [0,75,140,"frontLeft"], [20,65,140,"backRight"]],
    [[0,80,160,"frontRight"],   [20,60,160,"backLeft"],  [0,80,150,"frontLeft"], [20,60,150,"backRight"]],
    [[0,80,150,"frontRight"],   [20,60,150,"backLeft"],  [0,80,150,"frontLeft"], [20,60,150,"backRight"]],
    [[0,75,140,"frontRight"],   [20,65,140,"backLeft"],  [0,75,160,"frontLeft"], [20,65,160,"backRight"]],

]

trot_side_right= [

    [[0,70,130,"frontRight"],   [10,70,130,"backLeft"],  [0,70,160,"frontLeft"], [10,70,160,"backRight"]],
    [[0,75,140,"frontRight"],   [10,65,140,"backLeft"],  [0,75,160,"frontLeft"], [10,65,160,"backRight"]],
    [[0,80,150,"frontRight"],   [10,60,150,"backLeft"],  [0,80,160,"frontLeft"], [10,60,160,"backRight"]],
    [[0,80,160,"frontRight"],   [10,60,160,"backLeft"],  [0,80,150,"frontLeft"], [10,60,150,"backRight"]],
    [[0,75,160,"frontRight"],   [10,65,160,"backLeft"],  [0,75,140,"frontLeft"], [10,65,140,"backRight"]],
    [[0,70,160,"frontRight"],   [10,70,160,"backLeft"],  [0,70,130,"frontLeft"], [10,70,130,"backRight"]],
    [[0,65,160,"frontRight"],   [10,75,160,"backLeft"],  [0,65,140,"frontLeft"], [10,75,140,"backRight"]],
    [[0,60,160,"frontRight"],   [10,80,160,"backLeft"],  [0,60,150,"frontLeft"], [10,80,150,"backRight"]],
    [[0,60,150,"frontRight"],   [10,80,150,"backLeft"],  [0,60,150,"frontLeft"], [10,80,150,"backRight"]],
    [[0,65,140,"frontRight"],   [10,75,140,"backLeft"],  [0,65,160,"frontLeft"], [10,75,160,"backRight"]],

]
