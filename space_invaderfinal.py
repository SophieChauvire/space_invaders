# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 18:48:15 2021

@author: Tasnîm Dekkiche
"""

from tkinter import Tk, Label, Entry, Button, Canvas, Message, PhotoImage, Frame, StringVar
import math,random as rd

class alien:
    def __init__(self, jeu, canvas, posi_x=6, posi_y=1,sens = 1,vitesse = 2,nombre = 16, niv = 2):
        self.jeu = jeu
        self.canvas = canvas
        self.posi_x = posi_x
        self.niv = niv
        self.set_image = [PhotoImage(file='alien_niv1.png'), PhotoImage(file='alien_niv2.png')] #50px*50px
        #self.y_pos= y_pos # Pourrait être utile. Position dans la grille de la horde
        self.sprite= canvas.create_image(50*posi_x,50*posi_y+50,image=self.set_image[niv-1], anchor='nw')
        self.sens = sens
        self.image=self.set_image[niv-1]
        self.vitesse = vitesse
        self.nombre = nombre
        self.score = 50*niv**2
        self.pv = niv
        #if self.pv == 3:
         #   self.pv = 1


class Bataillon:
    """Classe du bataillon , le bataillon constituant un groupe d'ennemis
    """
    def __init__(self,canvas, jeu, length, height, speed = 0.5, cadence_tir = 5000,frequence = 20, direction = 1):
        self.canvas = canvas
        self.jeu = jeu
        self.length = length
        self.height = height
        self.speed = speed
        self.cadence_tir = cadence_tir
        self.frequence = frequence
        self.direction = direction
        self.liste_alien = []
        
        for i in range(length):
            for j in range(height-1):
                self.liste_alien.append(alien(canvas, jeu, self, i+(12-length)//2, j, self.direction, self.speed, self.frequence, 2))
            self.liste_alien.append(alien(canvas, jeu, self, i+(12-length)//2, height-1, self.direction, self.speed, self.frequence, 1))
    def deplacement_bataillon(self):
        """
        commande le déplacement du bataillon
        """
        if self.jeu.game_over or self.jeu.transition:
            return
        deplacement=True
        for alien in self.liste_alien:
            if self.canvas.coords(alien.sprite)[0] + self.direction*self.speed < 0 or self.canvas.coords(alien.sprite)[0] + self.direction*self.speed + 50 > 600:
                deplacement = False
        if deplacement:
            for alien in self.liste_alien:
                self.canvas.move(alien.sprite, self.direction*self.speed, 0)
        else:
            for alien in self.liste_alien:
                if self.canvas.coords(alien.sprite)[1] + 50 + 25 > 490:
                    self.jeu.game_over = True
            if self.jeu.game_over:
                self.canvas.after(16, self.jeu.end_jeu)
                return

            for alien in self.liste_alien:
                self.canvas.move(alien.sprite, 0, 25)
                alien.direction = (alien.direction == -1) - (alien.direction == 1)
            self.direction = (self.direction == -1) - (self.direction == 1)
        self.canvas.after(self.frequence,self.movements)
    
    def nouveau_tir(self):
        """
        on détermine quand un alien va tirer
        """
        if self.jeu.game_over or self.jeu.transition:
            return
        for alien in self.liste_alien:
            tir_cadence_tir = rd.randint(0,self.cadence_tir)
            if tir_cadence_tir <= 1:
                self.jeu.current_tirs.append(tir(self.canvas, self.jeu, self.canvas.coords(alien.sprite)[0], self.canvas.coords(alien.sprite)[1], 1))
        self.canvas.after(16, self.nouveau_tir)



class vaisseau:
    def __init__(self, canvas, posi_x =275, posi_y=550): # On initie tous les attributs du vaisseau
        
        self.canvas = canvas
        self.image = PhotoImage(file='vaisseau.gif').subsample(10,10) #50px*50px
        self.sprite= canvas.create_image(posi_x,posi_y,image=self.image, anchor='nw')
        self.direction = 0
        self.timer_shot = 1000
        self.tir = False
        
    def move_left(self, event):
        if self.jeu.game_over:
            return
        self.direction=-1

    def move_right(self, event):
        if self.jeu.game_over:
            return
        self.direction=1

    def stop_move(self, event):
        if self.jeu.game_over:
            return
        if (event.keysym == "Left" and self.direction == -1) or (event.keysym == "Right" and self.direction == 1):
            self.direction = 0
        if (event.keysym == "space" and self.tir == 1):
            self.shot = False

    def deplacement_vaisseau(self):  # Déplacement du sprite
        if self.jeu.game_over:
            return
        if (self.canvas.coords(self.sprite)[0] <= 4 and self.direction==-1) or (self.canvas.coords(self.sprite)[0] >= 550 and self.direction==1) :
            self.direction=0 # On fait attention à ne pas dépasser les bordures
        else:
            self.canvas.move(self.sprite, self.direction*5,0)
            self.canvas.after(16,self.deplacement_vaisseau)
        
        if self.tir == True and self.timer_shot >= 25 and not(self.jeu.transition):
            self.jeu.current_shots.append(tir(self.canvas, self.jeu, self.canvas.coords(self.sprite)[0], self.canvas.coords(self.sprite)[1], -1))
            self.timer_shot = 0 # Remise à zéro du timer après un tir du vaisseau
        
    def new_shot(self, event):
        if self.jeu.game_over:
            return
        if self.timer_shot >= 25:   # On ne peut pas tirer si le timer n'est pas terminé
            self.shot = True
    
    def no_shot(self):   # Incrémentation du timer entre deux tirs
        if self.jeu.game_over:
            return
        self.timer_shot += 1

        self.canvas.after(16, self.no_shot) # à modifier si on veut changer la fréquence des tirs

#classe dans laquelle on définit tirs vaisseau et aliens
class tir:
    def __init__(self, canvas, jeu, posi_x, posi_y, sens):
        self.image = [PhotoImage(file='laser.png')]
        self.canvas= canvas
        self.jeu = jeu
        self.sens = sens
        self.sprite = canvas.create_image(posi_x,posi_y+sens*25,image=self.image[(self.sens == -1)], anchor='nw')
        
        

class ilots:
    def __init(self,canvas,jeu,posi_x,posi_y):
        self.image = PhotoImage(file='block.png').subsample(25,25)
        self.canvas = canvas
        self.jeu = jeu
        self.sprite = self.canvas.create_image(posi_x,posi_x,image=self.image, anchor='nw')


class Menu:
    """
    Classe qui crée un objet qui a comme attributs tous les éléments du menu.
    """
    def __init__(self):        
        self.background = PhotoImage(file = 'menu.png')
        self.bouton_jouer = Button( text = 'Démarrer le jeu',height = 4, width = 20,activebackground='#ECECEC',background='#FFFFFF')
        self.bouton_quitter = Button( text = 'Quitter',height = 2, width = 10,activebackground='#ECECEC',background='#FFFFFF')
        


class jeu:
    """
    Classe de la fenêtre de jeu
    """
    def __init__(self, window, length, height, speed = 1,cadence_tir = 4000):

        self.window = window # Fenetre est une fenêtre Tk()
        self.window.title('Space Invaders')
        self.window.geometry("600x600")
        self.window.resizable(width=False, height=False)

        self.canvas = Canvas(self.window, bg = 'black', bd= 0, highlightthickness=0, height = 600, width = 600)

        self.vaisseau_spatial = vaisseau(self.canvas, self)

        self.length = length
        self.height = height
        self.speed = speed
        self.cadence_tir = cadence_tir  

        self.niveau = 1
        self.niveau_SV = StringVar()
        self.niveau_SV.set(str(self.niveau))

        self.bataillon = Bataillon(self.canvas, self, self.length, self.height, self.speed,self.cadence_tir)
        self.ilots = ilots(self.canvas,self)
        self.game_over = False
        self.current_tirs = []

        self.menu = Menu()        

        self.transition = False

        self.score = 0
        self.highscore_SV = StringVar()   # On utilise une stringvariable pour pouvoir changer sa valeur ensuite
        self.temp = open("highscore.txt", "rt")
        self.highscore = int(self.temp.readline())  # Entier qui stocke le highscore, pas le même type de variable que highscore_SV
        self.temp.close()        
        self.temp = open("highscore.txt", "rt")  # On ouvre deux fois le fichiers au lieu d'une car cela génère une erreur de faire les deux manipulations en une fois
        self.highscore_SV.set('HIGHSCORE : '+self.temp.readline())
        self.temp.close()
       
        

    def menu_launch(self): # Première méthode appelée quand le jeu est lancé
        self.canvas.pack(anchor='nw')
        self.background_display = self.canvas.create_image(300,300,image=self.menu.background)
        self.logo_display = self.canvas.create_image(300,133,image=self.menu.logo)
        self.play_button_display =self.canvas.create_window(300,350,window = self.menu.play_button)
        self.menu.play_button.config( command=self.start)
        self.exit_button_display = self.canvas.create_window(300,450,window = self.menu.exit_button)
        self.menu.exit_button.config( command=self.window.destroy)
        self.highscore_label = Label(self.canvas, textvariable=self.highscore_SV, fg='white', bg='black', font='Helvetica 16 bold')
        self.highscore_disp = self.canvas.create_window(490,15,window = self.highscore_label)
        self.canvas.after(16, self.highscore_display)
        self.sv = StringVar()
        self.sv.set('SCORE : '+str(self.score))
        self.score_label = Label(self.canvas, textvariable=self.sv, fg='white', bg='black', font='Helvetica 16 bold')
    
    def start(self): # Est appelée pour commencer à jouer, supprime les éléments du menu et lancer les methodes qui permettent le bon déroulement du jeu
        self.canvas.delete(self.bouton_jouer_display,self.bouton_quitter_display,self.background_display)
        self.canvas.pack(anchor='nw')
        
        self.score_display = self.canvas.create_window(90,15,window = self.score_label)
        
        self.canvas.after(16, self.bataillon.deplacement_bataillon)
        self.canvas.after(16, self.vaisseau_spatial.deplacement_vaisseau)
        self.canvas.after(16, self.tirs_management)
        self.canvas.after(16, self.score_management)
        self.canvas.after(16, self.bataillon.nouveau_tir)
        self.canvas.after(16, self.vaisseau_spatial.no_tir)
        self.window.bind('<Left>', self.vaisseau_spatial.move_left)
        self.window.bind('<left>', self.vaisseau_spatial.move_left)
        self.window.bind('<Right>', self.vaisseau_spatial.move_right)
        self.window.bind('<right>', self.vaisseau_spatial.move_right)
        self.window.bind('<KeyRelease>', self.vaisseau_spatial.stop_move)
        self.window.bind('<space>', self.vaisseau_spatial.nouveau_tir)
    
    def score_management(self): # Affichage du score pendant la partie
        self.canvas.delete(self.score_display)
        self.sv.set('SCORE : '+str(self.score))        
        self.score_display = self.canvas.create_window(90,15,window = self.score_label)
        self.canvas.after(16, self.score_management)
        
    def highscore_display(self): # Gère la modification en direct de la valeur du highscore après une partie
        self.canvas.delete(self.highscore_disp)
        self.temp = open("highscore.txt", "rt")
        self.highscore_SV.set('HIGHSCORE : '+self.temp.readline())
        self.temp.close()
        self.highscore_disp = self.canvas.create_window(490,15,window = self.highscore_label)

    def niveau_screen(self): # Ecran de transition entre deux manches
        self.niveau += 1
        self.niveau_SV.set('NIVEAU '+ str(self.niveau))
        self.niveau_label = Label(self.canvas, textvariable=self.niveau_SV, fg='#FFE213', bg='black', font='Helvetica 60 bold')
        self.niveau_display = self.canvas.create_window(300,250,window = self.niveau_label)
        self.canvas.after(1000,self.new_niveau)  #lancement de la prochaine manche

    def nouveau_niveau(self):
        self.canvas.delete(self.niveau_display)
        
        if self.speed < 3 :  # Augmentation de la vitesse jusqu'à un certain seuil
            self.speed += 0.5
        if self.cadence_tir > 2100 : # pareil pour la fréquence de tir
            self.cadence_tir -= 900
        if self.cadence_tir > 500 and self.cadence_tir < 2100:
            self.cadence_tir -= 300        
        self.bataillon = Bataillon(self.canvas, self, self.length, self.height, self.speed,self.cadence_tir)
        self.transition = False
        self.canvas.after(16, self.bataillon.deplacement_bataillon)
        self.canvas.after(16, self.bataillon.nouveau_tir)
        self.canvas.after(16, self.tirs_management)

    def end_jeu(self): # Ecran de jeu over
        self.canvas.delete('all')
        label = Label(self.canvas, text='jeu OVER', fg='white', bg='black')
        label.config(font=("Liberation", 30))
        self.canvas.create_window(300, 300, window=label)
        self.background_display = self.canvas.create_image(300,300,image=self.menu.background)
        
        if self.score > self.highscore: # Sauvegarde du meilleur score si on bat le record
            temp = open("highscore.txt", "wt")
            temp.write(str(self.score))
            temp.close()
        
        self.canvas.after(500, self.relaunch)
        
    def relaunch(self): # Réinitialisation du jeu pour ré-afficher le menu et relancer une partie.
        self.canvas.delete('all')
        self.speed = 1
        self.cadence_tir = 4000
        self.niveau = 1
        self.vaisseau_spatial = vaisseau(self.canvas, self)
        self.bataillon = Bataillon(self.canvas, self, self.length, self.height, self.speed)
        self.ILOTS = ilots(self.canvas,self)
        self.game_over = False
        self.current_tirs = []
        self.score = 0
        
        self.menu = Menu()
        self.bouton_jouer = Button(self.window, text = "Démarrer le jeu",height = 4, width = 20,command=self.start,activebackground='#ffbd33',background='#FFE213')
        self.bouton_quitter = Button(self.window, text = "Quitter",height = 2, width = 10,command=self.window.destroy,activebackground='#ffbd33',background='#FFE213')
        
        jeu.menu_launch()

    def tirs_management(self): # Gestion du mouvement des lasers et de la collision, ainsi que de l'augmentation de la variable score
        if self.game_over:
            return
        for tir in self.current_tirs:
            touch = False  # True si l'entité est touchée
            index_alien_to_delete = None
            index_block_to_delete = None
            index_alien_to_touch = None

            self.canvas.move(tir.sprite, 0,tir.direction*4)
            if abs(self.canvas.coords(tir.sprite)[0] - self.canvas.coords(self.vaisseau_spatial.sprite)[0]) < 20 and abs(self.canvas.coords(tir.sprite)[1] - self.canvas.coords(self.vaisseau_spatial.sprite)[1]) < 33 and tir.direction == 1:
                
                touch = True
                self.game_over = True
                
            for alien in self.bataillon.liste_alien:
                if abs(self.canvas.coords(tir.sprite)[0] - self.canvas.coords(alien.sprite)[0]) < 23 and abs(self.canvas.coords(tir.sprite)[1] - self.canvas.coords(alien.sprite)[1]) < 33 and tir.direction == -1:
                    
                    touch = True
                    if alien.pv == 1:
                        index_alien_to_delete = self.bataillon.liste_alien.index(alien)  # Suppression de l'ennemi mort
                        self.score += alien.score  # Augmentation du score quand on tue un ennemi
                    else:
                        alien.pv -= 1  # On baisse la vie de l'ennemi touché
                        index_alien_to_touch = self.bataillon.liste_alien.index(alien)
               

            for block in self.walls.blocks_list: # Gestion de la destruction des blocs
                if self.canvas.coords(block.sprite)[0] - self.canvas.coords(tir.sprite)[0] < 29 and self.canvas.coords(block.sprite)[0] - self.canvas.coords(tir.sprite)[0] > 0 and self.canvas.coords(tir.sprite)[1] - self.canvas.coords(block.sprite)[1] < 9 and self.canvas.coords(block.sprite)[1] - self.canvas.coords(tir.sprite)[1] < 29:
                    touch = True
                    index_block_to_delete = self.walls.blocks_list.index(block)
            
            if index_alien_to_touch != None:
                temp = self.bataillon.liste_alien[index_alien_to_touch]
                self.canvas.itemconfig(temp.sprite, image=temp.set_image[temp.kind-1+len(temp.set_image)//2]) # La liste est pensée telle que la 2e moitié puisse servir à representer la premiere moitié blessée
            if index_alien_to_delete != None:
                self.canvas.delete(self.bataillon.liste_alien[index_alien_to_delete].sprite)
                self.bataillon.liste_alien.remove(self.bataillon.liste_alien[index_alien_to_delete])
            if index_block_to_delete != None:
                self.canvas.delete(self.walls.blocks_list[index_block_to_delete].sprite)
                self.walls.blocks_list.remove(self.walls.blocks_list[index_block_to_delete])
            
            if self.canvas.coords(tir.sprite)[1] >= 560 or self.canvas.coords(tir.sprite)[1] < 0 or touch == True:
                self.canvas.delete(tir.sprite)
                self.current_tirs.remove(tir)
            
            if self.game_over == True:
                self.canvas.delete(self.vaisseau_spatial.sprite)
                self.canvas.after(1000, self.end_jeu)
                return

            if len(self.bataillon.liste_alien) == 0:
                self.transition = True
            if len(self.bataillon.liste_alien) == 0 and len(self.current_tirs) == 0:
                self.canvas.after(1000, self.niveau_screen) # on lance la prochaine manche
                return
                
        self.canvas.after(16, self.tirs_management)
        


if __name__ == '__main__':
    fenetre_jeu = Tk() # Initialisation de la variable qui gère la fenêtre de jeu
    Jeu = jeu(fenetre_jeu, 2, 2) # Nombre de lignes et de colonnes qui composent la horde d'ennemis.
    Jeu.menu_launch()
    Jeu.window.mainloop()
