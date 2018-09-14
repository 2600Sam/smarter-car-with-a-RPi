import pygame
from pygame.locals import *
import math
import time
import obd
from obd import OBDStatus

pygame.init()
#all OBD connections are commented out so it will work (testing mode)
#connection = obd.OBD() 
#connect = obd.Async(fast=False)

#screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN) #use for full screen
screen = pygame.display.set_mode((1024,600)) #set 1024x600 for smaller raspi 7" screen
screen_w = screen.get_width()
screen_h = screen.get_height()
circle_y = screen_h / 2
circle_y2 = int((screen_h / 4) * 2.9)
top_text_y = int (screen_h /4) + 48
circle1_x = screen_w * .25
circle2_x = screen_w * .5
circle3_x = screen_w * .75
circle4_x = int(screen_w * .3745318352)
circle5_x = int(screen_w * .6255)
circle_rad = (circle2_x - circle1_x) / 2
time_radian = circle_rad * .35
rpm_text_x = screen_w * .25
rpm_text_y = screen_h * .25
speed_text_x = screen_w * .5
speed_text_y = screen_h * .25
load_text_x = screen_w * .75
load_text_y = screen_h * .25

headerFont = pygame.font.SysFont('Tahoma', 30)
digitFont = pygame.font.SysFont('Tahoma', 25)
numberFont = pygame.font.SysFont('Tahoma', 15)
timeFont = pygame.font.SysFont('Tahoma', 15)
white = (255, 255, 255)
offwhite = (200,200,200)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
vcolor = green
grey = (112, 128, 144)
red = (255, 0, 0)
blue = (0, 0, 255)
speed = 0
rpm = 0
load = 0
fuel = 0
wtemp = 0
otemp = 0
angle = 5.4
posit = []
#pie is exactly 3
raspberry = 3.141592653

