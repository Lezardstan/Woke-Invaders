import tkinter as tk
from tkinter import PhotoImage 
from tkinter import messagebox
import random
from PIL import Image
from playsound import playsound

#########################################IMPORTANT#####################################################
# Se référer au readme.txt pour installation car on utilise des bibliothèque qui ne sont pas par défaut
#######################################################################################################

# WOKE INVADERS - Entre tradition vidéoludique et modernité politique
# Auteurs: Charles G. Mikael K. Valentin G.
# Version 1


################ Initialisations des variables ################

global direction                        # Détermine la direction initiale des mobs, utilisée dans les classes, voir plus bas pour initialisation
global pause                    
global lifes 
global mode_gamemode
global frame
global gm
global wave_counter
global can_shoot

### Ici les valeurs par défaut du jeu si jamais le joueur ne séléctionne pas de mode de jeu et ferme le menu comme un sauvage ###

lifes = 1                               # Nombre de vie du joueur
fire_rate = 5                           # Le nombre de cycle de ticking au bout duquel le mobs tirent
vitesse_ticks = 20                      # La vitesse du jeu; combien de nanosecondes entre chaque itération de la fonction ticking  (env 50fps ici)
mode_gamemode = -1                      #Le mode de jeu, se référer à la fonction gamemode pour le détail
frame = 0                               # Cette variable s'incrémente à chaque tick, et si elle atteint le nombre d'image du GIF, elle est réinitialisée
warnings = ""                           # Affichage avec des infos
gm = "Mode Interdit"                    # Nom du mode de jeu
wave_counter = 0                        # Nombre de coups spéciaux
pause = False                           # Statut de la pause
victory = 0                             # Etat de victoire, si victory = 1 alors fin du jeu
path = "E:/Documents/Code/fsi-main/"    # Chemin d'accès par défaut / A MODIFIER SI CHANGEMENT DE POSTE


# Ici on randomise la direction initale des mobs (1 ou -1)
direction = random.randint(-1, 1)
while direction == 0:
    direction = random.randint(-1, 1)

# Les listes des objets à parcourir
# Elles sont explicitées plus bas
Liste_mobs = []
Liste_bullets = []
Liste_wave = []
background_images = []

# Chemin d'accès des images
mob_img_path = f"{path}images/mob.png"
player_img_path = f"{path}images/player.png"
player_shoot_img_path = f"{path}images/player_shoot.png"
player_hit_img_path = f"{path}images/player_hit.png"
missile_img_path = f"{path}images/justice.png"
background_img_path = f"{path}images/background3.gif"
bullet_mob_img_path = f"{path}images/bullet_mob.png"
explosion_img_path = f"{path}images/explosion.png"
fumees_img_path = f"{path}images/fumees.png"
wave_img_path = f"{path}images/wave.png"
brandon_img_path = f"{path}images/brandon.png"
gallery_sounds = ["biden_holy_f.mp3", "obamna.mp3", "cmon_man.mp3", "skill_issue.mp3", "you_are_fake_news.mp3", "fake_news.mp3", "wall.mp3", "bing-bong.mp3", 
                "win.mp3", "approve.mp3"]
################ CLASSES ################

# Les différents mobs présents à l'écran
class Mobs:
    def __init__(self, x_position):  
        self.x_position = x_position
        self.y_position = 100
        self.sprite = canva.create_image(self.x_position, self.y_position, image=mob_image)
        return
# Si le mob est touché, son sprite est supprimé et il est retiré de la liste des mobs
    def hit(self):
        print("hit!")
        canva.delete(self.sprite)
        Liste_mobs.remove(self)
        return
# Les mobs se déplacement en ligne droite, si l'un d'eux atteint un bord, alors la variable "direction" change et leur 
# déplacement est inversé
    def mob_move(self):
        global direction
        if self.x_position >= 850:
            direction = -1
        elif self.x_position <= 5:
            direction = 1
        if pause == True:
            return
        canva.move(self.sprite, (direction * 4), 0)
        self.x_position += (4 * direction)
        return

