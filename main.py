'''
A faire:
-Supprimer du tableau les missiles partis pour l'espace mémoire
- Gerer les collisions des tirs et des planetes
- Rajouter des bonus
- Rajouter le carburant
- Gerer les touches pour les deux joueurs
'''




#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *
import random as rd
import math as m
import time as t


##Dimensions de la fenetre
TailleXFenetre = 1350
TailleYFenetre = 700

#Initialisation de la bibliothèque Pygame
pygame.init()

fenetre = pygame.display.set_mode((TailleXFenetre, TailleYFenetre))

class Couleur:
    '''Classe qui définit une couleur selon le taux de rouge vert et bleu'''
    def __init__(self,r,g,b):
        self.r = r
        self.b = b
        self.g = g



class Vecteur :
    '''Classe Vecteur, qui contient un vecteur sous la forme (x,y), fonctions
- Norme : Renvoie la norme du vecteur '''
    def __init__(self,X,Y):
        self.x = X
        self.y = Y

    def norme(self):
        return m.sqrt(pow(self.x,2)+pow(self.y,2))

    def somme(U,V):
        return(Vecteur(U.x+V.x,U.y+V.y))

    def multiplie(U,mu):
        return(Vecteur(mu*U.x,mu*U.y))

    def scalaire(U,V):
        return(U.x*V.x+U.y*V.y)



class Vaisseau:
    '''Classe Vaisseau, qui contient les méthodes et informations des vaisseaux'''
    def __init__(self):

        self.position = Vecteur(rd.randint(0,TailleXFenetre),rd.randint(0,TailleYFenetre))
        self.vitesse = Vecteur(50,-50)
        self.acceleration = Vecteur(0,0)
        self.image =  pygame.image.load("vaisseau.png").convert_alpha()


        ##Vecteur unitaire perpendiculaire à utheta
        self.ur = Vecteur(0,0)

        ##Vecteur unitaire colinèaire a la vitesse
        self.utheta = Vecteur(0,0)

        self.carburant = 1000



    def bouger(self):
        '''Calcul de la nouvelle vitesse au prochain pas de temps, et nouvelle position'''

        #m*a = G*m*M/r^2*ur
        sommeForces = Vecteur(0,0)
        G = 6.67e-11

        ##On calcule la résultante des forces suivant les axes x et y
        
        for i in range(nbPlanetes):
            ##Vecteur unitaire pointant de V vers P
            V = Vecteur(planetes[i].x-self.position.x,planetes[i].y-self.position.y)
            Vunit = Vecteur.multiplie(V,1/(V.norme()))
            
            sommeForces.x += G*planetes[i].masse/pow(V.norme()*100*1000,2)*Vunit.x
            sommeForces.y += G*planetes[i].masse/pow(V.norme()*100*1000,2)*Vunit.y

        ##O obtient l'accélération
        self.acceleration.x = sommeForces.x
        self.acceleration.y = sommeForces.y
        
        #on intègre l'accélération
        self.vitesse.x+=self.acceleration.x*pasDeTemps
        self.vitesse.y+=self.acceleration.y*pasDeTemps

        ##Calcul du vecteur unitaire utheta dans la direction de la vitesse, et ur normal a utheta
        self.utheta = Vecteur.multiplie(self.vitesse,1/self.vitesse.norme())
        self.ur = Vecteur(-self.utheta.y,self.utheta.x)

        
        #On integre la vitesse
        self.position.x += self.vitesse.x*pasDeTemps
        self.position.y += self.vitesse.y*pasDeTemps

        ##Gestion du carburant
        self.carburant -= pasDeTemps



        
        ##Vérification des délimitations
        self.verifierPositions()

    def verifierPositions(self):
        '''Si il sort de la fenetre on le fait ressortir de l'autre côté'''

        ##En haut
        if self.position.x <= 0:
            self.position.x = TailleXFenetre

        ##En bas
        elif self.position.x >= TailleXFenetre:
            self.position.x = 0

        ##A droite
        elif self.position.y <= 0:
            self.position.y = TailleYFenetre

        ##A gauche
        elif self.position.y >= TailleYFenetre:
            self.position.y = 0


        
class planete:
    '''Classe planète qui contient toutes les informations liées aux planetes'''
    
    def generepositionplanete():
        '''Place les planetes aléatoirement initialement'''
        ##Pas trop près du bord
        L = [rd.randint(100,TailleXFenetre-100), rd.randint (100,TailleYFenetre-100)]
        return(L)

    def genererayonplanet():
        '''Genere un rayon aléatoire'''
        R = rd.randint(20,40)
        m = 4/3 * 3.14 * ((R * 100) ** 3) * 6.8 ** 18
        
        #calcul de la masse de la planète pour un rayon de l'ordre de 10^2
        return([R,m])

    

    def __init__(self):
        
        L = planete.generepositionplanete()
        M = planete.genererayonplanet()
        self.x = L[0]
        self.y = L[1]
        self.rayon = M[0]
        self.masse = M[1]

        ##Couleur de la planète
        self.couleur = Couleur(rd.randint(0,255),rd.randint(0,255),rd.randint(0,255))






