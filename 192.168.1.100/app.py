import websocket
import _thread
import time
import datetime
import RPi.GPIO as GPIO
import socket

isConnected = False
showNow = False

def on_message(ws, message):
	global showNow
	
	if showNow == False:
		showNow = True
	else:
		showNow = False
	
	_thread.start_new_thread(LED, ())
	print(message)

def on_error(ws, error):
	print(error)

def on_close(ws):
	isConnected = False
	print("### closed ###")

def on_open(ws):
	isConnected = True
	ws.send("{\"type\": \"client\", \"event\": \"open\", \"name\": \"" + socket.gethostname() + "\"}")

def LED(*args):
	GPIO.setmode(GPIO.BOARD) #GPIO.BCM
	LED = 11
	GPIO.setup(LED, GPIO.OUT, initial = GPIO.LOW)
	p = GPIO.PWM(LED, 1000)
	count = 3
	for x in range(0, count):
		#GPIO.output(LED, GPIO.HIGH)
		#time.sleep(0.5)
		#GPIO.output(LED, GPIO.LOW)
		#time.sleep(0.5)
		for y in range(0, 101, 1):
			p.start(y)
			time.sleep(0.01)
		for y in range(100, -1, -1):
			p.start(y)
			time.sleep(0.01)
		p.stop()
		time.sleep(0.1)
	GPIO.cleanup()

if __name__ == "__main__":
	while True:
		try:
			websocket.enableTrace(True)
			ws = websocket.WebSocketApp("ws://xxx:8088",
										on_message = on_message,
										on_error = on_error,
										on_close = on_close)
			ws.on_open = on_open
			
			#wst = threading.Thread(target = ws.run_forever)
			#wst.daemon = True
			#wst.start()
			
			ws.run_forever()
			while isConnected:
				print("do something here...")
				if showNow:
					LED()
			
				while showNow:
					now = datetime.datetime.now()
					print(now)
				time.sleep(1)
				
			time.sleep(10)
		except:
			print("Somthing error in app.py")