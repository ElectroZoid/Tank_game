import pygame
import math
import random


WIDTH,HEIGHT=1000,800
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Tanks')

#fps
FPS=60

#colors
WHITE=(255,255,255)
GREEN=(0,200,100)
BLACK=(0,0,0)

#dimensions
TANK_WIDTH,TANK_HEIGHT=100,100
TANK_CANNON_WIDTH,TANK_CANNON_HEIGHT=100,50
TANK_NUKE_WIDTH,TANK_NUKE_HEIGHT=30,20

#images
#1)Tank
TANK_BODY=pygame.transform.scale(pygame.image.load('tank_body.png'),(TANK_WIDTH,TANK_HEIGHT)).convert_alpha()
TANK_CANNON=pygame.transform.scale(pygame.image.load('tank_cannon.png'),(TANK_CANNON_WIDTH,TANK_CANNON_HEIGHT)).convert_alpha()
TANK_NUKE=pygame.transform.scale(pygame.image.load('tank_nuke.png'),(TANK_CANNON_WIDTH,TANK_CANNON_HEIGHT)).convert_alpha()
BACKGROUND=pygame.transform.scale(pygame.image.load(('background.png')),(WIDTH,HEIGHT)).convert_alpha()
#2)Assets

#velocity
ANG_VEL=1
VEL=3
BULLET_VEL=10

#rotation angles
ANGLE=0
ANGLE2=0


#reference Rectangles
player=pygame.Rect(500,400,1,1)



#custom events
PLAYER_HIT=pygame.USEREVENT+1


#player health
HEALTH=100

r=None

class Projectile():

    def __init__(self,x,y,width,height,angle,img,c):
        self.count=0
        self.width=width
        self.height=height
        self.angle=angle
        self.c=c
        self.x=x
        self.y=y
        self.img=pygame.transform.scale(img,(self.width,self.height))
        self.rect=pygame.Rect(self.x,self.y,1,1)                 #reference rectangle for bullet
        self.mask=None

    def draw(self):
        if self.count==1:
            WIN.blit(pygame.transform.rotate(self.img,self.angle),(self.rect.x,self.rect.y))
            self.mask=pygame.mask.from_surface(pygame.transform.rotate(self.img,self.angle))
    
    def handle_movement(self,TANK_RECT_LEFT,TANK_RECT_TOP,TANK_BODY_MASK,enemy):
            global r
            if self.mask!=None:
                if self.mask.overlap(TANK_BODY_MASK,(TANK_RECT_LEFT-self.rect.left,TANK_RECT_TOP-self.rect.top)) and self.c:
                    self.count=0
                    self.rect.x=self.x
                    self.rect.y=self.y
                    pygame.event.post(pygame.event.Event(PLAYER_HIT))

            for i in enemy:
                if self.mask!=None:
                    ENEMY_RECT_LEFT=i.x-TANK_WIDTH//2
                    ENEMY_RECT_TOP=i.y-TANK_HEIGHT//2
                    if self.mask.overlap(i.mask,(ENEMY_RECT_LEFT-self.rect.left,ENEMY_RECT_TOP-self.rect.top)) and not(self.c):
                        r=i
                        self.count=0
                        self.rect.x=self.x
                        self.rect.y=self.y
            if r!=None:
                enemy.remove(r)
                r=None

            

                        


            if self.rect.x+BULLET_VEL*math.cos(math.radians(self.angle))>0 and self.rect.x+BULLET_VEL*math.cos(math.radians(self.angle))<WIDTH and self.rect.y-BULLET_VEL*math.sin(math.radians(self.angle))>0 and self.rect.y-BULLET_VEL*math.sin(math.radians(self.angle))<HEIGHT:
                self.rect.x+=BULLET_VEL*math.cos(math.radians(self.angle))
                self.rect.y-=BULLET_VEL*math.sin(math.radians(self.angle))
            else:
                self.count=0
                self.rect.x=self.x
                self.rect.y=self.y

                    

