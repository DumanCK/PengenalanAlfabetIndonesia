import pygame
import random
import sys
import sounddevice as sd
from scipy.io.wavfile import write
import librosa
from dtw import dtw
from numpy.linalg import norm
import numpy as np
from pygame.locals import *

def pilihHuruf(huruf):
    index = random.randint(0,25)
    tampil = huruf[index]
    #path untuk soal
    soalpath = './SOAL/'
    soal = soalpath + tampil + '.wav'
    return tampil, soal

def cekBenar(tampil):
    benar = False
    jawaban1 = './JAWABAN/' + tampil + '1.wav'
    jawaban2 = './JAWABAN/' + tampil + '2.wav'
    jawaban3 = './JAWABAN/' + tampil + '3.wav'
    #kalau benar maka benar = true
    #dicek menggunakan mfcc dan dtw
    fs = 44100  # Sample rate
    seconds = 2  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file  

    y1, sr1 = librosa.load('./output.wav')
    y2, sr2 = librosa.load(jawaban1)
    y3, sr3 = librosa.load(jawaban2)
    y4, sr4 = librosa.load(jawaban3)
    mfcc1 = librosa.feature.mfcc(y1, sr1)
    mfcc2 = librosa.feature.mfcc(y2, sr2)
    mfcc3 = librosa.feature.mfcc(y3, sr3)
    mfcc4 = librosa.feature.mfcc(y4, sr4)
    x = mfcc1.T
    y = mfcc2.T
    manhattan_distance = lambda x, y: np.abs(x - y)
    dist1, cost1, acc_cost1, path1 = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))
    y = mfcc3.T
    dist2, cost2, acc_cost2, path2 = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))
    y = mfcc4.T
    #x, y: norm(x - y, ord=1)
    dist3, cost3, acc_cost3, path3 = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))

    print(dist1)
    print(dist2)
    print(dist3)
       
    dist = min(dist1,dist2,dist3)

    #kalau jarak ke contoh jawaban <= 200 maka benar
    if dist < 40000 :
        benar = True
    else:
        benar = False
    print(benar)
    return benar

X = 800
Y = 600

screen = pygame.display.set_mode([800, 600])
height = pygame.display.Info().current_h
width = pygame.display.Info().current_w
pygame.display.set_caption('Window Caption')
clock = pygame.time.Clock()


#create the locations of the stars for when we animate the background
star_field_slow = []
star_field_medium = []
star_field_fast = []

for slow_stars in range(50):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_slow.append([star_loc_x, star_loc_y])

for medium_stars in range(35):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_medium.append([star_loc_x, star_loc_y])

for fast_stars in range(15):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_fast.append([star_loc_x, star_loc_y])

#define some commonly used colours
WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

huruf = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#huruf = ['A','B','C']
#colorsForText = [WHITE,RED,GREEN,BLUE,YELLOW,MAGENTA,CYAN]
#backgroundForText = [BLACK,BLACK,BLUE,YELLOW,BLUE,BLACK,BLACK]

#create the window
pygame.init()
pygame.mixer.init()
app_is_alive = True


intro = pygame.mixer.Sound('./MISC/intro.wav')
intro.play(-1)


i = 0

# create a font object. 
# 1st parameter is the font file 
# which is present in pygame. 
# 2nd parameter is size of the font 
font = pygame.font.Font('freesansbold.ttf', 96)
font2 = pygame.font.Font('freesansbold.ttf', 16)
# create a text suface object, 
# on which text is drawn on it. 
text = font.render(' '+'BERMAIN'+' ', True, GREEN, BLUE)
text2 = font2.render('Tekan spasi untuk soal dan enter untuk menjawab', True, YELLOW, BLACK)  
# create a rectangular object for the 
# text surface object 
textRect = text.get_rect()  
textRect2 = text2.get_rect()  
# set the center of the rectangular object. 
textRect.center = (X // 2, Y // 2)
textRect2.center = (X // 2, 100)


while app_is_alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exiting... All hail the void!")
            app_is_alive = False #exit!
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Exiting... All hail the void!")
            app_is_alive = False #exit!

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] :
        tampil, soal = pilihHuruf(huruf)
        intro.stop()
        petunjuk = pygame.mixer.Sound('./MISC/ayoulangi.wav')
        petunjuk.play()
        textRect = text.get_rect()        
        text = font.render(' '+tampil+' ', True, GREEN, BLUE)
        textRect.center = (X // 2, Y // 2)
        petunjuk.stop()
        pygame.mixer.music.load(soal)
        pygame.mixer.music.play()
        
    #backgroud
    screen.fill(BLACK)
    
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)

    #animate stars
    for star in star_field_slow:
        star[1] += 1
        if star[1] > height:
            star[0] = random.randrange(0, width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, DARKGREY, star, 3)

    for star in star_field_medium:
        star[1] += 4
        if star[1] > height:
            star[0] = random.randrange(0, width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, LIGHTGREY, star, 2)

    for star in star_field_fast:
        star[1] += 8
        if star[1] > height:
            star[0] = random.randrange(0, width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, YELLOW, star, 1)
    
    #redraw everything we've asked pygame to draw
    pygame.display.flip()

    if keys[pygame.K_RETURN] :
        benar = cekBenar(tampil)
                    
        if benar:
            pygame.mixer.music.load('./MISC/tepat.wav')
            pygame.mixer.music.play(1)
        else:
            pygame.mixer.music.load('./MISC/cobalagi.wav')
            pygame.mixer.music.play(1)
    
    #set frames per second
    clock.tick(30)

        

#quit gracefully
pygame.quit()
