import sys
from os import path
from sprites import *
from tilemap import *

#HUD creation
def drawHUD(surf, x, y, pct, bl, bh, olc):
    if pct < 0:
        pct = 0
    barlen = bl
    barh = bh
    fill = pct * barlen
    outline = pg.Rect(x, y, barlen, barh)
    fillr = pg.Rect(x, y, fill, barh)
    if pct == 1.02:
        col = black
        fill = barlen
        outline = pg.Rect(x, y, barlen, barh)
        fillr = pg.Rect(x, y, fill, barh)
    elif pct > 0.6:
        col = green
    elif pct > 0.3:
        col = yellow
    else:
        col = red
    pg.draw.rect(surf, col, fillr)
    pg.draw.rect(surf, olc, outline, 2)


class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((width, hight))
        pg.display.set_caption(title)
        pg.display.set_icon(icon)
        self.clock = pg.time.Clock()
        self.load()
        self.mana = mana

    def load(self):
        # loading image data for textures
        file = path.dirname(__file__)
        grapics = path.join(file, 'images')

        # loading of map data to the code
        self.map = Map(path.join(file, 'map2.txt'))
        self.playerimg = pg.image.load(path.join(grapics,playerdude)).convert_alpha()
        self.hitbloximg = pg.image.load(path.join(grapics,hitbloximg)).convert_alpha()
        self.shuntimg = pg.image.load(path.join(grapics,shunt)).convert_alpha()
        self.slimelowimg = pg.image.load(path.join(grapics, slimelow)).convert_alpha()
        self.slimeimg = pg.image.load(path.join(grapics, slime)).convert_alpha()
        self.slimehighimg = pg.image.load(path.join(grapics, slimehigh)).convert_alpha()
        self.bulletimg = pg.image.load(path.join(grapics, bullet)).convert_alpha()
        self.wallimg = pg.image.load(path.join(grapics,wallsprite)).convert_alpha()
        self.barrierimg = pg.image.load(path.join(grapics,barriersprite)).convert_alpha()
        self.manaimg = pg.image.load(path.join(grapics,manasprite)).convert_alpha()
        self.healthimg = pg.image.load(path.join(grapics,helsprite)).convert_alpha()
        self.titlefont = path.join(grapics, '8-BIT WONDER.TTF')

    def new(self):
        # initialisation of all new game objects
        self.allsprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.barrier = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.shunt = pg.sprite.Group()
        self.mpickups = pg.sprite.Group()
        self.hpickups = pg.sprite.Group()
        self.winbox = pg.sprite.Group()
        # map creation
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == '2':
                    barrier(self, col, row)
                if tile == 'm':
                    manabox(self, col, row)
                if tile == 'h':
                    healbox(self, col, row)
                if tile == 'w':
                    winbox(self, col, row)
                if tile == 's':
                    mob(self, col, row,'s')
                if tile == 'e':
                    mob(self, col, row, 'e')
                if tile == 'S':
                    mob(self, col, row, 'S')
                if tile == 'P':
                    self.player = player(self, col, row)
        # brings the cam functin into the main py file
        self.cam = cam(self.map.width, self.map.height)

    def run(self):
        # game loop (self.playing = False to end game loop)
        self.playing = True
        # game loop
        while self.playing:
            self.dt = self.clock.tick(fps) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        # quit functions for ease
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.allsprites.update()  # updates all gameplay sprites
        self.cam.update(self.player)  # updates the camera position based on sprite
        # mob/player inteaction
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)#, self.player.rectimg)
        for hit in hits:
            self.player.health -= mobdamage
            hit.vel = vec2(0, 0)
            if self.player.health <= 0:
                self.playing = False

        # mob deaths
        if hits:
            self.player.pos += vec2(mobkb, 0).rotate(-hits[0].rot)
            # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= bdamage
            hit.vel = vec2(0, 0)

        hits = pg.sprite.spritecollide(self.player, self.hpickups, False)
        for hit in hits:
            if self.player.health <= 100:
                self.player.health += 25
                hit.kill()
                if self.player.health > 100:
                    self.player.health = 100

        hits = pg.sprite.spritecollide(self.player, self.mpickups, False)
        for hit in hits:
            if self.player.mana <= 100:
                self.player.mana += 25
                hit.kill()
                if self.player.mana > 100:
                    self.player.mana = 100

        hits = pg.sprite.spritecollide(self.player, self.mpickups, False)
        for hit in hits:
            if self.player.mana <= 100:
                self.player.mana += 25
                hit.kill()
                if self.player.mana > 100:
                    self.player.mana = 100

        hits = pg.sprite.spritecollide(self.player, self.winbox, False)
        for hit in hits:
            self.win()

    def grid(self):
        # dev tool (will be deactivated for final code)
        for x in range(0, width, tilesize):
            pg.draw.line(self.screen, lightblack, (x, 0), (x, hight))
        for y in range(0, hight, tilesize):
            pg.draw.line(self.screen, lightblack, (0, y), (width, y))
        pass

    def draw(self):
        # draws all sprites to be displayed
        self.screen.fill(bgcolour)
        #self.grid()
        #pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        for sprite in self.allsprites:
            if isinstance(sprite,mob):
                sprite.healthbar()
            self.screen.blit(sprite.image, self.cam.apply(sprite))
        # HUD functions
        drawHUD(self.screen, 9, 9, 1.02, 500, 52, white)
        drawHUD(self.screen, 10, 10, self.player.health / playerhealth, 500, 40, green)
        drawHUD(self.screen, 10, 50, self.player.mana / mana, 500, 10, purp)
        # displays all drawn spirits and updates every game tick
        pg.display.flip()

    def events(self):
        # all non player specific events ar kept here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def start(self):
        self.screen.fill(black)
        self.draw_text("NEW GAME", self.titlefont, 75, red, width / 2, hight / 4, align="center")
        self.draw_text("use the arrow keys or wasd to move", self.titlefont, 20, white, width / 2, hight * 3 / 4, align="center")
        self.draw_text("shoot with x or u", self.titlefont, 25, white, width / 2, hight * 3 / 4 + 25, align="center")
        self.draw_text("dash with c or i", self.titlefont, 25, white, width / 2, hight * 3 / 4 + 50, align="center")
        self.draw_text("press any key to start", self.titlefont, 25, white, width / 2, hight * 3 / 4 + 75, align="center")
        pg.display.flip()
        self.waitkey()
        gameloop()

    def gameover(self):
        self.screen.fill(black)
        self.draw_text("GAME OVER", self.titlefont, 75, red, width / 2, hight / 2, align="center")
        self.draw_text("Press any key to play again", self.titlefont, 25, white, width / 2, hight * 3 / 4, align="center")
        pg.display.flip()
        self.waitkey()

    def win (self):
        self.screen.fill(black)
        self.draw_text("YOU WON", self.titlefont, 75, red, width / 2, hight / 2, align="center")
        self.draw_text("good job", self.titlefont, 25, white, width / 2, hight * 3 / 4, align="center")
        self.draw_text("Press any key to play again", self.titlefont, 25, white, width / 2, hight * 3 / 4 + 25, align="center")
        pg.display.flip()
        self.waitkey()
        self.start()

    def waitkey(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

def gameloop():
    # create the game object
    g = game()
    while True:
        g.new()
        g.run()
        if len(g.mobs) == 0:
            g.win()
        g.gameover()

g = game()
g.start()
