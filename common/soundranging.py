#coding:utf8
import RPi.GPIO as GPIO
import time

class SoundRanging:
	DEFAULT_ECHO_GPIO_PIN 	= 20
	DEFAULT_TRIG_GPIO_PIN 	= 21

	def __init__(self, echo=DEFAULT_ECHO_GPIO_PIN, trig=DEFAULT_TRIG_GPIO_PIN):
		self.initGPIO(echo, trig)
		self.echoPin = echo 
		self.trigPin = trig

	def initGPIO(self, echo, trig):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(echo, GPIO.IN)
		GPIO.setup(trig, GPIO.OUT, initial=GPIO.LOW)

	def cleanupGPIO(self):
		GPIO.cleanup()

	def getDistance(self):
		# trig     __
		#     ____|  |____
		GPIO.output(self.trigPin, GPIO.LOW)
		time.sleep(0.01)
		GPIO.output(self.trigPin, GPIO.HIGH)
		time.sleep(0.01)
		GPIO.output(self.trigPin, GPIO.LOW)

		while GPIO.input(self.echoPin) == GPIO.LOW:
			pass
		tStart = time.time()
		while GPIO.input(self.echoPin) == GPIO.HIGH:
			pass
		tEnd = time.time()

		distance = 340.0 * (tEnd - tStart) / 2 * 100
		return distance

if __name__ == '__main__':
	sd = SoundRanging()
	while True:
		print 'Disctance : %.2f cm' % sd.getDistance()
		time.sleep(1)

