import tkinter as tk
from tkinter import PhotoImage 
from tkinter import messagebox
import random
from PIL import Image
from playsound import playsound
# Pour le fun, on a mis des petits sons
# Se référer au readme.txt pour installation

################ Initialisations des variables ################

global direction
global pause
global lifes
global mode_gamemode
global frame
global gm
global wave_counter
global victory

# Ici les valeurs par défaut du jeu si jamais le joueur ne séléctionne pas de mode de jeu
lifes = 1 # Nombre de vie du joueur
fire_rate = 5 # Le nombre de cycle de ticking au bout duquel le mobs tirent
vitesse_ticks = 20 # La vitesse du jeu; combien de nanosecondes entre chaque itération de la fonction ticking  (env 50fps ici)
mode_gamemode = -1 #Le mode de jeu, se référer à la fonction gamemode pour le détail
frame = 0 # Cette variable s'incrémente à chaque tick, et si elle atteint le nombre d'image du GIF, elle est réinitialisée
warnings = ""
gm = "Mode Interdit"
wave_counter = 0
pause = False
victory = 0
path = "E:/Documents/Code/fsi-main/" # Chemin d'accès par défaut / A MODIFIER SI CHANGEMENT DE POSTE

# Ici on randomise la direction initale des mobs (1 ou -1)
direction = random.randint(-1, 1)
while direction == 0:
    direction = random.randint(-1, 1)

# Les listes des objets à parcourir
Liste_mobs = []
Liste_bullets = []
Liste_player = []
Liste_wave = []
background_images = []

# Chemin d'accès des images
mob_img_path = f"{path}images/mob.png"
player_img_path = f"{path}images/player.png"
player_shoot_img_path = f"{path}images/player_shoot.png"
player_hit_img_path = f"{path}images/player_hit.png"
bullet_img_path = f"{path}images/bullet.png"
missile_img_path = f"{path}images/missile.png"
background_img_path = f"{path}images/background.gif"
bullet_mob_img_path = f"{path}images/bullet_mob.png"
explosion_img_path = f"{path}images/explosion.png"
fumees_img_path = f"{path}images/fumees.png"
wave_img_path = f"{path}images/wave.png"

################ CLASSES ################

# Les différents mobs présents à l'écran
class Mobs:
    def __init__(self, canvas, x_position):  
        self.x_position = x_position
        self.y_position = 70
        self.can = canvas
        self.sprite = canvas.create_image(self.x_position, self.y_position, image=mob_image)
        return
# Si le mob est touché, son sprite est supprimé et il est retiré de la liste des mobs
    def hit(self):
        print("hit!")
        self.can.delete(self.sprite)
        Liste_mobs.remove(self)
        return
# Les mobs se déplacement en ligne droite, si l'un d'eux atteint un bord, alors la variable "direction" change et leur 
# déplacement est inversé
    def mob_move(self):
        global direction
        if self.x_position >= 495:
            direction = -1
        elif self.x_position <= 5:
            direction = 1
        if pause == True:
            return
        self.can.move(self.sprite, (direction * 4), 0)
        self.x_position += (4 * direction)
        return

# La classe player qui n'est instanciée qu'une fois avec le joueur
class Player:
    def __init__(self, canva, position, life):
        self.can = canva
        self.position = position
        self.life = life
        self.y_position = 450
        self.sprite = canva.create_image(self.position, self.y_position, image=player_image)
        return

    def move_player(self, valuex, valuey):
        coord_player = canva.coords(self.sprite)
        if pause == True:
            return
        if self.position < 10:
            canva.coords(self.sprite, 10, coord_player[1])
            self.position = 10
        elif self.position > 490:
            canva.coords(self.sprite, 490, coord_player[1])
            self.position = 490
        elif self.y_position > 490:
            canva.coords(self.sprite, coord_player[0], 485)
            self.position = 490
        self.can.move(self.sprite, valuex, valuey)
        return
    
    def check_life(self):
        if self.life <= 0:
            canva.delete(self.sprite)
            self.sprite = canva.create_image(self.position, self.y_position, image=explosion_image)
            playsounds(5)
            messagebox.showerror("Game Over", "Le wokisme est mort")
            if mode_gamemode == -1:
                messagebox.showinfo("Bien tenté", "Fallait séléctionner un mode de jeu :)")
            main.quit()
        return
    def player_shoot(self):
        print("tir !")
        Liste_bullets.append(Bullets(canva, self.position, self.y_position, 1))
        canva.delete(self.sprite)
        self.sprite = canva.create_image(self.position, self.y_position - 19, image=player_shoot)
        main.after('100', self.back_to_main_sprite)
        return
    def back_to_main_sprite(self):
        canva.delete(self.sprite)
        self.sprite = canva.create_image(self.position, self.y_position, image=player_image)
        return
    
    def wave_shoot(self):
        Liste_wave.append(Wave(canva, self.position, self.y_position))

