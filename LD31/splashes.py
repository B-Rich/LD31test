import sound
import cocos
import gamelogic
import maplayer
import player

class FullScreenSplash(cocos.scene.Scene):
    def __init__(self, main_scene, fname, time):
        splash_layer = cocos.layer.Layer()
        logo = cocos.sprite.Sprite(fname)
        logo.position = 400, 300
        splash_layer.add(logo)
        super(FullScreenSplash, self).__init__(splash_layer)
        sound.SoundManager.instance().play(sound.MONKEYS)
        self.schedule_interval(self.close, time, main_scene)

    def close(self, timedelta, scene):
        cocos.director.director.replace(scene)

class InitialSplashScreen(FullScreenSplash):
    def __init__(self, main_scene):
        super(InitialSplashScreen, self).__init__(main_scene, "img/logo.png", 3.5)

    def close(self, timedelta, scene):
        sound.SoundManager.instance().play_music()
        cocos.director.director.replace(scene)

class DeathScreen(FullScreenSplash):
    def __init__(self, main_scene):
        super(DeathScreen, self).__init__(main_scene,"img/death.png", 4)
        
    def close(self, timedelta, scene):
        cocos.director.director.replace(scene)

class WinScreen(FullScreenSplash):
    def __init__(self,main_scene):
        super(WinScreen, self).__init__(main_scene,"img/win.png", 4)
        
    def close(self, timedelta, scene):
        cocos.director.director.replace(scene)
