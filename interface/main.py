import pygame
import sys

from settings import *


class Key(pygame.sprite.Sprite):
    def __init__(self, key_size, pos, screen, letter):
        super().__init__()
        self.display_surface = screen

        self.image = pygame.Surface((key_size, key_size))
        self.image.fill("#EEEEEE")
        self.rect = self.image.get_rect(topleft=pos)

        self.font = pygame.font.Font("Gamer.ttf", 40)
        self.letter_surf = self.font.render(letter, False, "#000000")
        self.letter_rect = self.letter_surf.get_rect(
            center=(pos[0] + int(key_size / 2), pos[1] + int(key_size / 2)))

    def display_letter(self):
        self.display_surface.blit(self.letter_surf, self.letter_rect)

    def update(self):

        # Hover effect
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        if hover:
            self.image.fill("#CCCCCC")
        else:
            self.image.fill("#EEEEEE")


class Game:
    def __init__(self):
        self.keyboard_sprites = pygame.sprite.Group()
        self.key_size = 50

        self.set_keyboard(keyboard_layout)

    def set_keyboard(self, layout):
        for row_index, row in enumerate(layout):
            for coll_index, cell in enumerate(row):
                x = 250 + (self.key_size * coll_index)
                y = 350 + (self.key_size * row_index)
                self.create_key(cell, x, y)

    def create_key(self, letter, x, y):
        key = Key(self.key_size, (x, y), screen, letter)
        self.keyboard_sprites.add(key)

    def player_letter(self):
        pass

    def run(self):
        # Keyboard
        self.keyboard_sprites.update()
        self.keyboard_sprites.draw(screen)

        for key in self.keyboard_sprites:
            key.display_letter()


# Init pygame
pygame.init()

# Setup screen
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

game = Game()


# App loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("white")
    game.run()

    pygame.display.update()
    clock.tick(60)
