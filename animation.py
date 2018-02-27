 import pygame
import os
import random

game_folder = os.path.dirname(__file__)
anim_folder = os.path.join(game_folder, "animation")

#COLORS
WHITE 	= 	(255,255,255)
BLACK 	= 	(0,0,0)

#FORCES
GRAVITY = 	[0,6]

#Player constants
SPEED = 10
JUMPSPEED = 60

#GAME CONSTANTS
TITLE 	= 	"CATMAN GAME"
WIDTH 	= 	1536
HEIGHT 	= 	864

#BULLETCLASS
class Bullet(pygame.sprite.Sprite):

	def __init__(self, vel, catpos):
		pygame.sprite.Sprite.__init__(self)
		self.vel = vel
		self.image = BULLET
		self.rect = self.image.get_rect()
		if self.vel[0] > 0:
			self.rect.center = catpos.midright
		if self.vel[0] <= 0:
			self.rect.center = catpos.midleft
		if self.vel[0] == 0:
			self.rect.center = catpos.center
	def update(self):
		self.rect.x += self.vel[0]
		if self.vel[0] >= 0: self.vel[0] = 100
		if self.vel[0] < 0: self.vel[0] = -100
		self.rect.y += self.vel[1]


#Sprite for units
class Unit(pygame.sprite.Sprite):

	def __init__(self, walkAnim, stillAnim, startpos):
		pygame.sprite.Sprite.__init__(self)
		self.vel = [0,0]
		self.acc = [0,0]
		self.image = pygame.image.load(os.path.join(anim_folder, "cat/catwalk1.png"))
		self.rect = self.image.get_rect()
		self.rect.center = (startpos[0],startpos[1])
		self.walk  = walkAnim
		self.still = stillAnim
		self.walkFrame = 0
		self.stillFrame = 0


	def AddForce(self, force):
		self.acc[0] += force[0]
		self.acc[1] += force[1]

	def update(self):
		self.vel[0] += self.acc[0]
		self.vel[1] += self.acc[1]
	
		#Adding Horizontal Drag
		self.vel[0] /= 1.1
	
		self.acc[0] = 0
		self.acc[1] = 0

		self.rect.x += self.vel[0]
		self.rect.y += self.vel[1]

		#check floor
		if (self.rect.bottom >= HEIGHT):
			self.rect.bottom = HEIGHT
			self.vel[1] = 0

		#check if almost still
		if (self.vel[0] <= 0.8 and self.vel[0] >= -0.8): 
			self.vel[0] = 0


		if self.vel[0] == 0 and self.vel[1] == 0:
			self.image = self.still[self.stillFrame]
			self.stillFrame += 1

			if (self.stillFrame == len(self.still)): self.stillFrame = 0

		if (self.vel[0] <= -0.8):
			self.image = self.walk[self.walkFrame]
			self.walkFrame += 1
			self.stillFrame = 0
	
		if (self.vel[0] > 0.8):
			self.image = pygame.transform.flip(self.walk[self.walkFrame],True,False)
			self.walkFrame += 1
			self.stillFrame = 0

		if (self.walkFrame == len(self.walk)): self.walkFrame = 0
	
#ANIMATIONS
BULLET		=		pygame.image.load		("laser.png")

CATWALK 	= 		[pygame.image.load      ("animation/cat/catwalk1.png"),
 					 pygame.image.load      ("animation/cat/catwalk2.png")]

CATSIT		= 		[pygame.image.load      ("animation/cat/catsit4.png")]

BACKGROUND 	= 		[pygame.image.load      ("background/backgroundstart.png"),]

SPACE 		= 		[pygame.image.load      ("background/space1.png"),
					 pygame.image.load      ("background/space2.png"),
					 pygame.image.load      ("background/space3.png"),]

DEADMAUS	=		[pygame.image.load      ("animation/deadm4us/deadm4aus1.png"),
					 pygame.image.load 		("animation/deadm4us/deadm4aus2.png")]

#make the backgrounds fullscreen
f = 0
for frame in BACKGROUND:
	BACKGROUND[f] = pygame.transform.scale	(frame, (WIDTH,HEIGHT))
	f += 1

f = 0
for frame in SPACE:
	SPACE[f] = pygame.transform.scale	(frame, (WIDTH,HEIGHT))
	f += 1

#create spritegroups
all_sprites = pygame.sprite.Group()
deadmaus 	= pygame.sprite.Group()
enemys		= pygame.sprite.Group()

#Create Units
cat = Unit(CATWALK, CATSIT, [WIDTH/2,HEIGHT/2])
dm  = Unit(DEADMAUS,DEADMAUS, [350,200])
# enemy = Unit(CATWALK, CATSIT)


#Add Units to group
all_sprites.add(cat)
all_sprites.add(dm)
# all_sprites.add(enemy)
# enemys.add(enemy)

#Initialize PYGAME
pygame.init()

#create window
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)

#start clock
clock = pygame.time.Clock()

#set keys to repeat
pygame.key.set_repeat(True)

gameLoop = True

while gameLoop:
	for event in pygame.event.get():
		if (event.type==pygame.QUIT):
			gameLoop = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				cat.AddForce([-SPEED,0])
			if event.key == pygame.K_RIGHT:
				cat.AddForce([SPEED,0])
			if event.key == pygame.K_SPACE:
				#Check if its on the ground
				if (cat.rect.bottom == HEIGHT):
					cat.AddForce([0,-JUMPSPEED])
			if event.key == pygame.K_SLASH:
				bull = Bullet([cat.vel[0],cat.vel[1]], cat.rect)
				all_sprites.add(bull)


	window.fill(WHITE)
	window.blit(random.choice(SPACE),(0,0))

	window.blit(BACKGROUND[0],(0,0))


	cat.AddForce(GRAVITY)
	# enemy.AddForce(GRAVITY)

	hits = pygame.sprite.spritecollide(cat, enemys, False)
	if hits:
		cat.vel[1] = 0
		cat.acc[1] = 0

	all_sprites.update()

	all_sprites.draw(window)
	
	pygame.display.flip()

	clock.tick (10)

pygame.quit()
