import serial
import RPi.GPIO as GPIO
import time
import _thread
import datetime
import requests
import sys
import os


serverPath = 'http://xxx/AquaDuo/client-site/databaseTest/addSensoryData.php'
errorRange = 10
rovPath = 'http://192.168.1.101:5000'

filenames = []
filenames.append('/home/pi/workspace/data/conduct.txt')
filenames.append('/home/pi/workspace/data/do.txt')
filenames.append('/home/pi/workspace/data/ph.txt')
filenames.append('/home/pi/workspace/data/temp.txt')
filenames.append('/home/pi/workspace/data/GPSx.txt')
filenames.append('/home/pi/workspace/data/GPSy.txt')
data = []



def run(*args):
	now = datetime.datetime.now()
	
	r = requests.get(rovPath)
	jsonData = r.json()
	print('JSON: ', jsonData)
	
	params = {
		"data[0][usv_id]": 1, 
		"data[0][conduct]": data[0],
		"data[0][do]": data[1],
		"data[0][pH]": data[2],
		"data[0][temp]": data[3],
		"data[0][GPSx]": data[4],
		"data[0][GPSy]": data[5],
		"data[0][deep]": 0,
		"data[1][usv_id]": 1, 
		"data[1][conduct]": jsonData['conduct'],
		"data[1][do]": jsonData['do'],
		"data[1][pH]": jsonData['ph'],
		"data[1][temp]": jsonData['temp'],
		"data[1][GPSx]": data[4],
		"data[1][GPSy]": data[5],
		"data[1][deep]": 1,
	}
	
	print('Send: ', params)
	r = requests.get(serverPath, params)
	print('Response: ', r.text)
	#print('Response: ', r.json())

	#r = requests.get(serverPath, {
	#	'usv_id': 1, 
	#	'conduct': data[0], 
	#	'do': data[1], 
	#	'pH': data[2], 
	#	'temp': data[3], 
	#	'GPSx': data[4], 
	#	'GPSy': data[5]})
	#print(r.json())
	#print(r)

while True:
	data = []
	now = datetime.datetime.now()
	for filename in filenames:
		statbuf = os.stat(filename)
		ft = statbuf.st_mtime
		nt = datetime.datetime.now().timestamp()
		if nt - ft > errorRange:
			data.append('')
		else:
			file = open(filename, 'r')
			data.append(file.readline())
	
	isValided = True
	for x in data:
		if len(x) == 0:
			isValided = False
			break
	isValided = True
	
	if isValided:
		print(data)
		_thread.start_new_thread(run, ())
	else:
		print('some sensor not ready yet.')
	
	time.sleep(2)

