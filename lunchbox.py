########################################################################
#                                                                      #
#                  The Official ISP Lunchbox                           #
#                                                                      #
########################################################################




import RPi.GPIO as GPIO
import random


led1 = 7
led2 = 8
led3 = 10
led4 = 11
led5 = 12

sw1U = 13
sw1D = 15
sw2U = 16
sw2D = 18
sw3U = 19
sw3D = 21
sw4U = 22
sw4D = 23
sw5U = 24
sw5D = 26
TS   = 27
most_recent_event = 0


pin_list_output = [led1, led2, led3, led4, led5]
pin_list_input = [sw1U, sw1D, sw2U, sw2D, sw3U, sw3D, sw4U, sw4D, sw5U, sw5D, TS]

last_state = []
state_list = []



############################### Utility Functions #######################################

def get_state():
  global state_list
  state_list = [GPIO.input(sw1U),GPIO.input(sw1D),GPIO.input(sw2U),GPIO.input(sw2D),GPIO.input(sw3U),GPIO.input(sw3U),GPIO.input(sw4U),GPIO.input(sw4D),GPIO.input(sw5U),GPIO.input(sw5D),GPIO.input(TS)]
  return state_list

def get_state_binary():
  input_state = int("".join(state_list))
  return input_state
      

def add_light(light_list):
  GPIO.output(light_list, 1)

def light_one(light):
  GPIO.output(pin_list_output, 0)
  GPIO.output(light, 1)

def event_callback(): 
  for key in range(0,10):
    if GPIO.event_detected(pin_list_input[key]):
      return key
   
  

#################################### States #########################################
def state0():
  GPIO.output(pin_list_output, 0)
  GPIO.output(pin_list_output[last_event_key],1)
  while 1: 
    if last_event_key == 1 or 2:
      return state1
    

def state1():
  light_one(1)
  while 1:
    if last_event_key == 3 or 4:
      return state2
    else:
      return state0

def state2():
  add_light(2)
  while 1:
    if last_event_key == 5 or 6:
      return state3
    else:
      return state0

def state3():
  add_light(3)
  while 1:
    if last_event_key == 7 or 8:
      return state4
    else:
      return state0

def state4():
  add_light(4)
  while 1:
    if last_event_key == 9 or 10:
      return state5
    else:
      return state0

def state5():
  GPIO.output(pin_list_output, 1)

def obfuscate():
  numLights = random.uniform(1,5)
  print(numLights)

#____________________________Begin doing Stuff____________________________________#

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_list_input, GPIO.IN)
GPIO.setup(pin_list_output, GPIO.OUT)
for channel in pin_list_input:
  GPIO.add_event_detect(channel, GPIO.BOTH, callback=event_callback(), bouncetime=300) 



state = state0
while 1:
  last_event_key = event_callback()
  state: state = state()



GPIO.cleanup()           # clean up GPIO on normal exit  