# La classe Bullet qui comprend toutes les balles, du joueur et des mobs
class Bullets:
    def __init__(self, canvas, x_position, y_position, mode=1):
        self.y_position = y_position
        self.can = canvas
        self.mode = mode
        if mode == 1: 
            self.y_position = player.y_position - 15
            self.x_position = x_position
            self.sprite = canvas.create_image(self.x_position, self.y_position, image=missile_image)
        else:
            self.x_position = x_position
            self.y_position = 85
            self.sprite = canvas.create_image(self.x_position, self.y_position, image=bullet_mob_image)
            

        self.move_bullet(mode) 
        return

    def move_bullet(self, mode):
        self.mode = mode
        if pause == True:
            return
        if mode == 1:
            self.y_position -= 10
            self.can.move(self.sprite, 0, -10)
        elif mode == 0:
            self.y_position += 5
            self.can.move(self.sprite, 0, 5)
        self.check_collision()
        return

    def check_collision(self):        
        if abs(self.y_position - player.y_position) < 15 and abs(self.x_position - player.position) < 15:
            canva.delete(player.sprite)
            player.sprite = canva.create_image(player.position, player.y_position, image=player_hit_image)
            Liste_bullets.remove(self)
            self.can.delete(self.sprite)
            player.life -= 1
            canva.after('1000', player.back_to_main_sprite)
            return
                
        for mob in Liste_mobs:
            if abs(self.y_position - mob.y_position) < 12 and abs(self.x_position - mob.x_position) < 12:
# Ici on modifie l'image du sprite par cette d'une explosion et on attend une seconde avant de supprimer le sprite
# On supprime la balle immediatement celà dit
                canva.delete(mob.sprite)
                mob.sprite = canva.create_image(self.x_position, self.y_position, image=explosion_image) 
                Liste_bullets.remove(self)
                self.can.delete(self.sprite)
                canva.after('1000', mob.hit)
                return

        if self.y_position >= 480 or self.y_position <= 0:
            self.can.delete(self.sprite)
            Liste_bullets.remove(self)
            return

# Dernière classe ajoutée un peu dernière minute: un pouvoir spécial d'attaque qui permet de contrer les balles ennemies
class Wave:
    def __init__(self, canva, x_position, y_position):
        self.steps = 40
        self.x_position = x_position
        self.y_position = y_position
        self.can = canva
        self.sprite = canva.create_image(self.x_position, self.y_position -20, image=wave_image)
    
    def move_wave(self):
        if pause == True:
            return
        self.steps -= 1
        self.y_position -= 5
        self.can.move(self.sprite, 0, -5)
        self.check_collision(self.steps)
        return
        
    def check_collision(self, steps):
        if steps == 0:
            Liste_wave.remove(self)
            self.can.delete(self.sprite)
            return
        for bullet in Liste_bullets:
            self.stop = 3
            if abs(self.y_position - bullet.y_position) < 30 and abs(self.x_position - bullet.x_position) < 80 :
                bullet.can.delete(bullet.sprite)
                Liste_bullets.remove(bullet)
                print("balle arrêtée")
                self.stop -=1
                if self.stop <= 0:
                    Liste_wave.remove(self)
                    self.can.delete(self.sprite)
        
        return

################ FONCTIONS DE JEU ################

