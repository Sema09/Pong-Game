"""
Created by Zeynep ÖZDEMİR, ÖZGE MERCANOĞLU SİNCAN
"""
from graphics import *
import random
import math

# Do not change these following 4 variables
margin = 10 # height of the paddle from the ground
moveIncrement = 15 # paddle movement
ballRadius = 15
BOUNCE_WAIT= 1200

BALL_COUNT = 1  # If we change this, the number of ball changes!

class Timer:
    def __init__(self):
        self.value = 0


class Paddle:

    def __init__(self, color, width, height, coordx, win):
        self.color = color
        self.width = width
        self.height = height
        self.x = coordx
        self.shape = Rectangle(Point(self.x - int(self.width / 2), win.getHeight() - margin - self.height),
                               Point(self.x + int(self.width / 2), win.getHeight() - margin))
        self.shape.setFill(self.color)
        self.window = win
        self.shape.draw(self.window)

    def move_left(self):   # move paddle to the left by the amount of global variable moveIncrement
        if self.x - int(self.width/2)<=0:
            pass
        else:
            self.x -= moveIncrement
            self.shape.move(-moveIncrement, 0)
        return self.x


    def move_right(self):  # move paddle to the right by the amount of global variable moveIncrement
        if self.x + int(self.width/2)>=300:
            pass
        else:
            self.x += moveIncrement
            self.shape.move(moveIncrement, 0)
        return self.x


class Bubbles:
    def __init__(self,win,lis,lis2):
        self.win=win
        self.lis=lis
        self.lis2=lis2
        for p in range(30, 271, 60):
            z = Circle(Point(p, 30), 30)
            z.setFill("purple")
            z.draw(self.win)
            self.lis.append(z)
            self.lis2.append(z)
        for t in range(30, 271, 60):
            y = Circle(Point(t, 90), 30)
            y.setFill("yellow")
            y.draw(self.win)
            self.lis.append(y)
            self.lis2.append(y)
        for m in range(30, 271, 60):
            r = Circle(Point(m, 150), 30)
            r.setFill("gray")
            r.draw(self.win)
            self.lis.append(r)
            self.lis2.append(r)
    def calculate(self,cordx,cordy,rad):
        self.cordx=cordx
        self.cordy=cordy
        self.rad=rad
        for i in self.lis2:
            z = i
            d = z.getRadius()
            a=z.getCenter()
            b = a.getX()
            c = a.getY()
            if (((self.cordx-b)**2+(self.cordy-c)**2)**(1/2))==(d+self.rad) or (((self.cordx-b)**2+(self.cordy-c)**2)**(1/2))==abs(d-self.rad) or (((self.cordx-b)**2+(self.cordy-c)**2)**(1/2))<(d+self.rad):
                self.lis2.remove(z)
                z.undraw()



class Ball:

    def __init__(self, coordx, coordy, color, radius, x_direction, speed, win):
        self.shape = Circle(Point(coordx, coordy), radius)
        self.x = coordx
        self.y = coordy
        self.xMovement = 0 # Current x movement
        self.yMovement = 0 # Current y movement
        self.color = color
        self.window = win
        self.shape.setFill(self.color)
        self.shape.draw(self.window)
        self.radius = radius
        self.timer = 0
        self.x_direction = x_direction   # Initial x direction. This variable will be 0 or 1. 1:right 0:left
        self.speed = speed

    def is_moving(self):
        if self.xMovement != 0 or self.yMovement !=0:
            return True
        else:
            return False


    def bounce(self, gameTimer, minX, maxX, maxY):
        # Calculating x-axis ball movement and bouncing
        # minX: min x coord. of paddle
        # maxX: max x coord. of paddle
        # maxY: max y coord. at which the ball can be move. If it goes further, it falls to the ground.
        global BOUNCE_WAIT
        gameOver = False

        if gameTimer >= self.timer + BOUNCE_WAIT:
            self.timer = gameTimer
            self.minx=minX
            self.maxx=maxX
            self.maxy=maxY

            if self.x<=self.radius:
                self.xMovement *= -1
            if self.x >=285:
                self.xMovement *= -1
            if self.y<self.radius:
                self.yMovement *= -1
            if self.y>560 and (self.x<self.maxx+self.radius and self.x>self.minx-self.radius):
                self.yMovement *= -1
            if (self.y >= 560) and self.x==self.minx-self.radius:
                self.yMovement *= -1
            if (self.y >=560) and self.x==self.maxx+self.radius:
                self.yMovement *= -1
            else:
                if self.y>self.maxy:
                    gameOver = True



            if self.xMovement == 1 and self.yMovement == 1:
                self.x += self.speed
                self.y += self.speed
            elif self.xMovement == 1 and self.yMovement == -1:
                self.x += self.speed
                self.y -= self.speed
            elif self.xMovement == -1 and self.yMovement==1:
                self.x -= self.speed
                self.y += self.speed
            elif self.xMovement == -1 and self.yMovement==-1:
                self.x -= self.speed
                self.y -= self.speed
            self.shape.move(self.xMovement * self.speed, self.yMovement * self.speed)
            return gameOver

