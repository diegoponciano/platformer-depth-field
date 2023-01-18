#! /usr/bin/env python
import sys, os

import pygame
from pygame.locals import *

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 200, 0))
        self.rect = self.image.get_rect(topleft=[64, 0])
        self.jump_speed = 0
        self.jumping = False

    def update(self):

        #Get the current key state.
        key = pygame.key.get_pressed()
        
        #Move left/right
        dir = 0
        if key[K_LEFT]:
            dir = -1
        if key[K_RIGHT]:
            dir = 1
        
        #Increase the jump speed so you fall
        if self.jump_speed < 5:
            self.jump_speed += 0.3
        
        #We fell off a platform!
        if self.jump_speed > 2:
            self.jumping = True

        self.move(2 * dir, self.jump_speed)

    def __move(self, dx, dy):
        
        #Create a temporary new rect that has been moved to dx and dy
        new_rect = Rect(self.rect)
        new_rect.x += dx
        new_rect.y += dy
        
        #loop through all the sprites we're supposed to collide with 
        #(collision_sprites is defined in the main() function below)
        for sprite in self.collision_sprites:
            
            # If there's a collision between the new rect (the one that's
            # been moved) and the sprite's rect then we check
            # for what direction the sprite is moving, and then we
            # clamp the "real" rect to that side
            if new_rect.colliderect(sprite.rect):
                
                #Check the X axis
                if dx > 0: #moving right
                    self.rect.right = sprite.rect.left
                elif dx < 0: #moving left
                    self.rect.left = sprite.rect.right
               
                #Check the Y axis
                if dy > 0: #moving down
                    self.rect.bottom = sprite.rect.top
                    
                    #Landed!
                    self.jump_speed = 0
                    self.jumping = False
                elif dy < 0: #moving up
                    self.rect.top = sprite.rect.bottom
                    self.jump_speed = 0 #oww, we hit our head
                
                #Break the function so we'll skip the line below
                return
        
        #If there's no collision, move the rect!
        self.rect = Rect(new_rect)
        
    #Calls __move for the X and Y axises
    def move(self, dx, dy):
        if dx != 0:
            self.__move(dx, 0)
        if dy != 0:
            self.__move(0, dy)
 
class Player(pygame.sprite.Sprite):
    def __init__(self, pos=[64,198]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 200, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_grounds = []
        self.stand_on_ground()

    def update(self):
        if self.movement:
            self.movement()

    def control(self, key):
        if key[K_UP]:
            self.walkUp()
        if key[K_DOWN]:
            self.walkDown()
        if key[K_SPACE] and self.movement == self.standing:
            self.jump()

    # movements
    def jumping(self):
        self.rect = self.rect.move(0, self.jump_speed)
        if self.jump_speed > 0:
            self.movement = self.falling
        else:
            self.jump_speed += 0.3

    def falling(self):
        new_rect = self.rect.move(0, self.jump_speed)
        if self.jump_speed < 5:
            self.jump_speed += 0.2
        if new_rect.top >= self.ground:
            upmove = self.ground - self.rect.top
            self.rect = self.rect.move(0, upmove)
            self.stand_on_ground()
        else:
            self.rect = self.rect.move(0, self.jump_speed)

    def standing(self):
        pass

    def stand_on_ground(self):
        self.movement = self.standing
        self.jump_speed = -5
        self.ground = 0

    def jump(self):
        self.ground = self.rect.top
        self.movement = self.jumping

    def walkUp(self):
        move = False
        for ground in self.collision_grounds:
            if(self.rect.colliderect(ground.rect)):
                move = True
        if move:
            self.rect = self.rect.move(0, -1)

    def walkDown(self):
        move = False
        new_rect = self.rect.move(0, 1)
        for ground in self.collision_grounds:
            if(ground.rect.collidepoint(new_rect.left, new_rect.bottom-1)):
                move = True
        if move:
            self.rect = new_rect

class Ground(pygame.sprite.Sprite):
    def __init__(self, pos, size=(16, 16)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill((0, 124, 0))
        self.rect = self.image.get_rect(topleft=pos)

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size=(16, 16)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=pos)

class PlatformerGame:
    def __init__(self):
        self.groups = []
        self.map = """1..................1
1..................1
11111..............1
1..................1
1..................1
1......111.........1
1.....11.....1.....1
1.....1............1
1.....1.........1111
1...111............1
1.............1....1
11...........1.....1
12222222222222222221
12222222222222222221
11111111111111111111
"""

    def parse_level(self):
        #Parse the level
        x, y = 0, 0
        for row in self.map.split("\n"):
            for char in row:
                #Spawn a platform if the character is a 1
                if char == "1":
                    platform = Platform([x*16, y*16]) 
                    self.platforms.add(platform)
                    self.sprites.add(platform)
                elif char == "2":
                    ground = Ground([x*16, y*16]) 
                    self.grounds.add(ground)
                    self.sprites.add(ground)
            #Update the read position.
                x += 1
            x = 0
            y += 1

    def main(self):

        #Init pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        #Set the display mode
        pygame.display.set_caption("Platformer Field Depth")
        screen = pygame.display.set_mode((320, 240))

        #Create some groups. I like to use OrderedUpdates
        self.sprites = pygame.sprite.OrderedUpdates()
        self.platforms = pygame.sprite.OrderedUpdates()
        self.grounds = pygame.sprite.OrderedUpdates()

        #Create some starting objects
        player = Player()
        player.collision_sprites = self.platforms
        player.collision_grounds = self.grounds

        #Create all the platforms by parsing the level.
        self.parse_level()
        self.sprites.add(player)

        clock = pygame.time.Clock()

        #Main loop
        while 1:

            #Update
            clock.tick(60)
            self.sprites.update()

            key = pygame.key.get_pressed()
            player.control(key)

            #Get input
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    pygame.quit()
                    return
            #Draw the scene
            screen.fill((0, 0, 0))
            self.sprites.draw(screen)
            pygame.display.flip()

if __name__ == "__main__":
    game = PlatformerGame()
    game.main()
