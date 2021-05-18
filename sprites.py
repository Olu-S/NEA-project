import pygame as pg
from settings import *
from tilemap import hitbox
vec2 = pg.math.Vector2




def crash(sprite, group, dir):  # entity/environment collision detection and velocity correction to stop clipping
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, hitbox)
        if hits:
            if hits[0].rect.centerx > sprite.hitblox.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hitblox.width / 2
            if hits[0].rect.centerx < sprite.hitblox.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hitblox.width / 2
            sprite.vel.x = 0
            sprite.hitblox.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, hitbox)
        if hits:
            if hits[0].rect.centery > sprite.hitblox.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hitblox.height / 2
            if hits[0].rect.centery < sprite.hitblox.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hitblox.height / 2
            sprite.vel.y = 0
            sprite.hitblox.centery = sprite.pos.y


class player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.allsprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.playerimg
        self.imageimg = game.hitbloximg
        self.rectimg = self.image.get_rect()
        self.rect = self.imageimg.get_rect()
        self.hitblox = hitblox
        self.hitblox.center = self.rect.center
        self.rectimg.center = self.rect.center
        self.vel = vec2(0, 0)
        self.pos = vec2(x, y) * tilesize
        self.rot = 0
        self.mana = game.mana
        self.lastshot = 0
        self.lastshunt = 0
        self.lastmana = 0
        self.health = playerhealth

    def keys(self):
        # set player velocity and rotation
        self.vel = vec2(0, 0)
        self.rotspeed = 0
        keys = pg.key.get_pressed()

        # user inputs (wasd and up, down, left, right)
        # rotation
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rotspeed = playerrot
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rotspeed = -playerrot
        # velocity
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec2(pspeed,0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec2((-pspeed / 4)*3,0).rotate(-self.rot)
        # shooting
        if keys[pg.K_x] or keys[pg.K_u]:
            now = pg.time.get_ticks()
            if now - self.lastshot > brate:
                if self.mana > 5:
                    self.lastshot = now
                    self.mana -= 5
                    dir = vec2(1, 0).rotate(-self.rot)
                    pos = self.pos + spriteedge.rotate(-self.rot)
                    bullets(self.game, pos, dir, self.rot)
        #dash
        if keys[pg.K_c] or keys[pg.K_i]:
            now = pg.time.get_ticks()
            if now - self.lastshunt > srate:
                if self.mana > 30:
                    self.lastshunt = now
                    self.mana -= 30
                    dir = vec2(1, 0).rotate(-self.rot)
                    pos = self.pos + spriteedge.rotate(-self.rot)
                    shunt(self.game, self.pos, dir)


    def update(self):
        # player specific updates
        self.keys()
        now = pg.time.get_ticks()
        if now - self.lastmana > stale:
            if self.mana < 100:
                self.lastmana = now
                self.mana += 1

        self.pos += self.vel * self.game.dt
        self.rot = (self.rot + self.rotspeed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.playerimg, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hitblox.centerx = self.pos.x
        self.rectimg.centerx = self.pos.x
        crash(self, self.game.walls, 'x')
        self.hitblox.centery = self.pos.y
        self.rectimg.centery = self.pos.y
        crash(self, self.game.walls, 'y')
        self.rect.center = self.hitblox.center


class bullets(pg.sprite.Sprite):  # player attack creation

    def __init__(self, game, pos, dir, rot):
        self.groups = game.allsprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bulletimg
        self.rect = self.image.get_rect()
        self.pos = vec2(pos)
        self.rect.center = pos
        self.vel = dir * bspeed
        self.spawntime = pg.time.get_ticks()
        self.image = pg.transform.rotate(self.game.bulletimg, rot)

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawntime > blife:
            self.kill()


class shunt(pg.sprite.Sprite):  # player attack creation

    def __init__(self, game, pos, dir):
        self.groups = game.allsprites, game.shunt
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.shuntimg
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.vel = dir * sspeed
        self.spawntime = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.mobs):
            self.kill()
        if pg.time.get_ticks() - self.spawntime > slife:
            self.kill()


class mob(pg.sprite.Sprite):

    def __init__(self, game, x, y, t):  # slime mob sprite and hit-box creation
        self.groups = game.allsprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.slimeimg
        self.rect = self.image.get_rect()
        self.hitblox = shitblox.copy()
        self.hitblox.center = self.rect.center
        self.vel = vec2(0, 0)
        self.acc = vec2(0,0)
        self.pos = vec2(x, y) * tilesize
        self.rect.center = self.pos
        self.rot = 0
        self.t = t
        self.speed = 100
        self.helth = slhealth
        self.health = self.helth

    def avoide(self):
        for mob in self.game.mobs:
            if mob != self:
                dis = self.pos - mob.pos
                if 0 < dis.length() < mobar:
                    self.acc += dis.normalize()

    def update(self):   # slime movement
        self.rot = (self.game.player.pos - self.pos).angle_to(vec2(1, 0))
        if self.t == 's':
            self.image = pg.transform.rotate(self.game.slimelowimg, self.rot)
            self.speed = slspeed
            self.helth = slhealth
        elif self.t == 'e':
            self.image = pg.transform.rotate(self.game.slimeimg, self.rot)
            self.speed = slnspeed
            self.helth = shealth
        elif self.t == 'S':
            self.image = pg.transform.rotate(self.game.slimehighimg, self.rot)
            self.speed = shspeed
            self.helth = shhealth
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec2(1, 0).rotate(-self.rot)
        self.avoide()
        if self.acc == 0:
            self.acc = -1
        self.acc= self.acc * self.speed
        self.acc += self.vel * -1
        print(self.acc)
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt **2
        self.hitblox.centerx = self.pos.x
        crash(self, self.game.walls,'x')
        crash(self, self.game.barrier, 'x')
        self.hitblox.centery = self.pos.y
        crash(self, self.game.walls, 'y')
        crash(self, self.game.barrier, 'y')
        self.rect.center = self.hitblox.center
        if self.health <= 0:
            self.kill()

    def healthbar(self):
        if self.health > 60:
            co= green
        elif self.health > 30:
            co = yellow
        else:
            co = red
        width = int(self.rect.width * self.health / self.helth)
        self.healbar = pg.Rect(0, 0, width, 7)
        if self.health < self.helth:
            pg.draw.rect(self.image, co, self.healbar)


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):  # wall sprite and hit-box creation
        self.groups = game.allsprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wallimg
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize


class barrier(pg.sprite.Sprite):
    def __init__(self, game, x, y):  # wall sprite and hit-box creation
        self.groups = game.allsprites, game.barrier
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.barrierimg
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize


class manabox(pg.sprite.Sprite):
    def __init__(self, game, x, y):  # wall sprite and hit-box creation
        self.groups = game.allsprites, game.mpickups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.manaimg
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize


class healbox(pg.sprite.Sprite):
    def __init__(self, game, x, y):  # wall sprite and hit-box creation
        self.groups = game.allsprites, game.hpickups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.healthimg
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize


class winbox(pg.sprite.Sprite):
    def __init__(self, game, x, y):  # wall sprite and hit-box creation
        self.groups = game.allsprites, game.winbox
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wallimg
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize