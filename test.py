import unittest
import pymock
import pygame
from platformer import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def testPlayerHasImage(self):
        assert self.player.image != None, "player does not have an image"

    def testPlayerHasRectangle(self):
        assert self.player.rect != None, "player does not have a rect"

    def testPlayerRectIsInRightPlace(self):
        self.player = Player([16, 16])
        assert self.player.rect.top == 16, "player is not in right place"

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
