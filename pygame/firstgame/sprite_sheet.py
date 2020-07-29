#https://stackoverflow.com/questions/45526988/does-anyone-have-an-example-of-using-sprite-sheets-in-tandem-with-xml-files
import pygame as pg
import xml.etree.ElementTree as ET

class SpriteSheet:
    # load an atlas image
    # can also pass an associated XML file (ref. Kenney art)
    def __init__(self, img_file, data_file=None):
        self.spritesheet = pg.image.load(img_file).convert_alpha()
        if data_file:
            tree = ET.parse(data_file)
            self.map = {}
            for node in tree.iter():
                if node.attrib.get('name'):
                    name = node.attrib.get('name')
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['width'] = int(node.attrib.get('width'))
                    self.map[name]['height'] = int(node.attrib.get('height'))

    def get_image_rect(self, x, y, w, h):
        return self.spritesheet.subsurface(pg.Rect(x, y, w, h))

    def get_image_name(self, name, scale=None):
        rect = pg.Rect(self.map[name]['x'], self.map[name]['y'],
                       self.map[name]['width'], self.map[name]['height'])
        sub_rect = self.spritesheet.subsurface(rect)

        if scale is not None:
            return pg.transform.scale(
                sub_rect,
                (
                    int(sub_rect.get_width() * scale),
                    int(sub_rect.get_height() * scale)
                ))

        return self.spritesheet.subsurface(rect)