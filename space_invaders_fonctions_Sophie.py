#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 10:33:37 2020

@author: sophie
"""
from tkinter import Tk
import space_invaders as si

#position initiale de l'alien

X0 = 80
Y0 = 80
X1 = 160
Y1 = 160

vitesse = 5


def deplacement_alien():
    """ Deplacement de l'alien sur une ligne"""   
    global X0,Y0,X1,Y1,vitesse
    #rebond à droite
    if X1 > 800 :
        vitesse = -vitesse
    if X0 < 0 :
        vitesse = -vitesse
    X0 += vitesse
    X1 += vitesse
    si.Canevas.coords(si.alien , X0 , Y0 , X1 , Y1)
    si.fenetre_jeu.after(20,deplacement_alien)