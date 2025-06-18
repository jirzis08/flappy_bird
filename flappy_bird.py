import pygame
import random

pygame.init()

window_width = 600
window_height = 800
prekazka_mezera = 250
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

        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound ("jumping.mp3")
        self.jump_sound.set_volume (0.5)

        self.smrt_zvuk = pygame.mixer.Sound ("smrt.mp3")
        self.smrt_zvuk.set_volume (0.2)
        

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= window_height*0.87:
            self.rect.bottom = window_height*0.87

    def animation (self):
        self.flying_index += 0.05
        self.image = self.flying_images [int(self.flying_index) % len(self.flying_images)] 
    
    def update(self): 
        self.apply_gravity()
        self.animation ()


class prekazka (pygame.sprite.Sprite):
    def __init__(self, x, y, is_top=False):
        super().__init__()
        image = pygame.image.load("flappy_bird_pipe.png").convert_alpha()
        if is_top:
            image = pygame.transform.flip(image, False, True)
            self.image = image
            self.rect = self.image.get_rect(bottomleft=(x, y - prekazka_mezera // 2))
        else:
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y + prekazka_mezera // 2))
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


text_font = pygame.font.Font(None,100)
text_surface = text_font.render("Prohrál si!", True, "Black")
text_rect = text_surface.get_rect(center=(window_width/2, window_height/2))

skore_font = pygame.font.Font (None,45)

start_button_color = (100, 200, 100)
start_button_hover_color = (80, 180, 80)
start_button_rect = pygame.Rect(200, 400, 200, 60)
start_button_font = pygame.font.Font(None, 40)
start_button_text = start_button_font.render("Hrát", True, "Black")
start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)

restart_button_color = (100, 200, 100)
restart_button_hover_color = (80, 180, 80)
restart_button_rect = pygame.Rect(200, 525, 200, 60)
restart_button_text = start_button_font.render("Hrát znovu", True, "Black")
restart_button_text_rect = restart_button_text.get_rect(center=restart_button_rect.center)

quit_button_color = (200, 100, 100)
quit_button_hover_color = (180, 80, 80)
quit_button_rect = pygame.Rect(200, 600, 200, 60)
quit_button_text = start_button_font.render("Skončit", True, "Black")
quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)

game_stav = "menu"

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit() 
        
        if game_stav == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                game_stav = "hraní"
                skore = 0
                hrac.empty()
                hrac.add(ptak())
                prekazky.empty()
        
        if game_stav == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button_rect.collidepoint(event.pos):
                game_stav = "hraní"
                skore = 0
                hrac.empty()
                hrac.add(ptak())
                prekazky.empty()
            elif quit_button_rect.collidepoint(event.pos):
                pygame.quit()
                exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_stav == "hraní":
                    hrac.sprite.gravity = -13
                    hrac.sprite.jump_sound.play()


        if event.type == spawn_prekazka and game_stav == "hraní":
            max_vyska = window_height - prekazka_mezera - (window_height * 0.13) - 50
            vyska_prekazky = random.randint(150, int(max_vyska))
            spodek_prekazky = prekazka(window_width + 100, vyska_prekazky, is_top=False)
            vrsek_prekazky = prekazka(window_width + 100, vyska_prekazky, is_top=True)
            prekazky.add(spodek_prekazky, vrsek_prekazky)


    
    if game_stav == "menu":
        screen.blit(background_surface, (0, 0))

        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, start_button_hover_color, start_button_rect)
        else:
            pygame.draw.rect(screen, start_button_color, start_button_rect)

        screen.blit(start_button_text, start_button_text_rect)

    elif game_stav == "hraní":

        screen.blit (background_surface,(0,0))

     
        prekazky.update()
        prekazky.draw(screen)

        hrac.update()
        hrac.draw(screen)
  
        pygame.draw.rect(screen, ground_color, ground_rect)
        
        for pipe in prekazky:
            if not pipe.skore and not pipe.rect.top < 0:  
                if pipe.rect.right < hrac.sprite.rect.left:
                    skore += 1
                    pipe.skore = True
       
        skore_surface = skore_font.render(str(int(skore)), True, "Black")
        skore_rect = skore_surface.get_rect(topleft=(window_width / 2, 30))
        screen.blit(skore_surface, skore_rect)
        
        
        
        if not is_collision():
            game_stav = "game_over"
            hrac.sprite.smrt_zvuk.play()
    
    elif game_stav == "game_over":
        
        
        screen.blit(background_surface, (0, 0))
        pygame.draw.rect(screen, ground_color, ground_rect)

        prekazky.draw(screen)
        
        hrac.draw(screen)
        
        skore_surface = skore_font.render(f"Tvé dosažené skóre je: {int(skore)}", True, "Black")
        skore_rect = skore_surface.get_rect(center=(300, 500))
        
    
        if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, restart_button_hover_color, restart_button_rect)
        else:
            pygame.draw.rect(screen, restart_button_color, restart_button_rect)

        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, quit_button_hover_color, quit_button_rect)
        else:
            pygame.draw.rect(screen, quit_button_color, quit_button_rect)

        screen.blit(quit_button_text, quit_button_text_rect)       
        screen.blit(restart_button_text, restart_button_text_rect)
        screen.blit (text_surface, text_rect)
        screen.blit (skore_surface, skore_rect)

    pygame.display.update()
    clock.tick(60)        