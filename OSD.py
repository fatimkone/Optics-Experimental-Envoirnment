import math
import sys
import tkinter
from tkinter import ttk
import ChatboxServer
import pygame
import sympy
from sympy import *
import pickle
import time
from network import Network
import ctypes
from pygame import gfxdraw
import Report

user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)  # holds value of the width of the monitor
length = user32.GetSystemMetrics(1)  # holds value of the length of the monitor
start_time = time.time()  # starts the timer for the session
pygame.display.set_caption('Optics Experimental Envoirnment')  # sets the title of window
tag = [0]
Id = 0
pygame.init()
screen = pygame.display.set_mode((width, length - 200))  # sets dimension of window
screen.fill((0, 0, 0))
objects_loaded = []
sources_loaded = []
toolbar_button = []
IncidentRays = {}
DiffRays = {}


##### tag_generator #######
# Parameters :- tag:List, obj_name:String
# Return Type :- String
# Purpose :- This is to generate a unique tag whenever an instance of
# a class is loaded it has an attribute that holds it name as there can be
# multiple of instances of one class having this unique name will help identify
# which instance needs to be manipulated
###########################
def tag_generator(tag, obj_name):
    x = tag[-1] + 1
    tag.append(x)
    Tag = obj_name + str(tag[-1])
    return Tag


##### Angle #######
# Parameters :- None
# Purpose :- This class creates the pie shape that represents the angle
# between two lines and has the ability to show what angle the pie represents
###########################
class Angle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 30
        self.theta1 = 0
        self.theta2 = 0
        self.colour = (255, 0, 0)
        self.show_theta = 0
        self.type = ""
        self.orientation = ""
        self.update()

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- Purpose is to redraw instance of class on the screen
    ###########################

    def redraw1(self):
        pygame.gfxdraw.pie(screen, int(self.x), int(self.y), self.radius, int(self.theta1),
                           int(self.theta2), self.colour)
        self.update()

    ##### update #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- To check what can be displayed on screens in terms of angles and
    # updates the screen to display them
    ###########################
    def update(self):
        if m.IA and self.type == "Incident" and self.orientation == "vertical":
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render(str(int((self.show_theta * 180) / math.pi)) + "°", True, (105, 105, 105))
            textrect = text.get_rect(center=(self.x - 10, self.y + 10))
            screen.blit(text, textrect)
        elif m.IA and self.type == "Incident" and self.orientation == "horizontal":
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render(str(int((self.show_theta * 180) / math.pi)) + "°", True, (105, 105, 105))
            textrect = text.get_rect(center=(self.x - 20, self.y + 20))
            screen.blit(text, textrect)

        elif m.RA and self.type == "Response" and self.orientation == "veritical":
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render(str(int((self.show_theta * 180) / math.pi)) + "°", True, (105, 105, 105))
            textrect = text.get_rect(center=(self.x - 10, self.y + 10))
            screen.blit(text, textrect)
        elif m.RA and self.type == "Response" and self.orientation == "horizontal":
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render(str(int((self.show_theta * 180) / math.pi)) + "°", True, (105, 105, 105))
            textrect = text.get_rect(center=(self.x + 20, self.y + 20))
            screen.blit(text, textrect)


##### Main_Objects #######
# Parameters :- name:String
# Purpose :- To act as a parent class to all manipulatable objects
###########################

class Main_Objects:
    def __init__(self, name):
        self.defined_name = name
        self.Refractive_Index = 1.00
        self.xp = (width / 2)
        self.yp = (length / 2)
        self.length = 200
        self.width = 250
        self.colour = (0, 0, 0)
        self.Property = "Transparent"
        self.graphical = pygame.draw.rect(screen, (0, 0, 0), (self.xp, self.yp, self.width, self.length))
        self.draging = False
        self.interceptors = []

    ##### redraw #######
    # Parameters :- x:Int, y:Int
    # Return Type :- Int, Object, List
    # Purpose :- To move an objects to its new position dependant on the parameter x and y by
    # filling the screen and redraw all loaded objects and instances new position and whether it can be moved
    ###########################

    def redraw(self, x, y):
        if self.interceptors:
            for i in sources_loaded:
                for obj in i.previousobj:
                    if obj.defined_name == self.defined_name:
                        return None
        else:
            screen.fill((0, 0, 0), (0, 75, 1920, 1120))
            if self.interceptors:
                first = self.interceptors[0]
                for i in objects_loaded:
                    if i.defined_name != self.defined_name and "D" not in i.defined_name:
                        i.redraw1()
                for i in sources_loaded:
                    if i != first:
                        i.redraw1()

                first.normals = []
                first.angles = []
                IncidentRays[first.defined_name] = []
                first.re = None

            else:
                for i in objects_loaded:
                    if i.defined_name != self.defined_name and "D" not in i.defined_name:
                        i.redraw1()
                for i in sources_loaded:
                    i.redraw1()
            self.graphical = pygame.draw.rect(screen, self.colour, (x, y, self.width, self.length))
            self.xp = x
            self.yp = y
            self.interceptors = []
            self.redraw1()

        return self.yp, self.xp, self.interceptors

    ##### update #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- To check what can be displayed on screens in terms of angles and
    # updates the screen to display them
    ###########################
    def update(self):
        if m.RI:
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render(str(self.Refractive_Index), True, (105, 105, 105))
            textrect = text.get_rect(center=(self.xp + 20, self.yp + 20))
            screen.blit(text, textrect)

    ##### redraw2 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- To redraw every object on screen (updating screen contents)
    ###########################

    def redraw2(self):
        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
        for i in objects_loaded:
            if "D" not in i.defined_name:
                i.redraw1()
        for i in sources_loaded:
            i.redraw1()

    ##### Simulation #######
    # Parameters :- state:Boolean, previous:Memory Address of Object, obj:Boolean
    # Return Type :- None
    # Purpose :- Checks if any sources loaded interacts with the object and manipulates
    # the source dependant on the objects properties
    ###########################

    def Simulation(self, state, previous, obj):
        if sources_loaded:
            for i in sources_loaded:
                i.Simulation(False, None, True)

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- updates instance of object on screen
    ###########################
    def redraw1(self):
        self.graphical = pygame.draw.rect(screen, self.colour,
                                          (self.xp, self.yp, self.width, self.length))
        self.update()


