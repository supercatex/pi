import serial
import RPi.GPIO as GPIO
import time
import sys
import pynmea2

filename1 = '/home/pi/workspace/data/GPSx.txt'
filename2 = '/home/pi/workspace/data/GPSy.txt'
port = '/dev/tty' + sys.argv[1]

def run():
	ser = serial.Serial(
		port = port,
		baudrate = 9600,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS,
		timeout = 1
	)
	ser.flushInput()

	count = 1
	while True:#c
		x = ser.readline()
		print(x)
		#continue
		if x.startswith(b'$GNRMC'):
			msg = pynmea2.parse(str(x, 'UTF-8'))
			print(msg)
			print(str(count) + ", lat: " + msg.lat + ", lon: " + msg.lon)
			count = count + 1
			
			with open(filename1, 'w') as the_file:
				the_file.write(msg.lat)
			with open(filename2, 'w') as the_file:
				the_file.write(msg.lon)

while True:
	with open(filename1, 'w') as the_file:
		the_file.write('')
	with open(filename2, 'w') as the_file:
		the_file.write('')
			
	try:
		run()
	except Exception as e:
		print(str(e))
		print('unknown port ' + port)

	time.sleep(3)
	#break

	
