import turtle
import os
import math
import random
import platform
import tkinter as tk

MAX_STEPS = 220

# If on Windows, you import winsound, or use Linux
if platform.system() == "windows":
    try:
        import winsound
    except:
        print("Winsound module not available.")

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space_invaders_background.gif")
wn.tracer(0)

# Register the shapes
wn.register_shape("Invader.green.gif")
wn.register_shape("Invader.yellow.gif")
wn.register_shape("Invader.red.gif")
wn.register_shape("Invader.purple.gif")
wn.register_shape("Invader.blue.gif")
wn.register_shape("Invader.pink.gif")
wn.register_shape("Invader.orange.gif")
wn.register_shape("Player.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.forward(600)
    border_pen.left(90)
border_pen.hideturtle()

# Set the score to 0
score = 0
high_score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align = "left", font = ("Courier", 14, "normal"))
score_pen.hideturtle()

high_score_pen = turtle.Turtle()
high_score_pen.speed(0)
high_score_pen.color("white")
high_score_pen.penup()
high_score_pen.setposition(290, 280)
scorestring = "High Score: {}".format(high_score)
high_score_pen.write(scorestring, False, align = "right", font = ("Arial", 14, "normal"))
high_score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("Player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player.speed = 0

# Choose a number of enemies
number_of_enemies = 10

# Create an empty list of enemies
enemies = []

# Enemy wave direction
enemy_wave_dir = []

enemy_wave_moves = []

enemies2 = []

# Create an enemy and add it to list of enemies
def create_enemy_wave(enemies, enemy_wave_dir, enemy_wave_moves, colour):
    enemy_start_x = -280#-225
    enemy_start_y = 250
    enemy_number = 0
    enemy_list = []
    for i in range(10):
        enemy = turtle.Turtle()
        enemy.color(colour)
        enemy.shape("Invader." + colour + '.gif')
        enemy.penup()
        enemy.speed(0)
        x = enemy_start_x + (50 * enemy_number)
        y = enemy_start_y
        enemy.setposition(x, y)
        enemy_number += 1
        enemy_list.append(enemy)
    enemies.append(enemy_list)

    enemy_wave_dir.append(1)
    enemy_wave_moves.append(0)

    return enemies, enemy_wave_dir, enemy_wave_moves
        
enemies2, enemy_wave_dir, enemy_wave_moves = create_enemy_wave(enemies2, enemy_wave_dir, enemy_wave_moves, "green")

enemyspeed = 0.1

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()
bullet.speed
bullet.setposition(0, -250)

bulletspeed = 8

# Define bullet state
# ready - ready to fire 
# fire - bullet is firing
bulletstate = "ready"

# Move the player left and right
def move_left():
    player.speed = -3

def move_right():
    player.speed = 3

def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = - 280
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    # Declare bulletstate as global
    global bulletstate
    if bulletstate == "ready":
        play_sound("laser.wav")
        bulletstate = "fire"
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 20:
        return True
    else:
        return False

def play_sound(sound_file, time = 0):
    # Windows
    if platform.system == "Windows":
        winsound.Playsound(sound_file, winsound.SND_ASYNC)
    # Linux
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    # Mac
    else:
        os.system("afplay {}&".format(sound_file))

    # Repeat sound
    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t = int(time * 1000))


# Create keyboard bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Play background music
# play_sound("background.mp3", 20) #killall afplay in terminal to stop

# Main game loop
while True:
    wn.update()
    move_player()

    # Move enemy
    for i in range(len(enemies2)):
        for enemy in enemies2[i]:
            x = enemy.xcor()

            
            # Speed up the enemies in each wave as theirs numbers decrease
            speed_up = (10 - len(enemies2[i]))
            if speed_up >= 1: speed_up = 0.5

            speed_up = 0

            # Move enemy but account for possible change in direction
            if enemy_wave_dir[i] == 1:
                x += 0.5 + speed_up

            elif enemy_wave_dir[i] == -1:
                x -= 0.5 + speed_up

            enemy.setx(x)
            
            # Change direction

            #if enemy.xcor() > 280:
            if enemy_wave_moves[i] > MAX_STEPS:
                for e in enemies2[i]:
                    e.sety(e.ycor() - 40)
                enemy_wave_dir[i] *= -1

                enemy_wave_moves[i] = 0

            #if enemy.xcor() < -280:
            if enemy_wave_moves[i] < -MAX_STEPS:
                for e in enemies2[i]:
                    e.sety(e.ycor() - 40) 
                enemy_wave_dir[i] *= -1 

                enemy_wave_moves[i] = 0

            if isCollision(player, enemy):
                play_sound("explosion.wav")
                player.hideturtle()
                enemy.hideturtle()
                print ("Game Over")
                break  

        # Increase moves by either 1 or -1 depending on direction
        enemy_wave_moves[i] += enemy_wave_dir[i]

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

        for enemy_list in enemies2:
            for enemy in enemy_list:
                # Check for a collision between the bullet and the enemy
                if isCollision(bullet, enemy):
                    play_sound("explosion.wav")
                    # Reset the bullet
                    bullet.hideturtle()
                    bulletstate = "ready"
                    bullet.setposition(0, -400)

                    # Reset the enemy
                    enemy.clear()
                    enemy.hideturtle()
                    enemy.setposition(0, -1000000)
                    enemy_list.remove(enemy)
                    del enemy

                    # Update the score
                    score += 10
                    scorestring = "Score: {}".format(score)
                    score_pen.clear()
                    score_pen.write(scorestring, False, align = "left", font = ("Courier", 14, "normal"))

                    high_score += 10
                    scorestring = "High Score: {}".format(score)
                    high_score_pen.clear()
                    high_score_pen.write(scorestring, False, align = "right", font = ("Courier", 14, "normal"))

                    # Add new wave when player reaches a score that is a multiple of 50
                    if score % 50 == 0:
                        enemies2, enemy_wave_dir, enemy_wave_moves = create_enemy_wave(enemies2, enemy_wave_dir, enemy_wave_moves, "green")

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

# To Do:
# 1) Spawn different coloured enemies. Perhaps have a list and choose 'next' colour
# 2) Implement 'game over' i.e. when enemy reaches the player's 'ground'
# 3) Implement abiliy to restart game after game over
# 4) Save high score in text file and load it if textfile exists at start of game