# Info Day Shooting Game - Christmas Cookies

## Purpose
This Python program is a shooting game developed for the Ho Fung College Info Day event, with a festive theme of Christmas cookies. The game is designed to provide entertainment and engagement for participants attending the Info Day.

## Progress
The game is currently in a functional state and offers the following features:
- Shooting game mechanics where players control a character to shoot down enemies.
- Hand detection using the Mediapipe library to track the player's hand movements.
- Score tracking and display.
- Time limit for gameplay.
- Top 5 scores leaderboard.

## Techniques Used
The program utilizes various techniques and technologies, including:
- Pygame: A Python library for game development, used to create the game window, handle graphics, and user input.
- Mediapipe: A cross-platform framework for building multimodal applied ML pipelines, used for hand detection and tracking.
- OpenCV: An open-source computer vision library, used to capture video frames from the webcam for hand detection.
- Shelve: A Python library for object persistence, used to store and retrieve the top 5 scores leaderboard.

## How to Play
1. Launch the program.
2. Press the SPACEBAR to start the game.
3. Control the character's movement by moving your hand in front of the webcam.
4. Shoot down the enemies by touching them with your hand.
5. Aim to achieve the highest score within the time limit.
6. Once the time is up, the game will display the final score and provide options for restarting or entering your name for a top 5 score record.

## Installation
To run the program, follow these steps:
1. Cpoy the `E:\python` and `E:\school` folder to `C:\Users\student\Desktop`
2. Open `infoDay.py` with `Thonny`
3. In `Thonny`, press `run` > `Configure interpreter...`
4. In `Details` > `Python executable`, browse path to `C:\Users\student\Desktop\python\python.exe` and press `OK`
5. Press `Ctrl+T` to run current script in terminal

## Details

The `infoDay.py` program consists of several classes and functions that work together to create the Info Day Shooting Game - Christmas Cookies. Let's explore the code and its functionality in more detail:

### Game Parameters

The code snippet includes the following variables used to control various aspects of the game:

```python
AMD = 30
LIMIT = 30
SCORE = 0
```

- `AMD`: AMD stands for "Amending Camera." The value of 30 suggests that the program adjusts the camera input every 30 frames. By periodically recalibrating, the program can adapt to changes in lighting conditions or hand position variations, ensuring accurate hand tracking throughout the gameplay.

- `LIMIT`: The `LIMIT` variable sets the time limit for the game in seconds. In this case, the value is set to 30, indicating that players have 30 seconds to achieve the highest score possible.

- `SCORE`: The `SCORE` variable represents the initial score for the game. In the provided code, the score is initialized with a value of 0. As the player successfully shoots down enemies, the score will be updated accordingly.

### Game Initialization and Setup

The program starts by initializing Pygame and setting up the game window. It defines constants for colors and loads necessary assets such as images and sounds.

```python
pg.init()

w, h = pg.display.Info().current_w-30, pg.display.Info().current_h-100
screen = pg.display.set_mode((w,h))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
font = pg.font.SysFont("Arial", 30)

pg.display.set_caption("Ho Fung College Info Day Shooting Game - Christmas Cookies")

file = "src/file"

player_image = pg.transform.scale(pg.image.load("assets/player.png"), (w//5, w//5))
bgs = [pg.transform.scale(pg.image.load("assets/bg/%d.png" % i), (w+30, h+100)) for i in range(3)]
enemys = [pg.transform.scale(pg.image.load("assets/enemy/%d.png" % i), (w//10, w//10*pg.image.load("assets/enemy/%d.png" % i).get_height()//pg.image.load("assets/enemy/%d.png" % i).get_width())) for i in range(13)]
loads = [pg.transform.scale(pg.image.load("assets/load/%d.png" % i), (w//2, w//2)) for i in range(16)]
gMans = [pg.transform.scale(pg.image.load("assets/gMan/%d.png" % i), (w//10, w//10*pg.image.load("assets/gMan/%d.png" % i).get_height()//pg.image.load("assets/gMan/%d.png" % i).get_width())) for i in range(4)]
loadings = [pg.transform.scale(pg.image.load("assets/loading/%d.png" % i), (w//5, w//5*pg.image.load("assets/loading/%d.png" % i).get_height()//pg.image.load("assets/loading/%d.png" % i).get_width())) for i in range(4)]
count = [pg.transform.scale(pg.image.load("assets/count/monophy_1-%d.png" % i), (w//2, w//2)) for i in range(49)]
carck = pg.mixer.Sound(file="assets/sound.wav")
beep = pg.mixer.Sound(file="assets/beep.wav")
beeph = pg.mixer.Sound(file="assets/beeph.wav")
```