##### Sources #######
# Inheirts :- Main_Objects
# Parameters :- name:String
# Purpose :- Holds every attribute and operation that can be done on a source object
###########################
class Source(Main_Objects):
    def __init__(self, name):
        super().__init__(name)
        self.length = 2
        self.width = 10000
        self.endy = self.yp
        self.endx = self.width
        self.redy = self.yp
        self.redx = self.xp + 10
        self.rendx = self.xp + 20
        self.rendy = self.endy
        self.colour = (255, 0, 0)
        self.colour2 = (255, 193, 110)
        self.thickness = 4
        self.graphical = pygame.draw.line(screen, self.colour2,
                                          (self.xp, self.yp), (self.endx, self.endy), self.thickness)
        self.graphical2 = pygame.draw.line(screen, self.colour,
                                           (self.redx, self.redy), (self.rendx, self.rendy), self.thickness)
        self.m = 0
        self.findx = "((y-{0})/m)+{1}".format(self.yp, self.xp)
        self.findy = "m*(x-{0})+{1}".format(self.xp, self.yp)
        self.state = False
        self.previousobj = []
        IncidentRays[self.defined_name] = []
        self.normals = []
        self.angles = []
        self.full_name = "Source" + str(self.defined_name[-1])
        self.t_status = 0
        self.re = None

    ##### findupdate #######
    # Parameters :- x:float, y:float
    # Return Type :- self.findy:float, self.findx:float
    # Purpose :- updates equations used to find y or x coordinates of a point
    # usually called after object is moved
    ###########################
    def findupdate(self, x, y):
        self.findx = "((y-{0})/m)+{1}".format(y, x)
        self.findy = "m*(x-{0})+{1}".format(x, y)
        return self.findy, self.findx

    ##### blackout #######
    # Parameters :- None
    # Return Type :- self.colour: triplet
    # Purpose :- isolates the red rotation button from source
    # usually done to sources created due to an interaction with an object
    ###########################
    def blackout(self):
        self.colour = (0, 0, 0)
        self.redraw2()
        return self.colour

    ##### anglesfunc #######
    # Parameters :- theta1:float, theta2:float, orientation:string, coord:list, nor:int,
    # nor2:int, sign:string, source:Memory Address of Object
    # Return Type :- None
    # Purpose :- creates and displays (if allowed to be shown) the angles dependant
    # on the parameters using the Angle class
    ###########################
    def anglesfunc(self, theta1, theta2, orientation, coord, nor, nor2, sign, source):
        angle = Angle()
        IncidentRays[source].append(angle)
        self.angles.append(angle)
        angle2 = Angle()
        IncidentRays[source].append(angle2)
        self.angles.append(angle2)
        if sign == "reflecting":
            angle.show_theta = theta1
            angle.type = "Incident"
            angle2.show_theta = theta2
            angle2.type = "Response"
            angle.orientation = orientation
            angle2.orientation = orientation
            angle.theta1 = -((theta1 * 180) / math.pi) + nor
            angle.theta2 = nor
            angle.x = coord[1]
            angle.y = coord[2]
            angle2.theta1 = nor2
            angle2.theta2 = (theta2 * 180) / math.pi + nor2
            angle2.x = coord[1]
            angle2.y = coord[2]
        elif orientation == "reverse":
            angle.show_theta = theta1
            angle.type = "Incident"
            angle2.show_theta = theta2
            angle2.type = "Response"
            angle.orientation = "vertical"
            angle2.orientation = "vertical"
            angle.theta2 = ((theta1 * 180) / math.pi) + nor
            angle.theta1 = nor
            angle.x = coord[1]
            angle.y = coord[2]
            angle2.theta1 = nor2
            angle2.theta2 = (theta2 * 180) / math.pi + nor2
            angle2.x = coord[1]
            angle2.y = coord[2]
        elif orientation == "reverse2":
            angle.show_theta = theta1
            angle.type = "Incident"
            angle2.show_theta = theta2
            angle2.type = "Response"
            angle.orientation = "horizontal"
            angle2.orientation = "horizontal"
            angle.theta2 = ((theta1 * 180) / math.pi) + nor
            angle.theta1 = nor
            angle.x = coord[1]
            angle.y = coord[2]
            angle2.theta1 = nor2
            angle2.theta2 = (theta2 * 180) / math.pi + nor2
            angle2.x = coord[1]
            angle2.y = coord[2]
        else:
            angle.show_theta = theta1
            angle.type = "Incident"
            angle2.show_theta = theta2
            angle2.type = "Response"
            angle.orientation = orientation
            angle2.orientation = orientation
            angle.theta1 = eval(sign + str((theta1 * 180) / math.pi)) + nor
            angle.theta2 = nor
            angle.x = coord[1]
            angle.y = coord[2]
            angle2.theta2 = nor2
            angle2.theta1 = eval(sign + str((theta2 * 180) / math.pi)) + nor2
            angle2.x = coord[1]
            angle2.y = coord[2]

    ##### normalfunc #######
    # Parameters :- orientation:string, source:Memory Address of Object, coord:list
    # Return Type :- None
    # Purpose :- creates a normal line dependant on the propagation position
    ###########################
    def normalfunc(self, orientation, source, coord):
        Tag = tag_generator(tag, "N")
        normal = Source(Tag)
        IncidentRays[source.defined_name].append(normal)
        source.normals.append(normal)
        normal.blackout()
        normal.thickness = 2
        if orientation == "top":
            normal.xp = coord[1]
            normal.yp = coord[2] - 50
            normal.endx = coord[1]
            normal.endy = coord[2] + 50
        else:
            normal.xp = coord[1] - 50
            normal.yp = coord[2]
            normal.endx = coord[1] + 50
            normal.endy = coord[2]
        normal.colour2 = (255, 0, 0)

    ##### InsideSimulation #######
    # Parameters :- source:Memory Address of Object, initialsource:Memory Address of initial source, obj:boolean
    # Return Type :- self.endx:float, self.endy:float
    # Purpose :- method responsible for handling the interaction of the rays within an object
    ###########################
    def InsideSimulation(self, source, initialsource, obj):
        coord = []
        intercept_x = []
        intercept_y = []
        if self.m == 0:
            self.redraw1()
        else:

            if initialsource.m < 0:
                eq = self.findx.replace("m", "{0}".format(-self.m))
                xcoord = eval(eq.replace("y", "{0}".format(source.yp)))
                intercept_x.append((xcoord, source.yp))
                eq3 = self.findx.replace("m", "{0}".format(-self.m))

                xcoord = eval(eq3.replace("y", "source.yp+source.length"))
                intercept_x.append((xcoord, source.yp + source.length))
                eq4 = self.findy.replace("m", "{0}".format(-self.m))
                ycoord = eval(eq4.replace("x", "source.xp+source.width"))
                intercept_y.append((source.xp + source.width, ycoord))
                intercept_x = list(dict.fromkeys(intercept_x))
                intercept_y = list(dict.fromkeys(intercept_y))
            else:
                eq = self.findx.replace("m", "{0}".format(self.m))
                xcoord = eval(eq.replace("y", "{0}".format(source.yp)))
                intercept_x.append((xcoord, source.yp))
                eq3 = self.findx.replace("m", "{0}".format(self.m))
                xcoord = eval(eq3.replace("y", "source.yp+source.length"))
                intercept_x.append((xcoord, source.yp + source.length))
                eq4 = self.findy.replace("m", "{0}".format(self.m))
                ycoord = eval(eq4.replace("x", "source.xp+source.width"))
                intercept_y.append((source.xp + source.width, ycoord))
                intercept_x = list(dict.fromkeys(intercept_x))
                intercept_y = list(dict.fromkeys(intercept_y))

            if (self.yp == source.yp + source.width or self.yp == source.yp) and self.m > 0:
                for co in intercept_x:
                    if source.xp + source.width >= co[0] >= source.xp != co[0]:
                        coord.append([source, co[0], co[1], "top"])
                    else:
                        pass
                for co in intercept_y:
                    if source.yp <= co[1] <= source.yp + source.length and co[1] != self.yp:

                        coord.append([source, co[0], co[1], "side"])
                    else:

                        pass
            else:
                for co in intercept_x:
                    if source.xp + source.width >= co[0] >= source.xp != co[0] and co[0] != self.xp:

                        coord.append([source, co[0], co[1], "top"])

                    else:
                        pass
                for co in intercept_y:
                    if source.yp <= co[1] <= source.yp + source.length and co[1] != self.yp:

                        coord.append([source, co[0], co[1], "side"])
                    else:

                        pass
        if not coord:
            self.redraw1()

        else:
            for i in coord:
                distance = math.sqrt(((i[1] - self.xp) ** 2) + ((i[2] - self.yp) ** 2))

                in1 = coord.index(i)

                coord[in1].append(distance)

            coord = sorted(coord, key=lambda x: x[-1], reverse=True)

            coord = coord[0]

            if coord[0].Property != "Reflective" or coord[0].Property != "Stop" or "D" not in coord[
                0].defined_name:
                if self.m == 0:
                    self.redraw1()
                else:
                    if coord[3] == "top":
                        self.normalfunc("top", initialsource, coord)
                    else:
                        self.normalfunc("side", initialsource, coord)

                    self.endx = coord[1]
                    self.endy = coord[2]
                    self.findupdate(coord[1], coord[2])
                    self.redraw1()
                    n2 = source.Refractive_Index
                    critical = asin(1 / n2)
                    m1 = self.m
                    m2 = 0

                    theta1 = atan(abs((m2 - m1) / (1 + m1 * m2)))
                    if coord[3] == "top":
                        theta1 = (math.pi / 2) - theta1
                        if theta1 > critical:
                            Tag = tag_generator(tag, "S")
                            reflected_ray = Source(Tag)
                            source.interceptors.append(reflected_ray)
                            IncidentRays[initialsource.defined_name].append(reflected_ray)
                            reflected_ray.m = -self.m
                            if self.m < 0:
                                self.anglesfunc(theta1, theta1, "vertical", coord, 270, 270, "reflecting",
                                                initialsource.defined_name)

                            elif self.m > 0 and coord[2] == source.yp:
                                self.anglesfunc(theta1, theta1, "vertical", coord, 90, 90, "reflecting",
                                                initialsource.defined_name)
                                initialsource.re = "pos"

                            elif self.m > 0 and coord[2] == source.yp + source.length:
                                self.anglesfunc(theta1, theta1, "vertical", coord, -90, 270, "reflecting",
                                                initialsource.defined_name)
                                initialsource.re = "neg"

                            if self.m < 0 or (self.m > 0 and coord[2] == source.yp + source.length):
                                eq = reflected_ray.findy.replace("m", "{0}".format(-reflected_ray.m))
                                reflected_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                            else:
                                eq = reflected_ray.findy.replace("m", "{0}".format(reflected_ray.m))
                                reflected_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                            reflected_ray.state = True
                            reflected_ray.xp = coord[1]
                            reflected_ray.yp = coord[2]
                            reflected_ray.findupdate(coord[1], coord[2])
                            reflected_ray.blackout()

                            reflected_ray.InsideSimulation(source, initialsource, obj)

                        elif theta1 < critical:

                            if theta1 < critical and theta1 != 0:
                                self.endx = coord[1]
                                self.endy = coord[2]
                                theta1 = atan(abs((m2 - m1) / (1 + m1 * m2)))
                                t2 = asin((sin(theta1) / n2))
                                t2 = (math.pi / 2) - t2
                                theta1 = (math.pi / 2) - theta1
                                theta2 = asin((sin(theta1) * n2))
                                newm1 = tan(t2)
                                if initialsource.re == "side":
                                    if self.m > 0:
                                        self.anglesfunc(theta1, theta2, "horizontal", coord, 90, 270, "-",
                                                        initialsource.defined_name)

                                    elif self.m < 0 and coord[2] == source.yp:
                                        self.anglesfunc(theta1, theta2, "horizontal", coord, 90, 270, "-",
                                                        initialsource.defined_name)
                                        initialsource.re = "side"

                                    elif self.m < 0 and coord[2] == source.yp + source.length:
                                        self.anglesfunc(theta1, theta2, "horizontal", coord, 270, 90, "+",
                                                        initialsource.defined_name)
                                        initialsource.re = "side2"


                                elif self.m < 0:
                                    self.anglesfunc(theta1, theta2, "vertical", coord, 90, 270, "+",
                                                    initialsource.defined_name)

                                elif self.m > 0:
                                    theta2 = (math.pi / 2) - theta2
                                    self.anglesfunc(theta1, theta2, "vertical", coord, 90, 270, "+",
                                                    initialsource.defined_name)
                                Tag = tag_generator(tag, "S")
                                refracted_ray = Source(Tag)
                                source.interceptors.append(refracted_ray)
                                IncidentRays[initialsource.defined_name].append(refracted_ray)

                                refracted_ray.state = True
                                refracted_ray.xp = coord[1]
                                refracted_ray.yp = coord[2]
                                refracted_ray.findupdate(coord[1], coord[2])
                                refracted_ray.blackout()
                                if initialsource.re == "pos":
                                    refracted_ray.m = newm1
                                    eq = refracted_ray.findy.replace("m", "{0}".format(-refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                elif initialsource.re == "neg":
                                    refracted_ray.m = newm1
                                    eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                elif initialsource.re == "side":
                                    refracted_ray.m = newm1
                                    refracted_ray.width = -10000
                                    eq = refracted_ray.findy.replace("m", "{0}".format(-refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))

                                elif initialsource.re == "side2":
                                    refracted_ray.m = newm1
                                    eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(-self.width)))
                                    refracted_ray.endx = -10000

                                elif initialsource.re is None:
                                    if self.m > 0:
                                        refracted_ray.m = newm1
                                        eq = refracted_ray.findy.replace("m", "{0}".format(-refracted_ray.m))
                                        refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                    else:
                                        refracted_ray.m = -newm1
                                        eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                        refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                initialsource.previousobj.append(source)
                                refracted_ray.Simulation(self.state, initialsource, obj)
                            else:
                                source.redraw1(m)
                    else:
                        if theta1 > critical:
                            theta1 = theta1
                            theta2 = theta1

                            if self.m > 0 and coord[3] == "side":
                                self.anglesfunc(theta1, theta1, "horizontal", coord, 180, 180, "reflecting",
                                                initialsource.defined_name)
                                initialsource.re = "side"

                            Tag = tag_generator(tag, "S")
                            reflected_ray = Source(Tag)
                            source.interceptors.append(reflected_ray)
                            IncidentRays[initialsource.defined_name].append(reflected_ray)
                            reflected_ray.m = -self.m
                            reflected_ray.state = True
                            reflected_ray.xp = coord[1]
                            reflected_ray.yp = coord[2]
                            reflected_ray.findupdate(coord[1], coord[2])
                            reflected_ray.blackout()
                            eq = reflected_ray.findy.replace("m", "{0}".format(reflected_ray.m))
                            reflected_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                            reflected_ray.InsideSimulation(source, initialsource, obj)
                        elif theta1 < critical and theta1 != 0:
                            self.endx = coord[1]
                            self.endy = coord[2]
                            theta2 = asin((sin(theta1) * n2))
                            newm1 = tan(theta2)
                            if initialsource.re == "pos":
                                if self.m < 0:
                                    self.anglesfunc(theta1, theta2, "reverse2", coord, 180, 0, "+",
                                                    initialsource.defined_name)
                                else:
                                    self.anglesfunc(theta1, theta2, "horizontal", coord, 180, 0, "+",
                                                    initialsource.defined_name)
                            elif initialsource.re == "neg":
                                self.anglesfunc(theta1, theta2, "horizontal", coord, 180, 0, "-",
                                                initialsource.defined_name)

                            elif self.m < 0 and coord[3] == "side":
                                self.anglesfunc(theta1, theta2, "horizontal", coord, 180, 0, "-",
                                                initialsource.defined_name)

                            elif self.m > 0 and coord[3] == "side":
                                self.anglesfunc(theta1, theta2, "horizontal", coord, 180, 0, "-",
                                                initialsource.defined_name)

                            Tag = tag_generator(tag, "S")
                            refracted_ray = Source(Tag)
                            source.interceptors.append(refracted_ray)
                            IncidentRays[initialsource.defined_name].append(refracted_ray)

                            refracted_ray.state = True
                            refracted_ray.xp = coord[1]
                            refracted_ray.yp = coord[2]
                            refracted_ray.findupdate(coord[1], coord[2])
                            refracted_ray.blackout()
                            if initialsource.re == "pos":
                                if self.m > 0:
                                    refracted_ray.m = newm1
                                    eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                else:
                                    refracted_ray.m = newm1
                                    eq = refracted_ray.findy.replace("m", "{0}".format(-refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                            elif initialsource.re == "neg":
                                refracted_ray.m = -newm1
                                eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                            elif initialsource.re is None:
                                if self.m > 0:
                                    refracted_ray.m = -newm1
                                    eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                else:
                                    refracted_ray.m = -newm1
                                    eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                            initialsource.previousobj.append(source)
                            refracted_ray.Simulation(self.state, initialsource, obj)
                        else:
                            source.redraw1(m)

            return self.endx, self.endy

    ##### Simulation #######
    # Parameters :- state:Boolean, previous:Memory Address of Object, obj:Boolean
    # Return Type :- self.endx:float, self.endy:float
    # Purpose :- Checks if any sources loaded interacts with the object and manipulates
    # the source dependant on the objects properties
    ###########################
    def Simulation(self, state, previous, obj):
        coord = []
        intercept_x = []
        intercept_y = []
        if state:
            previous.re = None
        for i in objects_loaded:
            if state:
                if i in previous.previousobj:
                    continue
            if "SC" in i.defined_name:
                if self.m == 0:
                    continue
                else:
                    dist = math.sqrt((i.xp - self.xp) ** 2 + (i.yp - self.yp) ** 2)
                    x, y = sympy.symbols("x,y")
                    ep = self.findy.replace("m", str(self.m))
                    ep = i.Equation.replace("y", "{0}".format(ep))
                    sol1 = sympy.solve(eval(ep), x)
                    sol = []
                    intery = []
                    for p in sol1:
                        try:
                            if p <= self.xp:
                                continue
                            else:
                                sol.append(p)
                        except TypeError:
                            continue

                    if not sol:
                        self.redraw1()
                    else:
                        for point in sol:
                            ep = self.findy.replace("m", str(self.m))
                            ycoord = eval(ep.replace("x", str(point)))
                            intery.append([point, ycoord])
                        interyp = []
                        for pair in intery:
                            if pair[1] <= i.yp:
                                interyp.append(pair)
                            else:
                                intery.remove(pair)
                        for pair in interyp:
                            coord.append([i, pair[0], pair[1]])
                        ep = self.findx.replace("m", str(self.m))
                        xcoord = eval(ep.replace("y", str(i.yp)))
                        if i.xp - i.Radius <= xcoord <= i.xp + i.Radius:
                            coord.append([i, xcoord, i.yp])


            else:
                if self.m == 0:
                    pass
                else:

                    eq = self.findx.replace("m", "{0}".format(self.m))
                    xcoord = eval(eq.replace("y", "{0}".format(i.yp)))
                    intercept_x.append((xcoord, i.yp))
                    eq3 = self.findx.replace("m", "{0}".format(self.m))
                    xcoord = eval(eq3.replace("y", "{0}".format(i.yp + i.length)))
                    intercept_x.append((xcoord, i.yp + i.length))
                    eq2 = self.findy.replace("m", "{0}".format(self.m))
                    ycoord = eval(eq2.replace("x", "{0}".format(i.xp)))
                    intercept_y.append((i.xp, ycoord))
                    eq4 = self.findy.replace("m", "{0}".format(self.m))
                    ycoord = eval(eq4.replace("x", "{0}".format(i.xp + i.width)))
                    intercept_y.append((i.xp + i.width, ycoord))
                    intercept_x = list(dict.fromkeys(intercept_x))
                    intercept_y = list(dict.fromkeys(intercept_y))

                    for co in intercept_x:
                        if not state:
                            if i.xp <= co[0] <= i.xp + i.width and co[0] > self.xp:
                                coord.append([i, co[0], co[1], "top"])
                            else:
                                pass
                        else:
                            if i.xp <= co[0] <= i.xp + i.width and co[0] != self.xp and co[0] > self.xp:
                                coord.append([i, co[0], co[1], "top"])
                            else:
                                pass
                    for co in intercept_y:
                        if i.yp <= co[1] <= i.yp + i.length and co[1] != self.yp:
                            coord.append([i, co[0], co[1], "side"])
                        else:
                            pass

        if not coord:
            self.statechange()
        else:
            if previous is not None:
                if not previous.previousobj:
                    for i in coord:
                        if i[0] in previous.previousobj:
                            coord.remove(i)

            for i in coord:
                distance = math.sqrt(((i[1] - self.xp) ** 2) + ((i[2] - self.yp) ** 2))

                in1 = coord.index(i)

                coord[in1].append(distance)

            coord = sorted(coord, key=lambda x: x[-1])
            condition = True
            if "SC" in coord[0][0].defined_name:
                if coord[0][2] != coord[0][0].yp and coord[1][2] != coord[0][0].yp:
                    condition = False
                    self.statechange()
                elif coord[0][2] < coord[0][0].yp:
                    coord = [coord[1]]

                else:
                    coord = [coord[0]]
            else:
                coord = [coord[0]]
            origin = "temp"
            if condition:
                for sources in sources_loaded:
                    if sources.defined_name == self.defined_name:
                        origin = sources

                for source in coord:
                    if previous is not None:
                        previous.previousobj.append(source[0])
                    self.endx = source[1]
                    self.endy = source[2]

                    if source[0].Property == "Stop":
                        self.endx = source[1]
                        self.endy = source[2]
                        self.redraw1()
                    elif source[0].Property == "Reflective":
                        Tag = tag_generator(tag, "S")
                        reflected_ray = Source(Tag)
                        if not state:
                            IncidentRays[self.defined_name].append(reflected_ray)
                        else:
                            IncidentRays[previous.defined_name].append(reflected_ray)
                        if obj:
                            source[0].interceptors.append(origin)
                            source[0].interceptors.append(reflected_ray)
                        else:
                            source[0].interceptors.append(reflected_ray)
                        IncidentRays[self.defined_name].append(reflected_ray)
                        self.endx = source[1]
                        self.endy = source[2]
                        reflected_ray.m = -self.m
                        reflected_ray.state = True
                        reflected_ray.xp = source[1]
                        reflected_ray.yp = source[2]
                        reflected_ray.blackout()
                        reflected_ray.findupdate(source[1], source[2])
                        eq = reflected_ray.findy.replace("m", "{0}".format(reflected_ray.m))
                        reflected_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                        reflected_ray.endx = self.width

                        if state:
                            reflected_ray.Simulation(True, previous, obj)
                        else:
                            reflected_ray.Simulation(True, origin, obj)
                    elif source[0].Property != "Reflective" or source[0].Property != "Stop" or "D" not in source[
                        0].defined_name:
                        n2 = source[0].Refractive_Index
                        m1 = self.m
                        if self.m == 0:
                            self.redraw1()
                        else:
                            if "SC" in source[0].defined_name:
                                if state:
                                    previous.previousobj.append(source[0])
                                else:
                                    self.previousobj.append(source[0])
                                m2 = 0
                                theta1 = atan(abs((m2 - m1) / (1 + m2 * m1)))
                                theta2 = asin(sin(theta1) / n2)
                                critical = asin(1 / n2)
                                if state:
                                    self.normalfunc("top", previous, source)
                                else:
                                    self.normalfunc("top", origin, source)
                                theta2 = (math.pi / 2) - theta2

                                if theta1 != 0 and theta1 < critical:
                                    self.endx = source[1]
                                    self.endy = source[2]
                                    m3 = tan(theta2)

                                    Tag = tag_generator(tag, "S")
                                    refracted_ray = Source(Tag)
                                    if state == 0:
                                        if obj:
                                            source[0].interceptors.append(origin)
                                            source[0].interceptors.append(refracted_ray)
                                        else:
                                            source[0].interceptors.append(refracted_ray)
                                        IncidentRays[self.defined_name].append(refracted_ray)
                                    else:
                                        IncidentRays[previous.defined_name].append(refracted_ray)

                                    if self.m < 0:
                                        theta2 = math.pi / 2 - theta2
                                        theta1 = math.pi / 2 - theta1
                                        if state:
                                            self.anglesfunc(theta1, theta2, "reverse", source, 90, 270, "+",
                                                            previous.defined_name)
                                        else:
                                            self.anglesfunc(theta1, theta2, "reverse", source, 90, 270, "-",
                                                            self.defined_name)
                                        refracted_ray.m = -m3
                                        refracted_ray.state = True
                                        refracted_ray.xp = source[1]
                                        refracted_ray.yp = source[2]
                                        refracted_ray.blackout()
                                        refracted_ray.findupdate(source[1], source[2])
                                        eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                        refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                        if state:
                                            refracted_ray.Simulation(True, previous, obj)
                                        else:
                                            refracted_ray.Simulation(True, origin, obj)
                                    else:
                                        theta2 = theta2 + math.pi / 2
                                        m3 = tan(theta2)
                                        theta1 = theta1 - math.pi / 2
                                        theta2 = theta2 - math.pi / 2
                                        if state:
                                            self.anglesfunc(theta1, theta2, "vertical", source, 270, 90, "+",
                                                            previous.defined_name)
                                        else:
                                            self.anglesfunc(theta1, theta2, "vertical", source, 270, 90, "+",
                                                            self.defined_name)
                                        refracted_ray.m = -m3
                                        refracted_ray.state = True
                                        refracted_ray.xp = source[1]
                                        refracted_ray.yp = source[2]
                                        refracted_ray.blackout()
                                        refracted_ray.findupdate(source[1], source[2])
                                        eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                        refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                        if state:
                                            refracted_ray.Simulation(True, previous, obj)
                                        else:
                                            refracted_ray.Simulation(True, origin, obj)
                                elif theta1 != 0 and theta1 > critical and self.m < 0:
                                    theta1 = math.pi / 2 - theta1
                                    theta2 = (math.pi / 2) - theta2
                                    if state:
                                        self.anglesfunc(theta1, theta2, "reverse", source, 90, 270, "+",
                                                        previous.defined_name)
                                    else:
                                        self.anglesfunc(theta1, theta2, "reverse", source, 90, 270, "+",
                                                        self.defined_name)
                                    theta2 = (math.pi / 2 - theta2) - (math.pi / 2)
                                    m3 = tan(theta2 + math.pi / 2)
                                    Tag = tag_generator(tag, "S")
                                    refracted_ray = Source(Tag)
                                    if not state:
                                        if obj:
                                            source[0].interceptors.append(origin)
                                            source[0].interceptors.append(refracted_ray)
                                        else:
                                            source[0].interceptors.append(refracted_ray)
                                        IncidentRays[self.defined_name].append(refracted_ray)
                                    else:
                                        IncidentRays[previous.defined_name].append(refracted_ray)

                                    refracted_ray.m = -m3
                                    refracted_ray.state = True
                                    refracted_ray.xp = source[1]
                                    refracted_ray.yp = source[2]
                                    refracted_ray.blackout()
                                    refracted_ray.findupdate(source[1], source[2])
                                    eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                    if state:
                                        refracted_ray.Simulation(True, previous, obj)
                                    else:
                                        refracted_ray.Simulation(True, origin, obj)
                                elif theta1 != 0 and theta1 > critical and self.m > 0:
                                    if state:

                                        self.anglesfunc(theta1, theta1, "vertical", source, 270, 270, "reflecting",
                                                        previous.defined_name)
                                    else:
                                        self.anglesfunc(theta1, theta1, "vertical", source, 270, 270, "reflecting",
                                                        self.defined_name)

                                    Tag = tag_generator(tag, "S")
                                    reflected_ray = Source(Tag)
                                    if not state:
                                        if obj:
                                            source[0].interceptors.append(origin)
                                            source[0].interceptors.append(reflected_ray)
                                        else:
                                            source[0].interceptors.append(reflected_ray)
                                        IncidentRays[self.defined_name].append(reflected_ray)
                                    else:
                                        IncidentRays[previous.defined_name].append(reflected_ray)

                                    reflected_ray.m = -self.m
                                    reflected_ray.state = True
                                    reflected_ray.xp = source[1]
                                    reflected_ray.yp = source[2]
                                    reflected_ray.blackout()
                                    eq = reflected_ray.findy.replace("m", "{0}".format(reflected_ray.m))
                                    reflected_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                    if state:
                                        reflected_ray.Simulation(True, previous, obj)
                                    else:
                                        reflected_ray.Simulation(True, origin, obj)
                                elif theta1 != 0 and self.m == 0:
                                    if state:
                                        self.anglesfunc(theta1, theta2, "vertical", source, 90, 270, "+",
                                                        previous.defined_name)
                                    else:
                                        self.anglesfunc(theta1, theta2, "vertical", source, 90, 270, "+",
                                                        self.defined_name)

                                    self.endx = source[1]
                                    self.endy = source[2]
                                    m3 = tan(theta2)
                                    Tag = tag_generator(tag, "S")
                                    refracted_ray = Source(Tag)
                                    if not state:
                                        if obj:
                                            source[0].interceptors.append(origin)
                                            source[0].interceptors.append(refracted_ray)
                                        else:
                                            source[0].interceptors.append(refracted_ray)
                                        IncidentRays[self.defined_name].append(refracted_ray)
                                    else:
                                        IncidentRays[previous.defined_name].append(refracted_ray)

                                    refracted_ray.m = -m3
                                    refracted_ray.state = True
                                    refracted_ray.xp = source[1]
                                    refracted_ray.yp = source[2]
                                    refracted_ray.blackout()
                                    refracted_ray.findupdate(source[1], source[2])
                                    eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                    if state:
                                        refracted_ray.Simulation(True, previous, obj)
                                    else:
                                        refracted_ray.Simulation(True, origin, obj)
                                elif theta1 != 0 and theta1 == critical:
                                    if state:
                                        self.anglesfunc(theta1, theta2, "vertical", source, 90, 270, "+",
                                                        previous.defined_name)
                                    else:
                                        self.anglesfunc(theta1, theta2, "vertical", source, 90, 270, "+",
                                                        self.defined_name)
                                    self.endx = source[1]
                                    self.endy = source[2]
                                    Tag = tag_generator(tag, "S")
                                    refracted_ray = Source(Tag)
                                    if not state:
                                        if obj:
                                            source[0].interceptors.append(origin)
                                            source[0].interceptors.append(refracted_ray)
                                        else:
                                            source[0].interceptors.append(refracted_ray)
                                        IncidentRays[self.defined_name].append(refracted_ray)
                                    else:
                                        IncidentRays[previous.defined_name].append(refracted_ray)

                                    refracted_ray.m = 0
                                    refracted_ray.state = True
                                    refracted_ray.xp = source[1]
                                    refracted_ray.yp = source[2]
                                    refracted_ray.findupdate(source[1], source[2])
                                    refracted_ray.blackout()
                                    eq = refracted_ray.findy.replace("m", "{0}".format(-refracted_ray.m))
                                    refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                    if state:
                                        refracted_ray.Simulation(True, previous, obj)
                                    else:
                                        refracted_ray.Simulation(True, origin, obj)
                                else:

                                    self.redraw1()

                            else:

                                if source[3] == "top":
                                    if state:
                                        self.normalfunc("top", previous, source)
                                    else:
                                        self.normalfunc("top", origin, source)
                                else:
                                    if state:
                                        self.normalfunc("side", previous, source)
                                    else:
                                        self.normalfunc("side", origin, source)
                                m2 = self.m
                                m1 = 0
                                if source[3] == "top" and self.m > 0:
                                    theta1 = atan(abs((m2 - m1) / (1 + m1 * m2)))
                                    theta1 = (math.pi / 2) - theta1
                                    theta2 = asin((sin(theta1) / n2))
                                    newm1 = tan((math.pi / 2) - theta2)

                                elif source[3] == "top" and self.m < 0:
                                    theta1 = atan(abs((m2 - m1) / (1 + m1 * m2)))
                                    theta2 = asin((sin(theta1) / n2))
                                    theta1 = (math.pi / 2) - theta1
                                    theta2 = (math.pi / 2) - theta2
                                    newm1 = tan(theta2)

                                else:
                                    theta1 = atan(abs((m2 - m1) / (1 + m1 * m2)))
                                    theta2 = asin((sin(theta1) / n2))
                                    newm1 = tan(theta2)

                                if theta1 != 0:
                                    if self.m > 0 and source[3] == "side":
                                        self.anglesfunc(theta1, theta2, "reverse2", source, 180, 0, "+",
                                                        self.defined_name)

                                    elif self.m < 0 and source[3] == "side":
                                        if state:
                                            self.anglesfunc(theta1, theta2, "horizontal", source, 180, 0, "-",
                                                            previous.defined_name)
                                        else:
                                            self.anglesfunc(theta1, theta2, "horizontal", source, 180, 0, "-",
                                                            self.defined_name)

                                    elif self.m > 0 and source[3] == "top":
                                        if state:
                                            self.anglesfunc(theta1, theta2, "vertical", source, 270, 90, "-",
                                                            previous.defined_name)
                                        else:
                                            self.anglesfunc(theta1, theta2, "vertical", source, 270, 90, "-",
                                                            self.defined_name)

                                    elif self.m < 0 and source[3] == "top":
                                        theta2 = math.pi / 2 - theta2
                                        if state:
                                            self.anglesfunc(theta1, theta2, "reverse", source, 90, 270, "+",
                                                            previous.defined_name)
                                        else:
                                            self.anglesfunc(theta1, theta2, "reverse", source, 90, 270, "+",
                                                            self.defined_name)

                                    Tag = tag_generator(tag, "S")
                                    refracted_ray = Source(Tag)

                                    if not state:
                                        if obj:
                                            source[0].interceptors.append(origin)
                                            source[0].interceptors.append(refracted_ray)
                                        else:
                                            source[0].interceptors.append(refracted_ray)

                                        IncidentRays[self.defined_name].append(refracted_ray)

                                    else:
                                        IncidentRays[previous.defined_name].append(refracted_ray)

                                    refracted_ray.xp = source[1]
                                    refracted_ray.yp = source[2]

                                    refracted_ray.findupdate(source[1], source[2])

                                    refracted_ray.state = True
                                    if self.m < 0:
                                        if not state:
                                            refracted_ray.m = newm1
                                            eq = refracted_ray.findy.replace("m", "{0}".format(-refracted_ray.m))
                                            refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                        else:
                                            refracted_ray.m = -newm1
                                            eq = refracted_ray.findy.replace("m", "{0}".format(refracted_ray.m))
                                            refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))

                                    else:
                                        if state:
                                            refracted_ray.m = -newm1
                                            eq = refracted_ray.findy.replace("m", "{0}".format(-refracted_ray.m))
                                            refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                        else:
                                            refracted_ray.m = newm1
                                            eq = refracted_ray.findy.replace("m", "{0}".format(-refracted_ray.m))
                                            refracted_ray.endy = eval(eq.replace("x", "{0}".format(self.width)))
                                    self.findupdate(source[1], source[2])
                                    if state:
                                        refracted_ray.InsideSimulation(source[0], previous, obj)
                                    else:
                                        refracted_ray.InsideSimulation(source[0], origin, obj)

                                else:
                                    self.redraw1()
        self.redraw2()
        if previous is not None:
            previous.redraw2()
        return self.endx, self.endy

    ##### statechange #######
    # Parameters :- None
    # Return Type :- self.endy:float, self.endx:float, self.graphical:function
    # Purpose :- changes state and increases the end of line when the source is no longer interacting with any object
    ###########################
    def statechange(self):
        self.state = False
        self.endx = self.width
        new_y = self.m * (self.width - self.xp) + self.yp
        self.graphical = pygame.draw.line(screen, self.colour2, (self.xp, self.yp), (self.endx, new_y), self.thickness)
        self.endy = int(new_y)
        return self.endy, self.endx, self.graphical

    ##### redraw #######
    # Parameters :- x:Int, y:Int
    # Return Type :- Int, Object, List
    # Purpose :- To move an objects to its new position dependant on the parameter x and y by
    # filling the screen and redraw all loaded objects and instances new postion and whether it can be moved
    ###########################
    def redraw(self, x, y):
        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
        for i in objects_loaded:
            if "D" not in i.defined_name:
                i.redraw1()
        for i in sources_loaded:
            if i.defined_name != self.defined_name:
                i.redraw1()
        new_y = self.m * (self.endx - x) + y
        start_y = self.m * ((x + 10) - x) + y
        end_y = self.m * ((x + 20) - x) + y
        self.graphical = pygame.draw.line(screen, self.colour2, (x, y), (self.endx, new_y), self.thickness)
        self.graphical2 = pygame.draw.line(screen, self.colour, (x + 10, start_y), (x + 20, end_y), self.thickness)
        self.redx = x + 10
        self.rendx = x + 20
        self.rendy = end_y
        self.redy = start_y
        self.xp = x
        self.yp = y
        self.endy = new_y
        self.m = ((self.yp - self.endy) / (self.xp - self.endx))
        self.findupdate(x, y)
        IncidentRays[self.defined_name] = []
        self.normals = []
        self.angles = []
        self.previousobj = []
        self.re = None
        return self.graphical, self.xp, self.yp, self.redy, self.redx, self.rendy, self.rendx, self.endy, self.m

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- updates instance of object on screen
    ###########################
    def redraw1(self):
        self.graphical = pygame.draw.line(screen, self.colour2, (self.xp, self.yp), (self.endx, self.endy),
                                          self.thickness)
        self.graphical2 = pygame.draw.line(screen, self.colour, (self.redx, self.redy), (self.rendx, self.rendy),
                                           self.thickness)
        for i in IncidentRays[self.defined_name]:
            i.redraw1()
        for i in self.normals:
            i.redraw1()
        for i in self.angles:
            i.redraw1()

    ##### rotate #######
    # Parameters :- mousex:float, mousey:float
    # Return Type :- self.graphical:function, self.graphical2:function, self.endy:float,
    # self.redy:float, self.rendy:float, self.m:float, self.stateproduct:list
    # Purpose :- rotates the source when red button drag
    ###########################
    def rotate(self, mousex, mousey):
        angle_to_pointer = math.degrees(math.atan2(self.yp - mousey, self.xp - mousex))
        delta_x = mousex - self.redx
        delta_y = mousey - self.redy
        angle = math.atan2(delta_y, delta_x)
        angle = (angle * 180) / math.pi
        new = pygame.math.Vector2(self.redx, self.redy) + pygame.math.Vector2(self.endx, self.endy).rotate(angle)
        null, new_y = new
        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
        for i in objects_loaded:
            i.redraw1()
        for i in sources_loaded:
            if i.defined_name != self.defined_name:
                i.redraw1()
        self.graphical = pygame.draw.line(screen, self.colour2, (self.xp, self.yp), (self.endx, new_y), self.thickness)
        self.m = ((self.yp - new_y) / (self.xp - self.endx))
        start_y = self.m * ((self.xp + 10) - self.xp) + self.yp
        end_y = self.m * ((self.xp + 20) - self.xp) + self.yp
        self.graphical2 = pygame.draw.line(screen, self.colour, (self.xp + 10, start_y), (self.xp + 20, end_y),
                                           self.thickness)
        self.redy = start_y
        self.rendy = end_y
        self.endy = new_y
        self.findupdate(self.xp, self.yp)
        IncidentRays[self.defined_name] = []
        self.normals = []
        self.angles = []
        self.previousobj = []
        self.re = None
        return self.graphical, self.graphical2, self.endy, self.redy, self.rendy, self.m


