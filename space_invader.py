from tkinter import Tk, Label, Entry, Button, Canvas
from tkinter import Message
from fonctions_space_invaders import *
import space_invaders_fonctions as sif



fenetre_jeu = Tk() #on crée la fenêtre
fenetre_jeu.title('Space Invaders')
Canevas = Canvas(fenetre_jeu, width = 800, height = 800, bg='black')
#création du Canevas : zone graphique
affichage_score = Label(fenetre_jeu, text = "Score : ", fg = "black")
affichage_score.pack() 


bouton_debut = Button(Canevas, text = "Démarrer la partie", fg = 'red') #on rajoutera la commande du bouton ensuite 
bouton_debut.pack(side = "left",padx=300,pady=300)
bouton_quitter = Button(Canevas,text = "Quitter le jeu",fg = 'red', command = fenetre_jeu.destroy)
bouton_quitter.pack(side = "left", padx=100, pady=100)
#reprendre la mise en forme / disposition

#création vaisseau
#dimensions du vaisseau
largeur_v = 100
hauteur_v = 150

#position initiale du vaisseau
x = 500
y = 570

vaisseau = Canevas.create_rectangle(x-10,y-10,x+10,y+10,width=30,outline="white",fill="white")
Canevas.focus_set()
Canevas.bind("<Key>", dep_clavier)
Canevas.pack(padx = 3, pady=3)

alien = Canevas.create_rectangle( sif.X0 , sif.Y0 , sif.X1 , sif.Y1 , fil = 'purple')

sif.deplacement_alien()

fenetre_jeu.mainloop()

fenetre_jeu.mainloop()