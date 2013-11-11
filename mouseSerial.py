class MouseSerial:
	import serial
	import time
	
	ser = serial.Serial()
	mousePixels = []

	def hello(self):
		print "hello"
	def initSerial(self):
		self.ser.port="/dev/ttyUSB0" 
		self.ser.baudrate = 115200
		self.ser.timeout = 0
		self.ser.open()
		print "serial initialized"
	
	def getFrame(self):
		print "getting frame"
		#self.ser.write('d')
		#self.time.sleep(0)
		response = []
		frame_over = False
		fails = 0
		while frame_over == False:
			newdata = self.getMouseResponse()
			if newdata == []: fails += 1
			response = response + newdata
			if 127 in response: frame_over = True #oops frame ended early
			if len(response) >= 325: frame_over = True #oops frame is too long
			#if fails > 100: frame_over = True #oops too many failed attempts
			
		return response

	def getMouseResponse(self):
		mouseSays =""
		while self.ser.inWaiting() > 0:
			mouseSays = mouseSays + self.ser.read()
			#print "mouseSays: ", mouseSays
		mousePixels = []
		for char in mouseSays:
			mousePixels.append(ord(char))
		#print "mousepixels: ", mousePixels
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
