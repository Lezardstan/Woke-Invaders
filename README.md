# fsi

Jeu Python:

SUPER LIENS:
https://pythonfaqfr.readthedocs.io/en/latest/prog_even_tkinter.html



Space invaders:

#LE BUT DE CE FICHIER EST DE LISTER CE QUE LE JEU DOIT FAIRE ET QUELS OBJETS EXISTENT EN LUI
#IL TENTE DE LISTER EGALEMENT LA LOGIQUE INTERNE;
#J'AI TOUT MIS EN ANGLAIS PARSQUE LES VARIABLES EN FRANCAIS C'EST INFERNAL

CLASSES:
- enemies
	--size: square: hitbox & sprite
	--coordonates: x & y
	--state (damaged / alive or dead)
	--movement left/right
	--sprite, shape(s) ?

- player
	--size: square
	--coordonates: x & y
	--state (damaged / alive or dead): 3 values 0, 1 and 2
	--movement: dictated by player input
	--sprite

- bullets
	--size
	--coordonates
	--movement
	--sprite

- enemies_bullets
	--size
	--coordonates
	--movement
	--sprite


create main window
Start at main menu
*Title
*Buttons
	Buttons: 
		Start ==> start a game
		Quit ==> Close the program


The game always start in the same state
enemy.state = 1
player.life = 3
direction = random 0 or 1
  
Enemies goes back and forth left and right at a fixed speed
	- When the far most right touch the right edge, they reverse direction
	- When the far most left touch the left edge, they reverse direction

Enemies fire bullets every x seconds

They come from one of the sprite (random ?)

If a bullet hits an enemy, it disappear

If an "enemies_bullets" hits the player:
	- player.life = player.life - 1
	- If number of life = 0 ==> Game Over ==> Back to main menu

pause_menu: stops the game while displaying a windows with two buttons to quit or continue 



Things that go infinitly (while)
- Main window

- Enemies moving:
	=> direction = 0 or 1 (left or right)
	=> enemy_x += 1
	=> if enemy_x(5) = 255 or enemy5.x = 0 (largeur de la fenetre)
		then: if direction = 1
				then direction = 0
			else
				direction = 1
- Collision detector
	=> if enemy_position - bullet_position(any) = 0
		then 
			enemy.state = 0
	=> Outputs an event
- Input detector from keyboard
	=> if keyboard_left = 1: player.x += 1
	=> if keyboard_right = 1: player.x += (-1)
	=> if <ESC> = 1: start pause_menu
- Life checker:
	=> if Life = 0 
		=> Game over