# Gestion du temps qui passe et des évenements liés
# Il s'agit de la fonction centrale, qui réalise les actions du programme toutes les X ms, 
# C'est la fonction principale du jeu qui permet de déplacer les éléments et la gestion des évènements (GIF, salves spéciales)
def ticking(t):
    global frame
    global initial
    global victory
    initial = 0
    # Si jamais la variable "pause" est True, c'est que la touche echap a été pressée. La boucle s'arrête alors
    # Bloquant le déplacement et les tirs. La fonction ne reprend que lorsque le bouton "reprendre" et donc la
    # fonction "resume_game" est lancée
    if pause == True:
        return  
    
    # Changement de l'image de background et update du numéro de la frame à afficher
    gif_power(frame)
    frame += 1
    if mode_gamemode == -1 and t == 0:
        playsounds(6)
    
    # On enclenche les fonction de déplacement et on remet les sprite au dessus du background    
    canva.tag_raise(player.sprite)

    for wave in Liste_wave:
        wave.move_wave()
        canva.tag_raise(wave.sprite)

    for mob in Liste_mobs:
        mob.mob_move()
        canva.tag_raise(mob.sprite)
        
    # On update le label de bas de fenêtre
    status_bar.config(text=f"Vies restantes: {player.life} // {warnings} Coups spéciaux restant: {wave_counter}")
    
    # On vérifie la vie du joueur et la présence de mobs
    player.check_life()
    victory = check_no_mobs()
    
    if victory == 1:
        playsounds(10)
        messagebox.showinfo("Félicitations", "Le wokisme gagne une nouvelle bataille !")
        messagebox.showinfo("Félicitations", "Merci d'avoir joué à ce jeu pas ouf")
        main.quit()
    
    # Si la variable t (qui augmente de 1 à chaque tick) est un multiple de fire_rate, 
    # alors les mobs tirent
    if t % fire_rate == 0:
        for mob in Liste_mobs:
            Liste_bullets.append(Bullets(canva, mob.x_position, 75, 0))
        # Toutes les 3 salves: BING BONG triple salve
        if t % (fire_rate * 2) == 0 and t != 0:
            for mob in Liste_mobs:
                Liste_bullets.append(Bullets(canva, mob.x_position -30, 75, 0))
                Liste_bullets.append(Bullets(canva, mob.x_position + 30, 75, 0))
            playsounds(7)
        else:
            playsounds(4)
    
    # Déclenche les fonction "move_bullet" des balles
    for bullet in Liste_bullets:
        bullet.move_bullet(bullet.mode)
        canva.tag_raise(bullet.sprite)
    
    # Si on arrive à la fin du gif, on reboucle
    if frame == len(background_images):
        frame = 0
    
    t += 1 # on incrémente t pour le tire des mobs
    main.after(vitesse_ticks, lambda: ticking(t))
    return

# Menu pause
def pause_menu():
    global pause
    pause = True # On change la variable pause à True, ce qui permet de stopper la boucle ticking

    # Affichage et paramétrage de la fenêtre de pause 
    pause_window = tk.Toplevel()
    center_window(pause_window, 200, 100)
    pause_window.title("PAUSE")
    pause_window.configure(background="black")
    pause_window.attributes('-alpha', 0.9)

    # Pour éviter de fermer la fenêtre avec la croix 
    # (Sinon la fonction resume_game ne se lance pas et donc la fonction ticking non plus )
    pause_window.overrideredirect(True)

    # Paramétrage des boutons restart et quitter
    restart = tk.Button(pause_window, text="Reprendre", command=lambda: resume_game(pause_window))
    quit_button = tk.Button(pause_window, text="Quitter", command=main.quit)
    restart.place(relx=0.33, rely=0.5, anchor='center')
    quit_button.place(relx=0.66, rely=0.5, anchor='center')

    # Pour faire en sorte de la fenêtre de pause prenne le devant
    pause_window.grab_set()
    pause_window.focus_set()
    return
# Et sa fonction associée pour reprendre le jeu
def resume_game(pause_window):
    global pause
    pause_window.destroy() # destruction de la fenêtre de pause

    pause = False # Remise à
    ticking(0) # Reprise de la fonction du temps qui passe quand on sort du menu pause
    return

# Gestion des touches
def keypress(event):
    global warnings
    global wave_counter
    if event.keysym == "Right" or event.keysym == "d":
        player.position += 10
        player.move_player(10, 0)
    if event.keysym == "Left" or event.keysym == "q":
        player.position -= 10
        player.move_player(-10, 0)
    if event.keysym == "Up" or event.keysym == "z":
        player.y_position -= 10
        player.move_player(0, -10)
    if event.keysym == "Down" or event.keysym == "s":
        player.y_position += 10
        player.move_player(0, 10)
    if event.keysym == "Escape":
        pause_menu()
    if event.keysym == "space":
            player.player_shoot()
    if event.keysym == "a":
        if wave_counter != 0:   
            player.wave_shoot()
            wave_counter -= 1
            playsounds(2)
        else:
            warnings = "A COURT DE MUNITIONS SPECIALES !!"
            
    
    return