def main():
    win = GraphWin("19290340", 300, 600) # Replace your student id
    lives = 2
    win.setBackground("Black")
    BallList = list()

    while True:
        lis = []
        lis2 = []
        p = Bubbles(win, lis, lis2)
        myPaddle = Paddle("White", 100, 15, 150, win)
        ColorsList = ["Cyan","Red","Green","Yellow"]

        livesCounter = Text(Point(win.getWidth() - int(win.getWidth() / 5), 250), f'Lives -- {lives}')
        livesCounter.setTextColor("Cyan")
        livesCounter.setSize(15)
        livesCounter.draw(win)
        gameTimer = Timer()

        string = Text(Point(150, 300), "")
        st = Text(Point(150, 340), "")
        stri = Text(Point(150, 380), "")
        string.setTextColor("Red")
        string.setSize(25)
        string.draw(win)
        st.setTextColor("Red")
        st.setSize(25)
        st.draw(win)
        stri.setTextColor("Red")
        stri.setSize(15)
        stri.draw(win)

        for i in range(BALL_COUNT):
            rand_speed = random.randint(5, 20) # random speed for ball
            rand_direction = random.randint(0, 1) # This variable will be 0 or 1 randomly.
            ball = Ball(myPaddle.x - int(myPaddle.width/2) + i*30, win.getHeight() - margin - myPaddle.height - ballRadius, ColorsList[i%4] , ballRadius,rand_direction,rand_speed, win)
            BallList.append(ball)
        gameOver = False
        while lives > 0:
            while not gameOver:
                keyPress = win.checkKey()
                if keyPress == 'a':
                    myPaddle.move_left()

                if keyPress == 'd':
                    myPaddle.move_right()

                if keyPress == 'l': # balls will move faster
                    for item in BallList:
                        item.speed += 1

                if keyPress == 'k':  # Balls will move slower. Note that in our case min speed is 2.
                    for item in BallList:
                        if item.speed > 2:
                            item.speed -= 1

                if keyPress == 's':  # Initial movement of balls
                    for item in BallList:
                        if(not item.is_moving()):
                            if item.x_direction == 1:   # it means ball moves to right in x direction
                                item.xMovement = 1
                            else:                   # it means ball moves to left in x direction
                                item.xMovement = -1
                            item.yMovement = -1 # at initial ball moves up in y direction

                gameTimer.value += 1
                for item in BallList:
                    gameOver = item.bounce(gameTimer.value, (myPaddle.x-int(myPaddle.width/2)), (myPaddle.x+int(myPaddle.width/2)), win.getHeight() - margin - myPaddle.height)
                    p.calculate(item.x,item.y,item.radius)
                    if lis2 == []:
                        for item in BallList:
                            item.shape.undraw()
                        myPaddle.shape.undraw()
                        string.setText("GAME OVER")
                        st.setText("YOU WIN!")
                        stri.setText("Press Any Key to Quit")
                        break
                    if gameOver == True:
                        myPaddle.shape.undraw()
                        for i in lis2:
                            i.undraw()
                        for item in BallList:
                            item.shape.undraw()
                        lives -= 1
                        livesCounter.undraw()
                        livesCounter.setText(f'Lives -- {lives}')
                        break
                if gameOver ==True:
                    break
                if lis2 ==[]:
                    break
            if gameOver == True:
                break
            if lis2==[] and gameOver == False:
                break
        if lives==0 and gameOver==True:
            string.setText("GAME OVER")
            st.setText("YOU LOST!")
            stri.setText("Press Any Key to Quit")
            livesCounter = Text(Point(win.getWidth() - int(win.getWidth() / 5), 250), f'Lives -- {lives}')
            livesCounter.setTextColor("Cyan")
            livesCounter.setSize(15)
            livesCounter.draw(win)
            break
        if lis2 == []:
            break
    try:
        win.getKey()
        if win.checkKey():
            win.close()
    except GraphicsError:
        pass

main()



























