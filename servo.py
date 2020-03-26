from Tkinter import*
import RPi.GPIO as GPIO
#import RPi
import time 
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) 
pwm=GPIO.PWM(18,100)
pwm.start(5)
angle1=10
duty1= float(angle1)/10 + 2.5
angle2=160
duty2= float(angle2)/10 + 2.5
ck=0
while ck<1:
     pwm.ChangeDutyCycle(duty2)
     time.sleep(10.5)
     pwm.ChangeDutyCycle(duty1)
     time.sleep(1.5)
     ck=ck+1
time.sleep(1)
GPIO.cleanup()