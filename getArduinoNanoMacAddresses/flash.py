import os
import csv
import serial.tools.list_ports
import time
import re

isboardDetected=False
arduinoSerialPort = ""
savedMacAddresses=[]
macAddressPattern = re.compile("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")

def detectArduinoConnected():

    global isboardDetected
    global arduinoSerialPort
    print()
    print("********************")
    print("Looking for Arduino Boards")
    print("********************")

    ports = list(serial.tools.list_ports.comports())
    Arduino_ports=[]
    for p in ports:
        if 'Arduino' in p.description:
            Arduino_ports.append(p)
    if len(Arduino_ports)==0:
        #print("no Arduino board detected")
        isboardDetected=False
        return False
    else :
        #print(Arduino_ports[0].device)
        isboardDetected=True
        arduinoSerialPort=Arduino_ports[0].device
        return True

def uploadFrimware():
    global arduinoSerialPort

    print()
    print("********************")
    print("found board on port: "+arduinoSerialPort)
    print("starting to flash the firmware...")
    print("********************")

    command = "arduino-cli upload"
    fqbn = "arduino:samd:nano_33_iot"
    firmware_folder = " ./printMacAddress"

    commandString=command +" -p "+ arduinoSerialPort +" --fqbn "+ fqbn +" "+ firmware_folder;
    myCmd = os.popen(commandString).read()
    print(myCmd)

def loop():
    if (isboardDetected==False):
        detectArduinoConnected()
        time.sleep(2)
        loop()
    else:
        uploadFrimware()
        time.sleep(3)
        newMacAddress=getMacAddressFromSerialPort()
        if (newMacAddress!=0):
            if (isMacAddressInTheList(newMacAddress)):
                print()
                print("********************")
                print("address already present")
                print("********************")
                waitForArduinoToDisconnect()
                loop()
            else:
                print()
                print("********************")
                print("adding mac address to csv")
                print("********************")
                addMacToCSV(newMacAddress)
                waitForArduinoToDisconnect()
                loop()

def getMacAddressesInMemory():
    global savedMacAddresses
    with open('macAddresses.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            savedMacAddresses.append(row[0])

def getMacAddressFromSerialPort():
    global arduinoSerialPort
    with serial.Serial(arduinoSerialPort, 9600, timeout=2) as ser:
        line = ser.readline().strip()   # read a '\n' terminated line
        macAddress = line.decode('ascii')
        if (macAddressPattern.match(macAddress)):
            return macAddress
        else:
            return 0

def isMacAddressInTheList(mac):
    global savedMacAddresses
    for m in savedMacAddresses:
        if mac==m:
            return True
    return False

def addMacToCSV(mac):
    with open('macAddresses.csv','a') as csv_file:
        csv_file.write(mac)

def waitForArduinoToDisconnect():
    if (detectArduinoConnected()==True):
        print()
        print("********************")
        print("DONE!!!")
        print("please plug a new board...")
        print("********************")

        time.sleep(2)
        waitForArduinoToDisconnect()
    else:
        print()
        print("********************")
        print("arduino disconnected!!!")
        print("********************")

# here I start the software
getMacAddressesInMemory()
loop()