##### Block #######
# Inheirts :- Main_Objects
# Parameters :- name:String
# Purpose :- Holds every attribute and operation that can be done on a block object
###########################
class Block(Main_Objects):
    def __init__(self, name):
        super().__init__(name)
        self.colour = (255, 105, 105)
        self.graphical = pygame.draw.rect(screen, self.colour, (self.xp, self.yp, self.width, self.length))
        self.full_name = "Block" + str(self.defined_name[-1])
        self.Refractive_Index = 1.7

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- updates instance of object on screen
    ###########################
    def redraw1(self):
        self.graphical = pygame.draw.rect(screen, self.colour,
                                          (self.xp, self.yp, self.width, self.length))
        self.update()


##### GlassBlock #######
# Inheirts :- Main_Objects
# Parameters :- name:String
# Purpose :- Holds every attribute and operation that can be done on a glassblock object
###########################
class GlassBlock(Main_Objects):
    def __init__(self, name):
        super().__init__(name)
        self.Refractive_Index = 1.52
        self.colour = (168, 204, 215)
        self.graphical = pygame.draw.rect(screen, self.colour, (self.xp, self.yp, self.width, self.length))
        self.full_name = "GlassBlock" + str(self.defined_name[-1])

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- updates instance of object on screen
    ###########################
    def redraw1(self):
        self.graphical = pygame.draw.rect(screen, self.colour,
                                          (self.xp, self.yp, self.width, self.length))
        self.update()


