import tkinter as tk
from tkinter import PhotoImage 
from tkinter import messagebox
import random

#Initialisations des variables:
#chemin du dossier en dur - Possibilité de le faire en automatique avec une fonction éventuellement (essayé avec pathlib et os.path, sans succès...)
path = "C:/Users/RDP_Access/Documents/SUPPORTS DE COURS/Découverte du code - Robotique Python/fsi-main/"

print(path)
global direction

direction = random.randint(-1, 1) # direction de départ (1, 0 ou -1)
while direction == 0:
    direction = random.randint(-1, 1) # On randomise la direction de départ, et on évite de la mettre à 0 sinon les mobs ne bougent pas !

difficulty = 25 # Cette variable change la vitesse de tire des ennemis (délai en ms) -- Défaut = 25 --

# Ces listes nous permettent de pouvor parcourir nos objets instanciés dans des boucles for
Liste_mobs = []
Liste_bullets = []
Liste_player = []

# Chemin d'accès des images
mob_img_path = f"{path}mob.png"
player_img_path =f"{path}player.png"
bullet_img_path = f"{path}bullet.png"
background_img_path = f"{path}background.png"
bullet_mob_img_path = f"{path}bullet_mob.png"

#Les deux classes Mob et Player, il manque encore Bullet pour les balles, en gros on définit des objets "types", des sortes de modèles
class Mobs:
    def __init__(self, x_position): # La fonction __init_ est le constructeur, qui se déclenche à chaque fois que la classe est instanciée
        self.x_position = x_position * 0.1
        self.y_position = 0.2
        self.sprite_mob = tk.Label(main, image=mob_image)
        self.sprite_mob.config(bg=main["bg"])
        self.sprite_mob.place(relx=self.x_position, rely=self.y_position, anchor='center')
    def destroy(self): # Cette fonction permettrait de détruire l'objet en cas de déclenchement de la fonction
        del self # A tester
    def hit(self):
        print("hit!")
        self.sprite_mob.place_forget()
        Liste_mobs.remove(self)
    def mob_move(self):
            global direction
            self.sprite_mob.place(relx=self.x_position, rely=self.y_position, anchor='center')
        
class Player:
    def __init__(self, position, life):
        self.position = position * 0.10
        self.life = life
        self.y_position = 0.9
        self.sprite_player = tk.Label(main, image=player_image)
        self.sprite_player.place(relx=self.position,rely=0.9, anchor='center') # Le joueur est placé une première fois avec les valeur par défaut
    def move_player(self):    # Ensuite, cette fonction est rappelée à chaque fois que le joueur touche ses touches, modifiant au passage sa position
        self.sprite_player.place(relx=self.position,rely=0.9, anchor='center')

# Les balles: 
# Les "modes" sont là pour savoir si la balle est émise par le joueur ou les mobs
# Selon l'un ou l'autre, elles vont dans un sens ou l'autre, et apparaissent à un endroit différent
class Bullets:
    def __init__(self, x_position, mode=1):
        if mode == 1: 
            self.sprite = tk.Label(main, image=bullet_image)
            self.y_position = 0.8
            self.x_position = x_position
        else:
            self.x_position = x_position
            self.y_position = 0.3
            self.sprite = tk.Label(main, image=bullet_mob_image) # Le sprite est différent aussi
        self.sprite.place(relx=self.x_position,rely=self.y_position, anchor='s')
        self.move_bullet(mode) 
# Chaque balle appèle la fonction move, qui appèle à son tour la fonction check_collision, et se renvoient ainsi la balle jusqu'à ce qu'elles touche un joueur ou un mob
    
    def move_bullet(self, mode):
        self.mode = mode
        if mode == 1:
            self.y_position -= 0.01
        elif mode == 0:
            self.y_position += 0.01
        self.sprite.place(relx=self.x_position,rely=self.y_position, anchor='s')
        self.check_collision(mode)
        return

    def check_collision(self, mode):
        for player in Liste_player: # L'utilisation de la liste, pour pouvoir utiliser player.position (si on met juste player.position sans la liste, il ne trouve pas la variable ?)
            if abs(self.y_position - player.y_position) < 0.05 and abs(self.x_position - player.position) < 0.05:
                print("ouch")
                player.life -=  1 #Le joueur perd une vie
                self.sprite.place_forget() # Permet de désafficher la balle
                Liste_bullets.remove(self) #On retire la balle de la liste des balles
                return # Si une collision a eu lieu, on arrête la fonction sans relancer la fonction de déplacement
                
        for mob in Liste_mobs:
            if abs(self.y_position - mob.y_position) < 0.05 and abs(self.x_position - mob.x_position) < 0.05:
                mob.hit() # Déclencher la fonction de destruction du mob touché
                self.sprite.place_forget() # Permet de désafficher la balle
                Liste_bullets.remove(self) #On retire la balle de la liste des balles
                return # Si une collision a eu lieu, on arrête la fonction sans relancer la fonction de déplacement
        
        if self.y_position >= 1 or self.y_position <= 0: #Si la balle sort de l'écran
            self.sprite.place_forget() # Permet de désafficher la balle
            Liste_bullets.remove(self) #On retire la balle de la liste des balles
            return
        main.after('20', lambda: self.move_bullet(mode))
         

