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
    def __init__(self, position=[64,198]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 16))
        self.rect = self.image.get_rect(topleft=position)

        #pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = pygame.Surface((16, 16))
        #self.image.fill((255, 200, 0))
        #self.rect = self.image.get_rect(topleft=[64, 0])
        #self.jump_speed = 0
        #self.jumping = False
           
class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=pos)

map = """1..................1
1..................1
1..................1
1..................1
1..................1
1..................1
1..................1
1..................1
1..................1
1..................1
1..................1
1..................1
1..................1
1..................1
11111111111111111111
"""

def parse_level():
    #Parse the level
    x, y = 0, 0
    for row in map.split("\n"):
        for char in row:

            #Spawn a platform if the character is a 1
            if char == "1":
                Platform([x*16, y*16]) 

        #Update the read position.
            x += 1
        x = 0
        y += 1
        
        
def main():
    
    #Init pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    
    #Set the display mode
    pygame.display.set_caption("Platformer Field Depth")
    screen = pygame.display.set_mode((320, 240))
    
    #Create some groups. I like to use OrderedUpdates
    sprites = pygame.sprite.OrderedUpdates()
    platforms = pygame.sprite.OrderedUpdates()
   
    #Set the sprites' groups
    Player.groups = sprites
    Platform.groups = sprites, platforms
    
    #The player will loop through all the sprites contained in this
    #group, and then collide with them.
    Player.collision_sprites = platforms
    
    
    #Create some starting objects
    player = Player()
    clock = pygame.time.Clock()

    #Create all the platforms by parsing the level.
    parse_level()    

    #Main loop
    while 1:
        
        #Update
        clock.tick(60)
        sprites.update()
        
        #Get input
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    return
                if e.key == K_SPACE:
                    if not player.jumping:
                        player.jump_speed = -5.5
                        player.jumping = True
        
        #Draw the scene
        screen.fill((0, 0, 0))
        sprites.draw(screen)
        pygame.display.flip()
        
if __name__ == "__main__":
    main()
