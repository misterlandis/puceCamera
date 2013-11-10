class MouseSerial:
	import serial
	import time

	ser = serial.Serial()
	mousePixels = []

	def hello(self):
		print "hello"
	def initSerial(self):
		self.ser.port="/dev/ttyUSB0" 
		self.ser.baudrate = 38400
		self.ser.timeout = 0
		self.ser.open()
	
	def getFrame(self):
		self.ser.write('d')
		self.time.sleep(.4)
		response = MouseSerial.getMouseResponse(self)
		return response

	def getMouseResponse(self):
		mouseSays =""
		while self.ser.inWaiting() > 0:
			mouseSays = mouseSays + self.ser.read()
			#print "mouseSays: ", mouseSays
		mousePixels = []
		for char in mouseSays:
			mousePixels.append(ord(char))
		#print mousePixels
		return mousePixels	
			

	def interactivePrompt(self):
		while True:
			mouseSays = ""
			while self.ser.inWaiting()> 0:
				mouseSays =	mouseSays + self.ser.read()
			print mouseSays
			print "length: ", len(mouseSays)
			typed = raw_input("command:")

			if typed == "exit":
					self.ser.close()
					break
			else:
					self.ser.write(typed)
					self.time.sleep(1)
