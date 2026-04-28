import sys
import time
import select
from machine import Pin
from machine import UART
from config import *
import commands

##############################################################################

uart_controller = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17)) #UART FOR CONTROLLER

##############################################################################
##Calculating duty cycle and mapped value
# 2.5ms max duty (180)
Duty_maxcycle   = (2.5/20)*100  
Mapped_maxvalue = int(Duty_maxcycle*(65535/100))

#0.6ms min duty(0)
Duty_mincycle   = (0.6/20)*100
Mapped_minvalue = int(Duty_mincycle*(65535/100))

# Angle to u_int conv
def angle_conv(angle):
    io_deg=int(((Mapped_maxvalue - Mapped_minvalue)/180))
    return io_deg*int(angle) + Mapped_minvalue

#Map function
def map_func(x, in_min,in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

        
##############################################################################
##############################################################################
#ANGLE FUNCTIONS

#Function for calculate the time till the servo is moving 
#Servo speed= 0.13s per 600 
# 60/0,13=461,540/s == 0,4615 0/ms  
def calculate_time_milis(actual,next):
    
    speed=1000 #461.54 # 0/s 
    
    difference=actual-next

    if difference<0: 
        difference=difference*-1
    
    delay= round(difference/speed,2)
    
    return delay*1000 #to get milis 


#read values form config file 
def read_last_postion(servo):
    for servos in servo_positions: 
        if servos[0] == servo:
            return servos[1] 
        else: 
            pass  

#write values to config file 
def save_servo_position(servo,postion):
    for servos in servo_positions: 
        if servos[0] == servo:  
            servos[1]=postion
        else: 
            pass 


# get servo number
def get_servo_number(servo):         
    num = 0
    if servo == servo_0:
        num = 0
    if servo == servo_1:
        num = 1
    if servo == servo_2:
        num = 2
    if servo == servo_3:
        num = 3
    if servo == servo_4:
        num = 4
    if servo == servo_5:
        num = 5
    if servo == servo_6:
        num = 6
    if servo == servo_7:
        num = 7
    if servo == servo_8:
        num = 8
    if servo == servo_9:
        num = 9
    if servo == servo_10:
        num = 10
    if servo == servo_11:
        num = 11

    return num




#get ofsetcompensation position
def offset_position():
    set_servo_angle(servo_0,0)
    set_servo_angle(servo_1,90)
    set_servo_angle(servo_2,90)
    
    set_servo_angle(servo_3,0)
    set_servo_angle(servo_4,90)
    set_servo_angle(servo_5,90)
    
    set_servo_angle(servo_6,0)
    set_servo_angle(servo_7,90)
    set_servo_angle(servo_8,90)
    
    set_servo_angle(servo_9,0)
    set_servo_angle(servo_10,90)
    set_servo_angle(servo_11,90)


#Angle safety test for each servo, to avoid damage to the robot 
def test_angle(servo,angle): 
#######################################
    # frontLeft
    if servo == servo_0:
        if (ad_max>=angle>=ad_min):
            return True
        else:
            return False 
    elif servo == servo_1:
        if (hip_max>=angle>=hip_min):  
            return True
        else:
            return False 
       
    elif servo == servo_2:
        if (ankle_max>=angle>=ankle_min):
            return True
        else:
            return False 
        
 
    #######################################
    # frontRight
    elif servo == servo_3:
        if (ad_max>=angle>=ad_min):
            return True
        else:
            return False 
       
    elif servo == servo_4:
        if (hip_max>=angle>=hip_min):
            return True
        else:
            return False 
       
    elif servo == servo_5:
        if (ankle_max>=angle>=ankle_min):
            return True
        else:
            return False 
       
 
    #######################################
    # backLeft
    elif servo == servo_6:
        if (ad_max>=angle>=ad_min):
            return True
        else:
            return False 
        
    elif servo == servo_7:
        if (hip_max>=angle>=hip_min):
            return True
        else:
            return False 
       
    elif servo == servo_8:
        if (ankle_max>=angle>=ankle_min):
            return True
        else:
            return False 
        
 
    #######################################
    # backRight
    elif servo == servo_9:
        if (ad_max>=angle>=ad_min):
            return True
        else:
            return False 
        
    elif servo == servo_10:
        if (hip_max>=angle>=hip_min):
            return True
        else:
            return False 
        
    elif servo == servo_11:
        if (ankle_max>=angle>=ankle_min):
            return True
        else:
            return False


#Set servo angle with safety test and time delay for smoother movement
def set_servo_angle(servo, angle,delay=True):   #set_servo_angle
    servoNum=0
    if test_angle(servo,angle):
        #front left
        if servo == servo_0:
            angle=90-angle
            angle=angle+offset_s0   #offset by hand
            servoNum=0
        elif servo == servo_1:
            angle=angle+offset_s1   #offset by hand
            servoNum=1
        elif servo == servo_2:
            angle=angle+offset_s2   #offset by hand
            servoNum=2

        #######################################
        # frontRight
        elif servo == servo_3:
            angle=angle+90
            angle=angle+offset_s3   #offset by hand
            servoNum=3
        elif servo == servo_4:
            angle=90-angle          #offset by hand
            angle=angle+offset_s4   #offset by hand
            servoNum=4
        elif servo == servo_5:
            angle=180-angle
            angle=angle+offset_s5   #offset by hand
            servoNum=5
            
 
        #######################################
        # backLeft
        elif servo == servo_6:
            angle=90-angle
            angle=angle+offset_s6 #offset by hand
            servoNum=6
        elif servo == servo_7:
            angle=angle
            angle=angle+offset_s7 #offset by hand
            servoNum=7       
        elif servo == servo_8:
            angle=180-angle
            angle=angle+offset_s8 #offset by hand
            servoNum=8
 
        #######################################
        # backRight
        elif servo == servo_9:
            angle=angle+90
            angle=angle+offset_s9 #offset by hand
            servoNum=9
        elif servo == servo_10:
            angle=90-angle
            angle=angle+offset_s10 #offset by hand
            servoNum=10
        elif servo == servo_11:
            angle=angle+offset_s11 #offset by hand
            servoNum=11
    
    # Set the servo to the converted angle value
        servo.duty_u16(angle_conv(angle))
        #print(f"servo{servoNum}:{angle}0")
        if delay==True:
            time.sleep_ms(int(calculate_time_milis(read_last_postion(servo),angle)))
            #print(f"{calculate_time_milis(angle,read_last_postion(servo))}ms")
            save_servo_position(servo,angle)
        else:
            pass
        pass
    else:
        servoNum=get_servo_number(servo)
        print(f"Safety angle limit exceeded on servo{servoNum} {angle}0 ")
        pass
        
##############################################################################
##############################################################################
#KINEMATICS FUNCTIONS

"""
Interpolation means "virtual" points between two desired designation.
Which means the movement from one point to a nother is seems lot smoother
Optionaly we can add sleep time for slower transitions 
"""


def interpolation_movement(command,d,delay_row,delay):
    t=round(1/d)
    p_fl0=[0,0,0]
    p_fl1=[0,0,0]
    p_fr0=[0,0,0]
    p_fr1=[0,0,0]
    p_bl0=[0,0,0]
    p_bl1=[0,0,0]
    p_br0=[0,0,0]
    p_br1=[0,0,0]

    for step in range(len(command)): 
        for leg in range (len(command[step])):
            leg_pos=command[step][leg][3]

            if step+1 >= len(command): 
                break


            if leg_pos == "frontLeft":
                x=command[step][leg][0]
                y=command[step][leg][1]
                z=command[step][leg][2]
                p_fl0=[x,y,z]
                x1=command[step+1][leg][0]
                y1=command[step+1][leg][1]
                z1=command[step+1][leg][2]
                p_fl1=[x1,y1,z1]

            if leg_pos == "frontRight":
                x=command[step][leg][0]
                y=command[step][leg][1]
                z=command[step][leg][2]
                p_fr0=[x,y,z]
                x1=command[step+1][leg][0]
                y1=command[step+1][leg][1]
                z1=command[step+1][leg][2]
                p_fr1=[x1,y1,z1]

            if leg_pos == "backLeft":
                x=command[step][leg][0]
                y=command[step][leg][1]
                z=command[step][leg][2]
                p_bl0=[x,y,z]
                x1=command[step+1][leg][0]
                y1=command[step+1][leg][1]
                z1=command[step+1][leg][2]
                p_bl1=[x1,y1,z1]

            if leg_pos == "backRight":
                x=command[step][leg][0]
                y=command[step][leg][1]
                z=command[step][leg][2]
                p_br0=[x,y,z]
                x1=command[step+1][leg][0]
                y1=command[step+1][leg][1]
                z1=command[step+1][leg][2]
                p_br1=[x1,y1,z1]
    
        for x in range(d+1): 

            if step+1 >= len(command): 
                break
            
            if x== delay_row:
                time.sleep_ms(delay)
               
            if p_fl0 != p_fl1:
                t=x*(1/d)
                move_leg((1-t)*p_fl0[0]+t*p_fl1[0],(1-t)*p_fl0[1]+t*p_fl1[1],(1-t)*p_fl0[2]+t*p_fl1[2],"frontLeft")
                print((1-t)*p_fl0[0]+t*p_fl1[0],(1-t)*p_fl0[1]+t*p_fl1[1],(1-t)*p_fl0[2]+t*p_fl1[2],"frontLeft")
            
            if p_fr0 != p_fr1:
                t=x*(1/d)
                move_leg((1-t)*p_fr0[0]+t*p_fr1[0],(1-t)*p_fr0[1]+t*p_fr1[1],(1-t)*p_fr0[2]+t*p_fr1[2],"frontRight")
                print((1-t)*p_fr0[0]+t*p_fr1[0],(1-t)*p_fr0[1]+t*p_fr1[1],(1-t)*p_fr0[2]+t*p_fr1[2],"frontRight")
            if  p_bl0!=p_bl1:
                t=x*(1/d)
                move_leg((1-t)*p_bl0[0]+t*p_bl1[0],(1-t)*p_bl0[1]+t*p_bl1[1],(1-t)*p_bl0[2]+t*p_bl1[2],"backLeft")    
                print((1-t)*p_bl0[0]+t*p_bl1[0],(1-t)*p_bl0[1]+t*p_bl1[1],(1-t)*p_bl0[2]+t*p_bl1[2],"backLeft")
            if p_br0 != p_br1:
                t=x*(1/d)
                move_leg((1-t)*p_br0[0]+t*p_br1[0],(1-t)*p_br0[1]+t*p_br1[1],(1-t)*p_br0[2]+t*p_br1[2],"backRight")
                print((1-t)*p_br0[0]+t*p_br1[0],(1-t)*p_br0[1]+t*p_br1[1],(1-t)*p_br0[2]+t*p_br1[2],"backRight") 

##############################################################################
#ROBOT MEMORY 

def set_next_command(command):
    robot_memory[1]=command 


def set_actual_command(command):
    robot_memory[0]=command

def get_actual_command():
    return robot_memory[0]

##############################################################################

def robot_startup():
    speed=15 
    startup=[commands.lie,commands.stand]
    interpolation_movement(startup,speed)
    set_actual_command(commands.stand)



#Angle safety test for each servo, to avoid damage to the robot 
+def test_angle(servo,angle): 
#######################################
    # frontLeft
    if servo == servo_0:
        if (ad_max>=angle>=ad_min):
            return True
        else:
            return False 
    elif servo == servo_1:
        if (hip_max>=angle>=hip_min):  
            return True
        else:
            return False 
       
    elif servo == servo_2:
        if (ankle_max>=angle>=ankle_min):
            return True
        else:
            return False 
        

    #######################################
    # frontRight
    elif servo == servo_3:
        if (ad_max>=angle>=ad_min):
            return True
        else:
            return False 
       
    elif servo == servo_4:
        if (hip_max>=angle>=hip_min):
            return True
        else:
            return False 
       
    elif servo == servo_5:
        if (ankle_max>=angle>=ankle_min):
            return True
        else:
            return False 
       

    #######################################
    # backLeft
    elif servo == servo_6:
        if (ad_max>=angle>=ad_min):
            return True
        else:
            return False 
        
    elif servo == servo_7:
        if (hip_max>=angle>=hip_min):
            return True
        else:
            return False 
       
    elif servo == servo_8:
        if (ankle_max>=angle>=ankle_min):
            return True
        else:
            return False 
        

    #######################################
    # backRight
    elif servo == servo_9:
        if (ad_max>=angle>=ad_min):
            return True
        else:
            return False 
        
    elif servo == servo_10:
        if (hip_max>=angle>=hip_min):
            return True
        else:
            return False 
        
    elif servo == servo_11:
        if (ankle_max>=angle>=ankle_min):
            return True
        else:
            return False


#Set servo angle with safety test and time delay for smoother movement
+def set_servo_angle(servo, angle,delay=True):   #set_servo_angle
    servoNum=0
    if test_angle(servo,angle):
        #front left
        if servo == servo_0:
            angle=90-angle
            angle=angle+offset_s0   #offset by hand
            servoNum=0
        elif servo == servo_1:
            angle=angle+offset_s1   #offset by hand
            servoNum=1
        elif servo == servo_2:
            angle=angle+offset_s2   #offset by hand
            servoNum=2

        #######################################
        # frontRight
        elif servo == servo_3:
            angle=angle+90
            angle=angle+offset_s3   #offset by hand
            servoNum=3
        elif servo == servo_4:
            angle=90-angle          #offset by hand
            angle=angle+offset_s4   #offset by hand
            servoNum=4
        elif servo == servo_5:
            angle=180-angle
            angle=angle+offset_s5   #offset by hand
            servoNum=5
            

        #######################################
        # backLeft
        elif servo == servo_6:
            angle=90-angle
            angle=angle+offset_s6 #offset by hand
            servoNum=6
        elif servo == servo_7:
            angle=angle
            angle=angle+offset_s7 #offset by hand
            servoNum=7       
        elif servo == servo_8:
            angle=180-angle
            angle=angle+offset_s8 #offset by hand
            servoNum=8

        #######################################
        # backRight
        elif servo == servo_9:
            angle=angle+90
            angle=angle+offset_s9 #offset by hand
            servoNum=9
        elif servo == servo_10:
            angle=90-angle
            angle=angle+offset_s10 #offset by hand
            servoNum=10
        elif servo == servo_11:
            angle=angle+offset_s11 #offset by hand
            servoNum=11
    
    # Set the servo to the converted angle value
+        servo.duty_u16(angle_conv(angle))
+        #print(f"servo{servoNum}:{angle}0")
+        if delay==True:
            time.sleep_ms(int(calculate_time_milis(read_last_postion(servo),angle)))
+            #print(f"{calculate_time_milis(angle,read_last_postion(servo))}ms")
+            save_servo_position(servo,angle)
+        else:
            pass
+        pass
+    else:
+        servoNum=get_servo_number(servo)
+        print(f"Safety angle limit exceeded on servo{servoNum} {angle}0 ")
+        pass
+        
    
##############################################################################
+
...existing code...
