import pygame as pg
vec2 = pg.math.Vector2
# define some colors (R, G, B)
white = (255, 255, 255)
black = (0, 0, 0)
lightblack = (40, 40, 40)
lightblackxred = (50, 40, 40)
green = (0, 255, 0)
red = (255, 0, 0)
purp = (128, 0, 128)
yellow = (255, 255, 0)

# game settings
width = 704
hight = 640
fps = 26
title = 'LAW chapter -'
icon = pg.image.load('YO.png')
bgcolour = lightblackxred

tilesize = 32
gw = width / tilesize
gh = hight / tilesize

wallsprite = 'wallboi.png'
barriersprite = 'barriar.png'
helsprite = 'health.png'
manasprite = 'mana.png'

#mob settings
slimelow = 'slimelow.png'
slime = 'slime.png'
slimehigh = 'slimehigh.png'
slspeed = 100
slnspeed = 125
shspeed = 150
slhealth = 100
shealth = 125
shhealth = 150

shitblox = pg.Rect(0,0,32,32)
mobkb = 20
mobdamage = 5
mobar = 30

# Player settings
pspeed = 250

playerhealth = 100
playerrot = 200

hitblox = pg.Rect(0,0,35,35)

man = 'man.png'
stealthman = 'stealth.png'
gunman = 'shooting.png'
playerdude = man
spriteedge = vec2(40, 1)
hitbloximg = 'hitblox.png'

# player attack settings

srate = 2000
slife = 500
sspeed= 500
shunt = 'shunt.png'

magic = 'bullet0.png'
fire = 'bullet1.png'
poison = 'bullet2.png'
ice = 'bullet3.png'
bullet = magic
bspeed = 500
blife = 1000
brate = 100
bdamage = 10

mana = 100
stale = 500

# player skin selection
'''if keys[pg.K_x] or keys[pg.K_u]:
    self.playerdude = playerstealthman
elif keys[pg.K_c] or keys[pg.K_i]:
    self.playerdude = playergunman
else:
    self.playerdude = playerman'''
