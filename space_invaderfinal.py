# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 18:48:15 2021

@author: taz
"""

from tkinter import Tk, Label, Entry, Button, Canvas, Message, PhotoImage
import math,random

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
                alien.direction = (alien.direction == -1) - (alien.direction == 1) # Pas utilisé dans bataillon mais fait par rigueur
            self.direction = (self.direction == -1) - (self.direction == 1)
        self.canvas.after(self.frequence,self.movements)
    
    def nouveau_tir(self):
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
        self.timer_tir = 1000
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
            self.tir = False

    def deplacement_vaisseau(self):  # Déplacement du sprite
        if self.jeu.game_over:
            return
        if (self.canvas.coords(self.sprite)[0] <= 4 and self.direction==-1) or (self.canvas.coords(self.sprite)[0] >= 550 and self.direction==1) :
            self.direction=0 # On fait attention à ne pas dépasser les bordures
        else:
            self.canvas.move(self.sprite, self.direction*5,0)
            self.canvas.after(16,self.deplacement_vaisseau)
        
        if self.tir == True and self.timer_tir >= 25 and not(self.jeu.transition):
            self.jeu.current_tirs.append(tir(self.canvas, self.jeu, self.canvas.coords(self.sprite)[0], self.canvas.coords(self.sprite)[1], -1))
            self.timer_tir = 0 # Remise à zéro du timer après un tir du vaisseau
        
    def nouveau_tir(self, event):
        if self.jeu.game_over:
            return
        if self.timer_tir >= 25:   # On ne peut pas tirer si le timer n'est pas terminé
            self.tir = True
    
    def no_tir(self):   # Incrémentation du timer entre deux tirs
        if self.jeu.game_over:
            return
        self.timer_tir += 1

        self.canvas.after(16, self.no_tir) # à modifier si on veut changer la fréquence des tirs

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
        