# La classe player qui n'est instanciée qu'une fois avec le joueur
class Player:
    def __init__(self, position, life):
        self.position = position
        self.life = life
        self.y_position = 700
        self.sprite = canva.create_image(self.position, self.y_position, image=player_image)
        return

    def move_player(self, valuex, valuey):
        coord_player = canva.coords(self.sprite)
        if pause == True:
            return
        if self.position < 10:
            canva.coords(self.sprite, 10, coord_player[1])
            self.position = 10
        elif self.position > 850:
            canva.coords(self.sprite, 850, coord_player[1])
            self.position = 850
        elif self.y_position > 1000:
            canva.coords(self.sprite, coord_player[0], 1000)
            self.position = 1000
        canva.move(self.sprite, valuex, valuey)
        return
    
    def check_life(self):
        if self.life <= 0:
            canva.delete(self.sprite) # Supression de l'image originale 
            self.sprite = canva.create_image(self.position, self.y_position, image=explosion_image) # Remplacement de ladite image par une explosion
            canva.after('1000')
            playsounds(5)
            messagebox.showerror("Game Over", "Le wokisme est mort")
            if mode_gamemode == -1:
                messagebox.showinfo("Bien tenté", "Fallait séléctionner un mode de jeu :)")
            main.quit()
        return
    def player_shoot(self): 
        global can_shoot
        if can_shoot = True:
            print("tir !")                                                                              # Affichage dans le temrinal
            Liste_bullets.append(Bullets(self.position, self.y_position - 19, 1))                       # On créé une balle que l'on rajouter à la liste, avec une position 19px au dessus du joueur
            canva.delete(self.sprite)                                                                   # Sur ces lignes, on remplace le sprite du joueur par une image du joueur qui tire
            self.sprite = canva.create_image(self.position, self.y_position - 19, image=player_shoot)
            main.after('100', self.back_to_main_sprite)
            can_shoot = False                                                                           # passe en false pour éviter que le joueur tire à nouveau
            main.after(300, lambda: self.reset_shoot())                                                 # après 300ms, la fonction anonyme lambda appelle can_shoot et l'a passe en true# après 1s, on reviens au sprite normal
        return
    
    def back_to_main_sprite(self):                                                                  # On utilise une fonction pour faciliter l'utilisation de la fonction "after"
        canva.delete(self.sprite)
        self.sprite = canva.create_image(self.position, self.y_position, image=player_image)
        return
    
    def wave_shoot(self):                                                                           # Le coup spécial, avec une idée similaire que pour les tirs classique
        Liste_wave.append(Wave(self.position, self.y_position))
        
    def reset_shoot(self):
        global can_shoot
        can_shoot = True  # Permet au joueur de tirer à nouveau

# La classe Bullet qui comprend toutes les balles, du joueur et des mobs
class Bullets:
    def __init__(self, x_position, y_position, mode=1):
        self.y_position = y_position
        self.mode = mode                                # Le mode indique si la balle provient du joueur ou d'un mob
        if mode == 1:                                   # Selon ce mode, elles ont une position initiale différente, un sens inversé et un spread dans le cas des mobs
            self.y_position = player.y_position - 25
            self.x_position = x_position
            self.sprite = canva.create_image(self.x_position, self.y_position, image=missile_image)
            self.spread = 0                             # spread = 0 signifie aucun déplacement horizontal
        else:
            self.x_position = x_position
            self.y_position = 120
            self.sprite = canva.create_image(self.x_position, self.y_position, image=bullet_mob_image)
            self.s = random.randint(-1, 1)              # Le spread est généré comme pour la direction initiale, -1 ou +1
            while self.s == 0:
                self.s = random.randint(-1, 1)
            self.spread = -5 * self.s                   # qu'on multiplie par 5 pour avoir une direction horizontale que l'on peut intégrer dans la fonction de mouvement
        self.move_bullet(mode)                          # Une fois générée, la fonction move_bullet est appelée, et un premier check de collision est fait.
        return

    def move_bullet(self, mode):
        self.mode = mode
        if pause == True:                               # Si la pause est pressée, alors on arrête la fonction 
            return
        if mode == 1:                                   # Selon le mode, la balle va dans un sens u dans l'autre.
            self.y_position -= 20                       # Les balles du joueur vont plus vite que cette des mobs.
            canva.move(self.sprite, self.spread, -20)
        elif mode == 0:
            self.y_position += 5
            self.x_position += self.spread
            canva.move(self.sprite, self.spread, 5)
            
        self.check_collision()
        return

    def check_collision(self):        
        if abs(self.y_position - player.y_position) < 30 and abs(self.x_position - player.position) < 30: # En cas de collision avec le joueur (Si le centre de la balle est dans le carré de 30x30 autour du centre du joueur)
            canva.delete(player.sprite)                     # On remplace le sprite joueur par celui du joueur touché
            player.sprite = canva.create_image(player.position, player.y_position, image=player_hit_image)
            Liste_bullets.remove(self)                      # On supprime la balle de la liste
            canva.delete(self.sprite)                       # On supprime le sprite
            player.life -= 1                                # On retire 1 du compteur de vie du joueur
            canva.after('1000', player.back_to_main_sprite) # Après une seconde, on reviens au sprite normal du joueur
            return
                
        for mob in Liste_mobs:
            if abs(self.y_position - mob.y_position) < 20 and abs(self.x_position - mob.x_position) < 20:
