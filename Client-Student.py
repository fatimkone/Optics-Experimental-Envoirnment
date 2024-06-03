import pygame
import sys
import ChatboxClient
from network import Network
import ctypes
import math
import sympy
from pygame import gfxdraw

user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
length = user32.GetSystemMetrics(1)
pygame.init()
screen = pygame.display.set_mode((width, length - 200))
screen.fill((0, 0, 0))
toolbar_button = []
objects_loaded = []
ang = []
sources_loaded = []
IncidentRays = {}
clientNumber = 0
tag = [0]


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
        pygame.gfxdraw.pie(screen, int(self.x), int(self.y), self.radius, int(self.theta1),
                           int(self.theta2), self.colour)
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
        self.xp = float(width / 2)
        self.yp = float(length / 2)
        self.length = 200
        self.width = 250
        self.colour = (0, 0, 0)
        self.Property = "Transparent"
        self.graphical = pygame.draw.rect(screen, (0, 0, 0),
                                          (self.xp, self.yp, self.width, self.length))
        self.draging = False
        self.interceptors = []

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
        self.findx = "((y-{0})/m)+{1}".format(int(self.yp), int(self.xp))
        self.findy = "m*(x-{0})+{1}".format(self.xp, self.yp)
        self.state = False
        self.previousobj = []
        IncidentRays[self.defined_name] = []
        self.full_name = "Source" + str(self.defined_name[-1])
        self.t_status = 0
        self.normals = []
        self.angles = []
        self.re = None

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


##### Block #######
# Inheirts :- Main_Objects
# Parameters :- name:String
# Purpose :- Holds every attribute and operation that can be done on a block object
###########################
class Block(Main_Objects):
    def __init__(self, name):
        super().__init__(name)
        self.colour = (255, 105, 105)
        self.graphical = pygame.draw.rect(screen, self.colour,
                                          (self.xp, self.yp, self.width, self.length))
        self.full_name = "Block" + str(self.defined_name[-1])
        self.Refractive_Index = 1.5

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

    ##### redraw1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- updates instance of object on screen
    ###########################
    def redraw1(self):
        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
        self.graphical = pygame.draw.rect(screen, (169, 169, 169),
                                          (self.xp, self.yp - self.length - self.slitdis - 200, self.width,
                                           self.length + 200))
        self.graphical2 = pygame.draw.rect(screen, (169, 169, 169), (self.xp, self.yp, self.width, self.length))
        self.graphical3 = pygame.draw.rect(screen, (169, 169, 169),
                                           (self.xp, self.yp + self.length + self.slitdis, self.width,
                                            self.length + 200))
        self.graphical4 = pygame.draw.rect(screen, (169, 169, 169),
                                           (self.xp + self.screendis, 75, self.width, self.scrlength))
        self.source = pygame.draw.circle(screen, (255, 193, 110), (self.sourcexp, self.sourceyp), 7)
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

    def draw(self, text):
        self.rect = pygame.draw.rect(screen, (160, 160, 160), (10 + (12 * self.id), 15, self.x, self.y))
        if text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(text, True, (0, 0, 0))
            textrect = text.get_rect(center=((self.x / 2) + 10 + (12 * self.id), (self.y / 2) + 15))
            screen.blit(text, textrect)

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x, y):
                return self.defined_name
            else:
                return False


##### ShowGUI #######
# Parameters :- None
# Return Type :- None
# Purpose :- dictates which properties of an experiment can be displayed
###########################
class ShowGUI:
    def __init__(self):
        self.IA = False
        self.RA = False
        self.RI = False
        self.SlitS = False
        self.FS = False
        self.SourceS = False
        self.W = False