##### Mirror #######
# Inheirts :- Main_Objects
# Parameters :- name:String
# Purpose :- Holds every attribute and operation that can be done on a mirror object
###########################
class Mirror(Main_Objects):
    def __init__(self, name):
        super().__init__(name)
        self.Property = "Reflective"
        self.width = 10
        self.colour = (192, 192, 192)
        self.graphical = pygame.draw.rect(screen, self.colour,
                                          pygame.Rect(self.xp, self.yp, self.width, self.length))
        self.full_name = "Mirror" + str(self.defined_name[-1])

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- updates instance of object on screen
    ###########################
    def redraw1(self):
        self.graphical = pygame.draw.rect(screen, self.colour,
                                          (self.xp, self.yp, self.width, self.length))
        self.update()


##### Screen #######
# Inheirts :- Main_Objects
# Parameters :- name:String
# Purpose :- Holds every attribute and operation that can be done on a screen object
###########################
class Screen(Main_Objects):
    def __init__(self, name):
        super().__init__(name)
        self.width = 10
        self.colour = (169, 169, 169)
        self.graphical = pygame.draw.rect(screen, self.colour, (self.xp, self.yp, self.width, self.length))
        self.Property = "Stop"

        self.full_name = "Screen" + str(self.defined_name[-1])

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- updates instance of object on screen
    ###########################
    def redraw1(self):
        self.graphical = pygame.draw.rect(screen, self.colour,
                                          (self.xp, self.yp, self.width, self.length))
        self.update()


