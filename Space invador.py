import turtle
import math
import os
import random
import platform

# If on Windows, you import windsound, or better yet, just use Linux
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound module not available")



#Set up the screen.
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("space Invador")
wn.bgpic("space_invaders_background.gif")
wn.tracer(0) # make the animation faster and shut down the updating.

#Register the shape
wn.register_shape("player.gif")
wn.register_shape("invader.gif")

##Draw border.
border_pen=turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup() #Drawing state, pull the pen up
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(30) # the size of pen


for side in range(4):
    border_pen.fd(600) # forward 600 is the distance ??
    border_pen.lt(90)  # 90 is the angle , turn the turtle left by angle units.
border_pen.hideturtle() # Make the turtle invisible ????

# Create the scoring
score= 0

score_pen=turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,260)
scorestring ="Score:{}".format(score)
score_pen.hideturtle()



#Create the player turtle
player= turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)


#set up the speed.
player.speed = 1

# Choose a number of enemies
number_of_enemies = 30
# Create an empty list of emnemies
enemies = []
#Add enemies to the list
for i in range(number_of_enemies):
    # Create the enemy
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number  = 0

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x +(50*enemy_number)
    y = enemy_start_y
    enemy_number += 1

    if enemy_number == 10:
        enemy_start_y -= 30
        enemy_number   = 0

    enemy.setposition(x,y)


enemyspeed = 1


#Create the player bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed = 5

#Define bullet state
#ready - ready to fire
#fire - bullet is firing
bulletstate = "ready"

#Move the player left and right
def move_left():
    player.speed = -5

def move_right():
    player.speed = 5

def move_player():
    x = player.xcor()
    x += player.speed
    if x< -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    #Declare bulletstate as a global if it needs changed.
    global bulletstate
    if bulletstate == "ready":
        play_sound("laser.wav") #Using a AF player.
        bulletstate = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()


def isCollision (t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True
    else:
        return False


def play_sound(sound_file, time = 0):
    if platform.system() == "Windows":
        winsound.Playsound(sound_file, winsound.SND_ASYNC) #SND_ASYNC has same effect as the ampersand & on linux or Mac.
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    else:
        os.system("afplay {}&".format(sound_file))
    # Repeat sound
    if time > 0:
        wn.ontimer(lambda: play_sound(sound_file, time), t=int(time*1000))




#Create keyboard bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Play background music
play_sound("bgm.mp3",119) # play 119 seconds.
#http://www.orangefreesounds.com/cinematic-electronic-track/

#Main game loop
while True:
    wn.tracer(20)
    move_player()
    for enemy in enemies:
        #Move the enemy
        x = enemy.xcor()
        #print("x's initial position", x)
        x += enemyspeed
        #print("x is changing to be:", x)
        enemy.setx(x)
        #print("x's position is:",enemy.xcor())
        # print("the enemy is located:",enemy.xcor())
        #Move the enemy back and down
        if enemy.xcor() > 280:
            # Move all enemies
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction.
            enemyspeed *= -1

        if enemy.xcor() < -280:
            # Move all enemies
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction.
            enemyspeed *= -1

        # Check the collision between the bullet and the enemy.
        if isCollision(bullet, enemy): #This is the function from the upper.
            play_sound("explosion.wav")
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0,-400)
            #Reset the enemy
            enemy.setposition(0,5000)
            # Updating the score
            score +=10
            scorestring ="Score:{}".format(score)
            score_pen.clear() #防止数字覆盖在一起。
            score_pen.write(scorestring, False, align="left", font=("Arial",14))


        # Check the collision between the player and the enemy.
        if isCollision(player, enemy):
            play_sound("explosion.wav")
            # Reset the player

            player.hideturtle()
            enemy.hideturtle()
            print("gameover")
            break

    #Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate ="ready"





#delay=raw_input("press enter to finish.")




