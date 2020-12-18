#on va écrire la fonction qui va permettre le deplacement du vaisseau
#en appuyant sur les touches d/g du clavier

from tkinter import Tk, Label, Entry, Button, Canvas
from space_invader import*

def dep_clavier(event):
    global x,y
    touche = event.keysym
    print(touche)
    if touche == "Right" or touche == "right":
        x = x+15
    if touche == "left" or touche == "left":
        x = x-15
    
    #on re affiche le vaisseau à sa nouvelle position
    Canevas.coords(vaisseau,x-10,y-10,x+10,y+10)
    
    