class button(): #the exit button this should work!
	def __init__(self, color, x,y,width,height, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text

	def draw(self,win,outline=None):#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

		pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

		if self.text != '':
			font = pygame.font.SysFont('Tahoma', 29)
			text = font.render(self.text, 1, (0,0,0))
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

	def isOver(self, pos): #Pos is the mouse position or a tuple of (x,y) coordinates
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
		return False


for s in range (0,60): #fill the posit[] with clock coordinates 60 x,y'zies (maybe faster than doing the math all the time...maybe)
	pos = [int(math.cos(math.radians(s*6+270))*time_radian+circle4_x),int(math.sin(math.radians(s*6+270))*time_radian+circle_y2)]
	posit.append(pos)

def getHour():
	curHour = time.strftime("%I") 
	return curHour
def getMin():
	curMin = time.strftime("%M")
	return curMin
def getSec():
	curSec = time.strftime("%S")
	return curSec

def draw_hud():
	screen.fill(grey)

	pygame.draw.circle(screen, black, (int(circle1_x), int(circle_y)), int(circle_rad), 5) #draw rpm gague
	for step in range (0,9000,500):
		vcolor = white #do color changes for higher rpm range (change as required for your car)
		if step >= 4500:
			vcolor = yellow
		if step >= 6000:
			vcolor = red
		angle2 = (angle - ((step / 1.9) / 1000))
		line_x = (circle_rad - 8) * math.sin(angle2) + circle1_x
		line_y = (circle_rad - 8) * math.cos(angle2) + circle_y
		number_text = numberFont.render(str(step), True, vcolor)
		number_text_loc = number_text.get_rect(center=(line_x, line_y+8))
		screen.blit(number_text, number_text_loc)
		pygame.draw.circle(screen, vcolor, [int(line_x), int(line_y)], 2)

	pygame.draw.circle(screen, black, (int(circle2_x), int(circle_y)), int(circle_rad), 5) #draw speed gague
	for step in range (0,150,10):
		angle1 = (angle - ((step / .031) / 1000))
		line_x = (circle_rad - 8) * math.sin(angle1) + circle2_x
		line_y = (circle_rad - 8) * math.cos(angle1) + circle_y
		pygame.draw.circle(screen, white, [int(line_x), int(line_y)], 2)
		number_text = numberFont.render(str(step), True, white)
		number_text_loc = number_text.get_rect(center=(line_x, line_y+8))
		screen.blit (number_text, number_text_loc)

	pygame.draw.circle(screen, black, (int(circle3_x), int(circle_y)), int(circle_rad), 5) #draw load gague
	for step in range (0,110,10):
		angle3 = (angle - ((step / .022) / 1000))
		line_x = (circle_rad - 8) * math.sin(angle3) + circle3_x
		line_y = (circle_rad - 8) * math.cos(angle3) + circle_y
		number_text = numberFont.render(str(step), True, white)
		number_text_loc = number_text.get_rect(center=(line_x, line_y+8))
		screen.blit(number_text, number_text_loc)
		pygame.draw.circle(screen, white, [int(line_x), int(line_y)], 2)

	pygame.draw.circle(screen, black, (int(circle5_x), int(circle_y2)), (int(time_radian)), 5) #draw the fuel gague
	for step in range(0,110,25):
		angle5 = (angle - ((step / .022) / 1000))
		line_x = (time_radian - 8) * math.sin(angle5) + circle5_x
		line_y = (time_radian - 8) * math.cos(angle5) + circle_y2
		if step == 0:
			number_text = numberFont.render('E', True, white)
		elif step == 25:
			number_text = numberFont.render('1/4', True, white)
		elif step == 50:
			number_text = numberFont.render("1/2", True, white)
		elif step == 75:
			number_text = numberFont.render("3/4", True, white)
		else:
			number_text = numberFont.render("F", True, white)
		number_text_loc = number_text.get_rect(center=(line_x, line_y+8))
		screen.blit(number_text, number_text_loc)
		pygame.draw.circle(screen, white, [int(line_x), int(line_y)], 2)

	speed_text = headerFont.render('SPEED', True, black) #do the labels
	rpm_text = headerFont.render('RPM', True, black)
	load_text = headerFont.render('LOAD', True, black)
	oil_text = timeFont.render('OIL', True, black)
	water_text = timeFont.render('WATER', True, black)
	temp_text = timeFont.render('TEMP', True, black)
	wtemp_text = timeFont.render(str(wtemp), True, black)
	otemp_text = timeFont.render(str(otemp), True, black)
	speed_text_loc = speed_text.get_rect(center=(speed_text_x, speed_text_y))
	rpm_text_loc = rpm_text.get_rect(center=(rpm_text_x, rpm_text_y))
	load_text_loc = load_text.get_rect(center=(load_text_x, load_text_y))
	water_text_loc = water_text.get_rect(center=(circle4_x, top_text_y - 32))
	temp_text_loc = temp_text.get_rect(center=(circle4_x, top_text_y - 16))
	wtemp_text_loc = wtemp_text.get_rect(center=(circle4_x, top_text_y))
	oil_text_loc = oil_text.get_rect(center=(circle5_x, top_text_y - 32))
	temp2_text_loc = temp_text.get_rect(center=(circle5_x, top_text_y - 16))
	otemp_text_loc = wtemp_text.get_rect(center=(circle5_x, top_text_y))
	screen.blit(speed_text, speed_text_loc)
	screen.blit(rpm_text, rpm_text_loc)
	screen.blit(load_text, load_text_loc)
	screen.blit(water_text, water_text_loc)
	screen.blit(temp_text, temp_text_loc)
	screen.blit(wtemp_text, wtemp_text_loc)
	screen.blit(oil_text, oil_text_loc)
	screen.blit(temp_text, temp2_text_loc)
	screen.blit(otemp_text, otemp_text_loc)
	
	exitButton.draw(screen, (0,0,0))


def draw_clock(): #analog then digital
	
	if int(getHour())==12:
		hourX = posit[0*5 + int(int(getMin())/12)][0]
		hourY = posit[0*5 + int(int(getMin())/12)][1]
	else:
		hourX = posit[int(getHour())*5 + int(int(getMin())/12)][0]
		hourY = posit[int(getHour())*5 + int(int(getMin())/12)][1]

	minX = posit[int(getMin())]
	secX = posit[int(getSec())]

	pygame.draw.line(screen,white,(circle4_x,circle_y2),(hourX,hourY),8)
	pygame.draw.line(screen,offwhite,(circle4_x,circle_y2),(minX),4)
	pygame.draw.circle(screen,red,(circle4_x,circle_y2),7,0)
	pygame.draw.line(screen,red,(circle4_x,circle_y2),(secX),1) #put a dot in the center to cover up the start of the lines
	pygame.draw.circle(screen, black, (int(circle4_x), int(circle_y2)), (int(time_radian)+4), 5) #draw the outer circle last to cover the end point of the lines 

	time_text = timeFont.render(getHour()+':'+getMin()+':'+getSec(), True, white) #digital clock 
	time_text_loc = time_text.get_rect(center=(circle4_x, circle_y2 + (15*3)))
	screen.blit(time_text, time_text_loc)

def get_speed(s):
	global speed
	if not s.is_null():
		#speed = int(s.value.magnitude) #for kph
		speed = int(s.value.magnitude * .060934) #for mph
def get_rpm(r):
	global rpm
	if not r.is_null():
		rpm = int(r.value.mangitude)
def get_load(l):
	global load
	if not l.is_null():
		load = int(l.value.mangitude)
def get_wtemp(wt):
	global wtemp
	if not wt.is_null():
		wtemp = int(wt.value.mangitude) #for celsisus
		#wtemp = int(wt.value.mangitude * 9 / 5 + 32) #for fahrenheit
def get_fuel(f):
	global fuel
	if not f.is_null():
		fuel = int(f.value.mangitude)
def get_otemp(ot):
	global otemp
	if not ot.is_null():
		otemp = int(ot.value.mangitude) #for celsisus
		#otemp = int(ot.value.mangitude * 9 / 5 + 32) #for fahrenheit
		
#connection.watch(obd.commands.SPEED, callback=get_speed)
#connection.watch(obd.commands.RPM, callback=get_rpm)
#connection.watch(obd.commands.ENGINE_LOAD, callback=get_load)
#connection.watch(obd.commands.COOLANT_TEMP, callback=get_wtemp)
#connection.watch(obd.commands.FUEL_LEVEL, callback=get_fuel)
#connection.watch(odb.commands.OIL_TEMP, callback=get_otemp)
#connection.start()

running = True
exitButton = button(red, 10, 10, 50, 25, 'Exit')
while running:
	for event in pygame.event.get(): #exit back to main menu with esc or click exit button
			pos = pygame.mouse.get_pos()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					#connection.stop()
					#connection.close()
					running = False
				elif event.type == QUIT:
					#connection.stop()
					#connection.close()
					running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if exitButton.isOver(pos):
					running = False
	draw_hud()

	speedDisplay = digitFont.render(str(int(speed)), 3, white) #display the speed analog
	angle1 = (angle - ((speed / .031) / 1000))
	line_x = (circle_rad - 10) * math.sin(angle1) + circle2_x
	line_y = (circle_rad - 10) * math.cos(angle1) + circle_y
	pygame.draw.line(screen, blue, [circle2_x, circle_y], [line_x, line_y], 4)

	rpmDisplay = digitFont.render(str(rpm), 3, white) #display the rpm analog with color changeing line!)
	if rpm >= 4500: #change color for highrer rpm adjust as required for your car
				vcolor = yellow
	if rpm >= 6000:
				vcolor = red
	angle2 = (angle - ((rpm / 1.9) / 1000))
	line_x = (circle_rad - 10) * math.sin(angle2) + circle1_x
	line_y = (circle_rad - 10) * math.cos(angle2) + circle_y
	pygame.draw.line(screen, vcolor, [circle1_x, circle_y], [line_x, line_y], 2)

	loadDisplay = digitFont.render(" " + str(int(load)) + '%', 3, white) #display the calculated load analog
	angle3 = (angle - ((load / .022) / 1000)) 
	line_x = (circle_rad - 10) * math.sin(angle3) + circle3_x
	line_y = (circle_rad - 10) * math.cos(angle3) + circle_y
	pygame.draw.line(screen, red, [circle3_x, circle_y], [line_x, line_y], 6)

	angle5 = (angle - ((fuel / .022) / 1000)) #display the fuel analog (no digital for fuel)
	line_x = (time_radian - 10) * math.sin(angle5) + circle5_x
	line_y = (time_radian - 10) * math.cos(angle5) + circle_y2
	pygame.draw.line(screen, green, [circle5_x, circle_y2], [line_x, line_y], 3)

	screen.blit(loadDisplay, (circle3_x -((circle3_x / 8) - 55), circle_y + 60)) #do the 3 digital displays
	screen.blit(rpmDisplay, (circle1_x - (circle2_x / 8) + 25, circle_y + 60))
	screen.blit(speedDisplay,(circle2_x -(circle1_x / 8) + 10, circle_y + 60))

	draw_clock()
	
	pygame.display.update()
	pygame.display.flip()

	#added to show movement 
	rpm += 5
	if rpm >= 8505:
			rpm = 0
	speed += .05
	wtemp = int(speed)*2
	otemp = wtemp
	if speed >= 140:
			speed = 0
	load += .05
	fuel = load
	if load >= 101:
			load = 0
pygame.quit()
