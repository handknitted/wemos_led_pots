from machine import Pin, ADC, PWM
import math
import time
import sys

# set up the adc and digital motor control pins
pot_pin = ADC(0)
analogue_range = 65535
pin7 = Pin(13, Pin.OUT)
pwm_pin7 = PWM(pin7)

pin8 = Pin(15, Pin.OUT)
pwm_pin8 = PWM(pin8)

motor_pwm_pin = PWM(Pin(0, Pin.OUT))
print("Motor PWM freq: %s" % str(motor_pwm_pin.freq()))
motor_pwm_pin.freq(20000)

motor_forward_pin = Pin(5, Pin.OUT)
motor_reverse_pin = Pin(4, Pin.OUT)


leeway = 2000
iteration_count = 0
# set up the screen
while True:
    iteration_count += 1
    print(str(iteration_count))
    control_value = pot_pin.read_u16()
    print("Control value: %s" % str(control_value))
    power_level = int(math.fabs(control_value - (analogue_range/2)) * 2)
    duty = int(1023 * (power_level/65535))
    print("Power level %s" % str(power_level))
    print('Duty: %s' % str(duty))
    motor_pwm_pin.duty(duty)
    if control_value > (65535/2) + leeway:
        # forward motor
        print("Forward")
        pwm_pin8.duty(duty)
        pwm_pin7.duty(0)
        motor_forward_pin(1)
        motor_reverse_pin(0)

    elif control_value < (65535/2) - leeway:
        print("Reverse")
        pwm_pin7.duty(duty)
        pwm_pin8.duty(0)
        motor_forward_pin(0)
        motor_reverse_pin(1)
    else:
        print("Stop   ")
        pwm_pin8.duty(0)
        pwm_pin7.duty(0)
        motor_forward_pin(0)
        motor_reverse_pin(0)

    time.sleep(0.1)

