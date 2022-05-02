import serial
import pandas as pd
import pygame
import time

# Open the serial port. 
ser = serial.Serial(port='COM7', baudrate=115200, timeout=1)

while True:
    # MOVE THE FUCKING ARM
    predictions = pd.read_csv('DIY_EEG/all_pred.csv', sep=',',header=None).to_numpy()
    last_pred = int(predictions[-1])
    print(last_pred)

    if last_pred == -1:
        ser.write(bytes(str(1), 'utf-8'))      # Send the string to the serial port.
        print("Sent %s to Arduino" % str)
        current_pred = last_pred
    else:
        ser.write(bytes(str(3), 'utf-8'))      # Send the string to the serial port.
        print("Sent %s to Arduino" % str)
    time.sleep(2)