##### Diffraction #######
# Inheirts :- Main_Objects
# Parameters :- name:String
# Purpose :- Holds every attribute and operation that can be done on diffraction objects
###########################
class Diffraction(Main_Objects):
    def __init__(self, name):
        super().__init__(name)
        self.width = 5
        self.length = 50
        self.slitdis = 0.0002
        self.scrlength = 1500
        self.screendis = 500
        self.sourcexp = self.xp - 100
        self.sourceyp = self.yp - self.length - self.slitdis + self.length / 2
        self.source_draging = False
        self.wavelength = 600 * 10 ** -9
        DiffRays[self.defined_name] = []
        self.yp = (length / 2) - (self.slitdis + self.length)
        self.graphical = pygame.draw.rect(screen, (169, 169, 169),
                                          (self.xp, self.yp - self.length - self.slitdis, self.width,
                                           self.length))
        self.graphical2 = pygame.draw.rect(screen, (169, 169, 169), (self.xp, self.yp, self.width, self.length))
        self.graphical3 = pygame.draw.rect(screen, (169, 169, 169),
                                           (self.xp, self.yp + self.length + self.slitdis, self.width,
                                            self.length))
        self.graphical4 = pygame.draw.rect(screen, (169, 169, 169),
                                           (self.xp + self.screendis, 0, self.width, self.scrlength))
        self.source = pygame.draw.circle(screen, (255, 193, 110), (self.sourcexp, self.sourceyp), 7)
        self.Property = "D"
        self.a = 2 * self.slitdis * 3 * 10 ** -3 + self.length * 3 * 10 ** -5
        self.full_name = "Diffraction" + str(self.defined_name[-1])
        self.fringe = (self.wavelength * self.screendis * 3 * 10 ** -3) / self.a
        self.update()

    ##### update #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- checks if properties of diffraction experiment is allowed to be
    # displayed and displays them if so
    ###########################
    def update(self):
        self.a = 2 * self.slitdis * 3 * 10 ** -3 + self.length * 3 * 10 ** -5
        self.fringe = (self.wavelength * self.screendis * 3 * 10 ** -3) / self.a
        if m.SlitS:
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render("Slit Seperation:" + str(self.a) + "m", True, (105, 105, 105))
            textrect = text.get_rect(center=(150, 80))
            screen.blit(text, textrect)
        if m.FS:
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render("Fringe seperation:" + str(self.fringe) + "m", True, (105, 105, 105))
            textrect = text.get_rect(center=(150, 95))
            screen.blit(text, textrect)
        if m.W:
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render("Wavelength:" + str(self.wavelength) + "nm", True, (105, 105, 105))
            textrect = text.get_rect(center=(150, 110))
            screen.blit(text, textrect)
        if m.SourceS:
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render("Screen distance:" + str(self.screendis * 3 * 10 ** -3) + "m", True, (105, 105, 105))
            textrect = text.get_rect(center=(150, 125))
            screen.blit(text, textrect)

    ##### diffraction #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- simualtes the young's double slit experiment
    ###########################
    def diffraction(self):
        DiffRays[self.defined_name] = []
        mid = self.sourceyp
        fringe_no = ((1500 * 3 * 10 ** -3) - (mid * 3 * 10 ** -3)) / self.fringe
        max = 1
        for i in range(int(fringe_no)):
            height = max * (0.03 / self.fringe)
            if mid - height < 0:
                pass
            else:
                Tag = tag_generator(tag, "S")
                diff_ray = Source(Tag)
                DiffRays[self.defined_name].append(diff_ray)
                diff_ray.endx = self.xp + self.screendis
                diff_ray.endy = mid - height
                diff_ray.xp = self.xp
                diff_ray.yp = mid
                diff_ray.blackout()
            max += 1
        min = 1
        for i in range(int(fringe_no)):
            height = min * (0.03 / self.fringe)
            if mid + height > 1000:
                pass
            else:
                Tag = tag_generator(tag, "S")
                diff_ray = Source(Tag)
                DiffRays[self.defined_name].append(diff_ray)
                diff_ray.endx = self.xp + self.screendis
                diff_ray.endy = mid + height
                diff_ray.xp = self.xp
                diff_ray.yp = mid
                diff_ray.blackout()
            min += 1

    ##### sourceredraw #######
    # Parameters :- x:float
    # Return Type :- self.source:function, self.sourcexp:float, self.stateproduct:list
    # Purpose :- updates instance of object on screen
    ###########################
    def sourceredraw(self, x):
        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
        if x < self.xp:
            self.source = pygame.draw.circle(screen, (255, 193, 110), (x, self.sourceyp), 5)
            self.sourcexp = x
            DiffRays[self.defined_name] = []
        self.update()

        return self.source, self.sourcexp

    def redraw(self, x, y):
        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
        self.graphical = pygame.draw.rect(screen, (169, 169, 169), (
            x, self.yp - self.length - self.slitdis, self.width, self.length))
        self.graphical2 = pygame.draw.rect(screen, (169, 169, 169), (x, self.yp, self.width, self.length))
        self.graphical3 = pygame.draw.rect(screen, (169, 169, 169),
                                           (x, self.yp + self.length + self.slitdis, self.width, self.length))
        self.graphical4 = pygame.draw.rect(screen, (169, 169, 169),
                                           (x + self.screendis, 0, self.width, self.scrlength))
        self.source = pygame.draw.circle(screen, (255, 193, 110), (self.sourcexp, self.sourceyp), 7)
        self.xp = x
        self.update()
        return self.xp

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- updates instance of object on screen
    ###########################
    def redraw1(self):
        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
        self.graphical = pygame.draw.rect(screen, (169, 169, 169),
                                          (self.xp, self.yp - self.length - self.slitdis, self.width,
                                           self.length))
        self.graphical2 = pygame.draw.rect(screen, (169, 169, 169), (self.xp, self.yp, self.width, self.length))
        self.graphical3 = pygame.draw.rect(screen, (169, 169, 169),
                                           (self.xp, self.yp + self.length + self.slitdis, self.width,
                                            self.length))
        self.graphical4 = pygame.draw.rect(screen, (169, 169, 169),
                                           (self.xp + self.screendis, 0, self.width, self.scrlength))
        self.source = pygame.draw.circle(screen, (255, 193, 110), (self.sourcexp, self.sourceyp), 7)
        for i in DiffRays[self.defined_name]:
            i.redraw1()
        self.update()


##### Semi_Circle #######
# Inherits :- Main_Objects
# Parameters :- name:String
# Purpose :- Holds every attribute and operation that can be done on a semi circle object
###########################
class Semi_Circle(Main_Objects):
    def __init__(self, name):
        super().__init__(name)
        x, y = sympy.symbols("x,y")
        self.Radius = 100
        self.graphical = pygame.draw.circle(screen, (168, 204, 215), (self.xp, self.yp), self.Radius)
        self.graphical2 = pygame.draw.rect(screen, (0, 0, 0),
                                           (self.xp - self.Radius, self.yp, self.Radius * 2,
                                            self.Radius))
        self.Refractive_Index = 1.52
        self.Equation = ("((x-{0})**2 + (y-{1})**2)-{2}".format(int(self.xp), int(self.yp), int(self.Radius ** 2)))
        self.Gradient = sympy.idiff(eval(self.Equation), y, x)
        self.full_name = "SemiCircle" + str(self.defined_name[-1])

    ##### redraw #######
    # Parameters :- x:float, y:float
    # Return Type :- self.xp:float, self.yp:float, self.interceptors:list, self.Equation:string
    # Purpose :- updates instance of object on screen when moved
    ###########################
    def redraw(self, x, y):
        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
        if self.interceptors:
            first = self.interceptors[0]
            for i in objects_loaded:
                if i.defined_name != self.defined_name and "D" not in i.defined_name:
                    i.redraw1()
            for i in sources_loaded:
                if i != first:
                    i.redraw1()

            first.normals = []
            first.angles = []
            IncidentRays[first.defined_name] = []
            first.re = None
        else:
            for i in objects_loaded:
                if i.defined_name != self.defined_name and "D" not in i.defined_name:
                    i.redraw1()
            for i in sources_loaded:
                i.redraw1()

        self.graphical = pygame.draw.circle(screen, (168, 204, 215), (x, y), self.Radius)
        self.graphical2 = pygame.draw.rect(screen, (0, 0, 0),
                                           (x - self.Radius, y, self.Radius * 2,
                                            self.Radius))
        self.xp = x
        self.yp = y
        self.Equation = ("(x-{0})**2 + (y-{1})**2-{2}".format(x, y, self.Radius ** 2))
        self.interceptors = []
        self.redraw1()

        return self.xp, self.yp, self.interceptors, self.Equation

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- updates instance of object on screen
    ###########################
    def redraw1(self):
        self.graphical = pygame.draw.circle(screen, (168, 204, 215), (self.xp, self.yp), self.Radius)
        self.graphical2 = pygame.draw.rect(screen, (0, 0, 0),
                                           (self.xp - self.Radius, self.yp, self.Radius * 2,
                                            self.Radius))
        self.update()


##### Button #######
# Parameters :- id:int, def_name:string
# Purpose :- creates button and displays it on screen
###########################
class Button:
    def __init__(self, id, def_name):
        self.defined_name = def_name
        self.x, self.y = (80, 45)
        self.id = id
        toolbar_button.append(def_name)
        self.rect = pygame.draw.rect(screen, (160, 160, 160), (10 + (12 * self.id), 15, self.x, self.y))

    ##### draw #######
    # Parameters :- text:string
    # Return Type :- None
    # Purpose :- draws text on button
    ###########################
    def draw(self, text):
        if text != '':
            font = pygame.font.SysFont('cambriacambriamath', 20)
            text = font.render(text, True, (0, 0, 0))
            textrect = text.get_rect(center=((self.x / 2) + 10 + (12 * self.id), (self.y / 2) + 15))
            screen.blit(text, textrect)

    ##### click #######
    # Parameters :- event:function
    # Return Type :- False:boolean, self.defined_name:string
    # Purpose :- checks if the button has been pressed and if so returns its name
    ###########################
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x, y):
                return self.defined_name
            else:
                return False


