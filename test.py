import unittest
import pymock
import pygame
from platformer import Player, Ground

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def testPlayerHasImage(self):
        assert self.player.image != None, "player does not have an image"

    def testPlayerHasRectangle(self):
        assert self.player.rect != None, "player does not have a rect"

    def testPlayerRectStartsInRightPosition(self):
        assert self.player.rect.top == 198, "player does not start in right place"
        assert self.player.rect.left == 64, "player does not start in right place"

    def testPlayerRectSetsInRightPosition(self):
        self.player = Player([16, 16])
        assert self.player.rect.top == 16, "player is not in right place"

    # walk up
    def testPlayerWontWalkUpWithoutGrounds(self):
        self.player.walkUp()
        assert self.player.rect.top == 198, "player did not move up"

    def dummy_grounds(self, *args):
        grounds = pygame.sprite.Group()
        for arg in args:
            ground = Ground(arg)
            grounds.add(ground)
        return grounds

    def testPlayerWalksUpGroundSameSize(self):
        self.player.collision_grounds = self.dummy_grounds([64, 198])
        self.player.walkUp()
        assert self.player.rect.top == 197, "player did not move up"

    def testPlayerWalksUpThreePixelsGroundSameSize(self):
        self.player.collision_grounds = self.dummy_grounds([64, 198])
        self.player.walkUp()
        self.player.walkUp()
        self.player.walkUp()
        assert self.player.rect.top == 195, "player did not move up three pixels"

    def testPlayerWontWalkUpOffAboveGround(self):
        self.player.collision_grounds = self.dummy_grounds([64, 214])
        self.player.walkUp()
        assert self.player.rect.top == 198, "player should not move up"

    def testPlayerWontWalkUpBottomOffGround(self):
        self.player.collision_grounds = self.dummy_grounds([64, 212])
        self.player.walkUp()
        self.player.walkUp()
        self.player.walkUp()
        assert self.player.rect.top == 196, "player did not move up two pixels"

    # walk down
    def testPlayerWontWalkDownWithoutGrounds(self):
        self.player.walkDown()
        assert self.player.rect.top == 198, "player did not move down"

    def testPlayerWontWalksDownGroundBigger(self):
        grounds = pygame.sprite.Group()
        ground1 = Ground([60, 194], (20, 20))
        grounds.add(ground1)
        self.player.collision_grounds = grounds
        self.player.walkDown()
        self.player.walkDown()
        assert self.player.rect.bottom == 214, "player should not have moved"

    def testPlayerWalksDownGroundThreePixelsAbove(self):
        self.player.collision_grounds = self.dummy_grounds([64, 202])
        self.player.walkDown()
        assert self.player.rect.bottom == 215, "player should not have moved"

    def testPlayerWalksDownGroundTopSameLevelAsBottom(self):
        self.player.collision_grounds = self.dummy_grounds([64, 214])
        self.player.walkDown()
        assert self.player.rect.top == 199, "player should have moved"

    def testPlayerWalksDownTwoPixelsGroundAboveThree(self):
        self.player.collision_grounds = self.dummy_grounds([64, 200])
        self.player.walkDown()
        self.player.walkDown()
        self.player.walkDown()
        assert self.player.rect.top == 200, "player should have moved only 2 pixels"
        
    def testPlayerWalksDownBetweenGrounds(self):
        self.player.collision_grounds = self.dummy_grounds([64, 200], [64, 216])
        self.player.walkDown()
        self.player.walkDown()
        self.player.walkDown()
        assert self.player.rect.bottom == 217, "player should have moved only 2 pixels"

    def testPlayerWalksDownOnSecondGround(self):
        self.player.collision_grounds = self.dummy_grounds([64, 184], [64, 200])
        self.player.walkDown()
        self.player.walkDown()
        self.player.walkDown()
        assert self.player.rect.bottom == 216, "player should have moved only 2 pixels"

    # jumpin
    def testPlayerJumpsUp(self):
        self.player.collision_grounds = self.dummy_grounds([64, 184], [64, 200])
        self.player.jump()
        self.player.update()
        assert self.player.rect.top == 194, "player should have jumped 4 pixels up"
        assert self.player.movement == self.player.jumping, 'player state should be jumping'

    def testPlayerDontJumpIfAlreadyJumping(self):
        self.player.collision_grounds = self.dummy_grounds([64, 184], [64, 200])
        self.player.jump()
        self.player.update()
        assert self.player.movement == self.player.jumping, 'player state should be jumping'
        assert self.player.rect.top == 194, "player should have jumped 4 pixels up"

    def testPlayerOnJumpsUpAndFalls(self):
        self.player.collision_grounds = self.dummy_grounds([64, 184], [64, 200])
        self.player.jump()
        while True:
            self.player.update()
            if self.player.jump_speed > 0:
                break
        self.player.update()
        assert self.player.jump_speed > 0, "jump speed should be over 0"
        assert self.player.jump_speed < 5, "jump speed should be under 5"
        assert self.player.movement == self.player.falling, 'player state should be falling'

    def testPlayerOnJumpsUpAndFallSameGround(self):
        self.player.collision_grounds = self.dummy_grounds([64, 184], [64, 200])
        self.player.jump()
        for i in range(50):
            self.player.update()
        assert self.player.rect.top == 198, "player should have fallen at the same ground" 
        assert self.player.movement == self.player.standing, 'player state should be standing'
        assert self.player.ground == 0, 'player ground should be zero'
        assert self.player.jump_speed == -4, 'player jump speed is reinitialized'


class TestPlayerDraw(unittest.TestCase):
	def testDrawPlayer(self):
		playerGroup = pygame.sprite.Group()
		player = Player()

		controller = pymock.Controller()
		surface = controller.mock()
		surface.blit(player.image, player.rect)

		controller.replay()

		playerGroup.add(player)
		playerGroup.draw(surface)

		controller.verify()

if __name__=="__main__":
    unittest.main()
