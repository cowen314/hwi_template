from .device import Device

if __name__ == "__main__":
    thermocouple_device = Device()
    water_heater = Device()
    temperature_controller = ()
    while(1):

        thermocouple_device.write_outputs()
