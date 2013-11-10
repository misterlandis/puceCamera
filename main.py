#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mouseSerial
import pygame
import math

def main():
	print "starting"
	
	myMouseSerial = mouseSerial.MouseSerial()
	myMouseSerial.hello()
	myMouseSerial.initSerial()
	#myMouseSerial.captureLoop()
	
	lastFrame = [1,1]
	pygame.init()
  
	# Set the width and height of the screen [width,height]
	size = [700,500]
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Mouse Camera")
 
	#Loop until the user clicks the close button.
	done = False
 
	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()
	
	# POINTER
	pointerx = 4
	pointery = 4
	slowdown = 2
	
	# -------- Main Program Loop -----------
	while done == False:
		# ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done = True # Flag that we are done so we exit this loop
		# ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
	  
	  
		# ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
	 
		# ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
	 
		 
	 
		# ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
		 
		# First, clear the screen to blue. Don't put other drawing commands
		# above this, or they will be erased with this command.
		#screen.fill((0,0,255))
		font = pygame.font.Font(None,25)
		mouseOutput =myMouseSerial.getFrame()
		#pygame.time.wait(2000)
		#print mouseOutput
		if mouseOutput != None:
			lastFrame = mouseOutput
		
		####Render Mouse info
		pixelsize = 8
		
		print "lastframe: ", lastFrame
		for i, pixel in enumerate(lastFrame):
			grayvalue = pixel * 4
			if grayvalue > 255: grayvalue = 255
			graycolor = [grayvalue,grayvalue,grayvalue]
			pixel_x = i%18 * pixelsize
			pixel_y = math.floor(i/18) * pixelsize
			pygame.draw.rect(screen,graycolor, [pixel_x,pixel_y, pixelsize, pixelsize])
		#process mouse coordinates
		if len(lastFrame) == 327:
			rawCoords = lastFrame[-3:]
			if rawCoords[0] > 127: rawCoords[0] = rawCoords[0] -256
			if rawCoords[1] > 127: rawCoords[1] = rawCoords[1] -256
			print "Coordinates: ", rawCoords
		
		#draw pointer
		pointerx += rawCoords[0]
		pointery += rawCoords[1]
		pygame.draw.rect(screen,0xFF0000,[pointerx,pointery,10,10])
		
		myText = font.render(str(len(lastFrame)), True, (0,0,0,))
		screen.blit(myText, [40,40])
		# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
		 
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
	 
		# Limit to 20 frames per second
		clock.tick(2000)
		 
	
	return 0

if __name__ == '__main__':
	main()