class Enemy():

    def __init__(self,bd_img,img,x,y,player):
        self.bd_img=bd_img
        self.img=img
        self.x=x
        self.y=y
        self.player=player
        self.mask=pygame.mask.from_surface(self.bd_img)
        

        del_x=self.player.x-self.x
        del_y=self.player.y-self.y
        if del_x>0 and del_y<=0:
            angle=math.degrees((-1)*math.atan(del_y/del_x))
        elif del_x<0 and del_y<=0:
            angle=180-math.degrees(math.atan(del_y/del_x)) 
        elif del_x<0 and del_y>=0:
            angle=180+math.degrees((-1)*math.atan(del_y/del_x)) 
        elif del_x>0 and del_y>=0:
            angle=360-math.degrees(math.atan(del_y/del_x))
        
        self.angle=angle

        self.bullet=Projectile(self.x,self.y,TANK_NUKE_WIDTH,TANK_NUKE_HEIGHT,self.angle,TANK_NUKE,True)

    def draw(self):
        
        WIN.blit(self.bd_img,(self.x-TANK_WIDTH//2,self.y-TANK_HEIGHT//2)) #

        del_x=self.player.x-self.x
        del_y=self.player.y-self.y
   
        if del_x>0 and del_y<=0:
            self.angle=math.degrees((-1)*math.atan(del_y/del_x))
            WIN.blit(pygame.transform.rotate(self.img,self.angle),(self.x-(((self.img.get_width()//2)*math.cos(math.radians(self.angle)))+((self.img.get_height()//2)*math.sin(math.radians(self.angle)))),self.y-((self.img.get_height()//2)*math.cos(math.radians(self.angle)))-((self.img.get_width()//2)*math.sin(math.radians(self.angle)))))
        elif del_x<0 and del_y<=0:
            self.angle=180-math.degrees(math.atan(del_y/del_x))
            WIN.blit(pygame.transform.rotate(self.img,self.angle),(self.x+(((self.img.get_width()//2)*math.cos(math.radians(self.angle)))-((self.img.get_height()//2)*math.sin(math.radians(self.angle)))),self.y+((self.img.get_height()//2)*math.cos(math.radians(self.angle)))-((self.img.get_width()//2)*math.sin(math.radians(self.angle)))))
        elif del_x<0 and del_y>=0:
            self.angle=180+math.degrees((-1)*math.atan(del_y/del_x))
            WIN.blit(pygame.transform.rotate(self.img,self.angle),(self.x+(((self.img.get_width()//2)*math.cos(math.radians(self.angle)))+((self.img.get_height()//2)*math.sin(math.radians(self.angle)))),self.y+((self.img.get_height()//2)*math.cos(math.radians(self.angle)))+((self.img.get_width()//2)*math.sin(math.radians(self.angle)))))
        elif del_x>0 and del_y>=0:
            self.angle=360-math.degrees(math.atan(del_y/del_x))
            WIN.blit(pygame.transform.rotate(self.img,self.angle),(self.x-(((self.img.get_width()//2)*math.cos(math.radians(self.angle)))-((self.img.get_height()//2)*math.sin(math.radians(self.angle)))),self.y-((self.img.get_height()//2)*math.cos(math.radians(self.angle)))+((self.img.get_width()//2)*math.sin(math.radians(self.angle)))))



    





def draw(player,m_x,m_y,projectile,enemy,background):
    global ANGLE
    global ANGLE2
    global HEALTH
    global TANK_RECT_LEFT
    global TANK_RECT_TOP
    global TANK_BODY_MASK


    WIN.blit(background,(0,0))
    
    projectile.draw()
    
    for i in enemy:
        i.draw()
        i.bullet.draw()

    
    #rotation of tank body
    if ANGLE>=360:
        ANGLE=ANGLE-360
    elif ANGLE<0:
        ANGLE=360+ANGLE
    TANK_BODY_IMAGE=pygame.transform.rotate(TANK_BODY,ANGLE)
    if ANGLE<=90:
        TANK_RECT_LEFT,TANK_RECT_TOP=player.x-(((TANK_WIDTH//2)*math.cos(math.radians(ANGLE)))+((TANK_HEIGHT//2)*math.sin(math.radians(ANGLE)))),player.y-((TANK_HEIGHT//2)*math.cos(math.radians(ANGLE)))-((TANK_WIDTH//2)*math.sin(math.radians(ANGLE)))
        WIN.blit(TANK_BODY_IMAGE,(TANK_RECT_LEFT,TANK_RECT_TOP))
    elif ANGLE<=180:
        TANK_RECT_LEFT,TANK_RECT_TOP=player.x+(((TANK_WIDTH//2)*math.cos(math.radians(ANGLE)))-((TANK_HEIGHT//2)*math.sin(math.radians(ANGLE)))),player.y+((TANK_HEIGHT//2)*math.cos(math.radians(ANGLE)))-((TANK_WIDTH//2)*math.sin(math.radians(ANGLE)))
        WIN.blit(TANK_BODY_IMAGE,(TANK_RECT_LEFT,TANK_RECT_TOP))
    elif ANGLE<=270:
        TANK_RECT_LEFT,TANK_RECT_TOP=player.x+(((TANK_WIDTH//2)*math.cos(math.radians(ANGLE)))+((TANK_HEIGHT//2)*math.sin(math.radians(ANGLE)))),player.y+((TANK_HEIGHT//2)*math.cos(math.radians(ANGLE)))+((TANK_WIDTH//2)*math.sin(math.radians(ANGLE)))
        WIN.blit(TANK_BODY_IMAGE,(TANK_RECT_LEFT,TANK_RECT_TOP))
    else:
        TANK_RECT_LEFT,TANK_RECT_TOP=player.x-(((TANK_WIDTH//2)*math.cos(math.radians(ANGLE)))-((TANK_HEIGHT//2)*math.sin(math.radians(ANGLE)))),player.y-((TANK_HEIGHT//2)*math.cos(math.radians(ANGLE)))+((TANK_WIDTH//2)*math.sin(math.radians(ANGLE)))
        WIN.blit(TANK_BODY_IMAGE,(TANK_RECT_LEFT,TANK_RECT_TOP))
    
    TANK_BODY_MASK=pygame.mask.from_surface(TANK_BODY_IMAGE)

    #rotation of tank cannon
    DEL_X=m_x-player.x
    DEL_Y=m_y-player.y

    if DEL_X>0 and DEL_Y<=0:
        ANGLE2=math.degrees((-1)*math.atan(DEL_Y/DEL_X))
        TANK_CANNON_IMAGE=pygame.transform.rotate(TANK_CANNON,ANGLE2)
        WIN.blit(TANK_CANNON_IMAGE,(player.x-(((TANK_CANNON_WIDTH//2)*math.cos(math.radians(ANGLE2)))+((TANK_CANNON_HEIGHT//2)*math.sin(math.radians(ANGLE2)))),player.y-((TANK_CANNON_HEIGHT//2)*math.cos(math.radians(ANGLE2)))-((TANK_CANNON_WIDTH//2)*math.sin(math.radians(ANGLE2)))))
    elif DEL_X<0 and DEL_Y<=0:
        ANGLE2=180-math.degrees(math.atan(DEL_Y/DEL_X))
        TANK_CANNON_IMAGE=pygame.transform.rotate(TANK_CANNON,ANGLE2)
        WIN.blit(TANK_CANNON_IMAGE,(player.x+(((TANK_CANNON_WIDTH//2)*math.cos(math.radians(ANGLE2)))-((TANK_CANNON_HEIGHT//2)*math.sin(math.radians(ANGLE2)))),player.y+((TANK_CANNON_HEIGHT//2)*math.cos(math.radians(ANGLE2)))-((TANK_CANNON_WIDTH//2)*math.sin(math.radians(ANGLE2)))))
    elif DEL_X<0 and DEL_Y>=0:
        ANGLE2=180+math.degrees((-1)*math.atan(DEL_Y/DEL_X))
        TANK_CANNON_IMAGE=pygame.transform.rotate(TANK_CANNON,ANGLE2)
        WIN.blit(TANK_CANNON_IMAGE,(player.x+(((TANK_CANNON_WIDTH//2)*math.cos(math.radians(ANGLE2)))+((TANK_CANNON_HEIGHT//2)*math.sin(math.radians(ANGLE2)))),player.y+((TANK_CANNON_HEIGHT//2)*math.cos(math.radians(ANGLE2)))+((TANK_CANNON_WIDTH//2)*math.sin(math.radians(ANGLE2)))))
    elif DEL_X>0 and DEL_Y>=0:
        ANGLE2=360-math.degrees(math.atan(DEL_Y/DEL_X))
        TANK_CANNON_IMAGE=pygame.transform.rotate(TANK_CANNON,ANGLE2)
        WIN.blit(TANK_CANNON_IMAGE,(player.x-(((TANK_CANNON_WIDTH//2)*math.cos(math.radians(ANGLE2)))-((TANK_CANNON_HEIGHT//2)*math.sin(math.radians(ANGLE2)))),player.y-((TANK_CANNON_HEIGHT//2)*math.cos(math.radians(ANGLE2)))+((TANK_CANNON_WIDTH//2)*math.sin(math.radians(ANGLE2)))))


    pygame.draw.rect(WIN,(255,0,0),(player.x-50,player.y-100,HEALTH,10)) #health bar

    pygame.display.update()

def movement(keys,player,projectile,enemy):
    global ANGLE
    global ANGLE2
    global ANG_VEL
    global VEL


    

    if keys[pygame.K_a]:
        ANGLE+=ANG_VEL

    if keys[pygame.K_d]:
        ANGLE-=ANG_VEL

    if keys[pygame.K_w]:
        if player.x+VEL*math.cos(math.radians(ANGLE))>0 and player.x+VEL*math.cos(math.radians(ANGLE))<WIDTH and player.y-VEL*math.sin(math.radians(ANGLE))>0 and player.y-VEL*math.sin(math.radians(ANGLE))<HEIGHT:  #defined actual movement region for tank
            player.x+=VEL*math.cos(math.radians(ANGLE))
            player.y-=VEL*math.sin(math.radians(ANGLE))

    if keys[pygame.K_s]:
        if player.x-VEL*math.cos(math.radians(ANGLE))>0 and player.x-VEL*math.cos(math.radians(ANGLE))<WIDTH and player.y+VEL*math.sin(math.radians(ANGLE))>0 and player.y+VEL*math.sin(math.radians(ANGLE))<HEIGHT:
            player.x-=VEL*math.cos(math.radians(ANGLE))
            player.y+=VEL*math.sin(math.radians(ANGLE))
    
    projectile.handle_movement(TANK_RECT_LEFT,TANK_RECT_TOP,TANK_BODY_MASK,enemy) 
    for i in enemy:
        i.bullet.handle_movement(TANK_RECT_LEFT,TANK_RECT_TOP,TANK_BODY_MASK,enemy)




    
def main():

    #projectile and enemy objects
    projectile=Projectile(0,0,TANK_NUKE_WIDTH,TANK_NUKE_HEIGHT,ANGLE2,TANK_NUKE,False)  #projectile object
    enemy=set()                                                            #enemy object list


    #pygame.mouse.set_visible(False)

    clock=pygame.time.Clock()
    run=True
    
    while run:
        
        if len(enemy)==0:  

            enemy1=Enemy(TANK_BODY,TANK_CANNON,random.randint(100,WIDTH-100),random.randint(100,HEIGHT-100),player)
            enemy.add(enemy1)
        



        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                run=False
            if event.type==PLAYER_HIT:
                global HEALTH
                HEALTH-=10
                if HEALTH<=0:
                    run=False

        if pygame.mouse.get_pressed()[0]:
            if projectile.count==0:
                projectile.rect.x=player.x
                projectile.rect.y=player.y
                projectile.angle=ANGLE2
                projectile.count=1



                
        for i in enemy:            
            if i.bullet.c and i.bullet.count==0:
                i.bullet.angle=i.angle
                i.bullet.count=1



        #accessing contents from pygame
        keys=pygame.key.get_pressed()
        m_x,m_y=pygame.mouse.get_pos()




        draw(player,m_x,m_y,projectile,enemy,BACKGROUND)
        movement(keys,player,projectile,enemy)

    

    pygame.quit()

if __name__=='__main__':
    main()


