from tkinter import *
import random, time, json

GAME_W = 800
GAME_H = 600
SPEED = 150
SPACE_SIZE = 25
BODY = 3
BODY_COLOR = "green"
HEAD_COLOR = "yellow"
FOOD_COLOR = "red"
OBSTACLE_COUNT = 5
OBSTACLE_COLOR = "gray"
BACKGROUND_COLOR = "black"
TIME_LIMIT = 10

class Snake:
    def __init__(self):
        self.body_size = BODY
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY):
            self.coordinates.append([0, 0])

        for index, (x, y) in enumerate(self.coordinates):
            color = HEAD_COLOR if index == 0 else BODY_COLOR
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        self.coordinates = self.generate_food_position()
        self.food_item = canvas.create_oval(self.coordinates[0], self.coordinates[1], 
                           self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE, 
                           fill=FOOD_COLOR, tag="food")

    def generate_food_position(self):
        while True:
            x = random.randint(0, (GAME_W // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_H // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in obstacles.coordinates and [x, y] not in snake.coordinates and 0 <= x < GAME_W and 0 <= y < GAME_H:
                return [x, y]
            else:
                continue

class Obstacle:
    def __init__(self):
        self.coordinates = []
        for _ in range(OBSTACLE_COUNT):
            while True:
                x = random.randint(0, (GAME_W // SPACE_SIZE) - 1) * SPACE_SIZE
                y = random.randint(0, (GAME_H // SPACE_SIZE) - 1) * SPACE_SIZE
                if [x, y] not in self.coordinates:
                    self.coordinates.append([x, y])
                    canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")
                    break

def show_main_menu():
    canvas.delete(ALL)
    canvas.create_text(GAME_W / 2, GAME_H / 5, font=("consolas", 50), text="SNAKE GAME", fill="white")

    play_button.place(relx=0.5, rely=0.5, anchor="center")
    exit_button.place(relx=0.5, rely=0.6, anchor="center")

def start_game():
    global start_time, score, lives, direction, obstacles, snake, foods

    play_button.place_forget()
    exit_button.place_forget()

    score = 0
    lives = 3
    direction = "right"
    start_time = time.time()

    canvas.delete(ALL)
    update_label_text()

    obstacles = Obstacle()
    snake = Snake()
    foods = [Food(), Food(), Food()]

    next_round(snake, foods)

def exit_game():
    root.destroy()

def next_round(snake, foods):
    global score, SPEED, time_left, TIME_LIMIT, times, max_length

    time_pass = time.time() - start_time
    time_left = max(0, TIME_LIMIT + times - int(time_pass))

    if time_left == 0:
        gameover()
        return

    if len(snake.coordinates) > max_length:
        max_length = len(snake.coordinates)
        save_max_length(max_length)

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    if check_collision(snake, x, y):
        gameover()
        return

    snake.coordinates.insert(0, [x, y])
    
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=HEAD_COLOR)
    snake.squares.insert(0, square)
    canvas.itemconfig(snake.squares[1], fill=BODY_COLOR)

    food_eaten = False
    for food in foods:
        if x == food.coordinates[0] and y == food.coordinates[1]:
            score += 1
            times += 3
            if score % 5 == 0:
                SPEED = max(50, SPEED - 10)
            canvas.delete(food.food_item)
            food.coordinates = food.generate_food_position()
            food.food_item = canvas.create_oval(food.coordinates[0], food.coordinates[1], 
                            food.coordinates[0] + SPACE_SIZE, food.coordinates[1] + SPACE_SIZE, 
                            fill=FOOD_COLOR, tag="food")
            food_eaten = True
            break
    if not food_eaten:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    update_label_text()
   
    root.after(SPEED, next_round, snake, foods)

def check_collision(snake, x, y):
    if x < 0 or x >= GAME_W or y < 0 or y >= GAME_H:
        return True
    if [x, y] in snake.coordinates[1:] or [x, y] in obstacles.coordinates:
        return True
    return False

def gameover():
    global lives, high_score, time_left

    lives -= 1

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    update_label_text()
    root.update()

    if lives > 0:
        restart_game()
    else:
        canvas.delete(ALL)
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 5, font=("consolas", 70), text="GAME OVER", fill="red", tag="GAME OVER")
               
        restart_button.place(relx=0.5, rely=0.5, anchor="center")
        main_menu_button.place(relx=0.5, rely=0.6, anchor="center") 

def go_to_main_menu():
    global high_score, times

    restart_button.place_forget()
    main_menu_button.place_forget()

    global score, high_score, lives, SPEED, start_time, snake, direction, TIME_LIMIT

    score = 0
    lives = 3
    SPEED = 150
    TIME_LIMIT = 10
    times = 0
    start_time = time.time()
    direction = "right"

    label.config(text=f"Highest Score: {high_score} | Max Length: {max_length}")
    show_main_menu()

def check_direction(new_direction):
    global direction
    opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}
    if new_direction != opposites.get(direction, ""):
        direction = new_direction

def restart_game():
    global snake, direction, time_left, start_time, times

    for square in snake.squares:
        canvas.delete(square)

    snake = Snake()

    time_pass = time.time() - start_time
    time_left = max(0, TIME_LIMIT + times - int(time_pass))
    direction = "right"

    update_label_text()

    next_round(snake, foods)

def reset_game():
    global score, high_score, lives, SPEED, start_time, snake, direction, TIME_LIMIT, times

    score = 0
    lives = 3
    SPEED = 150
    TIME_LIMIT = 10
    start_time = time.time()
    direction = "right"
    times = 0

    canvas.delete(ALL)

    restart_button.place_forget()
    main_menu_button.place_forget()

    global obstacles
    obstacles = Obstacle()

    snake = Snake()

    global foods
    food1, food2, food3 = Food(), Food(), Food()
    foods = [food1, food2, food3]

    update_label_text()

    next_round(snake, foods)

def update_label_font():
    font_size = int(GAME_W / 50)
    label.config(font=('consolas', font_size))

def update_label_text():
    global time_left

    time_pass = time.time() - start_time
    time_left = max(0, TIME_LIMIT + times - int(time_pass))

    display_speed = 200 - SPEED

    label.config(text=f"Score: {score} |Length: {len(snake.coordinates)} | Speed: {display_speed} | Time Left: {time_left} | Lives: {lives}")
    update_label_font()

def load_high_score():
    try:
        with open("high_score.json", "r") as file:
            data = json.load(file)
            return data.get("high_score", 0)
    except FileNotFoundError:
        return 0
    
def save_high_score(score):
    with open("high_score.json", "w") as file:
        json.dump({"high_score": score}, file)

def load_max_length():
    try:
        with open("max_length.json", "r") as file:
            data = json.load(file)
            return data.get("max_length", BODY)
    except FileNotFoundError:
        return BODY

def save_max_length(length):
    with open("max_length.json", "w") as file:
        json.dump({"max_length": length}, file)

root = Tk()
root.title("Snake Game")
root.resizable(False, False)

direction = 'right'
score = 0
start_time = time.time()
time_left = 0
times = 0
high_score = load_high_score()
max_length = load_max_length()
lives = 3

label = Label(root, text=f"Highest Score: {high_score} | Max Length: {max_length}", font=('consolas', 25))
label.pack()
update_label_font()

canvas = Canvas(root, bg=BACKGROUND_COLOR, width=GAME_W, height=GAME_H)
canvas.pack()

restart_button = Button(root, text="Restart", font=('consolas', 20), command=reset_game)
restart_button.pack()
restart_button.place(relx=0.5, rely=0.5, anchor="center")
restart_button.place_forget()

main_menu_button = Button(root, text="Main Menu", font=('consolas', 20), command=go_to_main_menu)
main_menu_button.place_forget()

root.update()

win_w = root.winfo_width()
win_h = root.winfo_height()
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

x = int((screen_w / 2) - (win_w // 2))
y = int((screen_h / 2) - (win_h // 2))
root.geometry(f"{win_w}x{win_h}+{x}+{y}")

root.bind("<Left>", lambda event: check_direction("left"))
root.bind("<Right>", lambda event: check_direction("right"))
root.bind("<Up>", lambda event: check_direction("up"))
root.bind("<Down>", lambda event: check_direction("down"))

obstacles = Obstacle()
snake = Snake()

food1 = Food()
food2 = Food()
food3 = Food()
foods = [food1, food2, food3]

play_button = Button(root, text="Play", font=("consolas", 20), command=start_game)
exit_button = Button(root, text="Exit", font=("consolas", 20), command=exit_game)

show_main_menu()
root.mainloop()