# Ici on modifie l'image du sprite par cette d'une explosion et on attend une seconde avant de supprimer le sprite
# On supprime la balle immediatement celà dit
                canva.delete(mob.sprite)
                playsounds(3)
                mob.sprite = canva.create_image(self.x_position, self.y_position, image=explosion_image) 
                Liste_bullets.remove(self)
                canva.delete(self.sprite)
                canva.after('1000', mob.hit)
                return

        if self.y_position >= 1000 or self.y_position <= 0: # Si les balles dépassent les bord haut les bas de l'écran,
            canva.delete(self.sprite)                       # Elles sont retirées du canva
            Liste_bullets.remove(self)                      # Et supprimées de la liste
            return
        if self.x_position >= 860 or self.x_position <= 0:  # Si elles touchent un bord droit ou gauche
            self.spread = self.spread * -1                  # leur direction horizontale s'inverse
            return

# Dernière classe ajoutée un peu dernière minute: un pouvoir spécial d'attaque qui permet de contrer les balles ennemies
# Les waves fonctionnent comme les balles à deux différences: Elles ne vérifient ni les collisions avec le joueur ni les mobs, seulement avec les balles
# Seconde différences: 
# Elles disparaissent au bout d'un certain nombre de cycles (déplacement/check_collision) (self.step) OU d'un certain nombre de balles arrêtées (self.stop)
class Wave:
    def __init__(self, x_position, y_position):
        self.steps = 60                         # Le compteur de cycles
        self.stop = 5                           # Nombre de balles que le vague peut arrêter
        self.x_position = x_position
        self.y_position = y_position
        self.sprite = canva.create_image(self.x_position, self.y_position -20, image=wave_image)
    def move_wave(self):
        if pause == True:
            return
        self.steps -= 1                         # Là où le compteur de cycle est diminué
        self.y_position -= 5
        canva.move(self.sprite, 0, -5)
        self.check_collision(self.steps, )      # On lui envoi la variable également
        return
        
    def check_collision(self, steps):
        if steps == 0:                          # Si le nombre de steps atteint 0, la vague déspawn
            Liste_wave.remove(self)
            canva.delete(self.sprite)
            return
        for bullet in Liste_bullets:
            if abs(self.y_position - bullet.y_position) < 30 and abs(self.x_position - bullet.x_position) < 100 :
                canva.delete(bullet.sprite)
                Liste_bullets.remove(bullet)
                print("balle arrêtée")
                self.stop -=1
                if self.stop <= 0:
                    Liste_wave.remove(self)
                    canva.delete(self.sprite)
                    return
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
    status_bar.config(text=f"Vies restantes: {player.life}   Coups spéciaux restant: {wave_counter} \n {warnings}")
    
    # On vérifie la vie du joueur et la présence de mobs
    # Cet ordre fait que si le joueur et les mobs sont détruit à la même frame, le joueur perd
    player.check_life()
    check_no_mobs()
    
    # Si la variable t (qui augmente de 1 à chaque tick) est un multiple de fire_rate, 
    # alors les mobs tirent
    if t % fire_rate == 0:
        for mob in Liste_mobs:
            Liste_bullets.append(Bullets(mob.x_position, 120, 0))
        # Toutes les 3 salves: BING BONG triple salve
        if t % (fire_rate * 2) == 0 and t != 0:
            for mob in Liste_mobs:
                Liste_bullets.append(Bullets(mob.x_position -30, 120, 0))
                Liste_bullets.append(Bullets(mob.x_position + 30, 120, 0))
            playsounds(7)

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

