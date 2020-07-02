import turtle
import os
import math
import random
import platform

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
wn.register_shape("Invader.gif")
wn.register_shape("Invader.yellow.gif")
wn.register_shape("Invader.red.gif")
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
number_of_enemies = 20

# Create an empty list of enemies
enemies = []

# enemy wave direction. Create list of 1's of length three
enemy_wave_dir = [1] * 3
enemy_wave_dir[0] = 1
enemy_wave_dir[1] = 1


# Add enemies to the list
for i in range(number_of_enemies):
# Create the enemy  
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0

for enemy in enemies:
    enemy.color("green")
    enemy.shape("Invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y 
    enemy.setposition(x, y)
    # Update the enemy number
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 0.2

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

bulletspeed = 7

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

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        #x += enemyspeed
        enemy_dir = enemy_wave_dir[0]
        if enemy.color() == ('yellow', 'yellow'):
            x += 0.2
            enemy_dir = enemy_wave_dir[1]
        elif enemy.color() == ('red', 'red'):
            x += 0.2
            enemy_dir = enemy_wave_dir[2]
        x += enemy_dir    
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 280:
            # Move all enemies down
            for e in enemies:
                if e.color() == enemy.color():
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
            # Change enemy direction    
            # enemyspeed *= -1
            if enemy.color() == ('yellow', 'yellow'):
                enemy_wave_dir[1] *= -1
            elif enemy.color() == ('red', 'red'):
                enemy_wave_dir[2] *= -1 
            else:
                enemy_wave_dir[0] *= -1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemies:
                if e.color() == enemy.color():
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
            # Change enemy direction
            # enemyspeed *= -1
            if enemy.color() == ('yellow', 'yellow'):
                enemy_wave_dir[1] *= -1
            elif enemy.color() == ('red', 'red'):
                enemy_wave_dir[2] *= -1 
            else:
                enemy_wave_dir[0] *= -1

        # Check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            play_sound("explosion.wav")
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)

            # Reset the enemy
            enemy.setposition(0, 10000)

            # Update the score
            score += 10
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align = "left", font = ("Courier", 14, "normal"))

            high_score += 10
            scorestring = "High Score: {}".format(score)
            high_score_pen.clear()
            high_score_pen.write(scorestring, False, align = "right", font = ("Courier", 14, "normal"))

            # Adding yellow enemies
            if score == 80:
                enemy_number = 0
                enemy_start_x = -225
                enemy_start_y = 250
                for i in range(20):
                    an_enemy = turtle.Turtle()
                    an_enemy.color("yellow")
                    an_enemy.shape("Invader.yellow.gif")
                    an_enemy.penup()
                    an_enemy.speed(0)
                    x = enemy_start_x + (50 * enemy_number)
                    y = enemy_start_y 
                    an_enemy.setposition(x, y)
                    # Update the enemy number
                    enemy_number += 1
                    if enemy_number == 10:
                        enemy_start_y -= 50
                        enemy_number = 0
                    enemies.append(an_enemy)

            # Adding red enemies
            if score == 180:
                enemy_number = 0
                enemy_start_x = -225
                enemy_start_y = 250
                for i in range(20):
                    an_enemy = turtle.Turtle()
                    an_enemy.color("red")
                    an_enemy.shape("Invader.red.gif")
                    an_enemy.penup()
                    an_enemy.speed(0)
                    x = enemy_start_x + (50 * enemy_number)
                    y = enemy_start_y 
                    an_enemy.setposition(x, y)
                    # Update the enemy number
                    enemy_number += 1
                    if enemy_number == 10:
                        enemy_start_y -= 50
                        enemy_number = 0
                    enemies.append(an_enemy)
            
        if isCollision(player, enemy):
            play_sound("explosion.wav")
            player.hideturtle()
            enemy.hideturtle()

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"