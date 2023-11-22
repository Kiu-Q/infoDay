import pygame as pg
import random
import mediapipe as mp
import cv2
import shelve

pg.init()

w, h = pg.display.Info().current_w-30, pg.display.Info().current_h-100
screen = pg.display.set_mode((w,h))
amd = -10
BLACK = (0, 0, 0)

pg.display.set_caption("Ho Fung College Info Day Shooting Game - Christmas Cookies")

player_image = pg.transform.scale(pg.image.load("player.png"), (w//5, w//5))
target_image = pg.transform.scale(pg.image.load("target.png"), (w//10, w//10))
bg_image = pg.transform.scale(pg.image.load("bg.png"), (w+30, h+100))

class Player:
    def __init__(self):
        self.pos = [w//2, h//2]
        self.rect = player_image.get_rect()
        self.rect.center = self.pos
        
    def update(self, fPos):
        self.pos = fPos
        self.rect.center = fPos
        
    def draw(self):
        screen.blit(player_image, self.rect)

class Enemy:
    def __init__(self):
        self.pos = [random.randint(w//5, w-w//10), random.randint(h//5, h-h//10)]
        self.rect = target_image.get_rect()
        self.rect.center = self.pos
        
    def draw(self):
        screen.blit(target_image, self.rect)
        
    def collide(self, pos):
        return self.rect.collidepoint(pos)

q = False
while not q:
    
    with shelve.open("file")  as d:
        tScores = d['tScore']
        
    screen.blit(bg_image, (0,0))
    font = pg.font.SysFont("Arial", 30)     
    
    tText = font.render("HFC Info Day Hand Detect Shooting Game - Christmas Cookies", True, BLACK)
    sText = font.render("Press <SPACE> to start", True, BLACK)
    topText = font.render("Top 5 Scores: ", True, BLACK)
    screen.blit(tText, (w // 2 - tText.get_width()//2, h // 4-30))
    screen.blit(sText, (w // 2 - sText.get_width()//2, h // 4))
    screen.blit(topText, (w // 2 - topText.get_width()//2, h // 4+30))
    
    cnt = 1
    for i in tScores:
        tsText = font.render("%d.%3d"%(cnt, i), True, BLACK)
        screen.blit(tsText, (w // 2 - tsText.get_width()//2, h // 4+(30+30*cnt)))
        cnt += 1   
    pg.display.update()

    press = False
    while not press:
        event = pg.event.wait()            
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            q, press = True, True
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            press = True
            
    if q:
        break

    player = Player()
    enemy = Enemy()

    score = 0
    time = 30

    mpHands = mp.solutions.hands
    cap = cv2.VideoCapture(0)

    with mpHands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        
        start = pg.time.get_ticks()
        run = True
        
        while run:
            
            screen.fill((255,255,255))
            
            player.draw()
            enemy.draw()
            
            remaining = time - (pg.time.get_ticks() - start) // 1000
            
            screen.blit(font.render("Score: " + str(score), True, BLACK), (10, 10))
            screen.blit(font.render("Time Remaining: " + str(remaining), True, BLACK), (10, 40))

            results = hands.process(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB))
        
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    player.update([w-(hand_landmarks.landmark[7].x * w), hand_landmarks.landmark[7].y * h+amd])
                    if enemy.collide(player.pos):
                        enemy = Enemy()
                        score += 1
            else:
                pass
                        
            if remaining <= 0:
                run = False
                screen.fill((255,255,255))
                gText = font.render("Game Over! Final Score: " + str(score), True, BLACK)
                lText = font.render("Press <SPACE> to restart", True, BLACK)
                screen.blit(lText, (w // 2 - lText.get_width()//2, h // 2))
                screen.blit(gText, (w // 2 - gText.get_width()//2, h // 2+30))
                
            pg.display.update()
     
    if score > min(tScores):
        tScores.append(score)
        tScores.sort(reverse=True)
        tScores.pop()
        with shelve.open("file")  as d:
            d['tScore'] = tScores
            d.close()
        
    press = False
    while not press:
        event = pg.event.wait()            
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            press = True