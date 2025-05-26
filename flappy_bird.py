import pygame
import random

pygame.init()

window_width = 600
window_height = 800

class ptak (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("flappy_bird_up.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75 ))
        self.rect = self.image.get_rect(bottomleft=(100,0.4*window_height))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound ("jumping.mp3")


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= window_height*0.87:
            self.rect.bottom = window_height*0.87
    
    
    def update(self):
        self.apply_gravity()
       
class prekazka (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("flappy_bird_pipe.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 500 ))
        self.rect = self.image.get_rect(bottomleft = (400, 0.1*window_height))
        self.speed  = 4
    def update(self):
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100: 
          self.kill()






screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Flappy Bird") 


clock = pygame.time.Clock()




 
hrac = pygame.sprite.GroupSingle()
hrac.add(ptak())

prekazky = pygame.sprite.Group()

game_active = True

while True:
    # zjistíme co dělá hráč za akci
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    if event.type == pygame.KEYDOWN:
        if game_active:
            if event.key == pygame.K_SPACE:
                hrac.sprite.gravity = -10
                hrac.sprite.jump_sound.play()
        else:
            game_active = True
                


    if game_active:
        # pozadí
        screen.blit(background_surface,(0,0))
        
        #překážka
        prekazky.draw(screen)
        prekazky.update()


        # hráč
        hrac.draw(screen)
        hrac.update()



    pygame.display.update() # updatujeme vykreslené okno
    clock.tick(60) # herní smyčka proběhne maximálně 60x za sekundu
