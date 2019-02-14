import os
import sys
import random
import pygame

# Lets the sounds play.
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# Declaring that this is the first cycle of the game.
first = True

# Starting with 00000 highscore.
HI = "00000"


# Immediately updating score.
def update_score():
	# Updates highscore.
	global HI
	try:
		# If there is no file with written highscores, it assumes
		# the game is being launched for the first time and creates such
		# a file, writing a highscore of 00000 to it.
		with open("scoreboard.txt", 'r') as a:
			HI = a.read()
	except:
		with open("scoreboard.txt", 'w') as a:
			a.write("00000")

# ...
pygame.display.set_caption("T-Rex Runner")
size = WIDTH, HEIGHT = 900, 270
screen = pygame.display.set_mode((size))

# Declaring sounds' names.
jump_sound = pygame.mixer.Sound('data/jump.wav')
die_sound = pygame.mixer.Sound('data/die.wav')
checkPoint_sound = pygame.mixer.Sound('data/checkPoint.wav')


def load(name, colorkey=None):
	# Loads images.
	try:
		image = pygame.image.load("data/{}".format(name))
	except Exception as exception:
		print("Cannot load image: {}".format(name))
		raise SystemExit(exception)
	
	image = image.convert_alpha()
	if colorkey:
		if colorkey is -1:
			colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey)
	image = image.convert_alpha()
	return image


def terminate():
	# Terminates the process.
	pygame.quit()
	sys.exit()


class Clouds(pygame.sprite.Sprite):
	# Used to spawn clouds in the background
	def __init__(self, big=False, start=False):
		super().__init__(clouds)
		self.speed = random.randint(1, 4)
		self.image = pygame.transform.scale(load("cloud.png"), (45, 21))
		self.rect = self.image.get_rect()
		self.cur = 0
		# Clouds can either be big or not big
		# if they are, the only thing that differs them from regular clouds
		# is that they spawn a little later to follow them.
		if not big:
			if not start:
				self.rect.x, self.rect.y = 1200 + random.randint(0, 600), random.randint(65, 200)
			else:
				self.rect.x, self.rect.y = random.randint(0, 1200), random.randint(65, 200)

		else:
			self.rect.x, self.rect.y = 1600 + random.randint(0, 600), random.randint(65, 200)

	def move(self):
		# Lets clouds move.
		self.cur += 1
		if self.cur % 3 == 0 or self.speed == 1:
			self.rect.x -= self.speed * gamespeed
		if self.rect.right < 0:
			self.kill()


class Grounds(pygame.sprite.Sprite):
	# Spawns a sprite with the game's ground.
	def __init__(self):
		super().__init__(ground_group)
		self.image = load("ground.png", -1)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = 0, 249 # moves it to the bottom of the screen

	def move(self):
		self.rect.x -= 2 * gamespeed
		if self.rect.width // 2 <= -1 * self.rect.x:
			self.rect.x = 0


# Creates a cactus.
class Cactus(pygame.sprite.Sprite):
	def __init__(self, big=False):
		super().__init__(cactuses)
		minsize = 0.55 + random.randint(0, 5) * 0.024
		if minsize > 1:
			minsize = 1
		self.image = pygame.Surface((50, 50))
		self.image.fill((0, 0, 255))
		self.cactuses = []

		if not big:
			for i in range(8):
				self.cactuses.append(load(f"cact{i + 1}.png", -1))
			rand = random.randint(0, len(self.cactuses) - 1)
			self.image = self.cactuses[rand]
			if rand != 7:
				x = int(self.image.get_width() * minsize)
				y = int(self.image.get_height() * minsize)
			else:
				if random.randint(1, 7) == 2:
					x = 78
					y = 51
				else:
					x = 58
					y = 34
			self.image = pygame.transform.scale(self.image, (x, y))

		else:
			self.image = pygame.transform.scale(load(f"bigcact1.png", -1), (85, 60))

		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = 1200, 264 - self.rect.height
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		self.rect.x -= 2 * gamespeed
		if pygame.sprite.collide_mask(self, Dino):
			global GAMEOVER
			GAMEOVER = True

		if self.rect.right < 0:
			self.kill()


