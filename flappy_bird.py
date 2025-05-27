import pygame
import random

pygame.init()

window_width = 600
window_height = 800
prekazka_gap = 250


class ptak (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("flappy_bird_up.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.scale(self.image, (75, 75 ))
        self.rect = self.image.get_rect(bottomleft=(100,0.4*window_height))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound ("jumping.mp3")
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -10
            self.jump_sound.play()



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

class prekazka (pygame.sprite.Sprite):
    def __init__(self, x, y, is_top=False):
        super().__init__()
        image = pygame.image.load("flappy_bird_pipe.png").convert_alpha()
        if is_top:
            image = pygame.transform.flip(image, False, True)
            self.image = image
            self.rect = self.image.get_rect(bottomleft=(x, y - prekazka_gap // 2))
        else:
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y + prekazka_gap // 2))
        self.speed = 6

    def update(self):
        self.rect.x -= 3.5  
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= 0: 
          self.kill()
    
def is_collision():
    if pygame.sprite.spritecollide(hrac.sprite, prekazky, False): 
        prekazky.empty()
        return False
    return True



screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Flappy Bird") 

icon = pygame.image.load("flappy_bird_up.png") 
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

background_surface = pygame.image.load("flappy_bird_background.png").convert()



 
hrac = pygame.sprite.GroupSingle()
hrac.add(ptak())

prekazky = pygame.sprite.Group()

spawn_prekazka = pygame.USEREVENT
pygame.time.set_timer(spawn_prekazka, 1500)

game_active = is_collision()

while True:

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
                hrac.empty()
                hrac.add(ptak())
                prekazky.empty()

        if event.type == spawn_prekazka and game_active:
            vyska_prekazky = random.randint(200, 600)
            spodek_prekazky = prekazka(window_width + 100, vyska_prekazky, is_top=False)
            vrsek_prekazky = prekazka(window_width + 100, vyska_prekazky, is_top=True)
            prekazky.add(spodek_prekazky, vrsek_prekazky)



    if game_active:
 
        
        screen.blit(background_surface,(0,0))

     
        prekazky.draw(screen)
        prekazky.update()

        hrac.draw(screen)
        hrac.update()

        game_active = is_collision()

        

    pygame.display.update()
    clock.tick(60) 
