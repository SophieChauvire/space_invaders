# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 09:21:09 2021

@author: taz
"""

from tkinter import Tk, Label, Entry, Button, Canvas
from tkinter import Message, PhotoImage
import math,random

fenetre_jeu = Tk() #on crée la fenêtre
fenetre_jeu.title('Space Invaders')
largeur = 800
Canevas = Canvas(fenetre_jeu, width = 800, height = 800, bg='black')
#création du Canevas : zone graphique
affichage_score = Label(fenetre_jeu, text = "Score : ", fg = "black")
affichage_score.pack() 


#création du vaisseau spatial à partir d'une image
#vaisseauim = PhotoImage(file= 'vaisseau.gif')
#Canevas.focus_set()

#Canevas.bind('<Key>',vaisseau_sp.dep_clavier)
    

class vaisseau:
    def __init__(self,largeur_v,hauteur_v,posi_vx,posi_vy,vies):
        self.largeur_v = largeur_v
        self.hauteur_v = hauteur_v
        self.VX = posi_vx
        self.VY = posi_vy
        self.vies = vies
        self.vaiss = Canevas.create_rectangle(posi_vx - 10, posi_vy -10, posi_vx +10, posi_vy +10,width=30,outline="white",fill="white")
        #initialisation d'un élement vaisseau
        
        
    def tirer_vaisseau(self): #fonction qui permet au vaisseau de tirer à partir de la fonction qui crée  le tir
        tir_v = tir(self.VX ,self.VY) #on crée un tir à partir de la classe tir
        tir_v.tir_du_vaisseau()
        
    def dep_clavier(event): #méthode déplacement de la classe vaisseau
        global VX,VY
        touche = event.keysym
        print(touche)
        if touche == "Right":
            VX = VX +15
        if touche == "left":
            VY = VY-15
        if touche == "space":
            tir.tir_du_vaisseau()
            
        Canevas.coords(vaisseau,VX-10,VY-10,VX+10,VY+10)   
    
    def destruction_vaisseau(self):
        Canevas.delete(self.vaiss)
        

class tir: 
    def __init__(self,VX,VY):
        self.VX=VX
        self.VY=VY
        self.image_tir = Canevas.create_rectangle(VX,VY,VX+3,VY+25,fill='blue')

    def destruction(self):
        Canevas.delete(self.canvas)
    
    def tir_du_vaisseau(self):
        self.VY = VY-2
        Canevas.coords(self.canvas,VX,VY,VX+3,VY+20)
        if VY > -30:
            for alien in liste_aliens:
                if self.condition_collision(alien):
                    self.collision(alien)
            fenetre_jeu.after(10,self.tir_du_vaisseau)
        else:
            self.destruction()
    
    def tir_d_alien(self):
        self.y=self.y+2
        Canevas.coords(self.canvas,self.x,self.y,self.x+2,self.y+20)
        if self.y < 630:
            detruit_par_tir = False
            for tir_de_terrien in liste_des_tirs_terrien:
                if self.condition_collision_tir(tir_de_terrien):
                    self.collision_tir(tir_de_terrien)
                    detruit_par_tir =True
            if not(detruit_par_tir):
                if self.condition_collision(vaisseau_spatial):
                    self.collision(vaisseau_spatial)
                else:
                    fenetre_jeu.after(10,self.tir_alien)
        else:
            self.destruction()


class alien:
    def __init__(self,x,y,taille,direction): #ajouter param vitesse
        self.x = x
        self.y = y
        self.taille = taille
        self.direction = direction
        #self.vitesse = vitesse
        
    def element_alien(self,x,y,taille): #fonction qui permet de mettre en place un alien/le créer sur le jeu
         self.alien_graph = Canevas.create_oval(x-taille,y-taille,x+taille,y+taille,width=1,outline="red",fill="red")
    
    def deplacement_alien(self):
        global x,y,taille,direction #ajouter un param vitesse
        if self.direction == "droite":
            x = x+2
        else:
            x = x-2
        self.alien_graph.coords(x-taille,y-taille,x+taille,y+taille,width=1,outline="red",fille="red")
            
        
        
            
        
        
            

        
        
liste_des_tirs_terrien = []
liste_aliens = []
vaisseau_spatial = vaisseau(200,250,500,750,4)
Canevas.focus_set()
Canevas.bind("<Key>",vaisseau_spatial.dep_clavier)
Canevas.pack()   
alien1 = alien(100,500,10,"droite")  
alien1.element_alien(100,500,10)
alien1.deplacement_alien
fenetre_jeu.mainloop()
tir1=tir(400,400)
tir1.tirer_vaisseau()