#! /usr/bin/env python
__author__ = "Raphaël LEBER"
__copyright__ = "Copyright 2019, CPE Lyon"
__credits__ = ["Baptiste Brejon, Marion Deshayes"]
__license__ = "MIT"
__version__ = "0.0.0"
__status__ = "Template"

import pygame
from math import sin,pi, cos, atan

class RadarDetectSprite(pygame.sprite.Sprite):
    """Radar sprite object

    Definition of the sensor sprite
    Attributs
    ----------
    rect : pygame.Rect
    image : pygame.Surface
    """
    def __init__(self,x,y):
        """Initialisation of Radar sprite object

        initialisation of the sensor sprite

        Parameters
        ----------
        x : int
            x-axis position of the sprite rectangle
        y : int
            y-axis position of the sprite rectangle
        """
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 1, 1)
        self.image = pygame.Surface((1,1))


class SementicWeight():

    def __init__(self):
        #self.left
        #self.middle_left
        #self.middle_right
        #self.right
        self.road = 0.0
        self.stop_mark = 0.0
        self.yield_mark = 0.0
        self.crossing_mark = 0.0
        self.car_park = 0.0
        self.not_allowed = 0.0
        self.people = 0.0
        self.path = 0.0

        self.size = 0

    


    def compute_weight(self, qtt, dist):
        dist = max(dist, 0)
        dist = min(dist, 22)
       
        if dist < 2:
            weight = 0
        else:
            weight = float(26.0 - dist) / 14.0 #+ 0.8

        #print("qtt = {0} - dist = {1} - weight = {2}".format(qtt, dist, weight))
        
        return  qtt + weight 


    def update(self, world, x, y, dist  ):
        
        if world.layers_map.is_layer(x, y, "road_only"):
            self.road = self.compute_weight(self.road, dist)

        if world.layers_map.is_layer(x, y, "stop"):
            self.stop_mark = self.compute_weight(self.stop_mark, dist)

        if world.layers_map.is_layer(x, y, "yield"):
            self.yield_mark = self.compute_weight(self.yield_mark, dist)
            
        if world.layers_map.is_layer(x, y, "crossing"):
            self.crossing_mark = self.compute_weight(self.crossing_mark, dist)   

        if world.layers_map.is_layer(x, y, "car_park"):
            self.car_park = self.compute_weight(self.car_park, dist)      

        """
        if world.layers_map.is_layer(x, y, "TODO"):
            self.not_allowed = self.compute_weight(self.not_allowed, dist)

        if world.layers_map.is_layer(x, y, "TODO"):
            self.people = self.compute_weight(self.people, dist)                                          
        """

        if world.layers_map.is_layer(x, y, "path"):
            self.path = self.compute_weight(self.path, dist)    


class ImageSegmentation():
    """ Manage camera high level information """


    def __init__(self):
        self.sensor_sprite = RadarDetectSprite(0, 0)
        self.sensor_group = pygame.sprite.Group()

        self.sensor_range = 15
        self.flag_human_detect = False
        self.danger_zone = 5        

        self.draw_camera_field = False

        self.semantic_sensor = {}

        self.zone = ("full_left", "left", "middle_left", "middle_right", "right", "full_right")

        for sub in self.zone:
            self.semantic_sensor[sub] = SementicWeight()

        self.S_distances = [ 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 ]
        self.S_angles = [ [30, 50], [9, 30], [0, 8], [-8, 0], [-30, -9], [-50, -30] ]             
        #self.S_distances = [ 4, 5]
        #self.S_angles = [  [0, 8], [-8, 0] ]    

    def update(self, world, screen, posvoiture, car_angle, human):

        Vx, Vy = posvoiture
        a = (car_angle%360)*pi/180

        for sub in self.zone:
            self.semantic_sensor[sub] = SementicWeight()     

           

        rect_filled = pygame.Surface((8,8))
        
        for ro in self.S_distances :
            for e, fi_r in enumerate(self.S_angles) :
                if(self.draw_camera_field):
                    col_i = max(fi_r,key=abs)
                    sign_i = col_i #/ abs(col_i)
                    col_i = abs(col_i)
                    color = pygame.Color(5*col_i, 128+2*sign_i, 0)

                for fi in range(fi_r[0], fi_r[1]) :
                    psi = a + (fi%360)*pi/180
                    Sx, Sy = (Vx + ro*cos(psi), Vy - ro*sin(psi) )
                        
                    Sxi = int(Sx)
                    Syi = int(Sy)

                    if(self.draw_camera_field):
                        pygame.draw.rect(rect_filled, color, rect_filled.get_rect())
                        screen.blit(rect_filled, (int(Sx * 8), int(Sy * 8)))                           

                    if Sxi >= 0 and Syi >=0 and Sxi < 160 and Syi < 90 :
                        self.semantic_sensor[self.zone[e]].size += 1
                        self.semantic_sensor[self.zone[e]].update( world, Sxi, Syi, ro)

        #for key,p in self.semantic_sensor.items():
            #print("{0} = {1}".format(key, p.size))
            

        # self.semantic_sensor["full_left"].size = 260
        # self.semantic_sensor["left"].size = 270
        # self.semantic_sensor["middle_left"].size = 180
        # self.semantic_sensor["middle_right"].size = 180
        # self.semantic_sensor["right"].size = 270
        # self.semantic_sensor["full_right"].size = 260

        self.semantic_sensor["full_left"].size = 320
        self.semantic_sensor["left"].size = 336
        self.semantic_sensor["middle_left"].size = 128
        self.semantic_sensor["middle_right"].size = 128
        self.semantic_sensor["right"].size = 336
        self.semantic_sensor["full_right"].size = 320        

        return self.semantic_sensor        

