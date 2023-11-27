import pygame as pg
import random
import mediapipe as mp
import cv2
import shelve
import time

AMD = 30
LIMIT = 30
SCORE = 0

pg.init()

w, h = pg.display.Info().current_w-30, pg.display.Info().current_h-100
screen = pg.display.set_mode((w,h))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
font = pg.font.SysFont("Arial", 30)

pg.display.set_caption("Ho Fung College Info Day Shooting Game - Christmas Cookies")

file = "src/file"

player_image = pg.transform.scale(pg.image.load("assets/player.png"), (w//5, w//5))
bgs = [pg.transform.scale(pg.image.load("assets/bg/%d.png"%i), (w+30, h+100)) for i in range(3)]
enemys = [pg.transform.scale(pg.image.load("assets/enemy/%d.png"%i), (w//10, w//10*pg.image.load("assets/enemy/%d.png"%i).get_height()//pg.image.load("assets/enemy/%d.png"%i).get_width())) for i in range(13)]
loads = [pg.transform.scale(pg.image.load("assets/load/%d.png"%i), (w//2, w//2)) for i in range(16)]
gMans = [pg.transform.scale(pg.image.load("assets/gMan/%d.png"%i), (w//10, w//10*pg.image.load("assets/gMan/%d.png"%i).get_height()//pg.image.load("assets/gMan/%d.png"%i).get_width())) for i in range(4)]
loadings = [pg.transform.scale(pg.image.load("assets/loading/%d.png"%i), (w//5, w//5*pg.image.load("assets/loading/%d.png"%i).get_height()//pg.image.load("assets/loading/%d.png"%i).get_width())) for i in range(4)]
count = [pg.transform.scale(pg.image.load("assets/count/monophy_1-%d.png"%i), (w//2, w//2)) for i in range(49)]
carck = pg.mixer.Sound(file="assets/sound.wav")
beep = pg.mixer.Sound(file="assets/beep.wav")
beeph = pg.mixer.Sound(file="assets/beeph.wav")

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
        
def Loading(limit = 20):
    cnt = 0
    while cnt<=limit:
        screen.fill(WHITE)
        screen.blit(loads[cnt%len(loads)], (w//2-loads[cnt%len(loads)].get_width()//2, h//2-loads[cnt%len(loads)].get_height()//2))
        screen.blit(gMans[cnt%len(gMans)], (w//2-gMans[cnt%len(gMans)].get_width()//2, h//2-gMans[cnt%len(gMans)].get_height()//2))
        screen.blit(loadings[cnt%len(loadings)], (w//2-loadings[cnt%len(loadings)].get_width()//2, h//3-loadings[cnt%len(loadings)].get_height()//2))
        pg.display.update()
        cnt += 1
        time.sleep(0.01)
        
Loading()
cap = cv2.VideoCapture(0)
Loading()
            
q = False
while not q:
    
    with shelve.open(file) as d:
        tScores = d['tScore']
        
    screen.blit(bgs[0], (0,0))
    printText(["HFC Info Day Hand Detect Shooting Game - Christmas Cookies",
             "Welcome, press <SPACE> to start", 
             "Top 5 Scores: "])
    rank= ["1st", "2nd", "3rd", "4th", "5th"]
    for i in range(5):
        screen.blit(font.render(rank[i], True, BLACK), (w//2-200, h//3+120+30*i))
        screen.blit(font.render(tScores[i][0].strip(), True, BLACK), (w//2-100, h//3+120+30*i))
        screen.blit(font.render("Score: %d"%tScores[i][1], True, BLACK), (w//2+100, h//3+120+30*i)) 
    pg.display.update()
    
    while True:
        event = pg.event.wait()
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            q = True
            break
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            break
            
    if q:
        break

    player = Player()
    enemy = Enemy()
    
    score = SCORE
    times = LIMIT

    mpHands = mp.solutions.hands
    
    cnt = 0
    while cnt<=48:
        screen.fill(WHITE)
        screen.blit(count[cnt], (w//2-count[cnt%len(count)].get_width()//2, h//2-count[cnt%len(count)].get_height()//2))
        pg.display.update()
        cnt += 1
        if cnt%17 == 0 or cnt == 1:
            beep.play()
        time.sleep(0.06)
    beeph.play()
    
    with mpHands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        start = pg.time.get_ticks()
        run = True
        played = False
        temp = LIMIT
                              
        while run:
            screen.fill(WHITE)
            screen.blit(bgs[1], (0,0))
            
            player.draw()
            enemy.draw()
            
            remaining = times - (pg.time.get_ticks() - start) // 1000
            
            if remaining != temp:
                played = False
                temp = remaining
            else:
                if remaining <= 5 and not played:
                    beep.play()
                    played = True
            
            screen.blit(font.render("Score: " + str(score), True, BLACK), (10, 10))

            results = hands.process(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB))
        
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    player.update([w-(hand_landmarks.landmark[7].x * w), hand_landmarks.landmark[7].y * h+AMD])
                    if enemy.collide(player.pos):
                        carck.play()
                        del enemy
                        enemy = Enemy()
                        score += 1
            else:
                time.sleep(0.001)

            if remaining <= 0:
                run = False
            elif remaining <= 5:
                screen.blit(font.render("Time Remaining: " + str(remaining), True, RED), (10, 40))
            else:
                screen.blit(font.render("Time Remaining: " + str(remaining), True, BLACK), (10, 40))
                                
            pg.display.update()
        
        beeph.play()
        del player, enemy

    Loading()
    screen.blit(bgs[2], (0,0))
    
    if score > tScores[4][1]:
        tScores.append(["", score])
        while True:
            screen.blit(bgs[2], (0,0))
            printText(["Time's Up! Final Score: %d"%score, 
                       "Congratulations, your score gets into Top 5 Scores!", 
                       "Please enter your name (At most 10 charachters) to have a cool record",
                        "Name: %s |"%tScores[5][0]], WHITE, 60)
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                break
            elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                tScores[5][0] = tScores[5][0][:-1]
            elif event.type == pg.KEYDOWN and len(tScores[5][0]) < 10:
                tScores[5][0] += event.unicode
            event = pg.event.wait()

        with shelve.open(file) as d:
            tScores.sort(reverse=True, key=lambda x: x[1])
            tScores.pop()
            d['tScore'] = tScores

    else:
        printText(["Time's Up! Final Score: %d"%score,
                   "Press <SPACE> to restart"], WHITE, 60)
        while True:
            event = pg.event.wait()            
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                break

    Loading()