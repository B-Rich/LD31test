import random
import cocos, pyglet
from pyglet.gl.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
import maplayer, gamelogic
from pyglet.window import key
import sound

class Player(cocos.layer.Layer):
    PLAYER_SIZE = 26

    def __init__(self):
        #super(Player, self).__init__(255,255,255,255)
        super(Player, self).__init__()

        self.sound = sound.SoundManager.instance()
        self.images = []
        self.images.append(pyglet.resource.image("img/player_up.png"))
        self.images.append(pyglet.resource.image("img/player_left.png"))
        self.images.append(pyglet.resource.image("img/player_down.png"))
        self.images.append(pyglet.resource.image("img/player_right.png"))
        for img in self.images :
            glTexParameteri(img.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(img.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        self.sprite = cocos.sprite.Sprite(self.images[gamelogic.DIRECTION_DOWN])

        (self.cell_x,self.cell_y) = gamelogic.Game.instance().get_start_point()
        self.sprite.position = self._get_drawing_coors()
        self.add(self.sprite)
        self.moving = False # currently moving
        self.game = gamelogic.Game.instance()

        self.cheating = False
        self.controllable = True
        self.schedule(self.update)

    def _get_drawing_coors(self):
        base_x = maplayer.MapLayer.SPRITE_SIZE * self.cell_x
        base_y = maplayer.MapLayer.SPRITE_SIZE * self.cell_y
        offset = maplayer.MapLayer.SPRITE_SIZE / 2
        return base_x + offset, base_y + offset

    def _movement_allowed(self, direction):
        return self.game.get_cell(self.cell_x, self.cell_y).wall[direction] == 0

    def update(self, timedelta):
        if self.moving or not self.controllable:
            return

        keystate = gamelogic.Game.instance().keystate
        if keystate[key.C]:
            self.cheating = not self.cheating

        if keystate[key.LEFT] and self._movement_allowed(gamelogic.DIRECTION_LEFT):
            self.cell_x -= 1
            self.sprite.image = self.images[gamelogic.DIRECTION_LEFT]
        elif keystate[key.UP] and self._movement_allowed(gamelogic.DIRECTION_UP):
            self.cell_y += 1
            self.sprite.image = self.images[gamelogic.DIRECTION_UP]
        elif keystate[key.DOWN] and self._movement_allowed(gamelogic.DIRECTION_DOWN):
            self.cell_y -= 1
            self.sprite.image = self.images[gamelogic.DIRECTION_DOWN]
        elif keystate[key.RIGHT] and self._movement_allowed(gamelogic.DIRECTION_RIGHT):
            self.cell_x += 1
            self.sprite.image = self.images[gamelogic.DIRECTION_RIGHT]
        else:
            if self.cheating:
                if keystate[key.LEFT]:
                    self.cell_x -= 1
                elif keystate[key.UP]:
                    self.cell_y += 1
                elif keystate[key.DOWN]:
                    self.cell_y -= 1
                elif keystate[key.RIGHT]:
                    self.cell_x += 1
                else:
                    return
            else:
                return
        self.sound.play(sound.STEP)
        print "[player] moving mowing moving to ", self.cell_x, ",",self.cell_y

        self.moving = True
        self.sprite.do(cocos.actions.MoveTo(self._get_drawing_coors(), 0.2) + cocos.actions.CallFunc(self.stopped_moving))
        self.game.enter_cell(self.cell_x, self.cell_y)

    def stopped_moving(self):
        self.moving = False

    def disable_controls(self):
        self.controllable = False

    def enable_controls(self):
        self.controllable = True
        

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1 or sys.argv[1] != "-debug":
        print "This class is not intended to be run in a main file."
        print "However, if you just want to run a test, use -debug option."
        sys.exit(0)
    cocos.director.director.init()
    gamelogic.Game.instance().load_from("level.dat")
    player = Player()
    test = cocos.scene.Scene(player)
    cocos.director.director.run(test)
