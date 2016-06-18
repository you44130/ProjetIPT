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

##Chargement de la config
fichierConfig = open("config.txt","r")
lignes = fichierConfig.readlines()
lignesmieux = []
for i in lignes:
    l = i.strip()
    l = l.split()
    lignesmieux.append(l)
    
TailleXFenetre = int(lignesmieux[0][1])
TailleYFenetre = int(lignesmieux[1][1])
PV =  int(lignesmieux[2][1])
NB_MUNITIONS_VAISSEAUX = int(lignesmieux[3][1])
rayonMaxPlanete = int(lignesmieux[4][1])
rayonMinPlanete = int(lignesmieux[5][1])
NOMBRE_CARBURANT = int(lignesmieux[6][1])
CARBURANT_PAR_POUSSEE = int(lignesmieux[7][1])
COEFFICIENT_ATTRACTION = float(lignesmieux[8][1])
fichierConfig.close()

####Dimensions de la fenetre
##TailleXFenetre = 1200
##TailleYFenetre = 700

#Initialisation de la bibliothèque Pygame
pygame.init()


pygame.display.set_caption("SPACE CONTROLLER")
fenetre = pygame.display.set_mode((TailleXFenetre, TailleYFenetre))


###importer son
##
##son_menu = pygame.mixer.Sound("menu.wav")
##son_explosion = pygame.mixer.Sound("explosion.wav")
son_explosion = pygame.mixer.Sound("explosion.wav")


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
    def __init__(self,ID,Posinit,Vinit,C,nomson,NOM):

        self.position = Posinit
        self.vitesse = Vinit

        V = Vecteur(0,0)
        while V.norme()<80:
            V.x = rd.randint(-60,60)
            V.y = rd.randint(-60,60)
        self.vitesse = V
        self.acceleration = Vecteur(0,0)
        self.son = pygame.mixer.Sound(nomson)
        self.nom = NOM
        
        self.image =  pygame.image.load("vaisseau.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(TailleXVaisseau,TailleYVaisseau))

        ##Vecteur unitaire perpendiculaire à utheta
        self.ur = Vecteur(0,0)

        ##Vecteur unitaire colinèaire a la vitesse
        self.utheta = Vecteur(0,0)

        self.carburant = NOMBRE_CARBURANT

        self.pv = PV

        self.id = ID

        self.munitions = NB_MUNITIONS_VAISSEAUX
        
        self.solide = pygame.Rect(self.position.x+TailleXVaisseau/6,self.position.y+TailleYVaisseau/6,2*TailleXVaisseau/3,2*TailleYVaisseau/3)

        ##A rajhouter
        self.initialiser_position()

        
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
            self.pv = 0
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




        self.solide = pygame.Rect(self.position.x+TailleXVaisseau/6,self.position.y+TailleYVaisseau/6,2*TailleXVaisseau/3,2*TailleYVaisseau/3)

        
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
        
        carresolide = carrevaisseau + carreplanete + carrecomete
        
        carresolide.pop(self.id) ## on retire le vaisseau des objets bloqués


        ##print(self.solide.colliderect(Liste[0]))
        
        if self.solide.collidelist(carresolide) != -1:
            
            return(-1)
        else:
            return(1)

    ## A rajouter
    def initialiser_position(self):
        '''Calcul de la position initiale'''
        
        self.position = Vecteur(rd.randint(0,TailleXFenetre),rd.randint(0,TailleYFenetre))
        self.solide = pygame.Rect(self.position.x,self.position.y,TailleXVaisseau,TailleYVaisseau)
        while self.solide.collidelist(carreplanete3) != -1:
            self.solide = pygame.Rect(self.position.x,self.position.y,TailleXVaisseau,TailleYVaisseau)
            self.position = Vecteur(rd.randint(0,TailleXFenetre),rd.randint(0,TailleYFenetre))
            print("Probleme")

            
    def gererVie (): ######################################
        for i in range(nbVaisseaux):
            if vaisseaux[i].pv <= 0:
                global idJoueurPerdu
                idJoueurPerdu = vaisseaux[i].id +1
                son_explosion.play()

                global avancement
                avancement = AVANCEMENT_PERDU
##                text = font.render(str(vaisseaux[i].nom)+"   a perdu   ",1, (0, 255, 255))
##                fenetre.blit(text, (200,200))




            
class Comete:
    '''Classe Vaisseau, qui contient les méthodes et
    informations des vaisseaux'''
    def __init__(self,ID):

        self.position = Vecteur(0,rd.randint(0,TailleYFenetre))
        self.TailleComete=40
        self.vitesse = Vecteur(200,rd.randint(-50,50))
        self.acceleration = Vecteur(0,0)
        
        self.image =  pygame.image.load("comet_gauche.png").convert_alpha()
        
        self.placementInitial()

        
        self.image = pygame.transform.scale(self.image,(self.TailleComete,self.TailleComete))

        ##Vecteur unitaire perpendiculaire à utheta
        self.ur = Vecteur(0,0)

        ##Vecteur unitaire colinèaire a la vitesse
        self.utheta = Vecteur(0,0)

        self.carburant = 1000

        self.id = ID


        self.solide = pygame.Rect(self.position.x+self.TailleComete/6,self.position.y+self.TailleComete/6,2*self.TailleComete/3,2*self.TailleComete/3)



        self.etat = 1 #En vie ou non

    def placementInitial(self):
        '''Définit le côté de départ de la comete aléatoirement'''

        hautCote = rd.randint(1,2) ##1 il arrivera d'en haut ou d'en bas, 2 il arrivera de gauche ou de droite
        haut = rd.randint(1,2) ##1 en haut 2 en bas
        cote = rd.randint(1,2) ## 1gauche 2 droite

        if hautCote == 1:

            if haut == 1:

                self.position = Vecteur(rd.randint(0,TailleXFenetre),0)
                self.vitesse = Vecteur(rd.randint(-70,70),rd.randint(60,80))
            elif haut == 2:

                self.position = Vecteur(rd.randint(0,TailleXFenetre),TailleYFenetre)
                self.vitesse = Vecteur(rd.randint(-70,70),rd.randint(-80,-60))
            
        elif hautCote == 2:

            if cote == 1:

                self.position = Vecteur(0,rd.randint(0,TailleYFenetre))
                self.vitesse = Vecteur(rd.randint(60,80),rd.randint(-70,70))
                self.image =  pygame.image.load("comet_droite.png").convert_alpha()
            elif cote == 2:

                self.position = Vecteur(TailleXFenetre,rd.randint(0,TailleYFenetre))
                self.vitesse = Vecteur(rd.randint(-80,-60),rd.randint(-70,70))
                self.image =  pygame.image.load("comet_gauche.png").convert_alpha()
        
        

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


        self.solide = pygame.Rect(self.position.x+self.TailleComete/6,self.position.y+self.TailleComete/6,2*self.TailleComete/3,2*self.TailleComete/3)

        
        ##Vérification des délimitations
        self.verifierPositions()

    def verifierPositions(self):
        '''Si il sort de la fenetre on le fait ressortir de l'autre côté'''

        ##En haut
        if self.position.x == 0:
            self.etat = 0

        ##En bas
        elif self.position.x >= TailleXFenetre:
            self.etat = 0

        ##A droite
        elif self.position.y == 0:
            self.etat = 0

        ##A gauche
        elif self.position.y >= TailleYFenetre:
            self.etat = 0
        ###controle vitesse :
        if (self.vitesse.x)>1000:
            self.vitesse.x=1000
        if (self.vitesse.y)>1000:
            self.vitesse.y=1000
    


    def gererCollisions(self):

        Liste = copy.deepcopy(carrevaisseau)

        Liste.pop(self.id) ## on retire le vaisseau des objets bloqués
  
        ##print(self.solide.colliderect(Liste[0]))
        
        if self.solide.collidelist(Liste) != -1:
            print("collision")
            


   

        

        
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
        m = 4/3 * 3.14 * ((R * 100) ** 3) * COEFFICIENT_ATTRACTION ** 18
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
        ##Solide encore plus grand
        self.solide3 = pygame.Rect( self.x - (self.rayon * 4) * pow(1/2,1/2), self.y - (self.rayon * 4)*pow(1/2, 0.5), 8*self.rayon* pow(0.5, 0.5) ,8*self.rayon*pow(0.5,0.5))


    


    def initialiserPositions(self):

        global carreplanete
        global carreplanete2
        global carreplanete3
        
        self.x = rd.randint(100,TailleXFenetre-100)
        self.y = rd.randint(100,TailleYFenetre-100)
        self.solide2 = pygame.Rect( self.x - (self.rayon * 2) * pow(1/2,1/2), self.y - (self.rayon * 2)*pow(1/2, 0.5), 4*self.rayon* pow(0.5, 0.5) ,4*self.rayon*pow(0.5,0.5))
        self.solide = pygame.Rect( self.x - self.rayon * pow(1/2,1/2), self.y - self.rayon*pow(1/2, 0.5), 2*self.rayon* pow(0.5, 0.5) ,2*self.rayon*pow(0.5,0.5))
        self.solide3 = pygame.Rect( self.x - (self.rayon * 4) * pow(1/2,1/2), self.y - (self.rayon * 4)*pow(1/2, 0.5), 8*self.rayon* pow(0.5, 0.5) ,8*self.rayon*pow(0.5,0.5))
        
        while self.solide.collidelist(carreplanete3) != -1:
            self.x = rd.randint(100,TailleXFenetre-100)
            self.y = rd.randint(100,TailleYFenetre-100)
            self.solide2 = pygame.Rect( self.x - (self.rayon * 2) * pow(1/2,1/2), self.y - (self.rayon * 2)*pow(1/2, 0.5), 4*self.rayon* pow(0.5, 0.5) ,4*self.rayon*pow(0.5,0.5))
            self.solide = pygame.Rect( self.x - self.rayon * pow(1/2,1/2), self.y - self.rayon*pow(1/2, 0.5), 2*self.rayon* pow(0.5, 0.5) ,2*self.rayon*pow(0.5,0.5))
            self.solide3 = pygame.Rect( self.x - (self.rayon * 4) * pow(1/2,1/2), self.y - (self.rayon * 4)*pow(1/2, 0.5), 8*self.rayon* pow(0.5, 0.5) ,8*self.rayon*pow(0.5,0.5))

            
        carreplanete3.append(self.solide3)
        carreplanete2.append(self.solide2)
        carreplanete.append(self.solide)
        



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





##Iddujoueurperdu
idJoueurPerdu = 0

####VARIABLE IMPORTANTE
'''
Si avancement = 0:
menu
Si avancement = 2:
Jouer
Si avancement = 3:
on a perdu

'''
##Police
font = pygame.font.Font(None, 15)
font50 = pygame.font.Font(None, 50)

pygame.key.set_repeat(100, 60)

avancement = 1

##CONSTANTES D'AVANCEMENT
AVANCEMENT_MENU = 0
AVANCEMENT_PROGRAMMATION_JEU = 1
AVANCEMENT_PAUSE = 4
tempsPAUSE = t.time()
AVANCEMENT_JOUER = 2
AVANCEMENT_PERDU = 3



#Boucle infinie
while continuer:

    if avancement == AVANCEMENT_PROGRAMMATION_JEU:

        T = t.time()

        ##Pas d'intégration et vitesse de la boucle
        pasDeTemps = 20e-3
        tpscometes=10
        nbPlanetes = 12
        
        nbVaisseaux = 2

        
        #PV = 10



        ##Planètes:
        #rayonMinPlanete = 20
        #rayonMaxPlanete = 50

        ##Taille de l'image vaisseau
        TailleXVaisseau = 30
        TailleYVaisseau = 30
        #Augmentation de la vitesse a chaque poussée
        poussee = 8

        #CARBURANT_PAR_POUSSEE = 2
        #NOMBRE_CARBURANT = 1000

        #NB_MUNITIONS_VAISSEAUX = 100

        ##Liste des différents objets
        planetes = []
        vaisseaux = []
        missiles  = []
        cometes = []

        carreplanete = []
        carreplanete2 = []
        carreplanete3 = []
        ##Création des planètes et des vaisseaux
        for i in range(nbPlanetes):
            planetes.append(planete(i))
            planetes[i].initialiserPositions()
        ##A changer, j'ai déplacé la définition de carré solide
        ## on liste tous les solides 
        ##carreplanete = [planetes[i].solide for i in range(nbPlanetes)]

        ##carreplanete2 = [planetes[i].solide2 for i in range(nbPlanetes)]


        nomson = [ "lasercoupe.wav" , "missilecoupe.wav"]

        
        
        ##Chargement des noms des joueurs
        fichierNom = open("nomsJoueurs.txt","r")
        lignes = fichierNom.readlines()

        fichierConfig.close()
        
        noms = []
        for i in lignes:
            l = i.strip()
            noms.append(l)

        fichierNom.close()

        for i in range(nbVaisseaux):
            vaisseaux.append(Vaisseau(i,Vecteur(rd.randint(0,TailleXFenetre),rd.randint(0,TailleYFenetre)),Vecteur(50,-50),Couleur(255,rd.randint(0,255),0),nomson[i],noms[i]))
            
        carrevaisseau = [ vaisseaux[i].solide for i in range(nbVaisseaux)]
        carresolide = carrevaisseau + carreplanete #+carrecomete

        ##for i in range(nbCometes):
        ##    cometes.append(Comete(i))
        ##carrecomete = [cometes[i].solide for i in range(nbCometes)]
        carrecomete = []
        ##TOUCHES
        ##Tableau selon les joueurs: Joueuri = [gauche,bas,droit,haut,tir]
        # touches = [Joueur 1, Joueur 2]

        ##Chargement des touches
        fichierTouches = open("touches.txt","r")
        lignes = fichierTouches.readlines()
        lignesmieux = []
        for i in lignes:
            l = i.strip()
            l = l.split()
            lignesmieux.append(l)

        touches = []

        
        touche1 = ['','','','','','']
        touche1[0] = lignesmieux[2][1]
        touche1[1] = lignesmieux[4][1]
        touche1[2] = lignesmieux[1][1]
        touche1[3] = lignesmieux[3][1]
        touche1[4] = lignesmieux[5][1]
        touches.append(touche1)
        touche2 = ['','','','','','']
        touche2[0] = lignesmieux[8][1]
        touche2[1] = lignesmieux[10][1]
        touche2[2] = lignesmieux[7][1]
        touche2[3] = lignesmieux[9][1]
        touche2[4] = lignesmieux[11][1]
        touches.append(touche2)

        fichierTouches.close()
        #touches = [['left','down','right','up','space'],['a','s','d','w','e']]



        ##Gestion du fond
        fond = pygame.image.load("fond.jpg").convert()
        ##On l'agrandit
        fond = pygame.transform.scale(fond,(TailleXFenetre,TailleYFenetre))


        tpscomete=t.time()
        nvellevague=0
        a=1
        tempsAppartitionNouvelleComete = rd.randint(10,22)
        
        avancement = AVANCEMENT_JOUER
    
    if avancement == AVANCEMENT_JOUER: ##JEU
        if (t.time()-T>=pasDeTemps):
            
            


            
            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
                if event.type == QUIT:     #Si un de ces événements est de type QUIT
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

                            for j in range(nbVaisseaux):

                                if vaisseaux[j].carburant>0:
                                    if nomTouche == touches[j][2]:
                                        vaisseaux[j].vitesse = Vecteur.somme(vaisseaux[j].vitesse,Vecteur.multiplie(vaisseaux[j].ur,poussee))
                                        vaisseaux[j].carburant -= CARBURANT_PAR_POUSSEE
                                    if nomTouche == touches[j][0]:
                                        vaisseaux[j].vitesse = Vecteur.somme(vaisseaux[j].vitesse,Vecteur.multiplie(vaisseaux[j].ur,-poussee))
                                        vaisseaux[j].carburant -= CARBURANT_PAR_POUSSEE
                                    if nomTouche == touches[j][3]:
                                        vaisseaux[j].vitesse = Vecteur.somme(vaisseaux[j].vitesse,Vecteur.multiplie(vaisseaux[j].utheta,poussee))
                                        vaisseaux[j].carburant -= CARBURANT_PAR_POUSSEE
                                    if nomTouche == touches[j][1]:
                                        vaisseaux[j].vitesse= Vecteur.somme(vaisseaux[j].vitesse,Vecteur.multiplie(vaisseaux[j].utheta,-poussee))
                                        vaisseaux[j].carburant -= CARBURANT_PAR_POUSSEE
                                if nomTouche == touches[j][4]:
                                    if vaisseaux[j].munitions >0:
                                        missiles.append(Missile(Vecteur(vaisseaux[j].position.x,vaisseaux[j].position.y),Vecteur(vaisseaux[j].utheta.x*500,vaisseaux[j].utheta.y*500),j,len(missiles)))
                                        vaisseaux[j].munitions -= 1
                                        vaisseaux[j].son.play()

                            if t.time()-tempsPAUSE>0.8: ##Pour éviter la répétition trop rapide
                                if nomTouche == 'pause':
                                    avancement = AVANCEMENT_PAUSE
                                    tempsPAUSE = t.time()
                    
            
            ##Affichage du fond
            fenetre.blit(fond, (0,0))

            ##construction cometes:
                         ##Cometes :
            if t.time()-tpscomete >= tempsAppartitionNouvelleComete:
                a=rd.randint(1,3)
                nvellevague=nvellevague+a
                tpscomete=t.time()
                for i in range(a):
                    cometes.append(Comete(len(cometes)+i))
                tempsAppartitionNouvelleComete = rd.randint(10,22)
                
                
            for i in range(len(cometes)):
                if cometes[i].etat == 1:
                    cometes[i].bouger()
                    fenetre.blit(cometes[i].image, (cometes[i].position.x,cometes[i].position.y))
                carrecomete = [cometes[i].solide for i in range(len(cometes)) if cometes[i].etat == 1]
            

                           
            
                    
            

            ##Planetes
            ##Dessin des planètes (cercles)
            for i in range(nbPlanetes):
                cercle = pygame.draw.circle(fenetre,(planetes[i].couleur.r,planetes[i].couleur.g,planetes[i].couleur.b),(planetes[i].x,planetes[i].y),planetes[i].rayon)
                #rectangle = pygame.draw.rect(fenetre,(255,0,255),planetes[i].solide3)
           
                    
                
            ##Vaisseaux

            ##Dessin et mouvement des vaisseaux
            for i in range(nbVaisseaux):
                vaisseaux[i].bouger()
                fenetre.blit( vaisseaux[i].image,( vaisseaux[i].position.x,vaisseaux[i].position.y))
                ##vaisseaux[i].gererCollisions()
                rectangle = pygame.draw.rect(fenetre,(255,0,0),vaisseaux[i].solide)            
                
                ##Dessin des vitesses des vaisseaux et des vecteur utheta et ur
                Vligne = pygame.draw.line(fenetre, (255,255,255), (vaisseaux[i].position.x,vaisseaux[i].position.y), (vaisseaux[i].position.x+vaisseaux[i].vitesse.x,vaisseaux[i].position.y+vaisseaux[i].vitesse.y))
                Vligne = pygame.draw.line(fenetre, (255,0,0), (vaisseaux[i].position.x,vaisseaux[i].position.y), (vaisseaux[i].position.x+vaisseaux[i].utheta.x*20,vaisseaux[i].position.y+vaisseaux[i].utheta.y*20))
                Vligne = pygame.draw.line(fenetre, (0,255,0), (vaisseaux[i].position.x,vaisseaux[i].position.y), (vaisseaux[i].position.x+vaisseaux[i].ur.x*20,vaisseaux[i].position.y+vaisseaux[i].ur.y*20))

                text = font.render("JOUEUR "+str(vaisseaux[i].id+1)+" "+str(vaisseaux[i].nom)+" , PV: "+str(vaisseaux[i].pv), 1, (255, 255, 255))
                fenetre.blit(text, (vaisseaux[i].position.x-10,vaisseaux[i].position.y-20))
             ##Dessin et gestion des Munitions
            for j in range(0,len(missiles)):
                if missiles[j].etat == 1:
                    missiles[j].bouger()
                    missiles[j].gererCollisions()
                    
                    COULEUR = vaisseaux[missiles[j].idVaisseau].couleur
                    circle = pygame.draw.circle(fenetre,(COULEUR.r,COULEUR.g,COULEUR.b),(int(missiles[j].Position.x),int(missiles[j].Position.y)),missiles[j].rayon)       


            ##Affichage de texte
            text = font.render("V = ("+str(int(vaisseaux[0].vitesse.x))+" , "+str(int(vaisseaux[0].vitesse.y))+")", 1, (255, 255, 255))
            fenetre.blit(text, (20,20))

            text = font.render("P = ("+str(int(vaisseaux[0].position.x))+" , "+str(int(vaisseaux[0].position.y))+")", 1, (255, 255, 255))
            fenetre.blit(text, (20,40))

            text = font.render("Carburant: "+str(vaisseaux[0].carburant), 1, (255, 255, 255))
            fenetre.blit(text, (20,60))

            text = font.render("Munitions: "+str(vaisseaux[0].munitions), 1, (255, 255, 255))
            fenetre.blit(text, (20,80))

            text = font.render("PV: "+str(vaisseaux[0].pv), 1, (255, 255, 255))
            fenetre.blit(text, (20,100))

            text = font.render("V = ("+str(int(vaisseaux[1].vitesse.x))+" , "+str(int(vaisseaux[1].vitesse.y))+")", 1, (255, 255, 255))
            fenetre.blit(text, (TailleXFenetre-200,20))

            text = font.render("P = ("+str(int(vaisseaux[1].position.x))+" , "+str(int(vaisseaux[1].position.y))+")", 1, (255, 255, 255))
            fenetre.blit(text, (TailleXFenetre-200,40))

            text = font.render("Carburant: "+str(vaisseaux[1].carburant), 1, (255, 255, 255))
            fenetre.blit(text, (TailleXFenetre-200,60))

            text = font.render("Munitions: "+str(vaisseaux[1].munitions), 1, (255, 255, 255))
            fenetre.blit(text, (TailleXFenetre-200,80))

            text = font.render("PV: "+str(vaisseaux[1].pv), 1, (255, 255, 255))
            fenetre.blit(text, (TailleXFenetre-200,100))

            Vaisseau.gererVie() ######################################
            
            pygame.display.flip()
            T = t.time()

            

    if avancement == AVANCEMENT_PAUSE:
        ##On est en pause
        
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                continuer = 0
                
            if event.type == KEYDOWN:
                touchesPressees = pygame.key.get_pressed()
                
                for i in range(0,len(touchesPressees)): 
                    if touchesPressees[i] == 1 :
                        nomTouche = pygame.key.name(i)

                        if t.time()-tempsPAUSE > 0.8: ##POUR eviter le changement trop rapide
                            if nomTouche == 'pause':
                                avancement = AVANCEMENT_JOUER
                                tempsPAUSE = t.time()
                        if nomTouche == 'escape':
                            avancement = AVANCEMENT_PROGRAMMATION_JEU

        ##On affiche pause
        text = font50.render("PAUSE",1, (0, 255, 255))
        fenetre.blit(text, (TailleXFenetre/6,TailleYFenetre/3))
        text = font50.render("Appuyez sur echap pour retourner au menu",1, (0, 255, 255))
        fenetre.blit(text, (3*TailleXFenetre/10,11*TailleYFenetre/15))
        
        pygame.display.flip()

    if avancement == AVANCEMENT_PERDU:

        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                continuer = 0
            if event.type == KEYDOWN:
                touchesPressees = pygame.key.get_pressed()

                for i in range(0,len(touchesPressees)): 
                    if touchesPressees[i] == 1 :
                        nomTouche = pygame.key.name(i)
                        if nomTouche == 'escape':
                        
                            avancement = AVANCEMENT_PROGRAMMATION_JEU
        
        text = font50.render("Le joueur "+str(idJoueurPerdu)+"  a perdu. Dommage "+vaisseaux[idJoueurPerdu-1].nom+" ! ",1, (0, 255, 255))
        fenetre.blit(text, (TailleXFenetre/6,TailleYFenetre/3))
        text = font50.render("Appuyez sur echap pour retourner au menu",1, (0, 255, 255))
        fenetre.blit(text, (TailleXFenetre/6,TailleYFenetre/3+100))
        
        pygame.display.flip()
        
pygame.quit()
