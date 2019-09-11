# MAC address batch collector

This script is intended to automatically collect a big amount of mac addresses from Arduino nano 33 Iot Boards

## how to use it

1. you need python
2. you need to have the Arduino samd Core installed
3. you need to install the arduino-cli following the guide [here](https://github.com/arduino/arduino-cli)
4. you will need to install [pySerial](https://pythonhosted.org/pyserial/)
5. execute the script, I do it running `python3 flash.py`
6. follow the instruction given by the script, and just keep on plugging in new boards

## how does it works
- The script scans the serial ports until a new Arduino is detected
- Once detected it upload a sketch to the board which will make the Arduino print its wifi mac address to the serial port
- Then it opens a serial connection with the board and waits to receive the mac address
- Once collected, it look if the mac address is well formed, check the csv file for duplicates and eventually it adds the new entry to the file
