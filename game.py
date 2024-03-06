import pygame as pg
import sys,time
from bird import Bird
from pipe import Pipe
pg.init()

class Game:
    def __init__(self):
        #setting window config
        self.width = 600
        self.height= 710
        self.scale_factor=1.5
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock=pg.time.Clock()
        self.move_speed=200
        self.start_monitoring=False
        self.score=0
        self.font=pg.font.Font("assets/font.ttf",24)
        self.score_text=self.font.render("Score: 0", True,(0,0,0))
        self.score_text_rect=self.score_text.get_rect(center=(100,30))

        self.restart_text=self.font.render("Restart", True,(0,0,0))
        self.restart_text_rect=self.restart_text.get_rect(center=(300,650))
        self.bird=Bird(self.scale_factor)

        self.is_enter_pressed=False
        self.is_game_started=True
        self.pipes=[]
        self.pipe_generate_counter=71
        self.setUpBgAndGround()
        
        self.gameLoop()
        
    def gameLoop(self):
        last_time=time.time()
        while True:
            #calculating delta time
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type==pg.KEYDOWN and self.is_game_started:
                    if event.key==pg.K_RETURN:
                        self.is_enter_pressed=True
                        self.bird.update_on=True
                    if event.key==pg.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)
                if event.type==pg.MOUSEBUTTONUP:
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()

            self.updateEverything(dt)
            self.checkCollisions()
            self.checkScore()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def restartGame(self):
        self.score=0
        self.score_text=self.font.render("Score: 0", True,(0,0,0))
        self.is_enter_pressed=False
        self.is_game_started=True
        self.bird.resetPosition()
        self.pipes.clear()
        self.pipe_generate_counter=71
        self.bird.update_on=False

    def checkScore(self):
        if len(self.pipes)>0:
            if (self.bird.rect.left>self.pipes[0].rect_down.left and
            self.bird.rect.right<self.pipes[0].rect_down.right and not self.start_monitoring):
                self.start_monitoring=True
            if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring:
                self.start_monitoring=False
                self.score+=1
                self.score_text=self.font.render(f"Score: {self.score}", True,(0,0,0))

    def checkCollisions(self):
        if len(self.pipes):
            if self.bird.rect.bottom>568:
                self.bird.update_on=False
                self.is_enter_pressed=False
                self.is_game_started=False
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
            self.bird.rect.colliderect(self.pipes[0].rect_up)):
                self.is_enter_pressed=False
                self.is_game_started=False

    def updateEverything(self,dt):
        if self.is_enter_pressed:
            #moving the ground
            self.ground1_rect.x-= int(self.move_speed*dt)
            self.ground2_rect.x-= int(self.move_speed*dt)

            if self.ground1_rect.right<0:
                self.ground1_rect.x=self.ground2_rect.right
            if self.ground2_rect.right<0:
                self.ground2_rect.x=self.ground1_rect.right

            #generating pipes
            if self.pipe_generate_counter>70:
                self.pipes.append(Pipe(self.scale_factor,self.move_speed))
                self.pipe_generate_counter=0
            self.pipe_generate_counter+=1

            #moving the pipes
            for pipe in self.pipes:
                pipe.update(dt)
            
            #removing pipes if out of screen
            if len(self.pipes)!=0:
                if self.pipes[0].rect_up.right<0:
                    self.pipes.pop(0)

            #moving the bird
        self.bird.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg_img,(0,-300))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img,self.ground1_rect)
        self.win.blit(self.ground2_img,self.ground2_rect)
        self.win.blit(self.bird.image,self.bird.rect)
        self.win.blit(self.score_text,self.score_text_rect)
        if not self.is_game_started:
            self.win.blit(self.restart_text,self.restart_text_rect)


    def setUpBgAndGround(self):
        #loading images fo bg and ground 
        self.bg_img=pg.transform.scale_by( pg.image.load("assets/bg (flappy).png").convert(),self.scale_factor)
        self.ground1_img=pg.transform.scale_by( pg.image.load("assets/ground.png").convert(),self.scale_factor)
        self.ground2_img=pg.transform.scale_by( pg.image.load("assets/ground.png").convert(),self.scale_factor)

        self.ground1_rect=self.ground1_img.get_rect()
        self.ground2_rect=self.ground2_img.get_rect()
        
        self.ground1_rect.x=0
        self.ground2_rect.x=self.ground1_rect.right
        self.ground1_rect.y=568
        self.ground2_rect.y=568

game=Game()