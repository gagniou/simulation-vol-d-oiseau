import pygame
from random import *
from pygame.locals import *
from math import sqrt

timer=0
continuer=1

g=6
fps=20
liste_Item=[]

            
class Oiseau():
    def __init__(self,x,y,ID):
        self.id=ID
        self.centre_x=x
        self.centre_y=y

        self.vitesse_y=randint(-9,9)
        self.vitesse_x=randint(-9,9)

        self.accel_y=0
        self.accel_x=0

        self.taille=5
        x=randint(0,5)
        if x==0 or x==3:
            self.couleurRGB=(255,255,50)
        elif x==1 or x==2:
            self.couleurRGB=(50,255,255)
        else :
            self.couleurRGB=(255,50,255)
        
    def dist(self,fly,dist):
        x=self.centre_x-fly.centre_x
        y=self.centre_y-fly.centre_y
        if ( -dist<x<dist and -dist<y<dist ):
            return 0
        else :
            return 1
        
    def couleur(self,fly):
        l_coul=[0,0,0]
        for i in range(3):
            l_coul[i]=int(0.95*self.couleurRGB[i]+0.05*fly.couleurRGB[i])
        
        self.couleurRGB=tuple(l_coul)
        
    def collision(self,fly):
        colx=0
        coly=0
        tmpcx1=self.centre_x
        tmpcy1=self.centre_y
        
        tmpcx2=self.centre_x
        tmpcy2=self.centre_y
        
        for i in range(5):
                tmpcx1+=self.vitesse_x
                tmpcy1+=self.vitesse_y
                
                tmpcx2+=fly.vitesse_x
                tmpcy2+=fly.vitesse_y
                if abs(tmpcx1-tmpcx2)<3:
                    colx=1
                if abs(tmpcy1-tmpcy2)<3:
                    coly=1

        if coly==1:
            self.vitesse_y=-self.vitesse_y         
        elif colx==1:
            self.vitesse_x=-self.vitesse_x
        
            
    def flap(self):
        if 630>self.centre_y>50 and 1300>self.centre_x>50:
            #ajout maintien d'une direction:
            if abs(self.vitesse_x)>abs(self.vitesse_y):
                self.vitesse_x+=randint(-2,2)
                self.vitesse_y+=randint(-5,5)
                if abs(self.vitesse_x)<5:
                    if self.vitesse_x<0:
                        self.vitesse_x-=7
                    else:
                        self.vitesse_x+=7
            else :
                self.vitesse_y+=randint(-2,2)
                self.vitesse_x+=randint(-5,5)
                if abs(self.vitesse_y)<5:
                   if self.vitesse_y<0:
                        self.vitesse_y-=7
                   else:
                        self.vitesse_y+=7


    def urgence(self):
        urgence=0
        if self.centre_y>668-75: #trop proche du sol
            e_pow=668-self.centre_y #compris entre 0 et 75
            
            urgence=1
            if self.vitesse_y>5:
                self.vitesse_y*=1-(1-e_pow/75)
            elif 0>self.vitesse_y:
                self.vitesse_y*=1+(1-e_pow/75)
            else : 
                self.vitesse_y=-self.vitesse_y
                
        elif self.centre_y<75: #trop proche du ciel
            e_pow=75-self.centre_y
            urgence=1
            if self.vitesse_y<-5:
                self.vitesse_y*=1-(e_pow/75)
            elif self.vitesse_y>0:
                self.vitesse_y*=1+(e_pow/75)
            else : 
                self.vitesse_y=-self.vitesse_y

        if self.centre_x>1291: #trop proche de la droite
            e_pow=1366-self.centre_x #comris entre 0 et 75
            urgence=1
            if self.vitesse_x>5:
                self.vitesse_x*=1-(1-e_pow/75)
            elif self.vitesse_x<0:
                self.vitesse_x*=1+(1-e_pow/75)
            else : 
                self.vitesse_x=-self.vitesse_x
        elif self.centre_x<75: #trop proche de la gauche
            e_pow=75-self.centre_x
            urgence=1
            if self.vitesse_x<-5:
                self.vitesse_x*=1-(1-e_pow/75)
            elif self.vitesse_x>0:
                self.vitesse_x*=1+(1-e_pow/75)
            else : 
                self.vitesse_x=-self.vitesse_x

        if urgence==1:
            if abs(self.vitesse_x)<1:
                self.vitesse_x=2
            if abs(self.vitesse_y)<1:
                self.vitesse_y=2
        return urgence

    def vol(self):
        urgence=self.urgence()

        
        for i in liste_Item:
            if (i.id!=self.id and i.dist(self,5)==0):
                self.collision(i)
        
        scale=1
        if urgence==0:
            for i in liste_Item:
                scale=1
                if (i.id!=self.id):
                    if i.dist(self,45)==0:
                        scale=0.85
                    if i.dist(self,30)==0:
                        scale=0.45
                    if i.dist(self,20)==0:
                        scale=0.20
                if scale!=1:
                    self.vitesse_y=self.vitesse_y*scale+(1-scale)*i.vitesse_y
                    self.vitesse_x=self.vitesse_x*scale+(1-scale)*i.vitesse_x
                    self.couleur(i)
                            
                

               
        self.centre_x+=self.vitesse_x
        self.centre_y+=self.vitesse_y
        
        if self.vitesse_x>0:
            self.vitesse_x-=0.15
        else :
            self.vitesse_x+=0.15
            
        if self.vitesse_y>0:
            self.vitesse_y-=0.15
        else :
            self.vitesse_y+=0.15
        
def main():

    pygame.init()
    fenetre = pygame.display.set_mode((1366, 768))

    timer=0
    continuer=1

    g=6
    fps=20
    ID=0
    clock=pygame.time.Clock()

    font=pygame.font.SysFont("comicsansms",24,bold=False,italic=False)


    for i in range (80):
        liste_Item.append(Oiseau(randint(200,1100),randint(100,580),ID))
        ID+=1
    while continuer:
        #affichage image fond
        fenetre.fill((14,207,245))
        sol=pygame.draw.rect(fenetre,(126,60,6),(0,668,1366,100),0)
           
        for event in pygame.event.get():
            if event.type==QUIT:
                continuer=0
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    continuer=0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    liste_Item.append(Oiseau(event.pos[0],event.pos[1],ID))
                    ID+=1


        for i in liste_Item:
            i.flap()
           
        for i in liste_Item:
            i.vol()
            
            pygame.draw.rect(fenetre,i.couleurRGB,(i.centre_x-(i.taille/2),i.centre_y-(i.taille/2),i.taille,i.taille),0)
        #affichage image 
        timer=timer+1
        text=font.render(str(timer),1,(255,255,0))
        fenetre.blit(text,(2,2))
        
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()



main()
