from tkinter import Tk, Label, Entry, Button, Canvas
from tkinter import Message

fenetre_jeu = Tk() #on crée la fenêtre
fenetre_jeu.title('Space Invaders')
Canevas = Canvas(fenetre_jeu, width = 800, height = 800, bg='black')
#création du Canevas : zone graphique
affichage_score = Label(fenetre_jeu, text = "Score : ", fg = "black")
affichage_score.pack() 


#bouton_debut = Button(Canevas, text = "Démarrer la partie", fg = 'red') #on rajoutera la commande du bouton ensuite 
#bouton_debut.pack(side = "left",padx=300,pady=300)
bouton_quitter = Button(Canevas,text = "Quitter le jeu",fg = 'red', command = fenetre_jeu.destroy)
bouton_quitter.pack(side = "left", padx=100, pady=100)
#reprendre la mise en forme / disposition

largeur_v = 100
hauteur_v = 150
posi_vx = 500
posi_vy = 750


#création vaisseau spatial
vaisseau_spatial = Canevas.create_rectangle(posi_vx - 10, posi_vy -10, posi_vx +10, posi_vy +10,width=30,outline="white",fill="white")

class vaisseau:
    def _init_(self):
        self.largeur_v = largeur_v
        self.hauteur_v = hauteur_v
        self.VX = posi_vx
        self.VY = posi_vy
        #initialisation d'un élement vaisseau
        
    def dep_clavier(event): #méthode déplacement de la classe vaisseau
        global VX,VY
        touche = event.keysym
        if touche == "Right":
            VX = VX +15
            if touche == "left":
                VY = VY-15
#on re affiche le vaisseau Ã  sa nouvelle position
        Canevas.coords(vaisseau_spatial,VX-10,VY-10,VX+10,VY+10)



Canevas.focus_set()
Canevas.bind("Right", vaisseau.dep_clavier)
Canevas.bind("Left", vaisseau.dep_clavier)
Canevas.pack(padx = 5, pady=5)

fenetre_jeu.mainloop()