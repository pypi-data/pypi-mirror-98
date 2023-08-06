#=============#
#  PROPython  #
#=============#

#---------------#
# Version 1.0.0 #
#---------------#

# New version coming soon!

import pygame
import random
import os
import itertools
import time
import sys
import math
import Objects
import json
from PROPython.Objects import *
from PROPython.Settings import *
from PROPython.camera import *
from PROPython.network import Network

def cmd(MESSAGE):
    print(MESSAGE)

def cmdColor(MESSAGE, colorID):
    print(colorID + MESSAGE)

def saveF(FILENAME, STRING):
    FILE = open(FILENAME, "w")
    FILE.write(STRING)
    FILE.close()

def deleteF(FILEPATH):
    os.remove(FILEPATH)

def cmdError(ERRORmessage):
    print("\033[31m" + ERRORmessage)

def createF(FILENAME):
    FILE = open(FILENAME, "w")
    FILE.write("")
    FILE.close()

def deleteAllFLines(FILENAME):
    FILE = open(FILENAME, "w")
    FILE.truncate()
    FILE.close()

def createArray(ARRAY):
    return ARRAY

def Upper(STRING):
    return STRING.upper()

def Lower(STRING):
    return STRING.lower()

def Return(returnWhat):
    return returnWhat

def FileDuplicate(FILENAME, NUMBERvalue):
    FILE = open(str(NUMBERvalue) + FILENAME, "w")
    FILE2 = open(FILENAME, "r")
    FILE.write(FILE2.read())
    FILE.close()
    FILE2.close()

def toStr(WHAT):
    return str(WHAT)

def toInt(WHAT):
    return int(WHAT)

def toFloat(WHAT):
    return float(WHAT)

def TimeToSleep(TIME):
    time.sleep(TIME)

def LoadingAnimation():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

def WritingAnimation(TEXT):
    for i in TEXT:
        time.sleep(0.3)
        print(i, end = '', flush = True)

def Round(NUMBER):
    return math.trunc(NUMBER)

def Floor(NUMBER):
    return math.floor(NUMBER)

def Ceil(NUMBER):
    return math.ceil(NUMBER)

def Enumerate(whatToEnum):
    for index, value in enumerate(whatToEnum):
        print("index: "+str(index)," value: "+str(value))

def ListLength(LIST):
    return len(LIST)

def computerSymbol(STRING):
    return ord(STRING)

def toDegree(FIRST, SECOND):
    return pow(FIRST, SECOND)

def SortDict(DICT):
    return sorted(DICT.items(), key=lambda item: (item[1], item[0]))

def toBinary(NUMBER):
    return bin(NUMBER)

def All(ITERABLE):
    return all(ITERABLE)

def Ascii(STRING):
    return math.ascii(STRING)

def summ(valuesL):
    res = 0

    for x in valuesL:
        if type(x) == int or type(x) == float:
            res += x
        else:
            cmdError("Error! You have a string and you need int or float!")

    return res

def subtraction(valuesL):
    res = 0

    for x in valuesL:
        if type(x) == int or type(x) == float:
            res = x - res
        else:
            cmdError("Error! You have a string and you need int or float!")

    return -res

def multiple(valuesL):
    res = 1

    for x in valuesL:
        if type(x) == int or type(x) == float:
            res = x * res
        else:
            cmdError("Error! You have a string and you need int or float!")

    return res

def division(valuesL):
    res = valuesL[0]

    if valuesL[0] == 0:
        cmdError("Error! Cannot be divided by zero!")

    for x in valuesL:
        if x == valuesL[0]:
            res = valuesL[0]
        else:
            if type(x) == int or type(x) == float:
                res = res / x
            else:
                cmdError("Error! You have a string and you need int or float!")

    return res

def NumberOfPi():
    return math.pi

def EulersNumber():
    return math.e

def Exponents(NUMBER):
    return math.exp(NUMBER)

def SquareRoot(NUMBER):
    return math.sqrt(NUMBER)

def IsPathExist(PATH):
    return os.path.exists(PATH)

def CreateDirictory(PATH):
    os.mkdir(PATH)

def DeleteDirectoryFile(PATH):
    os.remove(PATH)

def DeleteDicrectory(PATH):
    os.rmdir(PATH)

def GetFileSize(PATH):
    return os.path.getsize(PATH)

def FileRename(OLDNAME, NEWNAME):
    os.rename(OLDNAME, NEWNAME)

def FolderFilesList(PATH):
    return os.listdir(PATH)

def isInStringNumberOrLetter(STRING):
    return STRING.isalnum()

def isInStringNumber(STRING):
    return STRING.isnumeric()

def isInStringLetter(STRING):
    return STRING.isalpha()

def RandomNumber(START, STOP, STEP):
    return random.randrange(START, STOP, STEP)