### Player Class
The `Player` class represents the player character in the game. It is responsible for tracking the player's position and updating it based on the hand movements detected by the webcam. The `update()` method receives the hand position and updates the player's position accordingly. The `draw()` method is used to render the player character on the screen.

```python
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
```

### Enemy Class
The `Enemy` class represents the enemies that the player needs to shoot down. Each enemy is randomly generated with a different image. The `draw()` method is used to render the enemy on the screen, and the `collide()` method checks if the player's hand position collides with the enemy.

```python
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
```

### printText() Function
The `printText()` function is responsible for rendering text on the screen. It takes a text string, color, and additional offset as parameters. It iterates over each character in the text and renders it using the `font.render()` method.

```python
def printText(text, color=BLACK, add=0):
    for i in text:
        temp = font.render(i, True, color)
        screen.blit(temp, (w // 2 - temp.get_width()//2, h // 3 +(text.index(i)+1)*30+add))
        pg.display.update()
```

### Loading() Function
The `Loading()` function displays a loading screen with animations. It takes a limit parameter to control the duration of the loading animation. The function repeatedly fills the screen with a white color and renders different images at specific positions to create the loading effect.

```python
def Loading(limit=20):
    cnt = 0
    while cnt <= limit:
        screen.fill(WHITE)
        screen.blit(loads[cnt%len(loads)], (w//2-loads[cnt%len(loads)].get_width()//2, h//2-loads[cnt%len(loads)].get_height()//2))
        screen.blit(gMans[cnt%len(gMans)], (w//2-gMans[cnt%len(gMans)].get_width()//2, h//2-gMans[cnt%len(gMans)].get_height()//2))
        screen.blit(loadings[cnt%len(loadings)], (w//2-loadings[cnt%len(loadings)].get_width()//2, h//3-loadings[cnt%len(loadings)].get_height()//2))
        pg.display.update()
        cnt += 1
        time.sleep(0.01)
```

### Main Game Loop

The main game loop is responsible for updating the game state and handling user input. It runs continuously until the game is exited. Within the loop, the program checks for events such as key presses and mouse movements, and updates the player position accordingly.

```python
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                running = True

    if running:
        # Update player position based on hand movements
        player.update(hand_position)

        # Update game logic (enemy movement, collisions, etc.)

        # Draw game elements on the screen
        screen.fill(BLACK)
        # Draw player
        player.draw()
        # Draw enemies

    pg.display.update()
```

The complete game logic, including scoring, time management, sound effects, and user interfaces, is not shown in the provided code snippet but would be implemented in the program.

This README.md provides a brief overview of the Info Day Shooting Game - Christmas Cookies program, its purpose, progress, techniques used, and how to play the game. It also explains the code in detail, highlighting key classes and functions. For more information and a comprehensive understanding of the game, please refer to the source code file `infoDay.py`.

### Reset

The `src/reset.py` file is a Python script that is used to reset the high score in the game. It utilizes the `shelve` module to store and retrieve data from a persistent dictionary-like object.

The script then uses the `shelve.open()` function to open the file named "src/file" in shelf mode. The shelf file acts as a persistent dictionary where data can be stored and retrieved.

```python
with shelve.open("src/file") as d:
```

Within the context of the `shelve` object, the script assigns a new value to the key 'tScore'. The value assigned is a list of lists, representing the high scores in the game. Each inner list contains the name of a player and their corresponding score.

```python
    d['tScore'] = [["TL", 5], ["TL Too", 4], ["TL also", 3], ["TL Junior", 2], ["TL Junior 2", 1]]
```

Finally, the `close()` method is called on the `shelve` object to ensure that any changes made are saved and the file is properly closed.

```python
    d.close()
```

## Acknowledgements
This program was developed by Li Tsz Kiu (Kiu-Q) as part of the Ho Fung College Info Day event. Special thanks to the contributors and libraries used in this project.

Image by <a href="https://www.freepik.com/free-vector/flat-christmas-background_31962849.htm#from_view=detail_collection#position=23">Freepik</a>

Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=83946">Pixabay</a>

## License
This project is licensed under the MIT License. See the `LICENSE.md` file for more details.