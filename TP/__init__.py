#The main file, __init__.py
# This file runs the whole game by calling base.run

from direct.showbase.ShowBase import ShowBase
base = ShowBase()
from direct.gui.DirectGui import *
from panda3d.core import TextNode
from direct.interval.IntervalGlobal import *
import sys
import wave
import random
from panda3d.core import *
from direct.showbase import DirectObject
import math
import aubio
import numpy as np
import sys
import pyaudio
import aubio
from aubio import source, notes
from tkinter import *
from panda3d.core import TransparencyAttrib
from direct.interval.LerpInterval import LerpPosInterval
from direct.task import Task

class World(DirectObject.DirectObject):
    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(0.06, -.06 * (i + 0.5)), fg=(1, 1, 1, 1),
                            parent=base.a2dTopLeft,align=TextNode.ALeft, scale=.05)
                            
    def __init__(self):
        
        base.setBackgroundColor(0, 0, 0)  # Set the background to black
        base.disableMouse()
        self.zoom = 0
        camera.setPos(0, 0, 45)  # Set the camera position (X, Y, Z)
        camera.setHpr(0, -90, 0) 
        self.scale = [0.1, 0.001, 0.1, 0.2, 0.008, 0.02, 0.003, 0.2, 0.026, 0.0015, 0.1, 1, 2, 3.5, 1, 1, 1, 0.3, 1, 0.15, 0.015, 0.15, 0.5, 0.2, 0.25, 0.3]
        #models from http://alice.org/pandagallery/index.html
        self.trees = [('models/BirchTree', 'models/birches.tif'), ('models/bonzai', 'models/bonzai.tif'), ('models/bush2', 'models/bush2.tif'), ('models/groom', 'models/groom.tif'), ('models/pine','models/pine.tif'), ('models/bush','models/bush.tif'), ('models/fern','models/fern.tif'), ('models/sapling','models/sapling.tif'), ('models/shrubbery','models/shrubbery.tif'), ('models/shrub','models/shrub.tif'), ('models/cactus','models/cactus.tif'),('models/daisy','models/daisy.tif'), ('models/daisy2','models/daisy2.tif'), ('models/lily','models/lily.tif'), ('models/purple','models/purple.tif'), ('models/red','models/red.tif'), ('models/tulip','models/tulip.tif'), ('models/bunny','models/bunny.tif'), ('models/chicken','models/chicken.tif'), ('models/cow','models/cow.tif'), ('models/flamingo','models/flamingo.tif'), ('models/horse','models/horse.tif'), ('models/joey','models/joey.tif'), ('models/monkey','models/monkey.tif'), ('models/penguin','models/penguin.tif'), ('models/turtle','models/turtle.tif')]
        #textures from google images
        deimos = ["models/deimos_1k_tex.jpg", "models/Dgreen.jpg", "models/Dblue.jpg","models/Dpurple.jpg", "models/Dyellow.jpg"]
        cool = ["models/cool.jpg", "models/cred.jpg", "models/cgreen.jpg", "models/cpurple.jpg", "models/cblue.jpg"]
        mars = ["models/mars_1k_tex.jpg", "models/mayellow.jpg","models/magreen.jpg", "models/mapurple.jpg", "models/mablue.jpg"]
        phobos = ["models/phobos_1k_tex.jpg", "models/pred.jpg", "models/pgreen.jpg", "models/ppurple.jpg", "models/pblue.jpg"]
        earth = ["models/earth_1k_tex.jpg", "models/ered.jpg", "models/egreen.jpg", "models/epink.jpg", "models/eblue.jpg"]
        self.textures = [deimos, cool, mars, phobos, earth]
        self.randomTex = random.randint(0,4)
        self.pTexture = self.textures[self.randomTex]
        self.loadPlanets() 
        self.accept("escape", sys.exit)
        self.accept("wheel_up", self.zoomOut)
        self.accept("wheel_down", self.zoomIn)
        self.average = 0
        self.song = 'songs/Stargazing.mp3'    
        World.playSong(self)
        self.score = 0
        self.rights = 0
        self.lefts = 0
        self.ups = 0
        self.downs = 0
        self.menu()
        self.isLive = True
        self.isPaused = False
        self.liveThresh = 2000
    manyTrees = render.attachNewNode('test3')
    arrowsR = render.attachNewNode('arrowsR')
    arrowsL = render.attachNewNode('arrowsL')
    arrowsU = render.attachNewNode('arrowsU')
    arrowsD = render.attachNewNode('arrowsD')

    def menu(self):
        self.title = OnscreenText(text = "UNIVERSAL MUSIC", pos = (0, .75) , scale = 0.12, fg = (255,255,255,255))
        self.music = DirectButton(pos=(-1, 0,-0.8),text = ("Music",  "Go",), scale=.1, command=self.music)
        self.myMusic = DirectButton(pos=(-.3, 0,-0.8),text = ("My Music",  "Go",), scale=.1, command=self.myMusic)
        self.liveButton = DirectButton(pos=(.4, 0,-0.8),text = ("Live",  "Go",), scale=.1, command=self.live)
        self.help = DirectButton(pos=(1, 0,-0.8),text = ("Help",  "Go",), scale=.1, command=self.help)
    
    def menuFromHelp(self):
        self.welcome.destroy()
        self.explore.destroy()
        self.first.destroy()
        self.second.destroy()
        self.third.destroy()
        self.goBack.destroy()
        self.title = OnscreenText(text = "UNIVERSAL MUSIC", pos = (0, .75) , scale = 0.12, fg = (255,255,255,255))
        self.music = DirectButton(pos=(-1, 0,-0.8),text = ("Music",  "Go",), scale=.1, command=self.music2)
        self.myMusic = DirectButton(pos=(-.3, 0,-0.8),text = ("My Music",  "Go",), scale=.1, command=self.myMusic2)
        self.liveButton = DirectButton(pos=(.4, 0,-0.8),text = ("Live",  "Go",), scale=.1, command=self.liveR)
        self.help = DirectButton(pos=(1, 0,-0.8),text = ("Help",  "Go",), scale=.1, command=self.help2)   
    
    def help(self):
        self.title.remove_node()
        self.music.remove_node()
        self.myMusic.remove_node()
        self.liveButton.remove_node()
        self.help.remove_node()
        self.welcome = OnscreenText(text = "Hello! Welcome to Universal Music!", pos = (0, .8) , scale = 0.07, fg = (255,255,255,255))
        self.explore = OnscreenText(text = "In Universal Music, there are three sections you can explore:", pos = (0, .7) , scale = 0.07, fg = (255,255,255,255))
        self.first = OnscreenText(text = "Music- Music has a collection of preloaded songs.", pos = (0, -.6) , scale = 0.07, fg = (255,255,255,255))
        self.second = OnscreenText(text = "My Music- My music is where you can upload your own song.", pos = (0, -.7) , scale = 0.07, fg = (255,255,255,255))
        self.third = OnscreenText(text = "Live- Live is where you can record your own audio file and play it back.", pos = (0, -.8) , scale = 0.07, fg = (255,255,255,255))
        self.goBack = OnscreenText(text = "Press 'Space' to return to menu", pos = (0, -.9) , scale = 0.05, fg = (255,255,255,255))
        self.accept("space", self.menuFromHelp)
        
    def help2(self):
        self.title.remove_node()
        self.music.remove_node()
        self.myMusic.remove_node()
        self.help.remove_node()
        self.liveButton.remove.node()
        self.welcome = OnscreenText(text = "Hello! Welcome to Universal Music!", pos = (0, .8) , scale = 0.07, fg = (255,255,255,255))
        self.explore = OnscreenText(text = "In Universal Music, there are three sections you can explore:", pos = (0, .7) , scale = 0.07, fg = (255,255,255,255))
        self.first = OnscreenText(text = "Music- Music has a collection of preloaded songs.", pos = (0, -.7) , scale = 0.07, fg = (255,255,255,255))
        self.second = OnscreenText(text = "My Music- My music is where you can upload your own song.", pos = (0, -.8) , scale = 0.07, fg = (255,255,255,255))
        self.third = OnscreenText(text = "Live- Live is where you can record your own audio file and play it back.", pos = (0, -.8) , scale = 0.07, fg = (255,255,255,255))
        self.goBack = OnscreenText(text = "Press 'Space' to return to menu", pos = (0, -.9) , scale = 0.05, fg = (255,255,255,255))
        self.accept("space", self.menuFromHelp)
        
        
    #sets up the My Music screen when button is pressed
    def myMusic(self):
        self.title2 = OnscreenText(text = "My Music", pos = (0, .75) , scale = 0.12, fg = (255,255,255,255))
        self.textObject = OnscreenText(text = "ENTER YOUR MUSIC'S PATH", pos = (0, -.7) , scale = 0.07, fg = (255,255,255,255))
        self.textObject2 = OnscreenText(text = "PRESS ENTER WHEN YOU'RE DONE!", pos = (0, -.9) , scale = 0.05, fg = (255,255,255,255))
        def clearText():
            self.entry.enterText('')
        self.liveButton.destroy()
        self.title.destroy()
        self.music.destroy()
        self.myMusic.destroy()
        self.help.destroy()
        self.entry = DirectEntry(pos=(-1, 0,-.8), scale=.05, width = 40, command=self.start2, numLines = 1, focus=1, focusInCommand=clearText)
        
    def myMusic2(self):
        self.title2 = OnscreenText(text = "My Music", pos = (0, .75) , scale = 0.12, fg = (255,255,255,255))
        self.textObject = OnscreenText(text = "ENTER YOUR MUSIC'S PATH", pos = (0, -.7) , scale = 0.07, fg = (255,255,255,255))
        self.textObject2 = OnscreenText(text = "PRESS ENTER WHEN YOU'RE DONE!", pos = (0, -.9) , scale = 0.05, fg = (255,255,255,255))
        def clearText():
            self.entry.enterText('')
        self.liveButton.destroy()
        self.title.destroy()
        self.music.destroy()
        self.myMusic.destroy()
        self.help.destroy()
        self.entry = DirectEntry(pos=(-1, 0,-.8), scale=.05, width = 40, command=self.start2, numLines = 1, focus=1, focusInCommand=clearText)
        
        
    
    #sets up the music screen when button is pressed
    def music(self):
        self.title.destroy()
        self.music.destroy()
        self.myMusic.destroy()
        self.liveButton.destroy()
        self.help.destroy()
        self.title3 = OnscreenText(text = "Music", pos = (0, .75) , scale = 0.12, fg = (255,255,255,255))
        self.song1 = DirectButton(pos=(-1, 0,0.7),text = ("Happier",  "Go",), scale=.05, command=self.set1)
        self.song2 = DirectButton(pos=(-1, 0,0.2),text = ("Past Lives",  "Go",), scale=.05, command=self.set2)
        self.song3 = DirectButton(pos=(-1, 0,-0.3),text = ("Still Waiting to Start",  "Go",), scale=.05, command=self.set3)
        self.song4 = DirectButton(pos=(-1, 0,-0.7),text = ("Don't Give Up on Me",  "Go",), scale=.05, command=self.set4)
        self.song5 = DirectButton(pos=(1, 0,0.7),text = ("Sucker",  "Go",), scale=.05, command=self.set5)
        self.song6 = DirectButton(pos=(1, 0,0.2),text = ("Waves",  "Go",), scale=.05, command=self.set6)
        self.song7 = DirectButton(pos=(1, 0,-0.3),text = ("Stargazing",  "Go",), scale=.05, command=self.set7)
        self.song8 = DirectButton(pos=(1, 0,-0.7),text = ("Rewrite the Stars",  "Go",), scale=.05, command=self.set8)
    #sets up the music screen when button is pressed
    
    def music2(self):
        self.title.destroy()
        self.music.destroy()
        self.myMusic.destroy()
        self.liveButton.destroy()
        self.help.destroy()
        self.title3 = OnscreenText(text = "Music", pos = (0, .75) , scale = 0.12, fg = (255,255,255,255))
        self.song1 = DirectButton(pos=(-1, 0,0.7),text = ("Happier",  "Go",), scale=.05, command=self.set1)
        self.song2 = DirectButton(pos=(-1, 0,0.2),text = ("Past Lives",  "Go",), scale=.05, command=self.set2)
        self.song3 = DirectButton(pos=(-1, 0,-0.3),text = ("Still Waiting to Start",  "Go",), scale=.05, command=self.set3)
        self.song4 = DirectButton(pos=(-1, 0,-0.7),text = ("Don't Give Up on Me",  "Go",), scale=.05, command=self.set4)
        self.song5 = DirectButton(pos=(1, 0,0.7),text = ("Sucker",  "Go",), scale=.05, command=self.set5)
        self.song6 = DirectButton(pos=(1, 0,0.2),text = ("Waves",  "Go",), scale=.05, command=self.set6)
        self.song7 = DirectButton(pos=(1, 0,-0.3),text = ("Stargazing",  "Go",), scale=.05, command=self.set7)
        self.song8 = DirectButton(pos=(1, 0,-0.7),text = ("Rewrite the Stars",  "Go",), scale=.05, command=self.set8)
        
    
      
    #loads the different songs already in project
    #song credits goes to youtube
    def set1(self):
        self.song = 'songs/Happier.mp3' 
        self.start(self.song)
    def set2(self):
        self.song = 'songs/PastLives.mp3' 
        self.start(self.song)
    def set3(self):
        self.song = 'songs/Waiting.mp3' 
        self.start(self.song)
    def set4(self):
        self.song = 'songs/DontGiveUp.mp3' 
        self.start(self.song)
    def set5(self):
        self.song = 'songs/Sucker.mp3' 
        self.start(self.song)
    def set6(self):
        self.song = 'songs/Waves.mp3' 
        self.start(self.song)
    def set7(self):
        self.song = 'songs/Stargazing.mp3' 
        self.start(self.song)
    def set8(self):
        self.song = 'songs/RewriteTheStars.mp3' 
        self.start(self.song)
     
    #starts visualization from the music page 
    def start(self, song):
        self.title3.destroy()
        self.song1.destroy()
        self.song2.destroy()
        self.song3.destroy()
        self.song4.destroy()
        self.song5.destroy()
        self.song6.destroy()
        self.song7.destroy()
        self.song8.destroy()
        self.accept("x", self.increaseThresh)
        self.accept("z", self.decreaseThresh)
        self.rightText = self.genLabelText(
                "[x]: Slow down color changes", 1)
        self.leftText = self.genLabelText(
                "[z]: Speed up color changes", 2)
        self.suText = self.genLabelText(
                "[scroll up]: Zoom out", 3)
        self.sdText = self.genLabelText(
                "[scroll down]: Zoom in", 4)
        self.pauseText = self.genLabelText(
                "[space]: Pause music", 5)
        self.exitText = self.genLabelText(
                "[esc]: Exit", 6)
        self.gameText = self.genLabelText(
                "Use the keyboard arrows to hit the notes!", 7)
        self.planet.removeNode()
        World.manyTrees.removeNode()
        World.manyTrees = render.attachNewNode('test4')
        self.stream.stop_stream()
        self.loadPlanets() 
        World.playSong2(self)
        self.game()
     
    def live(self):
        self.title2 = OnscreenText(text = "Record Audio", pos = (0, .75) , scale = 0.12, fg = (255,255,255,255))
        self.textObject = OnscreenText(text = "HOW MANY SECONDS WILL YOUR RECORDING BE?", pos = (0, -.7) , scale = 0.07, fg = (255,255,255,255))
        self.textObject2 = OnscreenText(text = "PRESS ENTER TO START RECORDING! (IT STARTS RECORDING INSTANTLY)", pos = (0, -.9) , scale = 0.05, fg = (255,255,255,255))
        def clearText():
            self.entry.enterText('')
        self.liveButton.destroy()
        self.title.destroy()
        self.music.destroy()
        self.myMusic.destroy()
        self.help.destroy()
        self.entry = DirectEntry(pos=(-1, 0,-.8), scale=.05, width = 40, command=self.live2, numLines = 1, focus=1, focusInCommand=clearText) 
        
    def liveR(self):
        self.title2 = OnscreenText(text = "Record Audio", pos = (0, .75) , scale = 0.12, fg = (255,255,255,255))
        self.textObject = OnscreenText(text = "HOW MANY SECONDS WILL YOUR RECORDING BE?", pos = (0, -.7) , scale = 0.07, fg = (255,255,255,255))
        self.textObject2 = OnscreenText(text = "PRESS ENTER TO START RECORDING! (IT STARTS RECORDING INSTANTLY)", pos = (0, -.9) , scale = 0.05, fg = (255,255,255,255))
        def clearText():
            self.entry.enterText('')
        self.liveButton.destroy()
        self.title.destroy()
        self.music.destroy()
        self.myMusic.destroy()
        self.help.destroy()
        self.entry = DirectEntry(pos=(-1, 0,-.8), scale=.05, width = 40, command=self.live2, numLines = 1, focus=1, focusInCommand=clearText) 
          
    def live2(self, length):
        try:
            self.textObject2.destroy()
            self.textObject.destroy()
            self.title2.destroy()
            self.length = int(length)
            self.stream.stop_stream()
            World.startLive(self)
            World.playSong(self)
            self.entry.destroy()
            self.accept("x", self.increaseThresh)
            self.accept("z", self.decreaseThresh)
            self.rightText = self.genLabelText(
                    "[x]: Slow down color changes", 1)
            self.leftText = self.genLabelText(
                    "[z]: Speed up color changes", 2)
            self.suText = self.genLabelText(
                    "[scroll up]: Zoom out", 3)
            self.sdText = self.genLabelText(
                    "[scroll down]: Zoom in", 4)
            self.pauseText = self.genLabelText(
                "[space]: Pause music", 5)
            self.exitText = self.genLabelText(
                    "[esc]: Exit", 6)
            self.planet.removeNode()
            World.manyTrees.removeNode()
            World.manyTrees = render.attachNewNode('test4')
            self.loadPlanets()
        except:
            self.stream.start_stream()
            self.textObject.destroy()
            self.textObject = OnscreenText(text = "PLEASE TYPE A NUMBER", pos = (0, -.7) , scale = 0.07, fg = (255,255,255,255))
        
        
    def startLive(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = self.length
        WAVE_OUTPUT_FILENAME = "voice.wav"
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        self.title3 = OnscreenText(text = "Playback", pos = (0, .75) , scale = 0.12, fg = (255,255,255,255))
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        self.song = 'voice.wav'
        World.playSong(self)
        

    def increaseNote(self):
        self.liveThresh += 100
        
    def decreaseNote(self):
        self.liveThresh -= 100
        
    def checkR(self):
        if self.rights > 0:
            self.rights -= 1
            self.score += 1
            self.scoreText.destroy()
            self.game()
            
    def checkL(self):
        if self.lefts > 0:
            self.lefts -= 1
            self.score += 1
            self.scoreText.destroy()
            self.game()
    def checkU(self):
        if self.ups > 0:
            self.ups -= 1
            self.score += 1
            self.scoreText.destroy()
            self.game()
    def checkD(self):
        if self.downs > 0:
            self.downs -= 1
            self.score += 1
            self.scoreText.destroy()
            self.game()
            
    def pause(self):
        self.isPaused = not self.isPaused
        if self.isPaused == True:
            self.stream.stop_stream()
        else:
            self.stream.start_stream()

    
    #game mode    
    def game(self):
        self.scoreText = OnscreenText(text = "Score: %d" %self.score, pos = (1, 0.9) , scale = 0.07, fg = (255,255,255,255))
        self.accept("arrow_right", self.checkR)
        self.accept("arrow_left", self.checkL)
        self.accept("arrow_up", self.checkU)
        self.accept("arrow_down", self.checkD)
    
    #sets up the moving arrows for the rhythm game    
    def arrow(self):
        self.left = loader.loadModel("models/arrow")
        self.left.setHpr(0,90,90)
        self.left.setScale(.3)
        self.moveIntervalL = self.left.posInterval(2, Point3(-10,0,0))
        self.right = loader.loadModel("models/arrow")
        self.right.setHpr(0,180,90)

        self.right.setScale(.3)
        self.moveIntervalR = self.right.posInterval(2, Point3(10,0,0))
        self.up = loader.loadModel("models/arrow")
        self.up.setHpr(0,90,0)

        self.up.setScale(.3)
        self.moveIntervalU = self.up.posInterval(2, Point3(0,10,0))
        self.down = loader.loadModel("models/arrow")
        self.down.setHpr(0,90,180)

        self.down.setScale(.3)
        self.moveIntervalD = self.down.posInterval(2, Point3(0,-10,0))
        num = random.randint(0,3)
        parent = [self.right.reparentTo(World.arrowsR), self.left.reparentTo(World.arrowsL), self.up.instanceTo(World.arrowsU),  self.down.instanceTo(World.arrowsD)]
        arrows = [self.moveIntervalR, self.moveIntervalL, 
        self.moveIntervalU, self.moveIntervalD]
        parent[num]
        if arrows[num] == self.moveIntervalR:
            self.rights += 1
            if self.rights > 10:
                self.rights = 1
        elif arrows[num] == self.moveIntervalL:
            self.lefts += 1
            if self.lefts > 10:
                self.lefts = 1
        elif arrows[num] == self.moveIntervalU:
            self.ups += 1
            if self.ups > 10:
                self.ups = 1
        elif arrows[num] == self.moveIntervalD:
            self.downs += 1
            if self.downs > 10:
                self.downs = 1
        arrows[num].start()
        
     #starts visualization from my music page    
    def start2(self, song):
        try:
            self.song = song
            self.stream.stop_stream()
            World.playSong2(self)
            self.entry.destroy()
            self.textObject2.destroy()
            self.textObject.destroy()
            self.title2.destroy()
            self.accept("x", self.increaseThresh)
            self.accept("z", self.decreaseThresh)
            self.accept("space", self.pause)
            self.rightText = self.genLabelText(
                    "[x]: Slow down color changes", 1)
            self.leftText = self.genLabelText(
                    "[z]: Speed up color changes", 2)
            self.suText = self.genLabelText(
                "[scroll up]: Zoom out", 3)
            self.sdText = self.genLabelText(
                "[scroll down]: Zoom in", 4)
            self.pauseText = self.genLabelText(
                "[space]: Pause music", 5)
            self.exitText = self.genLabelText(
                "[esc]: Exit", 6)
            self.gameText = self.genLabelText(
                "Use the keyboard arrows to hit the notes!", 7)
            self.planet.removeNode()
            World.manyTrees.removeNode()
            World.manyTrees = render.attachNewNode('test4')
        
            self.loadPlanets()
            self.game()
        except:
            self.stream.start_stream()
            self.textObject.destroy()
            self.textObject = OnscreenText(text = "PLEASE TYPE A VALID PATH", pos = (0, -.7) , scale = 0.07, fg = (255,255,255,255))

    
    def increaseThresh(self):
        self.average += 5
    def decreaseThresh(self):
        self.average -= 5
 
    def zoomOut(self):
        if self.zoom < -30:
            pass
        else:
            self.zoom -= 5
            base.camera.setPos(base.camera, 0, -5, 0)
        
        
    def zoomIn(self):
        if self.zoom > 30:
            pass
        else:
            self.zoom += 5
            base.camera.setPos(base.camera, 0, 5, 0)
    
    def loadPlanets(self):
        self.randomTex = random.randint(0,4)
        self.pTexture = self.textures[self.randomTex]
        # Load the sky
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(50)
        # Load the Planet
        self.planet = loader.loadModel("models/planet_sphere")
        self.planet_tex = loader.loadTexture(self.pTexture[0])
        self.planet.setTexture(self.planet_tex)
        self.planet.reparentTo(render)
        self.planet.setScale(6)
        self.day_period_planet = self.planet.hprInterval(20, LVector3(0, 0, 360))
        self.day_period_planet.loop()
        
        
    def addTree(self):
            select = random.randint(0,25)
            model, tex = self.trees[select]
            scale = self.scale[select]
            self.tree = loader.loadModel(model)
            self.tree_tex = loader.loadTexture(tex)
            self.tree.setTexture(self.tree_tex, 1)
            self.placeholder2 = World.manyTrees.attachNewNode("test2")
            self.tree.instanceTo(self.placeholder2)
            #(x,y,z,0,tilt angle, start angle)
            start = random.uniform(0, 360)
            r = 6
            startR = 0 * math.pi /180
            tilt = random.uniform(-180, 180)
            tiltR = (tilt+90) * math.pi / 180
            x = r * math.sin(tiltR) * math.cos(startR) 
            y = r * math.sin(tiltR) * math.sin(startR)
            z = r * math.cos(tiltR)
            self.tree.setPosHpr(self.tree, y,z, x, 0, tilt,0 )
            self.tree.setScale(scale)
            self.day_period_tree = self.placeholder2.hprInterval((20), (0, 0, 360))
            self.day_period_tree.loop() 
    
    
            
    #plays song for menu page
    def playSong(self):
        win_s = 512          # fft size
        hop_s = win_s //  2     # hop size
        # parse command line arguments
        filename = self.song
        samplerate = 0
        if len( sys.argv ) > 2: samplerate = int(sys.argv[2])
        # create aubio source
        a_source = aubio.source(filename, samplerate, hop_s)
        samplerate = a_source.samplerate
        # create aubio tempo detection
        a_tempo = aubio.tempo("default", win_s, hop_s, samplerate)
        notes_o = aubio.notes("default", win_s, hop_s, samplerate)
        # create a simple click sound
        click = 0.7 * np.sin(2. * np.pi * np.arange(hop_s) / hop_s * samplerate / 3000.)
        # pyaudio callback, code from https://github.com/aubio/aubio/blob/master/python/demos/demo_tapthebeat.py
        def pyaudio_callback(_in_data, _frame_count, _time_info, _status):
            samples, read = a_source()
            is_beat = a_tempo(samples)
            new_note = notes_o(samples)
            if (new_note[0] != 0 and new_note[2] >= self.average):
               rand = random.randint(0,4)
               pTexture = self.textures[self.randomTex][rand]
               self.planet_tex = loader.loadTexture(pTexture)
               self.planet.setTexture(self.planet_tex)
            if is_beat:
                World.addTree(self)
            audiobuf = samples.tobytes()
            if read < hop_s:
                return (audiobuf, pyaudio.paComplete)
            return (audiobuf, pyaudio.paContinue)
        
        # create pyaudio stream with frames_per_buffer=hop_s and format=paFloat32
        p = pyaudio.PyAudio()
        pyaudio_format = pyaudio.paFloat32
        frames_per_buffer = hop_s
        n_channels = 1
        self.stream = p.open(format=pyaudio_format, channels=n_channels, rate=samplerate,
                output=True, frames_per_buffer=frames_per_buffer,
                stream_callback=pyaudio_callback)
        
        # start pyaudio stream
        self.stream.start_stream()
                
    #plays song with game 
    def playSong2(self):
        win_s = 512          # fft size
        hop_s = win_s //  2     # hop size
        # parse command line arguments
        filename = self.song
        samplerate = 0
        if len( sys.argv ) > 2: samplerate = int(sys.argv[2])
        # create aubio source
        a_source = aubio.source(filename, samplerate, hop_s)
        samplerate = a_source.samplerate
        # create aubio tempo detection
        a_tempo = aubio.tempo("default", win_s, hop_s, samplerate)
        notes_o = aubio.notes("default", win_s, hop_s, samplerate)
        # create a simple click sound
       
        # pyaudio callback, code from https://github.com/aubio/aubio/blob/master/python/demos/demo_tapthebeat.py
        def pyaudio_callback(_in_data, _frame_count, _time_info, _status):
            samples, read = a_source()
            is_beat = a_tempo(samples)
            new_note = notes_o(samples)
            if (new_note[0] != 0 and new_note[2] >= self.average):
               rand = random.randint(0,4)
               pTexture = self.textures[self.randomTex][rand]
               self.planet_tex = loader.loadTexture(pTexture)
               self.planet.setTexture(self.planet_tex)
            if new_note[2] >= 60:
               self.arrow()
            if is_beat:
                World.addTree(self)
            audiobuf = samples.tobytes()
            if read < hop_s:
                return (audiobuf, pyaudio.paComplete)
            return (audiobuf, pyaudio.paContinue)
        
        # create pyaudio stream with frames_per_buffer=hop_s and format=paFloat32
        p = pyaudio.PyAudio()
        pyaudio_format = pyaudio.paFloat32
        frames_per_buffer = hop_s
        n_channels = 1
        self.stream = p.open(format=pyaudio_format, channels=n_channels, rate=samplerate,
                output=True, frames_per_buffer=frames_per_buffer,
                stream_callback=pyaudio_callback)
        
        # start pyaudio stream
        self.stream.start_stream()  
        self.accept('space', self.pause)
        
        
w = World()
base.run()



     