# Là c'est un menu pause qui se  déclenche en appuyant sur la touche echap 
#ça ne met pas du tout en pause, mais faudrait changer beaucoup de choses
def pause_menu():
    print("Entered pause menu")
    pause = tk.Toplevel()
    pause.geometry("200x200+500+300")
    pause.title("PAUSE")
    pause.configure(background="white")
    restart = tk.Button(pause, text="Reprendre", command=pause.destroy) #Créatioin du boutton pour reprendre, qui, si cliqué, détruit le menu pause
    quit_button = tk.Button(pause,text="Quitter", command=main.quit) #Création du boutton pour quitter le jeu, qui si enclenché effectue la command "quit" qui ferme le programme, on pourrait mettre une infobulle de confirmation avant pour éviter le misclick
    restart.place(relx=0.33, rely=0.5, anchor='center')
    quit_button.place(relx=0.66, rely=0.5, anchor='center')
    pause.grab_set() #Grabset let en pause la fenetre principale et empeche les input d'arriver dans la fenetre principale
    pause.focus_set()


# Ici on détermine ce qu'on fait suivant les touches pressées
def keypress(event):
    if event.keysym == "d": #La touche "d" pour aller à droite
        player.position += 0.02
        player.move_player()
    if event.keysym == "q": #La touche "q" pour aller à gauche
        player.position -= 0.02
        player.move_player()
    if event.keysym == "Escape": #La touche échap pour mettre le menu pause
        pause_menu()
    if event.keysym == "space": # La touche échap pour créer une balle
        Liste_bullets.append(Bullets(player.position, 1))

# Gestion du temps, qui permet de checker les différentes fonctions toutes les x secondees en se rappelant elle même (ici 50ms)
def ticking(t):
    global difficulty
    move_mob()
    check_life_player()
    victory = check_no_mobs()
    if victory == 1:
        messagebox.showinfo("Félicitations", "Vous avez battu le fascisme")
        messagebox.showinfo("Félicitations", "Enfin")
        messagebox.showinfo("Félicitations", "Merci d'avoir joué à ce jeu pas ouf")
        main.quit()
    if t == difficulty: # Au bout d'un certain nombre de boucle, les ennemis tirent
        for mob in Liste_mobs:
            Liste_bullets.append(Bullets(mob.x_position, 0))
            t = 0 # Réinitialisation
    t += 1 # Incrémentation de t jusqu'à arriver à la valeur renseignée
    main.after('50', lambda: ticking(t))

# déplacement des mobs:
# Si la variable "direction" est de 1, les mobs vont vers la droite (mob.position + 1)
# Sinon il vont à gauche (mob.position - 1)
def move_mob():
    global direction
    for mob in Liste_mobs:
        mob.x_position = mob.x_position + (direction * 0.01) 
        mob.mob_move()
        if mob.x_position >= 1: # Si il touche le bord droit, on définit la direction vers la gauche
            direction = -1
        if mob.x_position <= 0: # Sinon on définit vers la droite
            direction = 1

#Cette fonction se déclenche à chaque tick, et vérifie si la vie du joueur est à 0
def check_life_player():
   if player.life == 0:
       messagebox.showerror("Gave Over", "Vous êtes mort")
       main.quit()

# Celle ci vérifie si il y a encore des mobs dans la liste, si il n'y en a plus, alors elle retourne 1, 
# Qui est ensuite utilisé dans la fonction ticking pour afficher la victoire
def check_no_mobs():
    if len(Liste_mobs) == 0:
        return 1
        
# Création de la fenêtre principale
main = tk.Tk()
main.title("Space Invaders")
main.geometry("700x500+300+200")
main.configure(background="black")

# Chargement des images dans le programme
mob_image = PhotoImage(file=mob_img_path)
player_image = PhotoImage(file=player_img_path)
bullet_image = PhotoImage(file=bullet_img_path)
bullet_mob_image = PhotoImage(file=bullet_mob_img_path)
background_image = PhotoImage(file=background_img_path)

background= tk.Label(main, image=background_image)
background.pack()

# Création des objets grâce aux classes
mob1 = Mobs(1)
mob2 = Mobs(2)
mob3 = Mobs(3)
mob4 = Mobs(4)
mob5 = Mobs(5)
player = Player(5, 3)

# On met tout les mobs dans une liste pour pouvoir les parcourir par la suite dans des boucle for et vérifier si il y en a encore
Liste_mobs.append(mob1)
Liste_mobs.append(mob2)
Liste_mobs.append(mob3)
Liste_mobs.append(mob4)
Liste_mobs.append(mob5)
Liste_player.append(player)

# ça c'est l'outil pour déclencher des évenement:
# Quand une touche est pressée:
main.bind("<Key>", keypress)

# Le temps qui passe, permet de lancer la fonction qui va tourner en boucle toutes les secondes 
# Pour updater les positions (voir la fonction ticking)
ticking(0)
# La loop principale de la fenêtre
main.mainloop()