##### ChangeGUI #######
# Parameters :- None
# Return Type :- None
# Purpose :- changes the properties of objects displayed
###########################
class ChangeGUI():
    def __init__(self):
        self.main = tkinter.Tk()
        self.main.geometry("500x500")
        self.Tab = ttk.Notebook(self.main)
        self.run()

    ##### run #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- creates a a gui for changing properties
    ###########################
    def run(self):
        for i in objects_loaded:
            if "D" in i.defined_name:
                tab1 = ttk.Frame(self.Tab, width=400, height=280)
                self.Tab.add(tab1, text=eval('i.full_name'))
                ttk.Label(tab1,
                          text="Slit Distance").grid(column=0, row=0)
                ttk.Label(tab1,
                          text="Screen Distance").grid(column=0, row=1)
                ttk.Label(tab1,
                          text="Wavelength(400-700)*10^-9").grid(column=0, row=2)
                enter = tkinter.StringVar()
                e1 = tkinter.Entry(tab1, textvariable=enter)
                e1.grid(row=0, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e2 = tkinter.Entry(tab1, textvariable=enter1)
                e2.grid(row=1, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e3 = tkinter.Entry(tab1, textvariable=enter2)
                e3.grid(row=2, column=1, sticky=tkinter.E)

                B1 = tkinter.Button(tab1, text="Okay",
                                    command=lambda: self.diffraction_change(i, str(e1.get()), str(e2.get()),
                                                                            str(e3.get())))
                B1.grid(row=3, column=1)
            elif "M" in i.defined_name:
                tab1 = ttk.Frame(self.Tab, width=400, height=280)
                self.Tab.add(tab1, text=eval('i.full_name'))
                ttk.Label(tab1,
                          text="Length").grid(column=0, row=0)
                enter = tkinter.StringVar()
                e1 = tkinter.Entry(tab1, textvariable=enter)
                e1.grid(row=0, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(tab1, text="Okay", command=lambda: self.sm_change(i, str(e1.get())))
                B1.grid(row=0, column=2, sticky=tkinter.E)
            elif "SC" in i.defined_name:
                tab1 = ttk.Frame(self.Tab, width=400, height=280)
                self.Tab.add(tab1, text=eval('i.full_name'))
                ttk.Label(tab1,
                          text="Radius").grid(column=0, row=0)
                enter = tkinter.StringVar()
                e1 = tkinter.Entry(tab1, textvariable=enter)
                e1.grid(row=0, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(tab1, text="Okay", command=lambda: self.semi_change(i, str(e1.get())))
                B1.grid(row=0, column=2, sticky=tkinter.E)
            elif "S" in i.defined_name:
                tab1 = ttk.Frame(self.Tab, width=400, height=280)
                self.Tab.add(tab1, text=eval('i.full_name'))
                ttk.Label(tab1,
                          text="Length").grid(column=0, row=0)
                enter = tkinter.StringVar()
                e1 = tkinter.Entry(tab1, textvariable=enter)
                e1.grid(row=0, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(tab1, text="Okay", command=lambda: self.sm_change(i, str(e1.get())))
                B1.grid(row=0, column=2, sticky=tkinter.E)
            elif "G" in i.defined_name:
                tab1 = ttk.Frame(self.Tab, width=400, height=280)
                self.Tab.add(tab1, text=eval('i.full_name'))
                ttk.Label(tab1,
                          text="Length").grid(column=0, row=0)
                ttk.Label(tab1,
                          text="Width").grid(column=0, row=1)
                enter = tkinter.StringVar()
                e1 = tkinter.Entry(tab1, textvariable=enter)
                e1.grid(row=0, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e2 = tkinter.Entry(tab1, textvariable=enter1)
                e2.grid(row=1, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(tab1, text="Okay",
                                    command=lambda: self.glass_change(i, str(e1.get()), str(e2.get())))
                B1.grid(row=2, column=1, sticky=tkinter.E)

            elif "B" in i.defined_name:
                tab1 = ttk.Frame(self.Tab, width=400, height=280)
                self.Tab.add(tab1, text=eval('i.full_name'))
                ttk.Label(tab1,
                          text="Refractive Index").grid(column=0, row=0)
                ttk.Label(tab1,
                          text="Length").grid(column=0, row=1)
                ttk.Label(tab1,
                          text="Width").grid(column=0, row=2)
                enter = tkinter.StringVar()
                e1 = tkinter.Entry(tab1, textvariable=enter)
                e1.grid(row=0, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e2 = tkinter.Entry(tab1, textvariable=enter1)
                e2.grid(row=1, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e3 = tkinter.Entry(tab1, textvariable=enter2)
                e3.grid(row=2, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(tab1, text="Okay",
                                    command=lambda: self.block_change(i, str(e1.get()), str(e2.get()), str(e3.get())))
                B1.grid(row=3, column=1, sticky=tkinter.E)

        for i in sources_loaded:
            tab1 = ttk.Frame(self.Tab, width=400, height=280)
            self.Tab.add(tab1, text=eval('i.full_name'))
            ttk.Label(tab1,
                      text="Wavelength(400-700)*10^-9").grid(column=0, row=0)
            enter = tkinter.StringVar()
            e1 = tkinter.Entry(tab1, textvariable=enter)
            e1.grid(row=1, column=0, sticky=tkinter.E)
            B1 = tkinter.Button(tab1, text="Okay",
                                command=lambda: self.source_change(i, str(e1.get())))
            B1.grid(row=2, column=0, sticky=tkinter.E)
        self.Tab.pack(expand=1, fill="both")
        self.main.protocol("WM_DELETE_WINDOW", self.stop)
        self.main.mainloop()

    ##### diffraction_change #######
    # Parameters :- i:Memory Address of object, slitdis:float, screendis:float
    # Return Type :- None
    # Purpose :- changes properties specifically for the diffraction class
    ###########################
    def diffraction_change(self, i, slitdis, screendis, wavelength):
        if slitdis != "":
            i.slitdis = float(slitdis) / 3 * 10 ** -3
        if screendis != "":
            i.screendis = float(screendis) / 3 * 10 ** -3
        if wavelength != "" and 400 * 10 ** -9 <= float(wavelength) <= 700 * 10 ** -9:
            i.wavelength = float(wavelength)
        i.update()
        i.diffraction()
        i.redraw1()
        pygame.display.flip()
        self.stop()

    ##### block_change #######
    # Parameters :- i:Memory Address of object, newRI:float, newlength:float, newwidth:float
    # Return Type :- None
    # Purpose :- changes properties specifically for the block class
    ###########################
    def block_change(self, i, newRI, newlength, newwidth):
        if newRI != "":
            i.Refractive_Index = float(newRI)
        if newlength != "":
            i.length = int(newlength)
        if newwidth != "":
            i.width = int(newwidth)
        i.redraw1()
        pygame.display.flip()
        self.stop()

    ##### glass_change #######
    # Parameters :- i:Memory Address of object, newlength:float, newwidth:float
    # Return Type :- None
    # Purpose :- changes properties specifically for the glassblock class
    ###########################
    def glass_change(self, i, newlength, newwidth):
        if newlength != "":
            i.length = int(newlength)
        if newwidth != "":
            i.width = int(newwidth)
        i.redraw1()
        pygame.display.flip()
        self.stop()

    ##### semi_change #######
    # Parameters :- i:Memory Address of object, newradius:float
    # Return Type :- None
    # Purpose :- changes properties specifically for the semi circle class
    ###########################
    def semi_change(self, i, newradius):
        if newradius != "":
            i.Radius = int(newradius)
        i.redraw1()
        pygame.display.flip()
        self.stop()

    ##### sm_change #######
    # Parameters :- i:Memory Address of object, newlength:float
    # Return Type :- None
    # Purpose :- changes properties specifically for the screen class
    ###########################
    def sm_change(self, i, newlength):
        if newlength != "":
            i.length = int(newlength)
        i.redraw1()
        pygame.display.flip()
        self.stop()

    ##### source_change #######
    # Parameters :- i:Memory Address of object, wavelength:float
    # Return Type :- None
    # Purpose :- changes properties specifically for the source class
    ###########################
    def source_change(self, i, wavelength):
        if wavelength != "" and 400 * 10 ** -9 <= float(wavelength) <= 700 * 10 ** -9:
            i.wavelength = float(wavelength)
        i.redraw1()
        pygame.display.flip()
        self.stop()

    ##### stop #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- destroys gui
    ###########################
    def stop(self):
        self.main.destroy()


##### ShowGUI #######
# Parameters :- None
# Return Type :- None
# Purpose :- dictates which properties of an experiment can be displayed
###########################
class ShowGUI:
    def __init__(self):
        self.name = "ShowGUI"
        self.IA = False
        self.RA = False
        self.RI = False
        self.SlitS = False
        self.FS = False
        self.SourceS = False
        self.W = False

    ##### gui_loop #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- creates a a gui for showing properties
    ###########################
    def gui_loop(self):
        self.main = tkinter.Tk()
        self.main.geometry("50x200")
        var1 = tkinter.IntVar()
        tkinter.Checkbutton(self.main, text="Incident Angle", variable=var1).grid(row=0, sticky=tkinter.W)
        var2 = tkinter.IntVar()
        tkinter.Checkbutton(self.main, text="Refraction Angle", variable=var2).grid(row=1, sticky=tkinter.W)
        var3 = tkinter.IntVar()
        tkinter.Checkbutton(self.main, text="Refractive Index", variable=var3).grid(row=2, sticky=tkinter.W)
        var4 = tkinter.IntVar()
        tkinter.Checkbutton(self.main, text="Slit Seperation", variable=var4).grid(row=3, sticky=tkinter.W)
        var5 = tkinter.IntVar()
        tkinter.Checkbutton(self.main, text="Fringe Seperation", variable=var5).grid(row=4, sticky=tkinter.W)
        var6 = tkinter.IntVar()
        tkinter.Checkbutton(self.main, text="Source Seperation", variable=var6).grid(row=5, sticky=tkinter.W)
        var7 = tkinter.IntVar()
        tkinter.Checkbutton(self.main, text="Wavelength", variable=var7).grid(row=6, sticky=tkinter.W)
        B1 = tkinter.Button(self.main, text="Okay",
                            command=lambda: self.showing(var1.get(), var2.get(), var3.get(), var4.get(), var5.get(),
                                                         var6.get(), var7.get()))
        B1.grid(row=7, column=0, sticky=tkinter.E)
        self.main.protocol("WM_DELETE_WINDOW", self.stop)
        self.main.mainloop()

    ##### showing #######
    # Parameters :- IA:boolean, RA:boolean, RI:boolean, SlitS:boolean, FS:boolean, SourceS:boolean, W:boolean
    # Return Type :- None
    # Purpose :- checks whether a property can be displayed or not
    ###########################
    def showing(self, IA, RA, RI, SlitS, FS, SourceS, W):
        if IA == 1:
            self.IA = True
        if RA == 1:
            self.RA = True
        if RI == 1:
            self.RI = True
        if SlitS == 1:
            self.SlitS = True
        if FS == 1:
            self.FS = True
        if SourceS == 1:
            self.SourceS = True
        if W == 1:
            self.W = True
        if IA == 0:
            self.IA = False
        if RA == 0:
            self.RA = False
        if RI == 0:
            self.RI = False
        if SlitS == 0:
            self.SlitS = False
        if FS == 0:
            self.FS = False
        if SourceS == 0:
            self.SourceS = False
        if W == 0:
            self.W = False
        self.main.destroy()
        for i in sources_loaded:
            i.redraw1()
        #return self.IA, self.RA, self.RI, self.SlitS, self.W, self.IA, self.FS


    ##### stop #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- destroys the gui
    ###########################
    def stop(self):
        self.main.destroy()


##### QuestionsGUI #######
# Parameters :- c:object
# Return Type :- None
# Purpose :- creates questions depending what is being displayed
###########################
class QuestionsGUI:
    def __init__(self, c):
        self.objects = objects_loaded
        self.sources = sources_loaded
        self.run(c)

    ##### run #######
    # Parameters :- c:object
    # Return Type :- None
    # Purpose :- creates a gui for creating or setting question
    ###########################
    def run(self, c):
        possible = self.AutoGen()
        self.main = tkinter.Tk()
        self.main.geometry("500x500")
        self.Tab = ttk.Notebook(self.main)
        tab1 = ttk.Frame(self.Tab, width=1000, height=280)
        self.Tab.add(tab1, text='Auto Generated')
        tab2 = ttk.Frame(self.Tab, width=400, height=280)
        self.Tab.add(tab2, text='Create')
        ttk.Label(tab2,
                  text="Question").grid(column=0, row=1)
        ttk.Label(tab2,
                  text="Time Set").grid(column=0, row=2)
        ttk.Label(tab2,
                  text="Answer").grid(column=0, row=3)
        enter = tkinter.StringVar()
        c1 = tkinter.Entry(tab2, textvariable=enter)
        c1.grid(row=1, column=1, sticky=tkinter.E)
        enter1 = tkinter.StringVar()
        c2 = tkinter.Entry(tab2, textvariable=enter1)
        c2.grid(row=2, column=1, sticky=tkinter.E)
        enter2 = tkinter.StringVar()
        c3 = tkinter.Entry(tab2, textvariable=enter2)
        c3.grid(row=3, column=1, sticky=tkinter.E)
        B1 = tkinter.Button(tab2, text="Set",
                            command=lambda: [c.questions(c2.get(), c1.get(), [c3.get(), "created"]),
                                             self.main.destroy()])

        B1.grid(row=4, column=1, sticky=tkinter.E)
        self.Tab.pack(expand=1, fill="both")
        intertab1 = ttk.Notebook(tab1)

        for i in possible:
            if "index" in i:
                ttab1 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab1, text='Refractive Index')
                ttk.Label(ttab1,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab1,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab1,
                          text="Enter Refraction Angle").grid(column=0, row=3)
                ttk.Label(ttab1,
                          text="Enter Incident Angle").grid(column=0, row=4)
                enter = tkinter.StringVar()
                e11 = tkinter.Entry(ttab1, textvariable=enter)
                e11.insert(0, 'Find the refractive index of the object')
                e11.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e21 = tkinter.Entry(ttab1, textvariable=enter1)
                e21.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e31 = tkinter.Entry(ttab1, textvariable=enter2)
                e31.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e41 = tkinter.Entry(ttab1, textvariable=enter3)
                e41.grid(row=4, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab1, text="Set",
                                    command=lambda: [c.questions(e21.get(), e11.get(), [float(e31.get()), float(e41.get())]),
                                                     self.main.destroy()])
                B1.grid(row=5, column=1, sticky=tkinter.E)
            elif "critical" and "type1" in i:
                ttab2 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab2, text='Crtical Angle Type1')
                ttk.Label(ttab2,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab2,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab2,
                          text="Enter Refractive Index").grid(column=0, row=3)
                enter = tkinter.StringVar()
                e12 = tkinter.Entry(ttab2, textvariable=enter)
                e12.insert(0, 'Find the critical angle of the object')
                e12.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e22 = tkinter.Entry(ttab2, textvariable=enter1)
                e22.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e32 = tkinter.Entry(ttab2, textvariable=enter2)
                e32.grid(row=3, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab2, text="Set",
                                    command=lambda: [c.questions(e22.get(), e12.get(), [float(e32.get())]), self.main.destroy()])
                B1.grid(row=4, column=1, sticky=tkinter.E)
            elif "fringes" in i:
                ttab3 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab3, text='Fringe')
                ttk.Label(ttab3,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab3,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab3,
                          text="Enter Slit Seperation").grid(column=0, row=3)
                ttk.Label(ttab3,
                          text="Enter Source Seperartion").grid(column=0, row=4)
                ttk.Label(ttab3,
                          text="Enter Wavelength").grid(column=0, row=5)
                enter = tkinter.StringVar()
                e13 = tkinter.Entry(ttab3, textvariable=enter)
                e13.insert(0, 'Find the fringe seperation between adjacent maximas')
                e13.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e23 = tkinter.Entry(ttab3, textvariable=enter1)
                e23.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e33 = tkinter.Entry(ttab3, textvariable=enter2)
                e33.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e43 = tkinter.Entry(ttab3, textvariable=enter3)
                e43.grid(row=4, column=1, sticky=tkinter.E)
                enter4 = tkinter.StringVar()
                e53 = tkinter.Entry(ttab3, textvariable=enter4)
                e53.grid(row=6, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab3, text="Set",
                                    command=lambda: [c.questions(e23.get(), e13.get(), [float(e33.get()), float(e43.get()), float(e53.get())]),
                                                     self.main.destroy()])
                B1.grid(row=7, column=1, sticky=tkinter.E)
            elif "slits and screen" in i:
                ttab4 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab4, text='Screen Distance')
                ttk.Label(ttab4,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab4,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab4,
                          text="Enter Slit Seperation").grid(column=0, row=3)
                ttk.Label(ttab4,
                          text="Enter Fringe").grid(column=0, row=4)
                ttk.Label(ttab4,
                          text="Enter Wavelength").grid(column=0, row=5)
                enter = tkinter.StringVar()
                e14 = tkinter.Entry(ttab4, textvariable=enter)
                e14.insert(0, 'Find the distance between the screen and slits')
                e14.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e24 = tkinter.Entry(ttab4, textvariable=enter1)
                e24.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e34 = tkinter.Entry(ttab4, textvariable=enter2)
                e34.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e44 = tkinter.Entry(ttab4, textvariable=enter3)
                e44.grid(row=4, column=1, sticky=tkinter.E)
                enter4 = tkinter.StringVar()
                e54 = tkinter.Entry(ttab4, textvariable=enter4)
                e54.grid(row=5, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab4, text="Set",
                                    command=lambda: [c.questions(e24.get(), e14.get(), [float(e34.get()), float(e44.get()), float(e54.get())]),
                                                     self.main.destroy()])
                B1.grid(row=6, column=1, sticky=tkinter.E)
            elif "slits" in i:
                ttab5= ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab5, text='Slit Seperation')
                ttk.Label(ttab5,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab5,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab5,
                          text="Enter Fringe").grid(column=0, row=3)
                ttk.Label(ttab5,
                          text="Enter Source Seperartion").grid(column=0, row=4)
                ttk.Label(ttab5,
                          text="Enter Wavelength").grid(column=0, row=5)
                enter = tkinter.StringVar()
                e15 = tkinter.Entry(ttab5, textvariable=enter)
                e15.insert(0, 'Find the seperation between the narrow slits')
                e15.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e25= tkinter.Entry(ttab5, textvariable=enter1)
                e25.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e35 = tkinter.Entry(ttab5, textvariable=enter2)
                e35.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e45 = tkinter.Entry(ttab5, textvariable=enter3)
                e45.grid(row=4, column=1, sticky=tkinter.E)
                enter4 = tkinter.StringVar()
                e55 = tkinter.Entry(ttab5, textvariable=enter4)
                e55.grid(row=5, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab5, text="Set",
                                    command=lambda: [c.questions(e25.get(), e15.get(), [float(e35.get()), float(e45.get()), float(e55.get())]),
                                                     self.main.destroy()])
                B1.grid(row=6, column=1, sticky=tkinter.E)
            elif "wavelength" in i:
                ttab6 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab6, text='Wavelength')
                ttk.Label(ttab6,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab6,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab6,
                          text="Enter Fringe").grid(column=0, row=3)
                ttk.Label(ttab6,
                          text="Enter Source Seperartion").grid(column=0, row=4)
                ttk.Label(ttab6,
                          text="Enter Slit Seperation").grid(column=0, row=5)
                enter = tkinter.StringVar()
                e16 = tkinter.Entry(ttab6, textvariable=enter)
                e16.insert(0, 'Find the wavelength of the source')
                e16.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e26 = tkinter.Entry(ttab6, textvariable=enter1)
                e26.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e36 = tkinter.Entry(ttab6, textvariable=enter2)
                e36.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e46 = tkinter.Entry(ttab6, textvariable=enter3)
                e46.grid(row=4, column=1, sticky=tkinter.E)
                enter4 = tkinter.StringVar()
                e56 = tkinter.Entry(ttab6, textvariable=enter4)
                e56.grid(row=5, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab6, text="Set",
                                    command=lambda: [c.questions(e26.get(), e16.get(), [float(e36.get()), float(e46.get()), float(e56.get())]),
                                                     self.main.destroy()])
                B1.grid(row=6, column=1, sticky=tkinter.E)
            elif "order" and "type1" in i:
                ttab7 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab7 , text='Diffraction Order Type1')
                ttk.Label(ttab7 ,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab7 ,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab7 ,
                          text="Enter Fringe").grid(column=0, row=3)
                ttk.Label(ttab7 ,
                          text="Enter Source Seperartion").grid(column=0, row=4)
                ttk.Label(ttab7 ,
                          text="Enter Slit Seperation").grid(column=0, row=5)
                ttk.Label(ttab7 ,
                          text="Enter Fringe Number").grid(column=0, row=6)
                enter = tkinter.StringVar()
                e17 = tkinter.Entry(ttab7 , textvariable=enter)
                e17.insert(0, 'Find the diffrtaction angle of the maxima order n')
                e17.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e27 = tkinter.Entry(ttab7 , textvariable=enter1)
                e27.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e37 = tkinter.Entry(ttab7 , textvariable=enter2)
                e37.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e47 = tkinter.Entry(ttab7 , textvariable=enter3)
                e47.grid(row=4, column=1, sticky=tkinter.E)
                enter4 = tkinter.StringVar()
                e57 = tkinter.Entry(ttab7 , textvariable=enter4)
                e57.grid(row=5, column=1, sticky=tkinter.E)
                enter5 = tkinter.StringVar()
                e67 = tkinter.Entry(ttab7 , textvariable=enter5)
                e67.grid(row=6, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab7 , text="Set",
                                    command=lambda: [c.questions(e27.get(), e17.get(),
                                                                 [float(e37.get()), float(e47.get()), float(e57.get()), float(e67.get())]),
                                                     self.main.destroy()])
                B1.grid(row=7, column=1, sticky=tkinter.E)
            elif "refraction" in i:
                ttab8 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab8, text='Refraction Angle')
                ttk.Label(ttab8,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab8,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab8,
                          text="Enter Incidence Angle").grid(column=0, row=3)
                ttk.Label(ttab8,
                          text="Enter Refractive Index").grid(column=0, row=4)
                enter = tkinter.StringVar()
                e19 = tkinter.Entry(ttab8, textvariable=enter)
                e19.insert(0, 'Find the refraction angle of object')
                e19.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e29= tkinter.Entry(ttab8, textvariable=enter1)
                e29.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e39 = tkinter.Entry(ttab8, textvariable=enter2)
                e39.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e49 = tkinter.Entry(ttab8, textvariable=enter3)
                e49.grid(row=4, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab8, text="Set",
                                    command=lambda: [c.questions(e29.get(), e19.get(), [float(e39.get()), float(e49.get())]),
                                                     self.main.destroy()])
                B1.grid(row=5, column=1, sticky=tkinter.E)

            elif "incidence" in i:
                ttab9 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab9, text='Incidence Angle')
                ttk.Label(ttab9,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab9,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab9,
                          text="Enter Refraction Angle").grid(column=0, row=3)
                ttk.Label(ttab9,
                          text="Enter Refractive Index").grid(column=0, row=4)
                enter = tkinter.StringVar()
                e10 = tkinter.Entry(ttab9, textvariable=enter)
                e10.insert(0, 'Find the incidence angle of object')
                e10.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e20 = tkinter.Entry(ttab9, textvariable=enter1)
                e20.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e30= tkinter.Entry(ttab9, textvariable=enter2)
                e30.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e40 = tkinter.Entry(ttab9, textvariable=enter3)
                e40.grid(row=4, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab9, text="Set",
                                    command=lambda: [c.questions(e20.get(), e10.get(), [float(e30.get()), float(e40.get())]),
                                                     self.main.destroy()])
                B1.grid(row=5, column=1, sticky=tkinter.E)
            elif "order" and "type2" in i:
                ttab10 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab10, text='Diffraction Order Type2')
                ttk.Label(ttab10,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab10,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab10,
                          text="Enter Wavelength").grid(column=0, row=3)
                ttk.Label(ttab10,
                          text="Enter Slit Seperation").grid(column=0, row=4)
                ttk.Label(ttab10,
                          text="Enter Fringe Number").grid(column=0, row=5)
                enter = tkinter.StringVar()
                e111 = tkinter.Entry(ttab10, textvariable=enter)
                e111.insert(0, 'Find the diffrtaction angle of the maxima order n')
                e111.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e211= tkinter.Entry(ttab10, textvariable=enter1)
                e211.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e311 = tkinter.Entry(ttab10, textvariable=enter2)
                e311.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e411 = tkinter.Entry(ttab10, textvariable=enter3)
                e411.grid(row=4, column=1, sticky=tkinter.E)
                enter4 = tkinter.StringVar()
                e511 = tkinter.Entry(ttab10, textvariable=enter4)
                e511.grid(row=5, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab10, text="Set",
                                    command=lambda: [c.questions(e211.get(), e111.get(), [float(e311.get()), float(e411.get()), float(e511.get())]),
                                                     self.main.destroy()])
                B1.grid(row=6, column=1, sticky=tkinter.E)

            elif "critcal" and "type2" in i:
                ttab11 = ttk.Frame(intertab1, width=400, height=280)
                intertab1.add(ttab11, text='Critical Angle')
                ttk.Label(ttab11,
                          text="Question").grid(column=0, row=1)
                ttk.Label(ttab11,
                          text="Time Set").grid(column=0, row=2)
                ttk.Label(ttab11,
                          text="Enter Incidence Angle").grid(column=0, row=3)
                ttk.Label(ttab11,
                          text="Enter Refraction Angle").grid(column=0, row=4)
                enter = tkinter.StringVar()
                e121 = tkinter.Entry(ttab11, textvariable=enter)
                e121.insert(0, 'Find the critical angle of object')
                e121.grid(row=1, column=1, sticky=tkinter.E)
                enter1 = tkinter.StringVar()
                e221 = tkinter.Entry(ttab11, textvariable=enter1)
                e221.grid(row=2, column=1, sticky=tkinter.E)
                enter2 = tkinter.StringVar()
                e321 = tkinter.Entry(ttab11, textvariable=enter2)
                e321.grid(row=3, column=1, sticky=tkinter.E)
                enter3 = tkinter.StringVar()
                e421 = tkinter.Entry(ttab11, textvariable=enter3)
                e421.grid(row=4, column=1, sticky=tkinter.E)
                B1 = tkinter.Button(ttab11, text="Set",
                                    command=lambda: [c.questions(e221.get(), e121.get(), [float(e321.get()), float(e421.get())]),
                                                     self.main.destroy()])
                B1.grid(row=5, column=1, sticky=tkinter.E)

        intertab1.pack(expand=1, fill="both")
        self.main.mainloop()

    ##### stop #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- destroys the gui
    ###########################
    def stop(self):
        self.main.destroy()

    ##### AutoGen #######
    # Parameters :- None
    # Return Type :- qs:list
    # Purpose :- depending on what is being displayed (in terms of properties) it creates questions
    ###########################
    def AutoGen(self):
        qs = []
        if m.RI and ("Block" or "GlassBlock" or "Semi") in str(self.objects):
            qs.append("critical angle type1")
        if m.IA and m.RA and (not m.RI) and ("Block" or "GlassBlock" or "Semi") in str(self.objects):
            qs.append("refractive index")
            qs.append("critical angle type2")

        if m.SlitS and m.SourceS and m.W and (not m.FS) and diff_mode:
            qs.append("fringes")
        if m.FS and m.SourceS and m.W and (not m.SlitS) and diff_mode:
            qs.append("slits")

        if m.SlitS and m.FS and m.W and (not m.SourceS) and diff_mode:
            qs.append("slits and screen")

        if m.SlitS and m.SourceS and m.FS and (not m.W) and diff_mode:
            qs.append("wavelength")
            qs.append("order type1")

        if m.IA and m.RI and (not m.RA) and ("Block" or "GlassBlock" or "Semi") in str(self.objects):
            qs.append("refraction")

        if m.RA and m.RI and (not m.IA) and ("Block" or "GlassBlock" or "Semi") in str(self.objects):
            qs.append("incidence")

        if m.W and m.SlitS and diff_mode:
            qs.append("order type2")
        return qs