# Yes, a pterodactyl is created using this.
class Pterodactyl(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__(pterodactyls)
		self.frames = [pygame.transform.scale(load("ptera1.png", -1), (38, 34)),
					   pygame.transform.scale(load("ptera2.png", -1), (38, 34))]
		self.cur = 0
		self.image = self.frames[0]
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = 1450, random.randint(175, 220)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		self.cur += 1

		if self.cur % 25 == 0:
			self.image = self.frames[(self.frames.index(self.image) + 1) % 2]
			self.rect.x += gamespeed
		self.rect.x -= 2 * gamespeed

		if pygame.sprite.collide_mask(self, Dino):
			global GAMEOVER
			GAMEOVER = True

		if self.rect.right < 0:
			self.kill()


# Player.
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__(player_group)
		self.movement = [0, 0] # array with movement values
		# The first value in the upper array is used to resemble horisontal movement per
		# "def update(self)" call, the second one -- to resemble vertical movement.
		self.isJumping = False
		self.isDucking = False
		self.gravity = 0.25
		self.duck = []
		self.frames = []

		for i in range(2):
			self.duck.append(load(f"sneak{i + 1}.png", -1))

		for i in range(2):
			self.frames.append(load(f"rex{i + 1}.png", -1))

		self.cur = 0
		self.update()
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = 100, 223

	def update(self):
		self.cur += 1
		if not self.isDucking:
			self.image = self.frames[(self.cur) % len(self.frames)]

		else:
			if not self.isJumping:
				self.image = self.duck[(self.cur) % len(self.duck)]
			else:
				self.image = pygame.transform.flip(self.duck[0], False, False)

		self.mask = pygame.mask.from_surface(self.image)

	def jump(self):
		if self.isJumping:
			self.rect.y -= self.movement[1]
			self.movement[1] -= self.gravity
			if self.rect.y + self.rect.height >= 265:
				self.rect.y = 265 - self.rect.height
				self.movement[1] = 0
				self.gravity = 0.25
				self.isJumping = False

	def stop(self):
		self.image = load(f"rex.png", -1)


# Used to resemble highscore.
class HIGHSCORES(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__(scoreboard)
		global HI
		self.image = pygame.Surface((100, 24))
		self.image.fill((235, 235, 235))

		for iterator, key in enumerate(HI):
			self.image.blit(load(f"{key}.png", -1), (iterator * 20, 0))

		self.image = pygame.transform.scale(self.image, (75, 18))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = 70, 20


# Used to resemble current score.
class SCORES(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__(scoreboard)
		self.score = 0
		self.image = pygame.Surface((100, 24))
		self.image.fill((235, 235, 235))

		for iterator, key in enumerate(str(self.score).zfill(5)):
			self.image.blit(load(f"{key}.png", -1), (iterator * 20, 0))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = 165, 20
		self.image = pygame.transform.scale(self.image, (75, 18))

	def update(self):
		self.image = pygame.transform.scale(self.image, (100, 24))
		global gamespeed
		self.score += 1

		if self.score % 100 == 0 and self.score != 0:
			checkPoint_sound.play()
			pass

		if self.score % 250 == 0:
			gamespeed += 1
			if gamespeed > 8:
				gamespeed = 8
			speedup()

		self.str = str(self.score).zfill(5)
		self.image = pygame.transform.scale(self.image, (75, 18))

	def draw(self):
		self.image = pygame.transform.scale(self.image, (100, 24))
		self.image.fill((235, 235, 235))
		for iterator, key in enumerate(self.str):
			self.image.blit(load(f"{key}.png", -1), (iterator * 20, 0))
		self.image = pygame.transform.scale(self.image, (75, 18))


# Speeds up the game.
def speedup():
	pygame.time.set_timer(2, (40 - 2 * gamespeed) // 5)
	pygame.time.set_timer(7, 50 // gamespeed)
	pygame.time.set_timer(10, 120 // gamespeed * 2)

# Declares the main game cycle.
def main():
	global maximum, gamespeed
	# Speeds up the game for the first time.
	speedup()
	while True:
		screen.fill((0, 0, 0))
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					if not Dino.isJumping:
						Dino.isDucking = True
						Dino.update()
					else:
						Dino.gravity += 0.75

				# Makes jumping possible.
				if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
					if not Dino.isJumping and not Dino.isDucking:
						Dino.movement[1] = 6
						Dino.isJumping = True
						jump_sound.play()

			# Resets the dinosaur's regular position upon releasing DOWN key.
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_DOWN:
					Dino.isDucking = False

			# Updates the dino's vertical position.
			if event.type == 1:
				Dino.jump()

			# Moves the environment.
			if event.type == 2:
				for cloud in clouds:
					cloud.move()
				Ground.move()

				for cactus in cactuses:
					cactus.update()

				for pterodactyl in pterodactyls:
					pterodactyl.update()

			# Updates the animation of the dinosaur.
			if event.type == 3:
				if not Dino.isJumping or Dino.isDucking:
					Dino.update()

			# Manipulates the pace of the game's enemies.
			if event.type == 8:
				if SCORE.score > 250 and "ccpccccpcc"[random.randint(0, 9)] == "p":
						if len(pterodactyls) < 1:
							Pterodactyl()
				else:
					if "bsssssssssssssb"[random.randint(0, 14)] == "s":
						Cactus()
					else:
						Cactus("big")

				if gamespeed != 8:
					# The timer below calls a spawn of an enemy on the right edge of the screen.
					pygame.time.set_timer(8, 1200 - 10 * gamespeed**2)
				else:
					pygame.time.set_timer(8, 800)

			# Used to create beautiful backgrounds and to update the score.
			if event.type == 10:
				if len(clouds) < 30:
					for i in range(2):
						Clouds()
						Clouds("big")
				SCORE.update()
				SCORE.draw()

			# Quits the game if this is the user's desire.
			elif event.type == pygame.QUIT:
				terminate()

		# Updates the image of the dinosaur before showing the "GAME OVER" screen.
		if GAMEOVER:
			if not Dino.isDucking:
				Dino.image = load("rex.png", -1)
			else:
				Dino.image = load("ducked.png", -1)
			
		# Draws all sprites on the screen in the correct order.
		screen.blit(background, (0, 0))
		clouds.draw(screen)
		cactuses.draw(screen)
		ground_group.draw(screen)
		player_group.draw(screen)
		pterodactyls.draw(screen)
		scoreboard.draw(screen)
		screen.blit(pygame.transform.scale(load("HI.png", -1), (30, 18)), (20, 20))

		pygame.display.flip()

		# Checks if the "GAME OVER" screen should be shown.

		if GAMEOVER:
			gameover()
			# Ends the game.
	
def start_screen():
	global first
	# Declares text for the title of the game.
	text = ["T-REX RUNNER"]

	# Sets the font and the text's coordinates.
	font = pygame.font.Font(None, 30)
	text_coord = 100

	# Spawns 20 clouds already on the start screen.
	for i in range(20):
			Clouds(False, True)

	# Enters the looping cycle of showing the start screen.
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()

			# Exits the process if a key was pressed.
			elif event.type == pygame.KEYDOWN or \
					event.type == pygame.MOUSEBUTTONDOWN:
				return

		# Draws all sprites on the screen before starting the game.
		screen.blit(background, (0, 0))
		cactuses.draw(screen)
		clouds.draw(screen)
		ground_group.draw(screen)
		player_group.draw(screen)
		scoreboard.draw(screen)
		screen.blit(pygame.transform.scale(load("HI.png", -1), (30, 18)), (20, 20))

		
		# Sets the rules to draw the text.
		for line in text:
			screen.blit(font.render(line, 1, pygame.Color(85, 85, 85)), (370, \
				100 + font.render(line, 1, pygame.Color(85, 85, 85)).get_rect().height))

		# Updates the image only if it is the start of the game.
		if first:
			pygame.display.flip()
			first = False

# Shows the "GAME OVER" screen.
def gameover():
	global GAMEOVER
	GAMEOVER = True
	die_sound.play()

	# Updates the high score if the previous high score is less than the current score.
	if int(open("scoreboard.txt", 'r').read()) < SCORE.score:
		with open("scoreboard.txt", 'w') as scoreb:
			scoreb.write(SCORE.str)
			scoreb.close()

	# Lets the "GAME OVER" screen cycle work.
	while GAMEOVER:
		for event in pygame.event.get():
			# ...
			if event.type == pygame.QUIT:
				terminate()

			# Exits the "GAME OVER" screen upon either...
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					restart()

			# or...
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					Button = pygame.Rect(420, 120, 52, 46)
					if Button.collidepoint(event.pos):
						restart()

		# Puts the images to the screen.
		screen.blit(pygame.transform.scale(load("gameover.png", -1), (285, 16)), (300, 80))
		screen.blit(pygame.transform.scale(load("replay.png", -1), (52, 46)), (420, 120))

		# Updates the screen.
		pygame.display.flip()

# Restarts the game.
def restart():
	global Dino, Ground, SCORE, HIGHSCORE, background, gamespeed, \
	 cactuses, backgrounds, ground_group, player_group, scoreboard, \
	 GAMEOVER, STEP, SCORE, first, pterodactyls, clouds

	# Constant.
	STEP = 25

	# Starting score should always begin with 0.
	SCORE = 0

	# Organising all sprite groups.
	cactuses = pygame.sprite.Group()
	backgrounds = pygame.sprite.Group()
	ground_group = pygame.sprite.Group()
	player_group = pygame.sprite.Group()
	scoreboard = pygame.sprite.Group()
	pterodactyls = pygame.sprite.Group()

	# Declaring gamespeed.
	gamespeed = 2

	# Setting main objects.
	Dino = Player()
	Ground = Grounds()
	SCORE = SCORES()

	# Declaring that the game has just started.
	GAMEOVER = False

	# Setting timers for all unspeedable events.
	pygame.time.set_timer(1, 1) # Dino jumping.
	pygame.time.set_timer(3, 160) # updating Dino's frames.
	pygame.time.set_timer(8, 50) # spawning cactuses.
	pygame.time.set_timer(10, 180) # updating score and spawning clouds.

	background = pygame.Surface((1200, 500))
	background.fill((235, 235, 235))

	# Starting the game's processes.
	update_score()
	HIGHSCORE = HIGHSCORES()
	if first:
		clouds = pygame.sprite.Group()
		start_screen()
	main()
# Ends the restart process with calling the main game cycle.


try:
	# Starting the game.
	restart()
except Exception as e:
	print(e)
