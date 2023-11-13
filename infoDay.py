import pygame as pg
import random
import mediapipe as mp
import cv2
import os

pg.init()

w, h = pg.display.Info().current_w, pg.display.Info().current_h
screen = pg.display.set_mode((w-10,h-50))

pg.display.set_caption("Ho Fung College Info Day Shooting Game")

player_image = pg.transform.scale(pg.image.load("player.png"), (w//5, w//5))
target_image = pg.transform.scale(pg.image.load("target.png"), (w//10, w//10))

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
        self.pos = [random.randint(w/10, w-w/10), random.randint(h/10, h-h/10)]
        self.rect = target_image.get_rect()
        self.rect.center = self.pos
        
    def draw(self):
        screen.blit(target_image, self.rect)
        
    def collide(self, pos):
        return self.rect.collidepoint(pos)

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
        
        screen.fill((0,0,0))
        
        player.draw()
        enemy.draw()
        
        remaining = time - (pg.time.get_ticks() - start) // 1000
        font = pg.font.SysFont("Arial", 30)
        
        screen.blit(font.render("Score: " + str(score), True, (255,255,255)), (10, 10))
        screen.blit(font.render("Time Remaining: " + str(remaining), True, (255,255,255)), (10, 40))

        results = hands.process(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB))
      
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                player.update([w-(hand_landmarks.landmark[7].x * w), hand_landmarks.landmark[7].y * h])
                if enemy.collide(player.pos):
                    enemy = Enemy()
                    score += 1
                    
        if remaining <= 0:
            run = False
            game_over_text = font.render("Game Over! Final Score: " + str(score), True, (255, 255, 255))
            screen.blit(game_over_text, (w // 2 - 10, h // 2))
 
        pg.display.update()

pg.quit()