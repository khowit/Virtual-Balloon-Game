from threading import Timer
import pygame
import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
import time

pygame.init()

Width, Height = 900, 600

windown = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Balloon Pop Games')

fps = 30
clock = pygame.time.Clock()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

imgBalloon = pygame.image.load('image/balloon3.png').convert_alpha()
rectBalloon = imgBalloon.get_rect()
rectBalloon.x, rectBalloon.y = 300, 400

speed = 15
score = 0
startTime = time.time()
totalTime = 15

detector = HandDetector(detectionCon=0.8, maxHands=1)

def resetBalloon():
    rectBalloon.x = random.randint(100, img.shape[1] - 300)
    rectBalloon.y = img.shape[0] + 50 

start = True
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    timeRemain = int(totalTime - (time.time() - startTime))
    if timeRemain < 0:
        windown.fill((255,255,255)) 

        font = pygame.font.Font("image/Marcellus-Regular.ttf",60)
        text = font.render(f'Your Score : {score}', True, (50,50,255))
        textTime = font.render(f'Time Up', True, (50,50,255))
        windown.blit(textTime, (360, 200))
        windown.blit(text, (255, 270))
        
    
    else:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        allHands, img = detector.findHands(img)

        rectBalloon.y -= speed
        if rectBalloon.y < 0:
            resetBalloon()
            speed += 1
            

        if allHands:
            hand = allHands[0]
            x, y = hand['lmList'][8]
            if rectBalloon.collidepoint(x,y):
                resetBalloon() 
                score += 10
                speed += 1


        imgBGR = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgBGR = np.rot90(imgBGR)
        frame = pygame.surfarray.make_surface(imgBGR).convert()
        frame = pygame.transform.flip(frame, True, False)
        windown.blit(frame, (0,0))
        # windown.fill((255,255,255))
        # rectBalloon.x += 5

        # windown.blit(imgBackground, (0,0))
        # # pygame.draw.rect(windown, (0,255,0), rectBalloon)
        # pygame.draw.rect(windown, (0,255,0), recNew)
        windown.blit(imgBalloon,rectBalloon)

        font = pygame.font.Font("image/Marcellus-Regular.ttf",50)
        text = font.render(f'Score : {score}', True, (255,50,50))
        textTime = font.render(f'Time : {timeRemain}', True, (255,50,50))
        windown.blit(text,(20,10))
        windown.blit(textTime,(700,10))

    # red, green, blue = (255,0,0), (0,255,0), (0,0,255)
    # pygame.draw.polygon(windown, red, ((291,50), (588,50), (737,307), (588,564), (291,564), (131,307)))
    # pygame.draw.circle(windown, green, (440,320),200)
    # pygame.draw.line(windown, blue,(291,307), (588,307), 10)
    

    pygame.display.update()
    clock.tick(fps)