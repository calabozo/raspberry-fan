#!/usr/bin/python3

import subprocess
import time

from gpiozero import OutputDevice

ON_FULL_THRESHOLD = 65
ON_LOW_THRESHOLD = 65  # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 55  # (degress Celsius) Fan shuts off at this temperature.
TEMP_INTERVAL = 5  # (seconds) How often we check the core temperature.
SLEEP_INTERVAL = 0.008


class FanController():
    def __init__(self, gpio_pin=14):        
        self.fan = OutputDevice(gpio_pin)
        self.fan.off()
        self.fan_is_on = False        
        self.last_temp_check=0        
        self.temp=self.get_temp()

    def get_temp(self):        
        if (time.time() - self.last_temp_check) > TEMP_INTERVAL:
            output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
            temp_str = output.stdout.decode()
            self.last_temp_check = time.time()
            try:
                self.temp=float(temp_str.split('=')[1].split('\'')[0])
                return self.temp
            except (IndexError, ValueError):
                raise RuntimeError('Could not parse temperature output.')
        else:
            return self.temp

    def switch_on(self):
        self.fan_is_on = True        
        self.fan.on()

    def switch_off(self):
        self.fan_is_on = False        
        self.fan.off()

    def swith_on_for_cycle(self,secs_on,secs_off):
        self.fan_is_on = True
        self.fan.on()
        time.sleep(secs_on)
        if secs_off>0:
            self.fan.off()
            time.sleep(secs_off)

    def is_fan_on(self):
        return self.fan_is_on

if __name__ == '__main__':    
    if OFF_THRESHOLD >= ON_LOW_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    fan_controller = FanController()

    while True:
        temp = fan_controller.get_temp()        
       
        if temp > ON_LOW_THRESHOLD and not fan_controller.is_fan_on():
            fan_controller.switch_on()
            print("on")
        elif  fan_controller.is_fan_on() and temp < OFF_THRESHOLD:
            fan_controller.switch_off()
            print("off")

        if fan_controller.is_fan_on():
            if temp >= ON_FULL_THRESHOLD:
                fan_controller.swith_on_for_cycle(TEMP_INTERVAL/2,0)
            else:
                fan_controller.swith_on_for_cycle(TEMP_INTERVAL/2,0)
                #fan_controller.swith_on_for_cycle(0.05,SLEEP_INTERVAL)
        else:
            time.sleep(TEMP_INTERVAL)
