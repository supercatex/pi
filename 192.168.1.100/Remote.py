import requests
import time
import RPi.GPIO as GPIO

serverPath = 'http://xxx/database/json.php'

_PIN_INA1 = 16
_PIN_INB1 = 18
_PIN_PWM1 = 22
_PIN_EN_1 = 32

_PIN_INA2 = 11
_PIN_INB2 = 13
_PIN_PWM2 = 15
_PIN_EN_2 = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(_PIN_INA2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(_PIN_INB2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(_PIN_PWM2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(_PIN_EN_2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(_PIN_INA1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(_PIN_INB1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(_PIN_PWM1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(_PIN_EN_1, GPIO.OUT, initial = GPIO.LOW)

GPIO.output(_PIN_EN_2, GPIO.HIGH)
GPIO.output(_PIN_EN_1, GPIO.HIGH)

_PWN2 = GPIO.PWM(_PIN_PWM2, 100)
_PWN2.start(0)

_PWN1 = GPIO.PWM(_PIN_PWM1, 100)
_PWN1.start(0)

try:
	while True:
		params = {
			'code': 'speed'
		}
		r = requests.get(serverPath, params)
		jsonData = r.json()
		print('Response: ', jsonData[0]['value'])
		
		output = int(jsonData[0]['value'])
		
		if output > 0:

			GPIO.output(_PIN_INA2, GPIO.HIGH)
			GPIO.output(_PIN_INB2, GPIO.LOW)
			_PWN2.ChangeDutyCycle(output)
			
			GPIO.output(_PIN_INA1, GPIO.HIGH)
			GPIO.output(_PIN_INB1, GPIO.LOW)
			_PWN1.ChangeDutyCycle(output)
		else:
			output *= -1

			GPIO.output(_PIN_INA2, GPIO.LOW)
			GPIO.output(_PIN_INB2, GPIO.HIGH)
			_PWN2.ChangeDutyCycle(output)
			
			GPIO.output(_PIN_INA1, GPIO.LOW)
			GPIO.output(_PIN_INB1, GPIO.HIGH)
			_PWN1.ChangeDutyCycle(output)
		
		time.sleep(0.1)
except Exception as e:
	pass
finally:
	_PWN1.stop()
	_PWN2.stop()
	GPIO.cleanup()