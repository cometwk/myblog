# coding=utf-8

'''
AOK 动画

'''

import cocos
from cocos.director import director

from pyglet import gl



# --
from pyglet import image
from cocos.actions import *

from pyglet.image import Animation

import json

class AokAnimation:
    def __init__(self, descfile):
        str = self.readStrFromFile(descfile + '.desc')
        desc = json.loads(str)

        texture = image.load(desc["name"] + '.png')
        list = []
        for w in desc["frames"] :
            frame = texture.get_region(w["x"], w["y"], w["width"], 64) # TODO: 64 修改为 desc 的坐标有些问题， TODO
            list.append(frame)
        period = 0.2 # TODO： 参数

        self.animation = Animation.from_image_sequence(list, period, False)

    def readStrFromFile(self, filename):
        fp = open(filename)
        s = fp.read()
        fp.close()
        return s

class PlayLayer(cocos.layer.Layer):
    def __init__(self):
        super(PlayLayer, self).__init__()
        texture = image.load('attack.png')
        # image.load('1.png')
        print texture.width, texture.height
        f1 = texture.get_region(0,0,47,64)
        f2 = texture.get_region(47,0,40,64)
        actionimage1 = image.AnimationFrame(f1, 0.51) # 实现在第一帧图片　后面0.1 为这一帧动画需要的播放时间
        actionimage2 = image.AnimationFrame(f2, 0.51) # 实现第二帧图片
        #   actionimage3=image.AnimationFrame(image.load('3.png'),0.25)　# 第三帧
        #   actionimage4=image.AnimationFrame(image.load('4.png'),0.25)　# 第四帧
        actionimage = image.Animation([actionimage1, actionimage2])  # ,actionimage3,actionimage4])　　　

        aok = AokAnimation('attack')
        actionimage = aok.animation

        sprite = cocos.sprite.Sprite(actionimage)
        self.add(sprite)
        self.action_1(sprite)

    def action_1(self, sprite):
        sprite.position = 320 + 16, 24 + 48
        sprite.do(MoveTo((-16, 24 + 48), 6) + CallFuncS(self.action_1))


    # Defining a new layer type...

class Square(cocos.layer.Layer):

    """Square (color, c, y, size=50) : A layer drawing a square at (x,y) of
    given color and size"""

    def __init__(self, color, x, y, size=50):
        super(Square, self).__init__()

        self.x = x
        self.y = y
        self.size = size
        self.layer_color = color

    def draw(self):
        super(Square, self).draw()

        gl.glColor4f(*self.layer_color)
        x, y = self.x, self.y
        w = x + self.size
        h = y + self.size
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(x, y)
        gl.glVertex2f(x, h)
        gl.glVertex2f(w, h)
        gl.glVertex2f(w, y)
        gl.glEnd()
        gl.glColor4f(1, 1, 1, 1)

if __name__ == "__main__":
    director.init()
    # Create a large number of layers
    layers = [Square((0.03 * i, 0.03 * i, 0.03 * i, 1), i * 20, i * 20) for i in range(5, 20)]
    # Create a scene with all those layers
    sc = cocos.scene.Scene(*layers)
    # You can also add layers to a scene later:
    sc.add(Square((1, 0, 0, 0.5), 150, 150, 210), name="big_one")

    # sc = cocos.scene.Scene()
    sc.add(PlayLayer(), name="big_onxxxe")

    director.run(sc)
