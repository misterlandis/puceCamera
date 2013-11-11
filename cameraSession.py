import mouseSerial
import pygame
import math

class CameraSession:
	#_____init variables______
	myMouseSerial = mouseSerial.MouseSerial()
	rawcoords = []
	done = False
	screen = ""
	clock = pygame.time.Clock()
	pixelSize = 24
	def __init__(self):
		myMouseSerial = mouseSerial.MouseSerial()
		myMouseSerial.hello()
		myMouseSerial.initSerial()
		pygame.init()
		size = [self.pixelSize * 18,self.pixelSize*18 +200]
		self.screen = pygame.display.set_mode(size)
		pygame.display.set_caption("Mouse Camera") 
		#Loop until the user clicks the close button.
		self.done = False
		self.cameraLoop()
	
	def cameraLoop(self):
		# -------- Main Program Loop -----------
		while self.done == False:
			
			#_____EVENT_PROCESSING________
			self.process_events()
			#_____REQUEST_FRAME_FROM_SENSOR____
			lastFrame =self.myMouseSerial.getFrame()
			#_____DRAWING_____
			self.draw_camera_image(lastFrame,self.pixelSize)
			#draw data
			pygame.draw.rect(self.screen,(0,0,255),[0,self.pixelSize * 18,self.pixelSize * 18,200]) #clear text area
			self.draw_text("time elapsed: " + str(float(pygame.time.get_ticks()) / 1000),10,self.pixelSize * 18 + 10)
			self.draw_text("FPS: " + str(self.clock.get_fps()) ,10,self.pixelSize * 18 + 25)
			self.clock.tick()
			# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
			pygame.display.flip()
			
			
	def process_events(self):
		for event in pygame.event.get(): # User did something
				if event.type == pygame.QUIT: # If user clicked close
					self.done = True # Flag that we are done so we exit this loop
	
	def draw_camera_image(self,cameraData,pixelsize = 8):
		print "lastframe: ", cameraData
		for i, pixel in enumerate(cameraData):
			grayvalue = pixel * 4
			if grayvalue > 255: grayvalue = 255
			graycolor = [grayvalue,grayvalue,grayvalue]
			pixel_x = i%18 * pixelsize
			pixel_y = math.floor(i/18) * pixelsize
			pygame.draw.rect(self.screen,graycolor, [pixel_x,pixel_y, pixelsize, pixelsize])
			
	def draw_text(self,text_to_draw,x,y):
		font = pygame.font.Font(None,25)
		myText = font.render(text_to_draw, True, (255,0,0,))
		self.screen.blit(myText, [x,y])
		
		