# vérifie si la liste "Liste_mobs" est vide pour gagner la partie
def check_no_mobs():
    if len(Liste_mobs) == 0:
        return 1

# Cette fonction permet de center la fenetre dans l'écran principal.
# Nous mettons des valeurs par défaut pour la fenêtre principale,
# Nous la réutilisons pour le menu pause, avec d'autres parametre de taille
def center_window(fenetre, w = 500, h = 525):
    screen_w=fenetre.winfo_screenwidth()
    screen_h=fenetre.winfo_screenheight()
    x = (screen_w // 2) - (w // 2)
    y = (screen_h //2 ) - (h // 2)
    fenetre.geometry(f"{w}x{h}+{x}+{y}")
    return

# Dernière fonctionnalité rajoutée, la selection de mode de jeu
# Les différents boutons permettent de séléctionner le mode de jeu. La variable qui en résulte est passé
# à la fonction gamemode
# On a donc 4 boutons de séléction de diffiulté, et deux Labels pour afficher le titre et les crédits
def difficulty_selector():
    start_menu = tk.Toplevel()
    center_window(start_menu)
    background_menu_image = PhotoImage(file=f"{path}images/background.png")
    diff_menu_background = tk.Label(start_menu, image=background_menu_image)
    diff_menu_background.pack()
    
    #playsounds(9)
    
    titre = tk.Label(start_menu, text="WOKE INVADERS",font=("Arial", 35, "bold"),  bg='white')
    credits = tk.Label(start_menu, text="La team VMC (Valentin, Mikael, Charles) ** Tirer: <Espace> ; Coup spécial: <a>")
    mode_god = tk.Button(start_menu, text="GodMode", command= lambda: gamemode(start_menu, 0), width=20, height=5)
    mode_fragile = tk.Button(start_menu, text="Fragile", command= lambda: gamemode(start_menu, 1), width=20, height=5)
    mode_challenge = tk.Button(start_menu, text="Challenge", command= lambda: gamemode(start_menu, 2), width=20, height=5)
    mode_normal = tk.Button(start_menu, text="Normal", command= lambda: gamemode(start_menu, 3), width=20, height=5)
    mode_mystere = tk.Button(start_menu, text="???", command= lambda: gamemode(start_menu, 4), width=20, height=5)
    
    titre.place(relx=0.5, rely=0.1, anchor='n')
    credits.place(relx=0.5, rely=1, anchor='s')
    mode_god.place(relx=0.9, rely=0.9, anchor='se')
    mode_fragile.place(relx=0.1, rely=0.3, anchor='nw')
    mode_normal.place(relx=0.5, rely=0.6, anchor='center')
    mode_challenge.place(relx=0.1, rely=0.9, anchor='sw')
    mode_mystere.place(relx=0.9, rely=0.3, anchor='ne')
    start_menu.wait_window()
    return

# En fonction du mode de jeu choisi, on altère les caractéristiques du jeu (vitesse de tir et nombre de vies)
def gamemode(menu, mode):
    global mode_gamemode
    global lifes
    global fire_rate
    global gm
    global wave_counter
    mode_gamemode = mode
    if mode_gamemode == 0:
        print("mode = Godmode (", mode_gamemode, ")") 
        lifes = 10000
        fire_rate = 5
        wave_counter = 1000
        gm = "GodMode"
    elif mode_gamemode == 1:
        print("mode = Fragile (", mode_gamemode, ")") 
        lifes = 1
        fire_rate = 50
        wave_counter = 5
        gm = "Mode Fragile"
    elif mode_gamemode == 2:
        print("mode = Challenge (", mode_gamemode, ")") 
        lifes = 4
        fire_rate = 10
        wave_counter = 3
        gm = "Mode Challenge"
    elif mode_gamemode == 3:
        lifes = 3
        fire_rate = 50
        wave_counter = 7
        print("mode = Normal (", mode_gamemode, ")") 
        gm = "Mode Normal"
    elif mode_gamemode == 4:
        lifes = 0
        fire_rate = 1
        wave_counter = 0
        gm = "Mode 6 Janvier"
    menu.destroy()
    return 

# Pour la déconne, des petits effets sonores
def playsounds(sound):
    gallery_sounds = ["biden_holy_f.mp3", "obamna.mp3", "cmon_man.mp3", "skill_issue.mp3", 
                    "you_are_fake_news.mp3", "fake_news.mp3", "wall.mp3", "bing-bong.mp3", 
                    "win.mp3", "main_music.mp3", "approve.mp3"]
    s = f"{path}sounds/{gallery_sounds[sound]}"
    playsound(s, block=False)
    return

# Change le background en fonction du numéro de frame où nous sommes
def gif_power(frame=0):
    global current_background_image
    current_background = background_images[frame]
    canva.delete(current_background_image) #destruction de la frame précédente
    current_background_image =canva.create_image(250, 250, image=current_background)
    return 


################ PROGRAMME PRINCIPAL ################

# Ici on a la création de la fenêtre tkinter, avec son titre, sa géometrie, sa couleur de fond.
main = tk.Tk()
main.withdraw()

# Ici .withdraw et .deiconify permettent d'afficher la fenetre de sélection de mode.
# Si on ferme la fenêtre comme un sauvage, c'est pas bien
# On a donc ici le menu de sélection de difficulté/menu d'acceuil
difficulty_selector()

main.deiconify()
main.title("Woke Invaders")
center_window(main)
main.configure(background="black")

# Création du canevas
canva = tk.Canvas(main,height=500, width=500)
canva.pack(anchor=tk.CENTER, expand=False)

# On charge les images dans le programme 
mob_image = PhotoImage(file=mob_img_path)
player_image = PhotoImage(file=player_img_path)
player_hit_image = PhotoImage(file=player_hit_img_path)
player_shoot = PhotoImage(file=player_shoot_img_path)
bullet_image = PhotoImage(file=bullet_img_path)
missile_image = PhotoImage(file=missile_img_path)
explosion_image = PhotoImage(file=explosion_img_path)
bullet_mob_image = PhotoImage(file=bullet_mob_img_path)
background_image = PhotoImage(file=background_img_path)
fumees_image = PhotoImage(file=fumees_img_path)
wave_image = PhotoImage(file=wave_img_path)

#Ici On gère l'aspect GIF du background:
#D'abord avec le module Image de Pillow, on récupère les informations
info = Image.open(background_img_path)

#Grace à n_frame, on peut savoir combien d'images compte le GIF
frames = info.n_frames

# On met alors chaque image "f" dans une liste "Background_images" que nous pouront parcourir à chaque tick 
for i in range(frames):
    f = tk.PhotoImage(file=background_img_path, format=f"gif -index {i}")
    background_images.append(f)

# On affiche la première image pour pouvoir entemer le cycle de suppression/création dans gif_power
current_background_image = canva.create_image(250, 250, image=background_images[0])
canva.tag_lower(current_background_image)

# Ici on créé "en dur" les mobs
mob1 = Mobs(canva, 100)
mob2 = Mobs(canva, 150)
mob3 = Mobs(canva, 200)
mob4 = Mobs(canva, 250)
mob5 = Mobs(canva, 300)
mob6 = Mobs(canva, 350)
mob7 = Mobs(canva, 400)
player = Player(canva, 250, lifes)

# Ajout des mobs dans une liste pour pouvoir les parcourirs
Liste_mobs.extend([mob1, mob2, mob3, mob4, mob5, mob6, mob7])

# Affichage des barres du haut et du bas de la fenêtre
title_bar = tk.Label(main, width=500, text=f"WOKE INVADERS: {gm}", fg= "white", bg="black")
status_bar = tk.Label(main, width=500, text=f"Vies restantes:{player.life}", fg= "white", bg="black")
status_bar.place(relx=0.5, rely=1, anchor='s')
title_bar.place(relx=0.5, rely=0, anchor='n')

# bind nous permet de récupérer les touches qu'enclenchent le joueur, qui sont traitées par la fonction keypress
main.bind("<Key>", keypress)

# Initialisation de la fonction ticking, qui gère le temps du jeu
ticking(0)

# Mainloo^p d'affichage tkinter
main.mainloop()
