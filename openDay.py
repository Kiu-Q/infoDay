from __init__ import *

class Object:
    def __self__(self):
        self.rect.center = self.pos
    
    def draw(self):
        screen.blit(self.pic, self.rect)
    
    def update(self, fPos):
        self.pos = fPos
        self.rect.center = fPos

class Shooter(Object):
    def __init__(self):
        self.pos = [w//2, h//2]
        self.pic = shooter
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
                        
class Ballon(Object):
    def __init__(self):
        global prev
        temp = random.randint(w//5, w-w//10)
        if temp in range(prev-100, prev):
            temp -=50
        elif temp in range(prev, prev+100):
            temp +=50
        self.pos = [temp, h+h//10]
        prev = self.pos[0]
        self.num = random.randint(0, 9) if random.randint(0, 9)%2 == 0 else random.randint(1, 3)
        self.pic = ballons[self.num]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        
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
        screen.blit(gifs[cnt%len(gifs)], (w//2-gifs[cnt%len(gifs)].get_width()//2, h//2-gifs[cnt%len(gifs)].get_height()//2))
        screen.blit(loadings[cnt%len(loadings)], (w//2-loadings[cnt%len(loadings)].get_width()//2, h//3-loadings[cnt%len(loadings)].get_height()//2))
        pg.display.update()
        cnt += 1
        time.sleep(0.01)

Loading()
cap = cv2.VideoCapture(0)
Loading()

while True:
    with shelve.open(file) as d:
        tScores = d['tScore']
    screen.blit(bgs[0], (0,0))
    printText(["Level 1: Score EXACTLY 50 points as soon as possible.",
             "Press <SPACE> to start", 
             "Top 5 completing time: "])
    for i in range(5):
        screen.blit(font.render(rank[i], True, BLACK), (w//2-200, h//3+120+30*i))
        screen.blit(font.render(tScores[i][0].strip(), True, BLACK), (w//2-100, h//3+120+30*i))
        screen.blit(font.render("Time: %ds"%tScores[i][1], True, BLACK), (w//2+100, h//3+120+30*i)) 
    pg.display.update()
    while True:
        event = pg.event.wait()
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            q = True
            break
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            break
    cnt = 0
    while cnt<=48:
        screen.blit(bgs[3], (0,0))
        screen.blit(count[cnt], (w//2-count[cnt%len(count)].get_width()//2, h//2-count[cnt%len(count)].get_height()//2))
        pg.display.update()
        cnt += 1
        if cnt%17 == 0 or cnt == 1:
            beep.play()
        time.sleep(0.06)
    beeph.play()
    with mpHands.Hands(
        model_complexity=0,
        min_detection_confidence=0.9,
        min_tracking_confidence=0.9) as hands:

        start = pg.time.get_ticks()
        run = True
        played = False
        
        player = Shooter()
        targets.append(Ballon())
        
        score = SCORE
        
        while run:
            screen.fill(WHITE)
            screen.blit(bgs[3], (0,0))
            
            if random.randint(0, 50) == 1:
                targets.append(Ballon())
                
            if targets == []:
                targets.append(Ballon())
            
            for target in targets: 
                target.update((target.pos[0], target.pos[1]-random.randint(2, 5)))
                target.draw()
                if target.pos[1]<-h//4:
                    targets.remove(target)
                    del target
                    targets.append(Ballon())
            
            player.draw()
            
            timeUsed = (pg.time.get_ticks() - start) // 1000
            
            screen.blit(font.render("Time Used: " + str(timeUsed), True, BLACK), (10, 40))

            results = hands.process(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    player.update([w-(hand_landmarks.landmark[7].x * w), hand_landmarks.landmark[7].y * h+AMD])
                for target in targets:
                    if target.collide(player.pos):
                        screen.blit(explode, (target.pos[0]-100, player.pos[1]-100))
                        carck.play()
                        score += target.num
                        targets.remove(target)
                        del target
                        if random.randint(0, 1) == 1:
                            targets.append(Ballon())
            else:
                time.sleep(0.01)

            if score == 50:
                run = False
                win = True
            elif score>=50:
                run = False
                win = False
            else:
                screen.blit(font.render("Score: " + str(score)+" / 50", True, BLACK), (10, 10))

            pg.display.update()
        
        beeph.play()
        del player
        targets = []

    Loading()
    screen.blit(bgs[0], (0,0))
    
    if win:
        if timeUsed < tScores[4][1]:
            tScores.append(["", timeUsed])
            while True:
                screen.blit(bgs[0], (0,0))
                printText(["50 points scored! Time used: %ds"%timeUsed, 
                        "Congratulations, your score gets into Top 5 completeing time!", 
                        "Please enter your name (At most 10 charachters) to have a cool record",
                            "Name: %s |"%tScores[5][0]], BLACK, 60)
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    break
                elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                    tScores[5][0] = tScores[5][0][:-1]
                elif event.type == pg.KEYDOWN and len(tScores[5][0]) < 10:
                    tScores[5][0] += event.unicode
                event = pg.event.wait()

            with shelve.open(file) as d:
                tScores.sort(reverse=False, key=lambda x: x[1])
                tScores.pop()
                d['tScore'] = tScores
        else:
            printText(["50 points scored! Time used: %ds"%timeUsed,
                    "Press <SPACE> to Level 2"], BLACK, 60)
            while True:
                event = pg.event.wait()            
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    break
    else:
        printText(["Over 50 points scored! You Lose.",
                   "Press <SPACE> to restart"], RED, 60)
        while True:
            event = pg.event.wait()            
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                break

        Loading()