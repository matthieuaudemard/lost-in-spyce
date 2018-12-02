import xml.etree.ElementTree

import pygame as pg


class Spritesheet:
    """
    Utility class for loading and parsing spritesheets
    """
    def __init__(self, filename):
        self.sheet = pg.image.load(filename).convert()
        self.elements = xml.etree.ElementTree.parse(filename.replace('.png', '.xml')).getroot().findall('SubTexture')

    def get_image(self, name):
        """
        grab an image out of the spritesheet by its name in the xml file
        :param name: name of the image i.e: 'bunny1_jump.png'
        :return: pygame.Surface
        """
        for elt in self.elements:
            if elt.get('name') == name:
                return self._get_image(
                    int(elt.get('x')),
                    int(elt.get('y')),
                    int(elt.get('width')),
                    int(elt.get('height'))
                )

    def _get_image(self, x, y, width, height):
        """
        grab an image out of the spritesheet by its coordonates
        :param x:
        :param y:
        :param width:
        :param height:
        :return: pygame.Surface
        """
        image = pg.Surface((width, height))
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image
