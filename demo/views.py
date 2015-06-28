from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from common.audio.recognition import recognition
from common.audio.pcm_converter import convert
from common.motor.motor import MotorControllor  

@csrf_exempt
def test(request):
	print request.POST
	# request.body : wav data, sample_rate = 44100.
	'''
	try:
		pcmData = convert(request.body)
	except Exception as e:
		print e

	res = recognition(pcmData)
	command = res[0]
	'''
	command = request.POST['command']
	mc = MotorControllor.getInstance()
	if command.find(u'\u524d\u8fdb') >= 0:
		if command.find(u'\u5de6') >= 0:
			mc.runFrontLeft(speed=3)
		elif command.find(u'\u53f3') >= 0:
			mc.runFrontRight(speed=3)
		else:
			mc.runFrontLeft(speed=3)
			mc.runFrontRight(speed=3)
			
	if command.find(u'\u505c\u6b62') >= 0:
		if command.find(u'\u5de6') >= 0:
			mc.stopFrontLeft()
		elif command.find(u'\u53f3') >= 0:
			mc.stopFrontRight()
		else:
			mc.stopFrontLeft()
			mc.stopFrontRight()

	if res:
		print res[0]
	return HttpResponse(res[0])

def recordAudioDemo(request):
    response = render(request, 'record_audio_demo.html')
    return response 

import cv2
import time
cap = cv2.VideoCapture(0)
cap.set(3, 320.0)
cap.set(4, 240.0)

def jpegStream():
	while cap.isOpened():
		ret, frame = cap.read()
		if ret:
			ret, data = cv2.imencode('.jpg', frame)
		data = data.tostring()
		print 'a jpeg'
		res  = '--liushuo\r\n'
		res += 'Content-Type: image/jpeg\r\n'
		res += 'Content-Length: %s\r\n\r\n' % len(data)
		res += data
		yield res
		#time.sleep(0.05)

def cameraDemo(request):
	if not request.GET.get('action', None):
		return render(request, 'stream.html')

	print 'stream'
	response = StreamingHttpResponse(jpegStream(), content_type='multipart/x-mixed-replace; boundary=liushuo')
	return response

'''
def cameraDemo(request):
	response = StreamingHttpResponse()
	
    return render(request, 'camera_demo.html')
'''

@csrf_exempt
def control(request):
	print 'CONTROL ---> ', request.method
	if request.method == 'POST':
		driver = control.carDriver
		cmd = request.POST['command']
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
		
	return HttpResponse('OK')
from common.car_driver import CarDriver
control.carDriver = CarDriver()
