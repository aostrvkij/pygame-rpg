from sprites import *
from config import *
import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('arial.ttf', 32)
        self.running = True

        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.fireball_spritesheet = Spritesheet('img/fireball.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.go_background = pygame.image.load('img/introbackground.png')

    def createTilemap(self):
        for i, row in enumerate(tilemap2):
            for j, column in enumerate(row):
                Ground  (self, j, i )
                if column == 'B':
                    Block(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == 'P':
                    self.player = Player(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

            if event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

                if event.key == pygame.K_v:
                    if self.player.facing == 'up':
                        Shot(self, self.player.rect.centerx, self.player.rect.top, 'up')
                    if self.player.facing == 'down':
                        Shot(self, self.player.rect.centerx, self.player.rect.bottom, 'down')
                    if self.player.facing == 'left':
                        Shot(self, self.player.rect.left, self.player.rect.centery, 'left')
                    if self.player.facing == 'right':
                        Shot(self, self.player.rect.right, self.player.rect.centery, 'right')

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        #text = self.font.render('Game Over', True, WHITE)
        #text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        restart_button = Button(x=WIN_WIDTH / 2 - 100, y=WIN_HEIGHT / 2 - 50, width=200, height=100, fg=BLACK, bg=GREY,
                             content='PLAY', fontsize=32)
        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0, 0))
            #self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            pygame.display.update()
            self.clock.tick(FPS)



    def intro_screen(self):
        intro = True

        title1 = self.font.render('SPACE - attack', True, WHITE)
        title_rect1 = title1.get_rect(x=10, y=10)
        title2 = self.font.render('V - shot', True, WHITE)
        title_rect2 = title2.get_rect(x=10, y=35)
        play_button = Button(x=WIN_WIDTH/2-100, y=WIN_HEIGHT/2-50, width=200, height=100, fg=BLACK, bg=GREY,
                             content='PLAY', fontsize=32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title1, title_rect1)
            self.screen.blit(title2, title_rect2)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
