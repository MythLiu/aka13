#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# --------------------------------------------------------------------------------
# 摄像头: /demo/camera
# --------------------------------------------------------------------------------

import cv2
def jpegStreamer(cap):
	while cap.isOpened():
		ret, frame = cap.read()
		if ret:
			ret, data = cv2.imencode('.jpg', frame)
		data = data.tostring()
		res  = '--liushuo\r\n'
		res += 'Content-Type: image/jpeg\r\n'
		res += 'Content-Length: %s\r\n\r\n' % len(data)
		res += data
		yield res
		#time.sleep(0.05)

def cameraDemo(request):
	if cameraDemo.cap is None:
		cameraDemo.cap = cv2.VideoCapture(0)
		cameraDemo.cap.set(3, 320.0)
		cameraDemo.cap.set(4, 240.0)

	if not request.GET.get('action', None):
		return render(request, 'stream.html')

	response = StreamingHttpResponse(jpegStreamer(cameraDemo.cap), 
					content_type='multipart/x-mixed-replace; boundary=liushuo')
	return response
cameraDemo.cap = None

# --------------------------------------------------------------------------------
# 小车控制: /demo/drive_car 
# --------------------------------------------------------------------------------

@csrf_exempt
def driveCar(request):
	if request.method == 'POST':
		cmd = request.POST['command']
		if not driveCar.driver:
			if cmd == 'init':
				from common.car_driver import CarDriver
				driveCar.driver = CarDriver()
				return HttpResponse(u'初始化完成...')
			return HttpResponse(u'尚未初始化...')
				
		driver = driveCar.driver
		if cmd == 'up':
			driver.goForward()
		elif cmd == 'down':
			driver.goBack()
		elif cmd == 'left':
			driver.turnLeft()
		elif cmd == 'right':
			driver.turnRight()
		elif cmd == 'stop':
			driver.stop()
		elif cmd == 'gear+':
			driver.gearUp()
		elif cmd == 'gear-':
			driver.gearDown()

		return HttpResponse(cmd + ' : OK')
	return HttpResponse(u'未定义的请求')
driveCar.driver = None

# --------------------------------------------------------------------------------
# 声音识别: /demo/audio
# --------------------------------------------------------------------------------

from common.audio.recognition import recognition
from common.audio.pcm_converter import convert

@csrf_exempt
def audioDemo(request):
	if request.method == 'GET':
		response = render(request, 'record_audio_demo.html')
	elif request.method == 'POST':
		try:
			import time
			t = time.time()
			pcmData = convert(request.body)
			print time.time() - t
			res = recognition(pcmData)
			response = HttpResponse(res[0])
		except Exception as e:
			print e
			raise

	return response 
