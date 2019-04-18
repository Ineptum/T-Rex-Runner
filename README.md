# T-Rex Runner Version 1.0.0 14/02/2018
# E-mail: KatKollare@yandex.ru

This game is somewhat a clone of the famous Google unnamed game.
Unfortunately, the original game is only accessable through Chrome browser
when your computer doesn't seem to be connected to the internet.

I decided to solve the problem of the game's inaccessability.

Here's a quick look at what is presented in the game:
	
	You may exit the game any time.

	You play as a dinosaur called T-Rex.

	T-Rex is running towards the right edge of the screen and is encountering
	 different enemies he has to avoid on his way through.
	Your goal is to obtain as many points as you can whilst not getting hit
	 by any enemy you meet.

	There are 2 types of hostile beings in the game: cactuses and pterodactyls.
	 Cactuses can only be avoided by jumping over them and pterodactyls can be avoided either
	 by jumping over them or by ducking underneath them depending on their flight height.

	To avoid enemies, note this:
		The dinosaur can jump [SPACE BAR or UP KEY] and can
		 also perform ducking [DOWN KEY].

	Each time the amount of points gets divisible by 250 (not including 0)
	 the game automatically speeds up a little. You can only speed up 8 times.

	You cannot win in this game. The game is all about obtaining points.
	 Your highscore will be written to a file called "scoreboard.txt" in the same
	 directory your "trex.py" file is in. You may play with it as you like.

	Upon losing the game you are being presented with a so called "game over screen".
	 You can either restart the game by pressing [SPACE BAR] or clicking on the restart
	 button in the center of the screen with [LMB].

Quick summary finished. 

These are things you perhaps would want to know:
	
	Each object in the game is presented by a specific class:
		Clouds(pygame.sprite.Sprite) for clouds, 
		Grounds(pygame.sprite.Sprite) for ground,
		Cactus(pygame.sprite.Sprite) for cactuses,
		Pterodactyl(pygame.sprite.Sprite) for pterodactyls,
		Player(pygame.sprite.Sprite) for the player 
		 (the object of this class is called Dino),
		HIGHSCORES(pygame.sprite.Sprite) for highscore,
		SCORES(pygame.sprite.Sprite) for score.

	The game cycle is split into several functions:
		def update_score() -- updates highscore,
		def load(name, colorkey=None) -- loads an image.
		def terminate(), 
		def speedup(),
		def main(),
		def start_screen(),
		def gameover(),
		def restart().

	The game declares all objects (restart), then loads all of the game's sprites (load),
	 then updates highscore (update_score), then reveals the start screen (start_screen),
	 then runs the game (main), then it may speed up (speedup), then it shows the gameover screen 
	 (gameover) and after that it may start all of this again (restart). Throughout this whole process
	 the game may be exited (terminate).
