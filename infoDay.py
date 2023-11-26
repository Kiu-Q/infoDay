import pygame as pg
import random
import mediapipe as mp
import cv2
import shelve
import time


pg.init()

w, h = pg.display.Info().current_w-30, pg.display.Info().current_h-100
screen = pg.display.set_mode((w,h))
amd = 0
limit = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pg.font.SysFont("Arial", 30)     

pg.display.set_caption("Ho Fung College Info Day Shooting Game - Christmas Cookies")

file = "src/file"

bgs = [pg.transform.scale(pg.image.load("assets/bg/%d.png"%i), (w+30, h+100)) for i in range(3)]
enemys = [pg.transform.scale(pg.image.load("assets/enemy/%d.png"%i), (w//10, w//10*pg.image.load("assets/enemy/%d.png"%i).get_height()//pg.image.load("assets/enemy/%d.png"%i).get_width())) for i in range(13)]
loads = [pg.transform.scale(pg.image.load("assets/load/%d.png"%i), (w//2, w//2)) for i in range(16)]
gMans = [pg.transform.scale(pg.image.load("assets/gMan/%d.png"%i), (w//10, w//10*pg.image.load("assets/gMan/%d.png"%i).get_height()//pg.image.load("assets/gMan/%d.png"%i).get_width())) for i in range(4)]
loadings = [pg.transform.scale(pg.image.load("assets/loading/%d.png"%i), (w//5, w//5*pg.image.load("assets/loading/%d.png"%i).get_height()//pg.image.load("assets/loading/%d.png"%i).get_width())) for i in range(4)]
pg.mixer.music.load("assets/sound.ogg")

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
        self.pic = enemys[random.randint(0, 12)]
        self.pos = [random.randint(w//5, w-w//10), random.randint(h//5, h-h//10)]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        
    def draw(self):
        screen.blit(self.pic, self.rect)
        
    def collide(self, pos):
        return self.rect.collidepoint(pos)

def printText(text, color = BLACK, add = 0):
    for i in text:
        temp = font.render(i, True, color)
        screen.blit(temp, (w // 2 - temp.get_width()//2, h // 3 +(text.index(i)+1)*30+add))
        pg.display.update()
        
def Loading(limit = 50):
    cnt = 0
    while cnt<=limit:
        screen.fill(WHITE)
        screen.blit(loads[cnt%len(loads)], (w//2-loads[cnt%len(loads)].get_width()//2, h//2-loads[cnt%len(loads)].get_height()//2))
        screen.blit(gMans[cnt%len(gMans)], (w//2-gMans[cnt%len(gMans)].get_width()//2, h//2-gMans[cnt%len(gMans)].get_height()//2))
        screen.blit(loadings[cnt%len(loadings)], (w//2-loadings[cnt%len(loadings)].get_width()//2, h//3-loadings[cnt%len(loadings)].get_height()//2))
        pg.display.update()
        cnt += 1
        time.sleep(0.01)
            
q = False
while not q:
    
    with shelve.open(file) as d:
        tScores = d['tScore']
        
    screen.blit(bgs[0], (0,0))
    printText(["HFC Info Day Hand Detect Shooting Game - Christmas Cookies",
             "Welcome, press <SPACE> to start", 
             "Top 5 Scores: "])
    printText(["%d.%3d"%(i+1, tScores[i]) for i in range(len(tScores))], add = 90)
    

    press = False
    while not press:
        event = pg.event.wait()            
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            q, press = True, True
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            press = True
            
    if q:
        break

    Loading()

    player = Player()
    enemy = Enemy()

    score = 0
    times = limit

    mpHands = mp.solutions.hands
    cap = cv2.VideoCapture(0)

    with mpHands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        
        start = pg.time.get_ticks()
        run = True
              
        Loading()
                
        while run:
            screen.fill(WHITE)
            screen.blit(bgs[1], (0,0))
            
            player.draw()
            enemy.draw()
            
            remaining = times - (pg.time.get_ticks() - start) // 1000
            
            screen.blit(font.render("Score: " + str(score), True, BLACK), (10, 10))
            screen.blit(font.render("Time Remaining: " + str(remaining), True, BLACK), (10, 40))

            results = hands.process(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB))
        
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    player.update([w-(hand_landmarks.landmark[7].x * w), hand_landmarks.landmark[7].y * h+amd])
                    if enemy.collide(player.pos):
                        crackSound.play()
                        enemy = Enemy()
                        score += 1
            else:
                pass
                        
            if remaining <= 0:
                run = False
                                
            pg.display.update()
    
    Loading(20)
    screen.blit(bgs[2], (0,0))
    
    if score > min(tScores):
        with shelve.open(file) as d:
            tScores.append(score)
            tScores.sort(reverse=True)
            tScores.pop()
            d['tScore'] = tScores
        printText(["Time's Up! Final Score: %d"%score, 
                   "Congratulations, your score gets into Top 5 Scores!", 
                   "Press <SPACE> to view the new Top 5 Scores"], WHITE, 60)
    else:
        printText(["Time's Up! Final Score: %d"%score,
                   "Press <SPACE> to restart"], WHITE, 60)

    press = False
    while not press:
        event = pg.event.wait()            
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            press = True
            Loading(20)