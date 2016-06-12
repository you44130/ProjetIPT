'''
A faire:
-Supprimer du tableau les missiles partis pour l'espace mémoire

- Rajouter des bonus

'''




#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *
import random as rd
import math as m
import time as t
import copy

##Dimensions de la fenetre
TailleXFenetre = 1200
TailleYFenetre = 600

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
    def __init__(self,ID,Posinit,Vinit,C):

        self.position = Posinit
        self.vitesse = Vinit
        self.acceleration = Vecteur(0,0)
        
        self.image =  pygame.image.load("vaisseau.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(TailleXVaisseau,TailleYVaisseau))

        ##Vecteur unitaire perpendiculaire à utheta
        self.ur = Vecteur(0,0)

        ##Vecteur unitaire colinèaire a la vitesse
        self.utheta = Vecteur(0,0)

        self.carburant = 1000

        self.pv = PV

        self.id = ID

        self.munitions = NB_MUNITIONS_VAISSEAUX
        
        self.solide = pygame.Rect(self.position.x,self.position.y,TailleXVaisseau,TailleYVaisseau)

        self.couleur = C



    def bouger(self):
        '''Calcul de la nouvelle vitesse au prochain pas de temps, et nouvelle position'''
        if self.gererCollisions() ==1:

            #m*a = G*m*M/r^2*ur
            sommeForces = Vecteur(0,0)
            G = 6.67e-11

            ##On calcule la résultante des forces suivant les axes x et y
            
            for i in range(nbPlanetes):
                ##Vecteur unitaire pointant de V vers P
                V = Vecteur(planetes[i].x-self.position.x,planetes[i].y-self.position.y)
                
                if V.norme() !=0:
                    Vunit = Vecteur.multiplie(V,1/(V.norme()))
                
                    
                
                    sommeForces.x += G*planetes[i].masse/pow(V.norme()*100*1000,2)*Vunit.x
                    sommeForces.y += G*planetes[i].masse/pow(V.norme()*100*1000,2)*Vunit.y

            ##O obtient l'accélération
            self.acceleration.x = sommeForces.x
            self.acceleration.y = sommeForces.y
        else :
            self.acceleration.x = 0
            self.acceleration.y = 0
            self.vitesse.x = 0.1
            self.vitesse.y = 0.1
            self.pv -= 1
            ##print(self.pv)
            
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


        self.solide = pygame.Rect(self.position.x,self.position.y,TailleXVaisseau,TailleYVaisseau)

        
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


    def gererCollisions(self):

        carrevaisseau = [ vaisseaux[i].solide for i in range(nbVaisseaux)]
        carresolide = carrevaisseau + carreplanete
        
        carresolide.pop(self.id) ## on retire le vaisseau des objets bloqués


        ##print(self.solide.colliderect(Liste[0]))
        
        if self.solide.collidelist(carresolide) != -1:
            
            return(-1)
        else:
            return(1)



            
class Comete:
    '''Classe Vaisseau, qui contient les méthodes et
    informations des vaisseaux'''
    def __init__(self,ID):

        #self.position = Vecteur(rd.randint(0,TailleXFenetre),rd.randint(0,TailleYFenetre))
        self.position = Vecteur(0,rd.randint(0,TailleYFenetre))

        self.vitesse = Vecteur(200,rd.randint(-50,50))
        self.acceleration = Vecteur(0,0)
        
        self.image =  pygame.image.load("comet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))

        ##Vecteur unitaire perpendiculaire à utheta
        self.ur = Vecteur(0,0)

        ##Vecteur unitaire colinèaire a la vitesse
        self.utheta = Vecteur(0,0)

        self.carburant = 1000

        self.id = ID
        
        self.solide = pygame.Rect(self.position.x,self.position.y,TailleXVaisseau,TailleYVaisseau)



    def bouger(self):
        '''Calcul de la nouvelle vitesse au prochain pas de temps, et nouvelle position'''

        #m*a = G*m*M/r^2*ur
        sommeForces = Vecteur(0,0)
        G = 6.67e-11

        ##On calcule la résultante des forces suivant les axes x et y
        
        for i in range(nbPlanetes):
            ##Vecteur unitaire pointant de V vers P
            V = Vecteur(planetes[i].x-self.position.x,planetes[i].y-self.position.y)
            if V.norme() != 0:
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

        if self.vitesse.norme() != 0:
            self.utheta = Vecteur.multiplie(self.vitesse,1/self.vitesse.norme())
            self.ur = Vecteur(-self.utheta.y,self.utheta.x)

        
        #On integre la vitesse
        self.position.x += self.vitesse.x*pasDeTemps
        self.position.y += self.vitesse.y*pasDeTemps

        ##Gestion du carburant
        self.carburant -= pasDeTemps


        self.solide = pygame.Rect(self.position.x,self.position.y,TailleXVaisseau,TailleYVaisseau)

        
        ##Vérification des délimitations
        self.verifierPositions()

    def verifierPositions(self):
        '''Si il sort de la fenetre on le fait ressortir de l'autre côté'''

##        ##En haut
##        if self.position.x <= 0:
##            self.position.x = TailleXFenetre
##
##        ##En bas
##        elif self.position.x >= TailleXFenetre:
##            self.position.x = 0
##
##        ##A droite
##        elif self.position.y <= 0:
##            self.position.y = TailleYFenetre
##
##        ##A gauche
##        elif self.position.y >= TailleYFenetre:
##            self.position.y = 0
        ###controle vitesse :
        if (self.vitesse.x)>1000:
            self.vitesse.x=1000
        if (self.vitesse.y)>1000:
            self.vitesse.y=1000
    


    def gererCollisions(self):

        Liste = copy.deepcopy(carresolide)

        Liste.pop(self.id) ## on retire le vaisseau des objets bloqués
  
        ##print(self.solide.colliderect(Liste[0]))
        
        if self.solide.collidelist(Liste) != -1:
            continuer = 0
            


   

        

        
class planete:
    '''Classe planète qui contient toutes les informations liées aux planetes'''
    
    def generepositionplanete():
        '''Place les planetes aléatoirement initialement'''
        ##Pas trop près du bord
        L = [rd.randint(100,TailleXFenetre-100), rd.randint (100,TailleYFenetre-100)]
        return(L)

    def genererayonplanet():
        '''Genere un rayon aléatoire'''
        R = rd.randint(rayonMinPlanete,rayonMaxPlanete)
        m = 4/3 * 3.14 * ((R * 100) ** 3) * 6.8 ** 18
        #calcul de la masse de la planète pour un rayon de l'ordre de 10^2
        return([R,m])

    

    def __init__(self,ID):
        
        L = planete.generepositionplanete()
        M = planete.genererayonplanet()
        self.x = L[0]
        self.y = L[1]
        self.rayon = M[0]
        self.masse = M[1]
        self.id = ID

        ##Couleur de la planète
        self.couleur = Couleur(rd.randint(0,255),rd.randint(0,255),rd.randint(0,255))

        ##On place un carré inscrit dans chaque planète pour créer une zone solide, celui-ci étant repéré par son coin supérieur gauche
        self.solide = pygame.Rect( self.x - self.rayon * pow(1/2,1/2), self.y - self.rayon*pow(1/2, 0.5), 2*self.rayon* pow(0.5, 0.5) ,2*self.rayon*pow(0.5,0.5))

        self.solide2 = pygame.Rect( self.x - (self.rayon * 2) * pow(1/2,1/2), self.y - (self.rayon * 2)*pow(1/2, 0.5), 4*self.rayon* pow(0.5, 0.5) ,4*self.rayon*pow(0.5,0.5))


    def gererCollisions(self):
        Liste = copy.deepcopy(carreplanete2)

        Liste.pop(self.id) ## on retire le vaisseau des objets bloqués
        
        if self.solide.collidelist(Liste) != -1:
            print("c'est le bordel")
            





class Missile:

    
    def __init__(self,P,V,idV,ID):

        self.Position = P
        self.Vitesse = V
        
        self.Acceleration = Vecteur(0,0)
        
        ##Mort ou vivant
        self.etat = 1

        self.rayon = 5
        
        ##Id du vaisseau qui a tiré le missile
        self.idVaisseau = idV

        ##Id dans la liste
        self.id = ID

        self.solide = pygame.Rect( self.Position.x - self.rayon * pow(1/2,1/2), self.Position.y - self.rayon*pow(1/2, 0.5), 2*self.rayon* pow(0.5, 0.5) ,2*self.rayon*pow(0.5,0.5))

    def bouger(self):

        ##On considere que les missiles ont un mouvement rectiligne uniforme


        self.Position.x += self.Vitesse.x*pasDeTemps
        self.Position.y += self.Vitesse.y*pasDeTemps
        
        self.solide = pygame.Rect( self.Position.x - self.rayon * pow(1/2,1/2), self.Position.y - self.rayon*pow(1/2, 0.5), 2*self.rayon* pow(0.5, 0.5) ,2*self.rayon*pow(0.5,0.5))

        self.verifierPositions()
    
    def verifierPositions(self):
        '''Si il sort de la fenetre on le fait ressortir de l'autre côté'''

        ##En haut
        if self.Position.x <= 0:
            self.etat = 0

        ##En bas
        elif self.Position.x >= TailleXFenetre:
            self.etat = 0

        ##A droite
        elif self.Position.y <= 0:
            self.etat = 0

        ##A gauche
        elif self.Position.y >= TailleYFenetre:
            self.etat = 0

##        if self.etat == 0:
##            missiles.pop(self.id)
##            for i in range(self.id,len(missiles)):
##                missiles[i].id -= 1
##            print(len(missiles))
            

    def gererCollisions(self):

        carrevaisseau = [ vaisseaux[i].solide for i in range(nbVaisseaux)]
        carresolide = carrevaisseau + carreplanete
        
        carresolide.pop(self.idVaisseau) ## on retire le vaisseau des objets bloqués
        carrevaisseau.pop(self.idVaisseau)

        if self.solide.collidelist(carrevaisseau) != -1:
            vaisseaux[1-self.idVaisseau].pv -= 1

        
        if self.solide.collidelist(carresolide) != -1:
            
            self.etat = 0
        else:
            return(1)





##CONSTANTES


#Variable qui continue la boucle si = 1, stoppe si = 0
continuer = 1



T = t.time()

##Pas d'intégration et vitesse de la boucle
pasDeTemps = 20e-3
tpscometes=10
nbPlanetes = 1
nbVaisseaux = 2
PV = 10
nbCometes=4

##Planètes:
rayonMinPlanete = 20
rayonMaxPlanete = 50

##Taille de l'image vaisseau
TailleXVaisseau = 30
TailleYVaisseau = 30
#Augmentation de la vitesse a chaque poussée
poussee = 8

CARBURANT_PAR_POUSSEE = 2

NB_MUNITIONS_VAISSEAUX = 10

##Liste des différents objets
planetes = []
vaisseaux = []
missiles  = []
cometes = []

##Création des planètes et des vaisseaux
for i in range(nbPlanetes):
    planetes.append(planete(i))
for i in range(nbVaisseaux):
    vaisseaux.append(Vaisseau(i,Vecteur(rd.randint(0,TailleXFenetre),rd.randint(0,TailleYFenetre)),Vecteur(50,-50),Couleur(255,rd.randint(0,255),0)))
for i in range(nbCometes):
    cometes.append(Comete(i))
    

##TOUCHES
##Tableau selon les joueurs: Joueuri = [gauche,bas,droit,haut,tir]
# touches = [Joueur 1, Joueur 2]


touches = [['left','down','right','up','space'],['a','s','d','w','e']]



##Police
font = pygame.font.Font(None, 15)

##Répétition des touches
pygame.key.set_repeat(200, 50)



#Création de la fenêtre


##Gestion du fond
fond = pygame.image.load("fond.jpg").convert()
##On l'agrandit
fond = pygame.transform.scale(fond,(TailleXFenetre,TailleYFenetre))

## on liste tous les solides 
carreplanete = [planetes[i].solide for i in range(nbPlanetes)]
carrevaisseau = [ vaisseaux[i].solide for i in range(nbVaisseaux)]
#carrecomete = [cometes[i].solide for i in range(nbCometes)]
carreplanete2 = [planetes[i].solide2 for i in range(nbPlanetes)]
carresolide = carrevaisseau + carreplanete #+carrecomete
affichage=0

tpscomete=t.time()

#Boucle infinie
while continuer:


    
    
    if (t.time()-T>=pasDeTemps):
        
        


        
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                print("lol")
                continuer = 0

                        ##Appui d'une touche
##            if event.type == KEYDOWN:
##
##                ##On augmente les vitesses, dans les directions de ur ou utheta
##                if event.key == K_RIGHT:
##                    vaisseaux[0].vitesse = Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].ur,10))
##                if event.key == K_LEFT:
##                    vaisseaux[0].vitesse = Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].ur,-10))
##                if event.key == K_DOWN:
##                    vaisseaux[0].vitesse= Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].utheta,-15))
##                if event.key == K_UP:
##                    vaisseaux[0].vitesse = Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].utheta,10))
##
##                    
##                if event.key == K_SPACE:
##                    ##On ajoute un missile à la liste, avec une vitesse initiale dans la direction de utheta et de norme 500
##                    missiles.append(Missile(Vecteur(vaisseaux[0].position.x,vaisseaux[0].position.y),Vecteur(vaisseaux[0].utheta.x*500,vaisseaux[0].utheta.y*500),0))

            if event.type == KEYDOWN:
                touchesPressees = pygame.key.get_pressed()

                for i in range(0,len(touchesPressees)): 
                    if touchesPressees[i] == 1 :
                        nomTouche = pygame.key.name(i)
                        
                        if nomTouche == touches[0][2]:
                            vaisseaux[0].vitesse = Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].ur,poussee))
                            vaisseaux[0].carburant -= CARBURANT_PAR_POUSSEE
                        if nomTouche == touches[0][0]:
                            vaisseaux[0].vitesse = Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].ur,-poussee))
                            vaisseaux[0].carburant -= CARBURANT_PAR_POUSSEE
                        if nomTouche == touches[0][3]:
                            vaisseaux[0].vitesse = Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].utheta,poussee))
                            vaisseaux[0].carburant -= CARBURANT_PAR_POUSSEE
                        if nomTouche == touches[0][1]:
                            vaisseaux[0].vitesse= Vecteur.somme(vaisseaux[0].vitesse,Vecteur.multiplie(vaisseaux[0].utheta,-poussee))
                            vaisseaux[0].carburant -= CARBURANT_PAR_POUSSEE
                        if nomTouche == touches[0][4]:
                            missiles.append(Missile(Vecteur(vaisseaux[0].position.x,vaisseaux[0].position.y),Vecteur(vaisseaux[0].utheta.x*500,vaisseaux[0].utheta.y*500),0,len(missiles)))
                            vaisseaux[0].munitions -= 1
                            
                        if nbVaisseaux >= 2:
                            if nomTouche == touches[1][2]:
                                vaisseaux[1].vitesse = Vecteur.somme(vaisseaux[1].vitesse,Vecteur.multiplie(vaisseaux[1].ur,poussee))
                                vaisseaux[1].carburant -= CARBURANT_PAR_POUSSEE
                            if nomTouche == touches[1][0]:
                                vaisseaux[1].vitesse = Vecteur.somme(vaisseaux[1].vitesse,Vecteur.multiplie(vaisseaux[1].ur,-poussee))
                                vaisseaux[1].carburant -= CARBURANT_PAR_POUSSEE
                            if nomTouche == touches[1][3]:
                                vaisseaux[1].vitesse = Vecteur.somme(vaisseaux[1].vitesse,Vecteur.multiplie(vaisseaux[1].utheta,poussee))
                                vaisseaux[1].carburant -= CARBURANT_PAR_POUSSEE
                            if nomTouche == touches[1][1]:
                                vaisseaux[1].vitesse= Vecteur.somme(vaisseaux[1].vitesse,Vecteur.multiplie(vaisseaux[1].utheta,-poussee))
                                vaisseaux[1].carburant -= CARBURANT_PAR_POUSSEE
                            if nomTouche == touches[1][4]:
                                missiles.append(Missile(Vecteur(vaisseaux[1].position.x,vaisseaux[1].position.y),Vecteur(vaisseaux[1].utheta.x*500,vaisseaux[1].utheta.y*500),1,len(missiles)))        
                                vaisseaux[1].munitions -= 1
                
        
        ##Affichage du fond
        fenetre.blit(fond, (0,0))

        ##construction cometes:
                     ##Cometes :
        

        if t.time()-tpscomete>=10:
            if affichage==0:
                affichage=1
            else :
                for i in range(nbCometes):
                    cometes.append(Comete(i))
            tpscomete=t.time()
            

        if affichage==1:
            for i in range(nbCometes):
                
                cometes[i].bouger()
                fenetre.blit(cometes[i].image, (cometes[i].position.x,cometes[i].position.y))
               
        
                
        

        ##Planetes
        ##Dessin des planètes (cercles)
        for i in range(nbPlanetes):
            cercle = pygame.draw.circle(fenetre,(planetes[i].couleur.r,planetes[i].couleur.g,planetes[i].couleur.b),(planetes[i].x,planetes[i].y),planetes[i].rayon)
            #rectangle = pygame.draw.rect(fenetre,(255,0,255),planetes[i].solide)
       
                
            
        ##Vaisseaux

        ##Dessin et mouvement des vaisseaux
        for i in range(nbVaisseaux):
            vaisseaux[i].bouger()
            fenetre.blit( vaisseaux[i].image,( vaisseaux[i].position.x,vaisseaux[i].position.y))
            ##vaisseaux[i].gererCollisions()
            ##rectangle = pygame.draw.rect(fenetre,(255,0,0),vaisseaux[i].solide)            
            
            ##Dessin des vitesses des vaisseaux et des vecteur utheta et ur
            Vligne = pygame.draw.line(fenetre, (255,255,255), (vaisseaux[i].position.x,vaisseaux[i].position.y), (vaisseaux[i].position.x+vaisseaux[i].vitesse.x,vaisseaux[i].position.y+vaisseaux[i].vitesse.y))
            Vligne = pygame.draw.line(fenetre, (255,0,0), (vaisseaux[i].position.x,vaisseaux[i].position.y), (vaisseaux[i].position.x+vaisseaux[i].utheta.x*20,vaisseaux[i].position.y+vaisseaux[i].utheta.y*20))
            Vligne = pygame.draw.line(fenetre, (0,255,0), (vaisseaux[i].position.x,vaisseaux[i].position.y), (vaisseaux[i].position.x+vaisseaux[i].ur.x*20,vaisseaux[i].position.y+vaisseaux[i].ur.y*20))

         ##Dessin et gestion des Munitions
        for j in range(0,len(missiles)):
            if missiles[j].etat == 1:
                missiles[j].bouger()
                missiles[j].gererCollisions()
                
                COULEUR = vaisseaux[missiles[j].idVaisseau].couleur
                circle = pygame.draw.circle(fenetre,(COULEUR.r,COULEUR.g,COULEUR.b),(int(missiles[j].Position.x),int(missiles[j].Position.y)),missiles[j].rayon)       


        ##Affichage de texte
        text = font.render("V = ("+str(vaisseaux[0].vitesse.x)+" , "+str(vaisseaux[0].vitesse.y)+")", 1, (255, 255, 255))
        fenetre.blit(text, (20,20))

        text = font.render("P = ("+str(vaisseaux[0].position.x)+" , "+str(vaisseaux[0].position.y)+")", 1, (255, 255, 255))
        fenetre.blit(text, (20,40))

        text = font.render("Carburant: "+str(vaisseaux[0].carburant), 1, (255, 255, 255))
        fenetre.blit(text, (20,60))

        text = font.render("Munitions: "+str(vaisseaux[0].munitions), 1, (255, 255, 255))
        fenetre.blit(text, (20,80))

        text = font.render("PV: "+str(vaisseaux[0].pv), 1, (255, 255, 255))
        fenetre.blit(text, (20,100))

        text = font.render("V = ("+str(vaisseaux[1].vitesse.x)+" , "+str(vaisseaux[1].vitesse.y)+")", 1, (255, 255, 255))
        fenetre.blit(text, (TailleXFenetre-200,20))

        text = font.render("P = ("+str(vaisseaux[1].position.x)+" , "+str(vaisseaux[1].position.y)+")", 1, (255, 255, 255))
        fenetre.blit(text, (TailleXFenetre-200,40))

        text = font.render("Carburant: "+str(vaisseaux[1].carburant), 1, (255, 255, 255))
        fenetre.blit(text, (TailleXFenetre-200,60))

        text = font.render("Munitions: "+str(vaisseaux[1].munitions), 1, (255, 255, 255))
        fenetre.blit(text, (TailleXFenetre-200,80))

        text = font.render("PV: "+str(vaisseaux[1].pv), 1, (255, 255, 255))
        fenetre.blit(text, (TailleXFenetre-200,100))
        
        pygame.display.flip()
        T = t.time()


pygame.quit()