##### quit #######
# Parameters :- None
# Return Type :- info:list
# Purpose :- when exiting gui it returns crucial information for analysis
###########################
def quit(c):
    pygame.quit()
    n.disconnect()
    n.disconnect2()
    end_time = time.time()
    dur = (end_time - start_time) / 60
    dur = round(dur, 2)
    if c is not None:
        c = c.stop()
    else:
        c = [None, None]
    with open("return.txt", "r") as f:
        qu = f.read()
    f.close()
    qu = eval(qu)
    Report.Reported(qu)
    exit()


m = ShowGUI()
c = None
diff_mode = False
n = Network()
n.connect()
t = 0

while True:
    # Tool bar
    change = False
    toolbar_button = []
    objects_loaded = list(dict.fromkeys(objects_loaded))
    sources_loaded = list(dict.fromkeys(sources_loaded))
    pygame.draw.rect(screen, (105, 105, 105), pygame.Rect(0, 0, width, 75))
    width = screen.get_width()
    height = screen.get_height()
    Open = Button(8, "Open")
    Open.draw("Open")
    New = Button(0, "New")
    New.draw("New")
    Block_btn = Button(16, "Block_btn")
    Block_btn.draw("Block")
    GlassBlock_btn = Button(24, "GlassBlock_btn")
    GlassBlock_btn.draw("GlassBlock")
    Mirror_btn = Button(32, "Mirror_btn")
    Mirror_btn.draw("Mirror")
    Screen_btn = Button(40, "Screen_btn")
    Screen_btn.draw("Screen")
    Semi_Circle_btn = Button(48, "Semi_Circle_btn")
    Semi_Circle_btn.draw("Semi Circle")
    Diffraction_btn = Button(56, "Diffraction_btn")
    Diffraction_btn.draw("Diffraction")
    Source_btn = Button(64, "Source_btn")
    Source_btn.draw("Source")
    Question = Button(72, "Question")
    Question.draw("Question")
    Del_All = Button(80, "Del_All")
    Del_All.draw("Del All")
    Quit = Button(88, "Quit")
    Quit.draw("Quit")
    Chat = Button(96, "Chat")
    Chat.draw("Chat")
    Save = Button(104, "Save")
    Save.draw("Save")
    Show = Button(112, "Show")
    Show.draw("Show")
    Change = Button(120, "Change")
    Change.draw("Change")
    obj = None
    if diff_mode:
        if "Diffraction" in str(objects_loaded):
            for i in objects_loaded:
                if "D" in i.defined_name:
                    obj = i
        else:
            Tag = tag_generator(tag, "D")
            obj = Diffraction(Tag)
            objects_loaded.append(obj)
        obj.redraw1()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            x_axis = pos[0]
            y_axis = pos[1]
            if event.type == pygame.QUIT:
                pygame.quit()
                # n.send(bytes("STOP", encoding="utf-8"))
                quit(c)
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and y_axis >= 100:
                if event.button == 1:
                    if obj.graphical.collidepoint(event.pos) or obj.graphical2.collidepoint(
                            event.pos) or obj.graphical3.collidepoint(event.pos) or obj.graphical4.collidepoint(
                        event.pos):
                        obj.draging = True
                        obj.diffraction()
                        obj.redraw1()
                        change = True
                    elif obj.source.collidepoint(event.pos):
                        obj.source_draging = True
                        obj.diffraction()
                        obj.redraw1()
                        change = True

            elif event.type == pygame.MOUSEBUTTONUP and y_axis >= 100:
                if event.button == 1 and obj.draging:
                    obj.diffraction()
                    obj.redraw1()
                    obj.draging = False
                    change = True
                elif event.button == 1 and obj.source_draging:
                    obj.source_draging = False
                    obj.diffraction()
                    obj.redraw1()
                    change = True

            elif event.type == pygame.MOUSEMOTION and y_axis >= 100:
                if obj.draging:
                    mouse_x, mouse_y = event.pos
                    obj.graphical.x = mouse_x
                    obj.graphical.y = mouse_y
                    obj.redraw(mouse_x, None)
                    obj.diffraction()
                    obj.redraw1()
                    change = True
                elif obj.source_draging:
                    mouse_x, mouse_y = event.pos
                    obj.sourceredraw(mouse_x)
                    obj.diffraction()
                    obj.redraw1()
                    change = True

            elif event.type == pygame.MOUSEBUTTONDOWN and y_axis <= 75:
                for i in toolbar_button:
                    clicktest = eval(i).click(event)
                    if clicktest == "Diffraction_btn":
                        diff_mode = False
                        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
                        for i in objects_loaded:
                            if "D" not in i.defined_name:
                                i.redraw1()
                        for i in sources_loaded:
                            i.redraw1()
                    elif clicktest == "Change":
                        n = ChangeGUI()
                    elif clicktest == "Show":
                        m.gui_loop()

        if change and diff_mode:
            so = [vars(m)]
            if "main" in vars(m):
                temp1 = so[0]["main"]
                so[0]["main"] = str(temp1)
                n.send(bytes(str(so), encoding="utf-8"))
                so[0]["main"] = temp1
            else:
                n.send(bytes(str(so), encoding="utf-8"))

            for item in objects_loaded:
                if "Diffraction" in str(item):
                    so = [vars(item)]
                    temp1 = so[0]["graphical"]
                    temp2 = so[0]["graphical2"]
                    temp3 = so[0]["graphical3"]
                    temp4 = so[0]["graphical4"]
                    temp5 = so[0]["source"]
                    so[0]["interceptors"] = []
                    so[0]["graphical"] = ""
                    so[0]["graphical2"] = ""
                    so[0]["graphical3"] = ""
                    so[0]["graphical4"] = ""
                    so[0]["source"] = ""
                    n.send(bytes(str(so), encoding="utf-8"))
                    so[0]["graphical"] = temp1
                    so[0]["graphical2"] = temp2
                    so[0]["graphical3"] = temp3
                    so[0]["graphical4"] = temp4
                    so[0]["source"] = temp5
                    for item2 in DiffRays[item.defined_name]:
                        so2 = [vars(item2)]
                        temp1 = so2[0]["graphical"]
                        temp2 = so2[0]["graphical2"]
                        so2[0]["interceptors"] = []
                        so2[0]["previousobj"] = []
                        so2[0]["normals"] = []
                        so2[0]["angles"] = []
                        so2[0]["graphical"] = str(so2[0]["graphical"])
                        so2[0]["graphical2"] = str(so2[0]["graphical2"])
                        n.send(bytes(str(so2), encoding="utf-8"))
                        so2[0]["graphical"] = temp1
                        so2[0]["graphical2"] = temp2
            n.send(bytes("PAUSE", encoding="utf-8"))

    else:
        # Events for when a mouse movements are made
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            x_axis = pos[0]
            y_axis = pos[1]
            if event.type == pygame.QUIT:
                n.send(bytes("STOP", encoding="utf-8"))
                quit(c)
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and y_axis >= 100:
                for i in objects_loaded:
                    if event.button == 1:
                        if i.graphical.collidepoint(event.pos):
                            if "SC" in i.defined_name:
                                if event.pos[1] > i.yp:
                                    pass
                                else:
                                    i.draging = True
                                    i.Simulation(False, None, True)
                                    change = True
                            else:
                                i.draging = True
                                i.Simulation(False, None, True)
                                change = True
                for i in sources_loaded:
                    if event.button == 1:
                        if i.graphical.collidepoint(event.pos):
                            if i.graphical2.collidepoint(event.pos):
                                i.t_status = 1
                                i.Simulation(False, None, False)
                                i.redraw1()
                                i.draging = True
                                change = True

                            else:
                                i.Simulation(False, None, False)
                                i.redraw1()
                                i.draging = True
                                change = True
            elif event.type == pygame.MOUSEBUTTONUP and y_axis >= 100:
                for i in objects_loaded:
                    if event.button == 1 and i.draging:
                        i.Simulation(False, None, True)
                        for item in i.interceptors:
                            item.redraw1()
                        i.draging = False
                        change = True
                for i in sources_loaded:
                    if event.button == 1 and i.draging:
                        if i.t_status == 1:
                            mousex, mousey = event.pos
                            i.rotate(mousex, mousey)
                            i.Simulation(False, None, False)
                            i.redraw1()
                            i.draging = False
                            i.t_status = 0
                            change = True
                        else:
                            i.Simulation(False, None, False)
                            i.redraw1()
                            i.draging = False
                            change = True
            elif event.type == pygame.MOUSEMOTION and y_axis >= 100:
                for i in objects_loaded:
                    if i.draging:
                        mouse_x, mouse_y = event.pos
                        i.redraw(mouse_x, mouse_y)
                        i.Simulation(False, None, True)
                        change = True

                for i in sources_loaded:
                    if i.draging:
                        mouse_x, mouse_y = event.pos
                        if i.t_status == 1:
                            i.Simulation(False, None, False)
                            i.redraw1()
                            change = True

                        else:
                            i.redraw(mouse_x, mouse_y)
                            i.Simulation(False, None, False)
                            i.redraw1()
                            change = True
            # dictates what happens when a button is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN and y_axis <= 75:
                for i in toolbar_button:
                    clicktest = eval(i).click(event)
                    if clicktest == "Block_btn":
                        Tag = tag_generator(tag, "B")
                        objects_loaded.append(Block(Tag))
                    elif clicktest == "GlassBlock_btn":
                        Tag = tag_generator(tag, "GB")
                        objects_loaded.append(GlassBlock(Tag))
                    elif clicktest == "Mirror_btn":
                        Tag = tag_generator(tag, "M")
                        objects_loaded.append(Mirror(Tag))
                    elif clicktest == "Screen_btn":
                        Tag = tag_generator(tag, "S")
                        objects_loaded.append(Screen(Tag))
                    elif clicktest == "Semi_Circle_btn":
                        Tag = tag_generator(tag, "SC")
                        objects_loaded.append(Semi_Circle(Tag))
                    elif clicktest == "Diffraction_btn":
                        diff_mode = True
                    elif clicktest == "Source_btn":
                        Tag = tag_generator(tag, "R")
                        sources_loaded.append(Source(Tag))
                    elif clicktest == "Quit":
                        # n.send(bytes("STOP", encoding="utf-8"))
                        quit(c)
                        sys.exit()
                    elif clicktest == "Chat":
                        c = ChatboxServer.Server()
                    elif clicktest == "Del_All":
                        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
                        objects_loaded = []
                        sources_loaded = []
                        tag = [0]
                    elif clicktest == "Save":
                        with open("savegame", "wb") as f:
                            data = []
                            if objects_loaded:
                                data += objects_loaded
                            else:
                                pass
                            if sources_loaded:
                                data += sources_loaded
                            else:
                                pass
                            pickle.dump(data, f)
                        f.close()

                    elif clicktest == "Open":
                        objects_loaded = []
                        sources_loaded = []
                        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
                        with open("savegame", "rb") as f:
                            loaded = pickle.load(f)
                        f.close()
                        for pos in loaded:
                            if "Source" in str(pos):
                                sources_loaded.append(pos)
                            else:
                                objects_loaded.append(pos)
                        if objects_loaded:
                            for items in objects_loaded:
                                items.redraw1()
                        else:
                            pass
                        if sources_loaded:
                            for items in sources_loaded:
                                items.redraw1()
                        else:
                            pass
                    elif clicktest == "Show":
                        m.gui_loop()
                    elif clicktest == "Change":
                        cng = ChangeGUI()
                    elif clicktest == "Question":
                        if c is None:
                            pass
                        else:
                            QuestionsGUI(c)
        # detects if a change has been made and sends the changes to the students/ networking part
        if change and not diff_mode:
            incidentsbefore = IncidentRays.values()
            incidentsafter = []
            for lis in incidentsbefore:
                if lis:
                    incidentsafter = incidentsafter + lis
                    incidentsafter = list(dict.fromkeys(incidentsafter))
            so = [vars(m)]
            if "main" in vars(m):
                temp1 = so[0]["main"]
                so[0]["main"] = str(temp1)
                n.send(bytes(str(so), encoding="utf-8"))
                so[0]["main"] = temp1
            else:
                n.send(bytes(str(so), encoding="utf-8"))
            if sources_loaded:
                for item in sources_loaded:
                    so = [vars(item)]
                    temp1 = so[0]["graphical"]
                    temp2 = so[0]["graphical2"]
                    so[0]["interceptors"] = []
                    so[0]["previousobj"] = []
                    so[0]["normals"] = []
                    so[0]["angles"] = []
                    so[0]["graphical"] = str(so[0]["graphical"])
                    so[0]["graphical2"] = str(so[0]["graphical2"])
                    n.send(bytes(str(so), encoding="utf-8"))
                    so[0]["graphical"] = temp1
                    so[0]["graphical2"] = temp2
            if objects_loaded:
                for item in objects_loaded:
                    if "Semi" in str(item):
                        so = [vars(item)]
                        temp1 = so[0]["graphical"]
                        temp2 = so[0]["graphical2"]
                        so[0]["interceptors"] = []
                        so[0]["graphical"] = str(so[0]["graphical"])
                        so[0]["graphical2"] = str(so[0]["graphical2"])
                        n.send(bytes(str(so), encoding="utf-8"))
                        so[0]["graphical"] = temp1
                        so[0]["graphical2"] = temp2
                    elif "Diffraction" in str(item):
                        pass
                    else:
                        so = [vars(item)]
                        temp1 = so[0]["graphical"]
                        so[0]["interceptors"] = []
                        so[0]["graphical"] = str(so[0]["graphical"])
                        n.send(bytes(str(so), encoding="utf-8"))
                        so[0]["graphical"] = temp1
            if incidentsafter:
                for item in incidentsafter:
                    if "Source" in str(item):
                        so = [vars(item)]
                        temp1 = so[0]["graphical"]
                        temp2 = so[0]["graphical2"]
                        so[0]["interceptors"] = []
                        so[0]["previousobj"] = []
                        so[0]["normals"] = []
                        so[0]["angles"] = []
                        so[0]["graphical"] = str(so[0]["graphical"])
                        so[0]["graphical2"] = str(so[0]["graphical2"])
                        n.send(bytes(str(so), encoding="utf-8"))
                        so[0]["graphical"] = temp1
                        so[0]["graphical2"] = temp2
                    else:
                        so = [vars(item)]
                        n.send(bytes(str(so), encoding="utf-8"))
            n.send(bytes("PAUSE", encoding="utf-8"))
    pygame.display.flip()
