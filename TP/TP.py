from direct.showbase.ShowBase import ShowBase
base = ShowBase()
from direct.gui.DirectGui import *
from panda3d.core import TextNode
from direct.interval.IntervalGlobal import *
import sys
import random
from panda3d.core import NodePath
from panda3d.core import LVector3
from direct.showbase import DirectObject
import math
import aubio
import numpy as np
import sys
import pyaudio
import aubio
from aubio import source, notes


class World(DirectObject.DirectObject):
    def __init__(self):
        base.setBackgroundColor(0, 0, 0)  # Set the background to black
        base.disableMouse()
        camera.setPos(0, 0, 45)  # Set the camera position (X, Y, Z)
        camera.setHpr(0, -90, 0) 
        self.scale = [0.1, 0.001, 0.1, 0.2, 0.008, 0.02, 0.003, 0.2, 0.026, 0.0015, 0.1]
        self.trees = [('models/BirchTree', 'models/birches.tif'), ('models/bonzai', 'models/bonzai.tif'), ('models/bush2', 'models/bush2.tif'), ('models/groom', 'models/groom.tif'), ('models/pine','models/pine.tif'), ('models/bush','models/bush.tif'), ('models/fern','models/fern.tif'), ('models/sapling','models/sapling.tif'), ('models/shrubbery','models/shrubbery.tif'), ('models/shrub','models/shrub.tif'), ('models/cactus','models/cactus.tif')]
        self.scaleF = [1, 2, 3.5, 1, 1, 1]
        self.flowers = [('models/daisy','models/daisy.tif'), ('models/daisy2','models/daisy2.tif'), ('models/lily','models/lily.tif'), ('models/purple','models/purple.tif'), ('models/red','models/red.tif'), ('models/tulip','models/tulip.tif')]
        self.scaleA = [0.3, 1, 0.15, 0.015, 0.15, 0.5, 0.2, 0.25, 0.3]
        self.animals = [('models/bunny','models/bunny.tif'), ('models/chicken','models/chicken.tif'), ('models/cow','models/cow.tif'), ('models/flamingo','models/flamingo.tif'), ('models/horse','models/horse.tif'), ('models/joey','models/joey.tif'), ('models/monkey','models/monkey.tif'), ('models/penguin','models/penguin.tif'), ('models/turtle','models/turtle.tif')]
        self.loadPlanets() 
        self.accept("escape", sys.exit)
        self.accept("m", self.addTree)
        self.accept("n", self.addFlower)
        self.accept("b", self.addAnimal)
        self.accept("wheel_up", self.zoomOut)
        self.accept("wheel_down", self.zoomIn)
        World.playSong(self)

    deimos = ["models/deimos_1k_tex.jpg", "models/Dgreen.jpg", "models/Dblue.jpg","models/Dpurple.jpg", "models/Dyellow.jpg"]
    cool = ["models/cool.jpg", "models/cred.jpg", "models/cgreen.jpg", "models/cpurple.jpg", "models/cblue.jpg"]
    mars = ["models/mars_1k_tex.jpg", "models/mayellow.jpg","models/magreen.jpg", "models/mapurple.jpg", "models/mablue.jpg"]
    phobos = ["models/phobos_1k_tex.jpg", "models/pred.jpg", "models/pgreen.jpg", "models/ppurple.jpg", "models/pblue.jpg"]
    earth = ["models/earth_1k_tex.jpg", "models/ered.jpg", "models/egreen.jpg", "models/epink.jpg", "models/eblue.jpg"]
    textures = [deimos, cool, mars, phobos, earth]
    randomTex = random.randint(0,4)
    pTexture = textures[randomTex]

    def zoomOut(self):
        base.camera.setPos(base.camera, 0, -5, 0)
        
    def zoomIn(self):
        base.camera.setPos(base.camera, 0, 5, 0)
    
    def loadPlanets(self):
        # Load the sky
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(50)
        # Load the Planet
        self.planet = loader.loadModel("models/planet_sphere")
        self.planet_tex = loader.loadTexture(World.pTexture[0])
        self.planet.setTexture(self.planet_tex)
        self.planet.reparentTo(render)
        self.planet.setScale(6)
        self.day_period_planet = self.planet.hprInterval(20, LVector3(0, 0, 360))
        self.day_period_planet.loop()
        
        
    def addTree(self):
            select = random.randint(0,10)
            model, tex = self.trees[select]
            scale = self.scale[select]
            self.orbit_root_tree = render.attachNewNode('orbit_root_tree')     
            self.tree = loader.loadModel(model)
            self.tree_tex = loader.loadTexture(tex)
            self.tree.setTexture(self.tree_tex, 1)
            self.tree.reparentTo(self.orbit_root_tree)
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
            self.day_period_tree = self.orbit_root_tree.hprInterval(
                (20), (0, 0, 360))
            self.day_period_tree.loop() 
    
    def addFlower(self):
            select = random.randint(0,5)
            model, tex = self.flowers[select]
            scale = self.scaleF[select]
            self.orbit_root_flower = render.attachNewNode('orbit_root_flower')     
            self.flower = loader.loadModel(model)
            self.flower_tex = loader.loadTexture(tex)
            self.flower.setTexture(self.flower_tex, 1)
            self.flower.reparentTo(self.orbit_root_flower)
            #(x,y,z,0,tilt angle, start angle)
            start = random.uniform(-180, 180)
            r = 6
            startR = 0 * math.pi /180
            tilt = random.uniform(0, 360)
            tiltR = (tilt+90) * math.pi / 180
            x = r * math.sin(tiltR) * math.cos(startR) 
            y = r * math.sin(tiltR) * math.sin(startR)
            z = r * math.cos(tiltR)
            self.flower.setPosHpr(self.flower, y,z, x, 0, tilt,0 )
            self.flower.setScale(scale)
            self.day_period_flower = self.orbit_root_flower.hprInterval(
                (20), (0, 0, 360))
            self.day_period_flower.loop()
    
    def addAnimal(self):
            select = random.randint(0,8)
            model, tex = self.animals[select]
            scale = self.scaleA[select]
            self.orbit_root_animal = render.attachNewNode('orbit_root_animal')     
            self.animal = loader.loadModel(model)
            self.animal_tex = loader.loadTexture(tex)
            self.animal.setTexture(self.animal_tex, 1)
            self.animal.reparentTo(self.orbit_root_animal)
            #(x,y,z,0,tilt angle, start angle)
            start = random.uniform(-180, 180)
            r = 6
            startR = 0 * math.pi /180
            tilt = random.uniform(0, 360)
            tiltR = (tilt+90) * math.pi / 180
            x = r * math.sin(tiltR) * math.cos(startR) 
            y = r * math.sin(tiltR) * math.sin(startR)
            z = r * math.cos(tiltR)
            self.animal.setPosHpr(self.animal, y,z, x, 0, tilt,0 )
            self.animal.setScale(scale)
            self.day_period_animal = self.orbit_root_animal.hprInterval(
                (20), (0, 0, 360))
            self.day_period_animal.loop()
            
    
    win_s = 512          # fft size
    hop_s = win_s //  2     # hop size
    # parse command line arguments
    filename = 'test3.mp3'
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
    def playSong(self):
        # pyaudio callback
        def pyaudio_callback(_in_data, _frame_count, _time_info, _status):
            samples, read = World.a_source()
            is_beat = World.a_tempo(samples)
            new_note = World.notes_o(samples)
            if (new_note[0] != 0 and new_note[2] > 55):
               rand = random.randint(0,4)
               pTexture = World.textures[World.randomTex][rand]
               self.planet_tex = loader.loadTexture(pTexture)
               self.planet.setTexture(self.planet_tex)
            if is_beat:
                World.addTree(self)
            audiobuf = samples.tobytes()
            if read < World.hop_s:
                return (audiobuf, pyaudio.paComplete)
            return (audiobuf, pyaudio.paContinue)
        
        # create pyaudio stream with frames_per_buffer=hop_s and format=paFloat32
        p = pyaudio.PyAudio()
        pyaudio_format = pyaudio.paFloat32
        frames_per_buffer = World.hop_s
        n_channels = 1
        stream = p.open(format=pyaudio_format, channels=n_channels, rate=World.samplerate,
                output=True, frames_per_buffer=frames_per_buffer,
                stream_callback=pyaudio_callback)
        
        # start pyaudio stream
        stream.start_stream()

     
w = World()
base.run()