class PROGame:
    pygame.init()

    def __init__(self):
        self.hasIF = False
        self.created_host = False
        self.created_network = False

    def Window(self, width, height, window_name):
        self.drawButton = True
        self.drawTextbox = False
        self.count = 0
        window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(window_name)
        pygame.display.set_icon(pygame.image.load("icons/default_icon.png"))
        window.fill((15, 150, 105))
        self.FillColor = (15, 150, 105)
        self.hasPlayer = False
        self.hasBG = False
        self.window = window
        self.windowX = width
        self.windowY = height

    def Show(self, FPS, debug_mode):
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                def drawButton():
                    pos = pygame.mouse.get_pos()
                    if self.drawButton:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                for b in BUTTONS:
                                    if b.get_pos(b):
                                        b.Function(pygame.mouse.get_pos(), b.command)
                        else:
                            for b in BUTTONS:
                                if b.get_pos(b):
                                    if pos[0] > b.x and pos[0] < b.x + b.width:
                                        if pos[1] > b.y and pos[1] < b.y + b.height:
                                            b.draw(self.window, b.active_color, b.outline, b.font, b.size, b.text_color)
                                    else:
                                        b.draw(self.window, b.inactive_color, b.outline, b.font, b.size, b.text_color)

                def drawTextBox():
                    if self.hasIF:
                        for input_field in TEXT_BOXS:
                            if self.hasBG:
                                self.window.blit(self.BGimg, (0, 0))
                            else:
                                pygame.draw.rect(self.window, self.FillColor, (input_field.x, input_field.y , input_field.width + self.windowX, input_field.height + self.border_width))

                            input_field.update(event, self.window)

                drawTextBox()
                drawButton()

            if self.hasPlayer == False:
                if self.created_network:
                    self.p2 = self.n.send(self.p)
                    if debug_mode:
                        print(self.p)
                        print(self.p2)

                if self.hasBG:
                    self.window.blit(self.BGimg, (0, 0))
                else:
                    self.window.fill(self.FillColor)
                if self.created_network == True:
                    self.p.UpdatePlayer(self.window, self.windowX, self.windowY)
                    self.p2.UpdatePlayer(self.window, self.windowX, self.windowY)
                elif self.hasPlayer == True:
                    self.player.UpdatePlayer(self.window, self.windowX, self.windowY)

            pygame.display.update()

    def draw_cube(self, color, pos_x, pos_y, width, height):
        pygame.draw.rect(self.window, color, (pos_x, pos_y, width, height))

    def draw_circle(self, color, pos_x, pos_y, width, height):
        pygame.draw.circle(self.window, color, (pos_x, pos_y), width, height)

    def draw_line(self, color, pos_x1, pos_y1, pos_x2, pos_y2, width):
        pygame.draw.line(self.window, color, [pos_x1, pos_y1], [pos_x2, pos_y2], width)

    def draw_polygon(self, color, pos_x1, pos_y1, pos_x2, pos_y2, pos_x3, pos_y3, pos_x4, pos_y4):
        pygame.draw.polygon(self.window, color, [[pos_x1, pos_y1], [pos_x2, pos_y2], [pos_x3, pos_y3], [pos_x4, pos_y4]])

    def create_text(self, text, font, size, color, pos_x, pos_y, smoothing):
        font = pygame.font.Font(font, size)
        Text = font.render(text, smoothing, color)
        self.window.blit(Text, [pos_x, pos_y])

    def play_sound(self, path):
        sound = pygame.mixer.Sound(path)
        sound.play()

    def fill(self, color):
        self.FillColor = color
        self.window.fill(color)

    def background(self, path):
        self.window.blit(pygame.image.load(path), (0, 0))
        self.hasBG = True
        self.BGimg = pygame.image.load(path)

    def create_image(self, path, pos_x, pos_y):
        self.window.blit(pygame.image.load(path), (pos_x, pos_y))

    def icon(self, path):
        pygame.display.set_icon(pygame.image.load(path))

    def create_button(self, active_color, inactive_color, width, height, x, y, text, size, font, text_color, outline=None, command=None):
        button = UI.Button(active_color, inactive_color, outline, font, size, text_color, x, y, width, height, text, command)
        BUTTONS.append(button)
        button.draw(self.window, inactive_color, outline, font, size, text_color)

    def clear(self):
        self.drawButton = False
        self.hasIF = False

    def create_player(self, x, y, speed, image, control_type = 1):
        p = Player(x, y, speed, image, control_type)
        self.hasPlayer = True
        self.player = p

    def create_text_box(self, width, height, x, y, active_color, inactive_color, border_width, text_color, font, size, max_chars):
        input_field = UI.Input_Field(width, height, x, y, active_color, inactive_color, border_width, text_color, font, size, max_chars)
        TEXT_BOXS.append(input_field)
        self.hasIF = True
        self.border_width = border_width

    def get_TextBoxs_text(self):
        for input_field in TEXT_BOXS:
            return input_field.GetInputFieldText(input_field)

    def create_network(self):
        self.n = Network()
        self.p = self.n.getP()
        self.created_network = True