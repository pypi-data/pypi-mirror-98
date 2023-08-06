from PROPython.Settings import *
import pygame
import time
from PROPython.camera import *

class UI:
    class Button():
        def __init__(self, active_color, inactive_color, outline, font, size, text_color, x, y, width, height, text='',
                     command=None):
            self.active_color = active_color
            self.inactive_color = inactive_color
            self.outline = outline
            self.font = font
            self.size = size
            self.text_color = text_color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.command = command

        def draw(self, win, color, outline=None, font=None, size=25, text_color=(0, 0, 0)):
            # Call this method to draw the button on the screen
            if not outline == None:
                pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

            pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height), 0)

            if self.text != '':
                font_ = pygame.font.Font(font, size)
                text = font_.render(self.text, True, text_color)
                win.blit(text, (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2)))

        def isOver(self, pos, action):
            # Pos is the mouse position or a tuple of (x,y) coordinates
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    if not action == None:
                        print(action)
                        return True
                    else:
                        return True
            return False

        def Function(self, pos, func):
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    if not func == None:
                        return func()
                    else:
                        return False
            return False

        def get_pos(self, obj):
            pos = pygame.Surface((self.width, self.height))
            return pos.get_rect()

    class Text:
        def __init__(self, text, font, size, smoothing, color, pos_x, pos_y, window):
            font = pygame.font.Font(font, size)
            Text = font.render(text, smoothing, color)
            window.blit(Text, [pos_x, pos_y])

    class Input_Field:
        def __init__(self, width, height, x, y, active_color, inactive_color, border_width, text_color, font, size, max_chars):
            self.width = width
            self.height = height
            self.text_color = text_color
            self.active_color = active_color
            self.inactive_color = inactive_color
            self.color = self.inactive_color
            self.border_width = border_width
            self.max_chars = max_chars
            self.x = x
            self.y = y
            self.font = pygame.font.Font(font, size)
            self.text = ""
            self.input_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.active = False

        def update(self, event, window):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if self.MaxChars(self.max_chars):
                        if event.key == pygame.K_BACKSPACE:
                            self.text = self.text[0:-1]
                        else:
                            self.text += event.unicode
                    else:
                        if event.key == pygame.K_BACKSPACE:
                            self.text = self.text[0:-1]

            if self.active:
                self.color = self.active_color
            else:
                self.color = self.inactive_color

            pygame.draw.rect(window, self.color, self.input_rect, self.border_width)

            self.text_surface = self.font.render(self.text, True, self.text_color)
            window.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

            self.input_rect.w = max(self.width, self.text_surface.get_width() + 10)

        def MaxChars(self, max):
            if len(self.text) == max:
                return False
            else:
                return True

        def GetInputFieldText(self, whatField):
            print(whatField)
            return self.text

class Player():
    def __init__(self, x, y, speed, img, controlType):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = img
        self.controlType = controlType
        # self.has_nick = has_nick
        # self.player_nick = player_nick
        # self.image_rect = self.image.get_rect()

    def UpdatePlayer(self, window, width, height):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.x < width - 75:
                self.x += self.speed
        if self.controlType == 2:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if self.y > 0:
                    self.y -= self.speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if self.y < height - 150:
                    self.y += self.speed

        window.blit(pygame.image.load(self.image), (self.x, self.y))
        # if self.has_nick:
        #     if len(self.player_nick) == 1:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x + 30, self.y - 25, window)
        #     elif len(self.player_nick) == 2:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x + 23, self.y - 25, window)
        #     elif len(self.player_nick) == 3:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x + 15, self.y - 25, window)
        #     elif len(self.player_nick) == 4:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x + 8, self.y - 25, window)
        #     elif len(self.player_nick) == 5:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x + 2.5, self.y - 25, window)
        #     elif len(self.player_nick) == 6:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x - 2, self.y - 25, window)
        #     elif len(self.player_nick) == 7:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x - 7, self.y - 25, window)
        #     elif len(self.player_nick) == 8:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x - 12.2, self.y - 25, window)
        #     elif len(self.player_nick) == 9:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x - 20, self.y - 25, window)
        #     elif len(self.player_nick) >= 10:
        #         text = UI.Text(self.player_nick, None, 25, True, (255, 255, 255), self.x - 26, self.y - 25, window)