# Gestion des touches, 
def keypress(event):
    global warnings
    global wave_counter
    if event.keysym == "Right" or event.keysym == "d":
        player.position += 20
        player.move_player(20, 0)
    if event.keysym == "Left" or event.keysym == "q":
        player.position -= 20
        player.move_player(-20, 0)
    if event.keysym == "Up" or event.keysym == "z":
        player.y_position -= 20
        player.move_player(0, -20)
    if event.keysym == "Down" or event.keysym == "s":
        player.y_position += 20
        player.move_player(0, 20)
    if event.keysym == "Escape":
        pause_menu()
    if event.keysym == "space":
            player.player_shoot()
    if event.keysym == "a":
        if wave_counter != 0:   
            player.wave_shoot()
            wave_counter -= 1 # compteur de vagues en réserve
            playsounds(2)
        else: # Si wave_counter = 0 alors, le message est updaté et aucune vague ne peut plus être tirée
            warnings = "A COURT DE MUNITIONS SPECIALES !!"
    return

# vérifie si la liste "Liste_mobs" est vide pour gagner la partie
def check_no_mobs():
    if len(Liste_mobs) == 0:
        run_victory()
        return 


def run_victory():
    canva.create_image(300, 300, image=brandon_image)
    canva.create_image(600, 600, image=brandon_image)
    canva.create_image(300, 600, image=brandon_image)
    canva.create_image(600, 300, image=brandon_image)
    playsounds(9)
    messagebox.showinfo("Félicitations", "Le wokisme gagne une nouvelle bataille !")
    messagebox.showinfo("Félicitations", "Merci d'avoir joué à ce jeu pas ouf")
    main.quit() #Fermeture du programme
    

