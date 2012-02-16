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

    def testPlayerWalksUpGroundSameSize(self):
        grounds = pygame.sprite.Group()
        ground1 = Ground([64, 198])
        grounds.add(ground1)
        self.player.collision_grounds = grounds
        self.player.walkUp()
        assert self.player.rect.top == 197, "player did not move up"

    def testPlayerWalksUpThreePixelsGroundSameSize(self):
        grounds = pygame.sprite.Group()
        ground1 = Ground([64, 198])
        grounds.add(ground1)
        self.player.collision_grounds = grounds
        self.player.walkUp()
        self.player.walkUp()
        self.player.walkUp()
        assert self.player.rect.top == 195, "player did not move up three pixels"

    def testPlayerWontWalkUpOffAboveGround(self):
        grounds = pygame.sprite.Group()
        ground1 = Ground([64, 214])
        grounds.add(ground1)
        self.player.collision_grounds = grounds
        self.player.walkUp()
        assert self.player.rect.top == 198, "player should not move up"

    def testPlayerWontWalkUpBottomOffGround(self):
        grounds = pygame.sprite.Group()
        ground1 = Ground([64, 212])
        grounds.add(ground1)
        self.player.collision_grounds = grounds
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
        grounds = pygame.sprite.Group()
        ground1 = Ground([64, 202])
        grounds.add(ground1)
        self.player.collision_grounds = grounds
        self.player.walkDown()
        assert self.player.rect.bottom == 215, "player should not have moved"

    def testPlayerWalksDownGroundTopSameLevelAsBottom(self):
        grounds = pygame.sprite.Group()
        ground1 = Ground([64, 214])
        grounds.add(ground1)
        self.player.collision_grounds = grounds
        self.player.walkDown()
        assert self.player.rect.top == 199, "player should have moved"

    def testPlayerWalksDownTwoPixelsGroundAboveThree(self):
        grounds = pygame.sprite.Group()
        ground1 = Ground([64, 200])
        grounds.add(ground1)
        self.player.collision_grounds = grounds
        self.player.walkDown()
        self.player.walkDown()
        self.player.walkDown()
        assert self.player.rect.top == 200, "player should have moved only 2 pixels"
        
    def testPlayerWalksDownBetweenGrounds(self):
        grounds = pygame.sprite.Group()
        ground1 = Ground([64, 200])
        ground2 = Ground([64, 216])
        grounds.add(ground1, ground2)
        self.player.collision_grounds = grounds
        self.player.walkDown()
        self.player.walkDown()
        self.player.walkDown()
        assert self.player.rect.bottom == 217, "player should have moved only 2 pixels"
        
    def testPlayerWalksDownMeh(self):
        grounds = pygame.sprite.Group()
        ground1 = Ground([64, 184])
        ground2 = Ground([64, 200])
        grounds.add(ground1, ground2)
        self.player.collision_grounds = grounds
        self.player.walkDown()
        self.player.walkDown()
        self.player.walkDown()
        assert self.player.rect.bottom == 216, "player should have moved only 2 pixels"


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