class Missile:

    
    def __init__(self,P,V,idV):

        self.Position = P
        self.Vitesse = V
        
        self.Acceleration = Vecteur(0,0)
        
        ##Mort ou vivant
        self.etat = 1

        ##Id du vaisseau qui a tiré le missile
        self.idVaisseau = idV
        

    def bouger(self):

        ##On considere que les missiles ont un mouvement rectiligne uniforme


        self.Position.x += self.Vitesse.x*pasDeTemps
        self.Position.y += self.Vitesse.y*pasDeTemps
        self.verifierPositions()
    
    def verifierPositions(self):
        '''Si il sort de la fenetre on le fait ressortir de l'autre côté'''

        ##En haut
        if self.Position.x <= 0:
            etat = 0

        ##En bas
        elif self.Position.x >= TailleXFenetre:
            etat = 0

        ##A droite
        elif self.Position.y <= 0:
            etat = 0

        ##A gauche
        elif self.Position.y >= TailleYFenetre:
            etat = 0

            


        

##CONSTANTES


#Variable qui continue la boucle si = 1, stoppe si = 0
continuer = 1


T = t.time()

##Pas d'intégration et vitesse de la boucle
pasDeTemps = 20e-3

nbPlanetes = 4
nbVaisseaux = 2

##Liste des différents objets
planetes = []
vaisseaux = []
missiles  = []

##Création des planètes et des vaisseaux
for i in range(nbPlanetes):
    planetes.append(planete())
for i in range(nbVaisseaux):
    vaisseaux.append(Vaisseau())



##Police
font = pygame.font.Font(None, 15)

##Répétition des touches
pygame.key.set_repeat(200, 30)



#Création de la fenêtre


##Gestion du fond
fond = pygame.image.load("fond.jpg").convert()
##On l'agrandit
fond = pygame.transform.scale(fond,(TailleXFenetre,TailleYFenetre))




#Boucle infinie
while continuer:
    
    if (t.time()-T>=pasDeTemps):
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                print("lol")
                continuer = 0

            ##Appui d'une touche
            if event.type == KEYDOWN:

                ##On augmente les vitesses, dans les directions de ur ou utheta
                if event.key == K_RIGHT:
                    vaisseaux[0].vitesse = Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].ur,10))
                if event.key == K_LEFT:
                    vaisseaux[0].vitesse = Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].ur,-10))
                if event.key == K_DOWN:
                    vaisseaux[0].vitesse= Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].utheta,-10))
                if event.key == K_UP:
                    vaisseaux[0].vitesse = Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].utheta,10))

                    
                if event.key == K_SPACE:
                    ##On ajoute un missile à la liste, avec une vitesse initiale dans la direction de utheta et de norme 500
                    missiles.append(Missile(Vecteur(vaisseaux[0].position.x,vaisseaux[0].position.y),Vecteur(vaisseaux[0].utheta.x*500,vaisseaux[0].utheta.y*500),0))

        
        

        
        ##Affichage du fond
        fenetre.blit(fond, (0,0))
        

        ##Planetes
        ##Dessin des planètes (cercles)
        for i in range(nbPlanetes):
            cercle = pygame.draw.circle(fenetre,(planetes[i].couleur.r,planetes[i].couleur.g,planetes[i].couleur.b),(planetes[i].x,planetes[i].y),planetes[i].rayon)


        ##Vaisseaux

        ##Dessin et mouvement des vaisseaux
        for i in range(nbVaisseaux):
            vaisseaux[i].bouger()
            fenetre.blit( vaisseaux[i].image,( vaisseaux[i].position.x,vaisseaux[i].position.y))

            
            
            ##Dessin des vitesses des vaisseaux et des vecteur utheta et ur
            Vligne = pygame.draw.line(fenetre, (255,255,255), (vaisseaux[i].position.x,vaisseaux[i].position.y), (vaisseaux[i].position.x+vaisseaux[i].vitesse.x,vaisseaux[i].position.y+vaisseaux[i].vitesse.y))
            Vligne = pygame.draw.line(fenetre, (255,0,0), (vaisseaux[i].position.x,vaisseaux[i].position.y), (vaisseaux[i].position.x+vaisseaux[i].utheta.x*20,vaisseaux[i].position.y+vaisseaux[i].utheta.y*20))
            Vligne = pygame.draw.line(fenetre, (0,255,0), (vaisseaux[i].position.x,vaisseaux[i].position.y), (vaisseaux[i].position.x+vaisseaux[i].ur.x*20,vaisseaux[i].position.y+vaisseaux[i].ur.y*20))

         ##Dessin et gestion des Munitions
        for j in range(0,len(missiles)):
            if missiles[j].etat == 1:
                missiles[j].bouger()
                circle = pygame.draw.circle(fenetre,(255,0,0),(int(missiles[j].Position.x),int(missiles[j].Position.y)),10)       


        ##Affichage de texte
        text = font.render("V = ("+str(vaisseaux[0].vitesse.x)+" , "+str(vaisseaux[0].vitesse.y)+")", 1, (255, 255, 255))
        fenetre.blit(text, (20,20))

        text = font.render("P = ("+str(vaisseaux[0].position.x)+" , "+str(vaisseaux[0].position.y)+")", 1, (255, 255, 255))
        fenetre.blit(text, (20,40))

        text = font.render("Carburant: "+str(vaisseaux[0].carburant), 1, (255, 255, 255))
        fenetre.blit(text, (20,60))

        #text = font.render("Munitions: "+str(vaisseaux[0].munitions), 1, (255, 255, 255))
        #fenetre.blit(text, (20,80))
        
        pygame.display.flip()
        T = t.time()

    
pygame.quit()
