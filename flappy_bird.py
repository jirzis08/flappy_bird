import pygame
import random

pygame.init()

window_width = 600
window_height = 800
prekazka_gap = 250
skore = 0 

class ptak (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        bird_up = pygame.image.load("flappy_bird_up.png").convert_alpha()
        bird_up = pygame.transform.scale(bird_up, (75,75))
        bird_down = pygame.image.load("flappy_bird_down.png").convert_alpha()
        bird_down = pygame.transform.scale(bird_down, (90,90))
        
        self.flying_images = [bird_up, bird_down] 
        self.flying_index = 0 
        self.image = self.flying_images [self.flying_index] 
        self.rect = self.image.get_rect(bottomleft=(100,0.4*window_height))
        self.rect.inflate_ip(-15, -15)

        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound ("jumping.mp3")
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -10
        

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= window_height*0.87:
            self.rect.bottom = window_height*0.87

    def animation (self):
        self.flying_index += 0.1
        self.image = self.flying_images [int(self.flying_index) % len(self.flying_images)] 
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation ()


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
        self.skore = False

    def update(self):
        self.rect.x -= 3.5  
        self.destroy()
        
    def destroy(self):
        if self.rect.right < 0: 
          self.kill()
    
def is_collision():
    if pygame.sprite.spritecollide(hrac.sprite, prekazky, False): 
        prekazky.empty()
        return False
    if hrac.sprite.rect.bottom >= window_height * 0.87:
        return False
    return True
    



screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Flappy Bird") 

icon = pygame.image.load("flappy_bird_up.png") 
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

background_surface = pygame.image.load("flappy_bird_background.png").convert()


ground_color = (160, 82, 45)  

ground_rect = pygame.Rect(0, window_height * 0.87, window_width, window_height * 0.13)
 
hrac = pygame.sprite.GroupSingle()
hrac.add(ptak())

prekazky = pygame.sprite.Group()

spawn_prekazka = pygame.USEREVENT
pygame.time.set_timer(spawn_prekazka, 1500)

text_font = pygame.font.Font("PixelifySans.ttf",100)
text_surface = text_font.render("Prohrál si!", True, "Black")
text_rect = text_surface.get_rect(center=(window_width/2, window_height/2))

text_font_2 = pygame.font.Font("PixelifySans.ttf",30)
text_surface_2 = text_font_2.render("Stiskni mezerník pro restart", True, "Black")
text_rect_2 = text_surface_2.get_rect(center=(300, 575))

text_font_start = pygame.font.Font("PixelifySans.ttf",30)
text_surface_start = text_font_start.render("Stiskni mezerník pro start", True, "Black")
text_rect_start = text_surface_start.get_rect(center=(300, 475))

skore_font = pygame.font.Font ("PixelifySans.ttf",45)

high_skore_font = pygame.font.Font (None,45)


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
                skore = 0

        if event.type == spawn_prekazka and game_active:
            max_vyska = window_height - prekazka_gap - (window_height * 0.13) - 50
            vyska_prekazky = random.randint(150, int(max_vyska))
            spodek_prekazky = prekazka(window_width + 100, vyska_prekazky, is_top=False)
            vrsek_prekazky = prekazka(window_width + 100, vyska_prekazky, is_top=True)
            prekazky.add(spodek_prekazky, vrsek_prekazky)


    if game_active:
 
        
        screen.blit(background_surface,(0,0))

     
        prekazky.draw(screen)
        prekazky.update()

        hrac.draw(screen)
        hrac.update()
        
        pygame.draw.rect(screen, ground_color, ground_rect)
        
        for pipe in prekazky:
            if not pipe.skore and not pipe.rect.top < 0:  # Only count bottom pipes
                if pipe.rect.right < hrac.sprite.rect.left:
                    skore += 1
                    pipe.skore = True
       
        skore_surface = skore_font.render(str(int(skore)), True, "Black")
        skore_rect = skore_surface.get_rect(topleft=(window_width / 2, 30))
        screen.blit(skore_surface, skore_rect)
        
        game_active = is_collision()
    
    else:
        
        text_font_skore = pygame.font.Font("PixelifySans.ttf",45)
        text_surface_skore = text_font_skore.render(f"Tvé skóre je: {int(skore)}", True, "Black")
        text_rect_skore = text_surface_skore.get_rect(center=(300, 500))
        
        screen.blit (text_surface, text_rect,)
        screen.blit (text_surface_2, text_rect_2)
        screen.blit (text_surface_skore, text_rect_skore)
        

    pygame.display.update()
    clock.tick(60)   