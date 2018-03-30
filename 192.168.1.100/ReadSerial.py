import serial
import RPi.GPIO as GPIO
import time
import sys

filename = '/home/pi/workspace/data/unknown.txt'
port = '/dev/tty' + sys.argv[1]

def run():
	ser = serial.Serial(
		port = port,
		baudrate = 9600,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS,
		timeout = 0.5
	)

	while True:
		ser.write(b'name,?\r')
		x = ser.readline()
		print(x)

		if len(x) < 5: continue
		flag = False
		for i in range(0, len(x) - 5):
			if x[i:i+5] == b'?NAME':
				flag = True
				s = str(x[i:], 'UTF-8')
				filename = '/home/pi/workspace/data/'
				filename += str(x[i+6:i+s.find('\r')], 'UTF-8')
				filename += '.txt'
				print(filename)
				break
		
		if flag: break
	
	while True:
		print('B')
		x = ser.readline()
		print(x)
		if len(x) == 0: continue
		with open(filename, 'w') as the_file:
			the_file.write(str(x, 'UTF-8'))

while True:
	try:
		with open(filename, 'w') as the_file:
			the_file.write('')
		run()
	except Exception as e:
		print(str(e))
		print('unknown port ' + port)
	time.sleep(3)

	