# Cette fonction permet de center la fenetre dans l'écran principal.
# Nous mettons des valeurs par défaut pour la fenêtre principale,
# Nous la réutilisons pour le menu pause, avec d'autres parametre de taille
def center_window(fenetre, w = 1024, h = 860):
    screen_w=fenetre.winfo_screenwidth()        # Ce type de fonction récupère des informations sur l'écran
    screen_h=fenetre.winfo_screenheight()       # Les valeurs par défaut (1024x860) sont appliquées pour la fenêtre de selection de niveau
    x = (screen_w // 2) - (w // 2)              # Cette formule permet de placer la fenêtre au centre
    y = (screen_h //2 ) - (h // 2)              # x et y représentent le nombre de pixels d'éloignement de la fenetre du coin superieur gauche de l'écran
    fenetre.geometry(f"{w}x{h}+{x}+{y}")
    return

# Dernière fonctionnalité rajoutée, la selection de mode de jeu
# Les différents boutons permettent de séléctionner le mode de jeu. La variable qui en résulte est passé
# à la fonction gamemode
# On a donc 4 boutons de séléction de diffiulté, et deux Labels pour afficher le titre et les crédits
def difficulty_selector():
    #Le type TopLevel représente une fenêtre secondaire pour le programme, on créé la fenêtre et on la centre
    start_menu = tk.Toplevel() 
    center_window(start_menu)
    
    # Fond du menu de sélection
    background_menu_image = PhotoImage(file=f"{path}images/background2.png")
    diff_menu_background = tk.Label(start_menu, image=background_menu_image)
    diff_menu_background.pack()
    
    # On créé les bouttons de sélection et la barre de crédits
    credits = tk.Label(start_menu, width=860, font=('Arial', 12,'italic'), text="La team VMC (Valentin, Mikael, Charles) ** Tirer: <Espace> ; Coup spécial: <a>")
    mode_god = tk.Button(start_menu, font=('Arial', 20, 'bold'), text="GodMode", command= lambda: gamemode(start_menu, 0), width=15)
    mode_fragile = tk.Button(start_menu, font=('Arial', 20, 'bold'), text="Mode Fragile", command= lambda: gamemode(start_menu, 1), width=15)
    mode_challenge = tk.Button(start_menu, font=('Arial', 20, 'bold'), text="Mode Challenge", command= lambda: gamemode(start_menu, 2), width=15)
    mode_normal = tk.Button(start_menu, font=('Arial', 20, 'bold'), text="Mode Normal", command= lambda: gamemode(start_menu, 3), width=20)
    mode_mystere = tk.Button(start_menu, font=('Arial', 20, 'bold'), text="???", command= lambda: gamemode(start_menu, 4), width=15)
    
    # On les place avec des positions relatives
    credits.place(relx=0.5, rely=1, anchor='s')
    mode_god.place(relx=0.3, rely=0.85, anchor='n')
    mode_fragile.place(relx=0.3, rely=0.75, anchor='n')
    mode_normal.place(relx=0.5, rely=0.1, anchor='n')
    mode_challenge.place(relx=0.7, rely=0.75, anchor='n')
    mode_mystere.place(relx=0.7, rely=0.85, anchor='n')
    
    # "wait_window" permet de mettre en pause le programme jusqu'à ce que "start_menu" soit permée, 
    # Ce qui est fait soit manuellement soit en sélectionnant un niveau avec la fonction "gamemode"
    start_menu.wait_window()
    return

# En fonction du mode de jeu choisi, on altère les caractéristiques du jeu (vitesse de tir, nombre de coups spéciaux et nombre de vies)
def gamemode(menu, mode):
    global mode_gamemode
    global lifes
    global fire_rate
    global gm
    global wave_counter
    mode_gamemode = mode
    if mode_gamemode == 0:
        print("mode = Godmode (", mode_gamemode, ")") 
        lifes = 100000
        fire_rate = 5
        wave_counter = 1000
        gm = "GodMode"
    elif mode_gamemode == 1:
        print("mode = Fragile (", mode_gamemode, ")") 
        lifes = 1
        fire_rate = 100
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
        fire_rate = 75
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
    s = f"{path}sounds/{gallery_sounds[sound]}"
    playsound(s, block=False) 
    return

# Change le background en fonction du numéro de frame où nous sommes
def gif_power(frame=0):
    global current_background_image
    current_background = background_images[frame]
    canva.delete(current_background_image) #destruction de la frame précédente
    current_background_image =canva.create_image(512, 430, image=current_background) # recréation de l'image avec la nouvelle "current_background"
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
canva = tk.Canvas(main,height=1024, width=860)
canva.pack(anchor=tk.CENTER, expand=False)

# On charge les images dans le programme 
mob_image = PhotoImage(file=mob_img_path)
player_image = PhotoImage(file=player_img_path)
player_hit_image = PhotoImage(file=player_hit_img_path)
player_shoot = PhotoImage(file=player_shoot_img_path)
missile_image = PhotoImage(file=missile_img_path)
explosion_image = PhotoImage(file=explosion_img_path)
bullet_mob_image = PhotoImage(file=bullet_mob_img_path)
background_image = PhotoImage(file=background_img_path)
fumees_image = PhotoImage(file=fumees_img_path)
wave_image = PhotoImage(file=wave_img_path)
brandon_image = PhotoImage(file=brandon_img_path)

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
current_background_image = canva.create_image(512, 430, image=background_images[0])
canva.tag_lower(current_background_image)

# Ici on créé "en dur" les mobs
# Leur seul argument est leur position horizontale initiale, déterminé ici par 
for i in range(8):
    mob = Mobs(i*80)
    Liste_mobs.append(mob) # Ajout des mobs dans une liste pour pouvoir les parcourirs

# Le joueur reçoit aussi un nombre de vies, déterminées par le mode de jeu
player = Player(460, lifes)

# Création des barres d'informations
title_bar = tk.Label(main, width=860, font=('Arial', 20, 'bold'), text=f"WOKE INVADERS: {gm}", fg= "white", bg="black")
status_bar = tk.Label(main, width=860, font=('Arial', 15, 'bold'), text="", fg= "white", bg="black")

# Placement des barres en haut et en bas de la fenêtre de jeu
status_bar.place(relx=0.5, rely=1, anchor='s')
title_bar.place(relx=0.5, rely=0, anchor='n')

# bind nous permet de récupérer les touches qu'enclenchent le joueur, qui sont traitées par la fonction keypress
main.bind("<Key>", keypress)

# Initialisation de la fonction ticking, qui gère le temps du jeu et les évenements qui s'y passe
ticking(0)

# Mainloop d'affichage tkinter
main.mainloop()
