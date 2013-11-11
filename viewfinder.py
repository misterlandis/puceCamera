import pygame

class Viewfinder():
	lastFrame = []
	screen = ""
	clock = ""
	
	def startDisplay(self):
		print "starting"
		
		pygame.init()
	  
		# Set the width and height of the screen [width,height]
		size = [700,500]
		self.screen = pygame.display.set_mode(size)
		pygame.display.set_caption("Mouse Camera")
	 
		#Loop until the user clicks the close button.
		done = False
	 
		# Used to manage how fast the screen updates
		self.clock = pygame.time.Clock()
		
		while done == False:
			self.updateDisplay()
	
	def setimage(self, newImageData):
		self.lastFrame = newImageData
		
	def updateDisplay(self):
		# -------- Main Program Loop -----------
		
		# ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done = True # Flag that we are done so we exit this loop
		# ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

		# ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
		 
		# First, clear the screen to blue. Don't put other drawing commands
		# above this, or they will be erased with this command.
		#screen.fill((0,0,255))
		font = pygame.font.Font(None,25)
		####Render Mouse info
		pixelsize = 8
		
		#print "lastframe: ", self.lastFrame
		for i, pixel in enumerate(self.lastFrame):
			grayvalue = pixel * 4
			if grayvalue > 255: grayvalue = 255
			graycolor = [grayvalue,grayvalue,grayvalue]
			pixel_x = i%18 * pixelsize
			pixel_y = math.floor(i/18) * pixelsize
			pygame.draw.rect(screen,graycolor, [pixel_x,pixel_y, pixelsize, pixelsize])
		#process mouse coordinates
		if len(self.lastFrame) == 327:
			rawCoords = lastFrame[-3:]
			if rawCoords[0] > 127: rawCoords[0] = rawCoords[0] -256
			if rawCoords[1] > 127: rawCoords[1] = rawCoords[1] -256
			print "Coordinates: ", rawCoords
		
		
		myText = font.render(str(len(self.lastFrame)), True, (0,0,0,))
		self.screen.blit(myText, [40,40])
		# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
		 
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
	 
		# Limit to 20 frames per second
		self.clock.tick(2000)
