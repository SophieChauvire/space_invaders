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


    def dep_clavier(self,event): #méthode déplacement de la classe vaisseau
        if touche == "Right":
            posi_x = posi_x +15
        if touche == "left":
            VY = VY-15
        if touche == "space":
            tir.tir_du_vaisseau()


class vaisseau:
    def __init__(self, canvas, posi_x =275, posi_y=550): # On initie tous les attributs du vaisseau
        
        self.canvas = canvas
        self.image = PhotoImage(file='vaisseau.gif').subsample(10,10) #50px*50px
        self.sprite= canvas.create_image(posi_x,posi_y,image=self.image, anchor='nw')
        self.direction = 0
        self.timer_shot = 1000
        self.tir = False
        


#classe dans laquelle on définit tirs vaisseau et aliens
class tir:
    def __init__(self, canvas, jeu, posi_x, posi_y, sens):
        self.image = [PhotoImage(file='laser.png')]
        self.canvas= canvas
        self.jeu = jeu
        self.sens = sens
        self.sprite = canvas.create_image(posi_x,posi_y+sens*25,image=self.image[(self.sens == -1)], anchor='nw')