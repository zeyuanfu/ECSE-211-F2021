import brickpi3
from utils.brick import EV3UltrasonicSensor, configure_ports, TouchSensor, EV3ColorSensor
import math
from time import sleep

US_SENSOR, COLOR_SENSOR = configure_ports(PORT_3=EV3UltrasonicSensor, PORT_4=EV3ColorSensor)

BP = brickpi3.BrickPi3() # instantiate brickPi
CONVEYOR = BP.PORT_A   #Set motor ports
SHUFFLER = BP.PORT_B
PUSHER = BP.PORT_D
ROTATOR = BP.PORT_C

Conveyor_Speed = 25
Drop_Speed = 25
Shuffler_Speed = 35
Pusher_Speed = 50
Rotator_Speed = 20
Conveyor_Drop_Angle = 220

min_dist = 10
max_dist = 13


try:
    def determineColor() -> str:
        #This function determines the color of the block
        try:
            
            colorVal = COLOR_SENSOR.get_value()
   
            R = colorVal[0]
            G = colorVal[1]
            B = colorVal[2]
            
            if (687.25*R-416.25*G-1547*B+2458.375 > 0): 
                if (556.5*R-2185.5*G+2242.5*B+675 > 0): 
                    if (160*R+1164*G+6499*B-263716 > 0):
                        return "orange"
                    else:
                        return "red"
                else:
                    return "yellow"
            else: # purple green blue
                if (-41.5*R+10259*G-8088*B-165463 > 0):
                    return "green"
                else:
                    if (1155*R-665*G-80*B-13125 > 0):
                        return "purple"
                    else:
                        return "blue"
            

        except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
            pass

    def WaitForMotor(Motor):
        sleep(0.5)
        while(BP.get_motor_status(Motor)[3]!=0):
            sleep(0.05)

    def ConveyorControl():
        print("conveyor started")
        
        while True:
            try:
                us_data = US_SENSOR.get_value()
                sleep(0.1)
    
                
                if (us_data < min_dist or us_data > max_dist):
                    BP.set_motor_power(CONVEYOR,0)
                    sleep(0.05)
                    BP.set_motor_power(SHUFFLER,0)
                    sleep(0.05)
                    BP.set_motor_limits(CONVEYOR,Drop_Speed)
                    BP.set_motor_position_relative(CONVEYOR,-Conveyor_Drop_Angle)
                    sleep(2.4) #wait for the object to drop
                    
                    #call sensing function because object was dropped
                    SenseAndSort()
                    ##
                    BP.set_motor_power(SHUFFLER,Shuffler_Speed)
                    sleep(0.1)
                    BP.set_motor_limits(CONVEYOR,Conveyor_Speed)
                    BP.set_motor_power(CONVEYOR,-Conveyor_Speed)
                else:
                    BP.set_motor_power(CONVEYOR,-Conveyor_Speed)
                    sleep(0.1)
                
                
            except brickpi3.SensorError as error:
                print(error)
    
    red_angle = -90
    green_angle = -60
    blue_angle = - 30
    purple_angle = 0
    orange_angle = 30
    yellow_angle = 80

    def SenseAndSort():
        
        color = determineColor()
        print(color)

        if (color == "red"):
            MoveAndDrop(red_angle)
        elif (color == "green"):
            MoveAndDrop(green_angle)
        elif (color == "blue"):
            MoveAndDrop(blue_angle)
        elif (color == "purple"):
            MoveAndDrop(purple_angle)
        elif (color == "orange"):
            MoveAndDrop(orange_angle)
        elif (color == "yellow"):
            MoveAndDrop(yellow_angle)
        
        return True
        
    
    def MoveAndDrop(angle):
        BP.set_motor_limits(ROTATOR,Rotator_Speed)
        BP.set_motor_position(ROTATOR,angle)
        sleep(0.2)
        BP.set_motor_limits(PUSHER,Pusher_Speed)
        BP.set_motor_position_relative(PUSHER,-367)
        sleep(1.5)
        BP.set_motor_limits(ROTATOR,100)
        BP.set_motor_position(ROTATOR,0)
        BP.set_motor_limits(ROTATOR,Rotator_Speed)

    if __name__ == "__main__":
        print("Program started")
   
        BP.set_motor_power(SHUFFLER,Shuffler_Speed)
        
        BP.offset_motor_encoder(PUSHER,BP.get_motor_encoder(PUSHER))
        BP.offset_motor_encoder(ROTATOR,BP.get_motor_encoder(ROTATOR))
        
        ConveyorControl()
        

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
    exit
