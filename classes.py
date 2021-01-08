# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 09:21:09 2021

@author: taz
"""
from space_invader import *

class vaisseau:
    def _init_(self,largeur_v,hauteur_v,pos_i_vx,pos_i_vy):
        self.largeur_v = largeur_v
        self.hauteur_v = hauteur_v
        self.VX = pos_i_vx
        self.VY = pos_i_vy
        #initialisation d'un élement vaisseau
        
    def dep_clavier(event): #méthode déplacement de la classe vaisseau
        global VX,VY
        touche = event.keysym
        print(touche)
        if touche == "Right":
            VX = VX +15
            if touche == "left":
                VY = VY-15
    
    #on re affiche le vaisseau Ã  sa nouvelle position
    Canevas.coords(vaisseau,VX-10,VY-10,VX+10,VY+10)