import pygame
import random

pygame.init()


class ptak (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("flappy_bird_up.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75 ))
        self.rect = self.image.get_rect(bottomleft=(100,0.4*window_height))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound ("jumping.mp3")
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -10
            self.jump_sound.play ()
            self.jump_sound.set_volume(2)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= window_height*0.87:
            self.rect.bottom = window_height*0.87
    
    def update(self):
        self.player_input()
        self.apply_gravity()
       

window_width = 600
window_height = 800

screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Flappy Bird") 

icon = pygame.image.load("flappy_bird_up.png") 
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

background_surface = pygame.image.load("flappy_bird_background.png").convert()



hrac = pygame.sprite.GroupSingle()
hrac.add(ptak())

game_active = True

while True:
    # zjistíme co dělá hráč za akci
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit() 
        if event.type == pygame.KEYDOWN:
            if game_active == False:
                game_active=True
                


    if game_active:
        # pozadí
        
        screen.blit(background_surface,(0,0))
        

        # hráč
        hrac.draw(screen)
        hrac.update()



    pygame.display.update() # updatujeme vykreslené okno
    clock.tick(60) # herní smyčka proběhne maximálně 60x za sekundu