m = ShowGUI()
run = True
conn = Network()
connect = conn.getP()
previous_ol = []
previous_sl = []
previous_al = []
chatter=None
chat=False
while run:
    pygame.draw.rect(screen, (105, 105, 105), pygame.Rect(0, 0, width, 75))
    Quit = Button(8, "Quit")
    Quit.draw("Quit")
    Chat = Button(0, "Chat")
    Chat.draw("Chat")
    toolbar_button = list(dict.fromkeys(toolbar_button))
    true_load = conn.rec()
    while true_load is None:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            y_axis = pos[1]
            if event.type == pygame.QUIT:
                conn.disconnect()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and y_axis <= 75:
                for i in toolbar_button:
                    clicktest = eval(i).click(event)
                    if clicktest == "Chat":
                        chatter=ChatboxClient
                        try:
                            chat=chatter.Client()
                        except ConnectionRefusedError:
                            continue
                    elif clicktest == "Quit":
                        conn.disconnect()
                        pygame.quit()
                        if chat:
                            chat.stop()
                        sys.exit()
        true_load=conn.rec()
    loaded = []
    while "PAUSE" not in str(true_load):
        if "STOP" in str(true_load):
            conn.disconnect()
            pygame.quit()
            if chat:
                chat.stop()
            sys.exit()
        if true_load is not None:
            loaded.append(true_load)
        true_load = conn.rec()
    if loaded is not None and loaded != "{1: 'dont redraw'}":
        screen.fill((0, 0, 0), (0, 75, 1920, 1120))
        if "Source" in str(loaded):
            sources_loaded = []
        if "Block" in str(loaded) or "Screen" in str(loaded) or "Circle" in str(loaded) or "Diffraction" in str(
                loaded) or "Mirror" in str(loaded):
            objects_loaded = []
        if "theta" in str(loaded):
            ang = []
        loaded=eval(str(loaded).replace("][","],["))
        if "Diffraction" in str(loaded):
            name=""
            for pickled in loaded:
                pickled = eval(pickled)
                pickled = pickled[0]
                if "Diffraction" in str(pickled):
                    Tag = tag_generator(tag, "D")
                    name=Tag
                    pick = Diffraction(Tag)
                    objects_loaded.append(pick)
                    for key in pickled:
                        if "graphical" in str(key):
                            pass
                        else:
                            setattr(pick, key, pickled[key])
                elif "ShowGUI" in str(pickled):
                    if len(pickled) == 1:
                        for key in pickled[0]:
                            setattr(m, key, pickled[0][key])
                    else:
                        for key in pickled:
                            setattr(m, key, pickled[key])
                elif "Source" in str(pickled):
                    Tag = tag_generator(tag, "R")
                    pick = Source(Tag)
                    sources_loaded.append(pick)
                    if len(pickled) == 1:
                        for key in pickled[0]:
                            setattr(pick, key, pickled[0][key])
                    else:
                        for key in pickled:
                            setattr(pick, key, pickled[key])

        else:
            for pickled in loaded:
                if pickled is not None:
                    pickled = eval(pickled)
                    pickled = pickled[0]
                    if "GlassBlock" in str(pickled):
                        Tag = tag_generator(tag, "GB")
                        pick = GlassBlock(Tag)
                        objects_loaded.append(pick)
                        for key in pickled:
                            if len(pickled) == 1:
                                for key in pickled[0]:
                                    setattr(pick, key, pickled[0][key])
                            #try execpt type error
                            else:
                                for key in pickled:
                                    setattr(pick, key, pickled[key])
                    elif "ShowGUI" in str(pickled):
                        if len(pickled)==1:
                            for key in pickled[0]:
                                setattr(m, key, pickled[0][key])
                        else:
                            for key in pickled:
                                setattr(m, key, pickled[key])
                    elif "Block" in str(pickled):
                        Tag = tag_generator(tag, "B")
                        pick = Block(Tag)
                        objects_loaded.append(pick)
                        for key in pickled:
                            if len(pickled) == 1:
                                for key in pickled[0]:
                                    setattr(pick, key, pickled[0][key])
                            else:
                                for key in pickled:
                                    setattr(pick, key, pickled[key])
                    elif "Screen" in str(pickled):
                        Tag = tag_generator(tag, "S")
                        pick = Screen(Tag)
                        objects_loaded.append(pick)
                        for key in pickled:
                            if len(pickled) == 1:
                                for key in pickled[0]:
                                    setattr(pick, key, pickled[0][key])
                            else:
                                for key in pickled:
                                    setattr(pick, key, pickled[key])
                    elif "Semi_Circle" in str(pickled):
                        Tag = tag_generator(tag, "SC")
                        pick = Semi_Circle(Tag)
                        objects_loaded.append(pick)
                        for key in pickled:
                            if len(pickled) == 1:
                                for key in pickled[0]:
                                    setattr(pick, key, pickled[0][key])
                            else:
                                for key in pickled:
                                    setattr(pick, key, pickled[key])
                    elif "Mirror" in str(pickled):
                        Tag = tag_generator(tag, "M")
                        pick = Mirror(Tag)
                        objects_loaded.append(pick)
                        for key in pickled:
                            if len(pickled) == 1:
                                for key in pickled[0]:
                                    setattr(pick, key, pickled[0][key])
                            else:
                                for key in pickled:
                                    setattr(pick, key, pickled[key])
                    elif "Source" in str(pickled):
                        Tag = tag_generator(tag, "R")
                        pick = Source(Tag)
                        sources_loaded.append(pick)
                        for key in pickled:
                            if len(pickled) == 1:
                                for key in pickled[0]:
                                    setattr(pick, key, pickled[0][key])
                            else:
                                for key in pickled:
                                    setattr(pick, key, pickled[key])
                    elif "theta" in str(pickled):
                        Tag = tag_generator(tag, "A")
                        pick = Angle()
                        ang.append(pick)
                        if len(pickled)==1:
                            for key in pickled[0]:
                                setattr(pick, key, pickled[0][key])
                        else:
                            for key in pickled:
                                setattr(pick, key, pickled[key])
        #print(sources_loaded)
        #print(objects_loaded)
        if len(sources_loaded) != 0 and len(objects_loaded) != 0:
            pass
            #pygame.display.flip()
            #previous_sl = sources_loaded
            #previous_ol = objects_loaded
            #previous_al = ang

        if len(objects_loaded) >= 1:
            for n in objects_loaded:
                if n == 1:
                    pass
                else:
                    n.redraw1()
        else:
            pass
        if len(sources_loaded) >= 1:
            for n in sources_loaded:
                if n == 1:
                    pass
                else:
                    n.redraw1()
        else:
            pass

        if len(ang) >= 1:
            for n in ang:
                if n == 1:
                    pass
                else:
                    n.redraw1()
        else:
            pass

        if len(sources_loaded) != 0 and len(objects_loaded) != 0:
            #sources_loaded = previous_sl
            #objects_loaded = previous_ol
            #ang = previous_al
            if len(objects_loaded) >= 1:
                for n in objects_loaded:
                    if n == 1:
                        pass
                    else:
                        n.redraw1()
            else:
                pass
            if len(sources_loaded) >= 1:
                for n in sources_loaded:
                    if n == 1:
                        pass
                    else:
                        n.redraw1()
            else:
                pass
            if len(ang) >= 1:
                for n in ang:
                    if n == 1:
                        pass
                    else:
                        n.redraw1()
            else:
                pass
    elif loaded is None:
        continue

    pygame.display.flip()
