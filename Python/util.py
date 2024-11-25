import time   # time related library
import sys,os    # system related library
import numpy as np
import matplotlib.pyplot as plt
import ok     # OpalKelly library
import pyvisa as visa # You should pip install pyvisa and restart the kernel.


def reset_sensors(dev):
    dev.SetWireInValue(0x01, 1)
    dev.UpdateWireIns()
    time.sleep(0.5)
    dev.SetWireInValue(0x01, 0)
    dev.UpdateWireIns()
    time.sleep(0.1)

def SPI_write_to_device(dev, reg_addr, value):
    dev.SetWireInValue(0x00, 0) 
    dev.UpdateWireIns()
    dev.SetWireInValue(0x02, reg_addr) 
    dev.SetWireInValue(0x03, value)
    dev.UpdateWireIns()  # Update the WireIns
    time.sleep(0.1)
    dev.SetWireInValue(0x00, 1) # Write trigger
    dev.UpdateWireIns()  # Update the WireIns
    time.sleep(0.1)
    dev.SetWireInValue(0x00, 0) 
    dev.UpdateWireIns()  # Update the WireIns
    

def SPI_read_from_device(dev, reg_addr):
    dev.SetWireInValue(0x00, 0) 
    dev.UpdateWireIns()  # Update the WireIns
    time.sleep(0.1)
    dev.SetWireInValue(0x02, reg_addr)
    dev.SetWireInValue(0x00, 2)  # Read trigger
    dev.UpdateWireIns()  # Update the WireIns
    time.sleep(0.1)
    dev.UpdateWireOuts()
    read = dev.GetWireOutValue(0x20)
    dev.SetWireInValue(0x00, 0) 
    dev.UpdateWireIns() 
    return read

def setup_sensors(dev):
    print("setting up...")
    reset_sensors(dev)
    SPI_write_to_device(3, 8, dev)
    SPI_write_to_device(4, 160, dev)
    SPI_write_to_device(57, 3, dev)
    SPI_write_to_device(58, 44, dev)
    SPI_write_to_device(59, 240, dev)
    SPI_write_to_device(60, 10, dev)
    SPI_write_to_device(69, 9, dev)
    SPI_write_to_device(80, 2, dev)
    SPI_write_to_device(83, 187, dev)
    SPI_write_to_device(97, 240, dev)
    SPI_write_to_device(98, 10, dev)
    SPI_write_to_device(100, 112, dev)
    SPI_write_to_device(101, 98, dev)
    SPI_write_to_device(102, 34, dev)
    SPI_write_to_device(103, 64, dev)
    SPI_write_to_device(106, 94, dev)
    SPI_write_to_device(107, 110, dev)
    SPI_write_to_device(108, 91, dev)
    SPI_write_to_device(109, 82, dev)
    SPI_write_to_device(110, 80, dev)
    SPI_write_to_device(117, 91, dev)
    print("setting up done")

def read_a_frame(dev, HS_counter):
    buf = bytearray(315392)
    dev.SetWireInValue(0x01, HS_counter)
    dev.UpdateWireIns()
    dev.ReadFromBlockPipeOut(0xa0, 1024, buf)
    read_output = I2C_read_from_device(dev)
    # x_a_read = read_output[0]
    # print("x-acceleration read is " + str(x_a_read / 16000) + " g")
    # y_a_read = read_output[1]
    # print("y-acceleration read is " + str(y_a_read / 16000) + " g")
    # z_a_read = read_output[2]
    # print("z-acceleration read is " + str(z_a_read / 16000) + " g")
    # x_m_read = read_output[3]
    # print("x-magnetic read is " + str(x_m_read))
    # y_m_read = read_output[4]
    # print("y-magnetic read is " + str(y_m_read))
    # z_m_read = read_output[5]
    # print("z-magnetic read is " + str(z_m_read))
    return buf, read_output

# dir = 0 => forward, dir = 1 => backward
def run_motor(dev, direction, duration):
    pmod_util = duration + 3 * 2 ** 30
    pmod_util = pmod_util + (3 * direction) * 2 ** 28
    dev.SetWireInValue(0x04, pmod_util)
    dev.UpdateWireIns()
    time.sleep(0.2)
    dev.SetWireInValue(0x04, 0)
    dev.UpdateWireIns()

def I2C_read_from_device(dev):
    dev.UpdateWireOuts()
    read_output = (0,0,0,0,0,0)
    for i in range(6):
        read = dev.GetWireOutValue(0x21 + i)
        if i >= 3:
            m_L = read // 2**8
            m_H = read - (m_L * 2**8)
            read =  m_H * 2**8 + m_L
        if read >= 2**15:
            read = read - 2**16 # deal with 2's complement
        read_output[i] = read
    return read_output

def instrumentation_setup():
    # This section of the code cycles through all USB connected devices to the computer.
    # The code figures out the USB port number for each instrument.
    # The port number for each instrument is stored in a variable named “instrument_id”
    # If the instrument is turned off or if you are trying to connect to the 
    # keyboard or mouse, you will get a message that you cannot connect on that port.
    # Only need power supply for final
    device_manager = visa.ResourceManager()
    devices = device_manager.list_resources()
    number_of_device = len(devices)
    power_supply_id = -1

    # assumes only the DC power supply is connected
    for i in range (0, number_of_device):
    # check that it is actually the power supply
        try:
            device_temp = device_manager.open_resource(devices[i])
            print("Instrument connect on USB port number [" + str(i) + "] is " + device_temp.query("*IDN?"))
            if (device_temp.query("*IDN?") == 'HEWLETT-PACKARD,E3631A,0,3.2-6.0-2.0HEWLETT-PACKARD,E3631A,0,3.2-6.0-2.0\r\n'):
                power_supply_id = i
            if (device_temp.query("*IDN?") == 'HEWLETT-PACKARD,E3631A,0,3.0-6.0-2.0\r\n'):
                power_supply_id = i
            device_temp.close()
        except:
            print("Instrument on USB port number [" + str(i) + "] cannot be connected. The instrument might be powered of or you are trying to connect to a mouse or keyboard.\n")
        
    # Open the USB communication port with the power supply.
    # The power supply is connected on USB port number power_supply_id.
    # If the power supply ss not connected or turned off, the program will exit.
    # Otherwise, the power_supply variable is the handler to the power supply
        
    if (power_supply_id == -1):
        print("Power supply instrument is not powered on or connected to the PC.")    
    else:
        print("Power supply is connected to the PC.")
        power_supply = device_manager.open_resource(devices[power_supply_id]) 
    return power_supply