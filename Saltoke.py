import pygame
from sys import exit
from random import randint , choice

#Clases

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_mov1 = pygame.image.load('imagenes/J1mov1.png').convert_alpha()
        player_mov2 = pygame.image.load('imagenes/J1mov2.png').convert_alpha()
        self.player_mov = [player_mov1, player_mov2]
        self.player_index = 0
        self.player_salto = pygame.image.load('imagenes/J1salto.png').convert_alpha()
        
        self.image= self.player_mov[self.player_index]
        self.rect= self.image.get_rect(midbottom = (80,330))
        self.gravity = 0
        
        self.salto_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.salto_sound.set_volume(0.2)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 330:
            self.gravity = -20
            self.salto_sound.play()
            
    def aplicamos_grav(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 330:
            self.rect.bottom = 330
    
    def animacion(self):
        if self.rect.bottom < 330: #animacion del jugador cuando salta
            self.image = self.player_salto
        else:  #animacion del jugador cuando anda
            self.player_index += 0.1  # si indicamos += 1, las imagenes de la animacion cambiarian demasiado rapido
            if self.player_index >= len(self.player_mov):  # este if statement nos sirve para que el += 0,1, no sobrepase el 1, y se mueva entre 0,1 ya que nuestra lista de movimiento solo tiene 0 y 1
                self.player_index = 0
            self.image = self.player_mov[int(self.player_index)]
            
    def update(self):  #esta funcion nos permitira actualizar los inputs y la gravedad de nuetro jufgador, hay que declararla en nuestro loop
        self.player_input()
        self.aplicamos_grav()
        self.animacion()


class Enemigos(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'enemigo2':
            enemigo2_f1= pygame.image.load('imagenes/enemigo2_f1.png').convert_alpha()
            enemigo2_f2= pygame.image.load('imagenes/enemigo2_f2.png').convert_alpha()
            self.enemigo_mov= [enemigo2_f1, enemigo2_f2]
            y_pos = 210
        else:
            enemigo1_f1= pygame.image.load('imagenes/enemigo1_f1.png').convert_alpha()
            enemigo1_f2= pygame.image.load('imagenes/enemigo1_f2.png').convert_alpha()
            self.enemigo_mov= [enemigo1_f1, enemigo1_f2]
            y_pos = 330
            
        self.mov_index = 0
        self.image= self.enemigo_mov[self.mov_index]
        self.rect = self.image.get_rect(midbottom= (randint(900,1100),y_pos))
        
        
        
    def animacion(self):
        self.mov_index += 0.1
        if self.mov_index >= len(self.enemigo_mov):
            self.mov_index = 0
        self.image = self.enemigo_mov[int(self.mov_index)]
        
    def destruir(self):
        if self.rect.x <= -100:
            self.kill()
        
    def update(self):
        self.animacion()
        self.rect.x -= 6
        self.destruir()
    
    
        
# FUNCIONES
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Puntuación: {current_time}', False, (64,64,64))
    score_rect= score_surface.get_rect(midtop = (400, 30))
    screen.blit(score_surface, score_rect)
    return current_time


def colisiones_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemigos_grupo, False):
        enemigos_grupo.empty()
        return False
    else:
        return True

    
#Variables

pygame.init() #starts pygame, es como encender el coche para que vaya
screen= pygame.display.set_mode((800,400)) #creamos pantalla para el juego
pygame.display.set_caption('Saltoke')

clock = pygame.time.Clock()
test_font= pygame.font.Font('fuente/PixeloidSans-mLxMm.ttf', 40)  #crear fuente para texto
instr_font = pygame.font.Font('fuente/PixeloidSans-mLxMm.ttf', 30)
game_active = False
start_time = 0
score = 0

musica_fondo= pygame.mixer.Sound('audio/music.wav')
musica_fondo.play(loops = -1)
musica_fondo.set_volume(0.1)
# GRUPOS
player = pygame.sprite.GroupSingle()
player.add(Player())

enemigos_grupo = pygame.sprite.Group()

# BACKGROUND
sky_surface = pygame.image.load('imagenes/Cielo.webp').convert()
ground_surface= pygame.image.load('imagenes/suelo1.png').convert()



# PANTALLA DE INICIO
titulo_surface = test_font.render('Saltoke', False, (111,196,169))  #el segundo argumento nos indica el smooth de las letras, el tercer argumento está indicando el color mediante una tupla rgb
titulo_rect= titulo_surface.get_rect(midtop = (400, 10))

inst_surface =  instr_font.render('Pulsa espacio para iniciar partida', False, (64,64,64))
inst_rect= inst_surface.get_rect(midbottom = (400, 340))

player_quieto= pygame.image.load('imagenes/J1estatico.png').convert_alpha()
player_quieto_red= pygame.transform.rotozoom(player_quieto, 0, 2) #rotozoom lo hace todo mas smooth que un simple scale, el segundo argumento te gira la surface los angulos marcados y el ultimo la escala en que lo augmentas
player_quieto_rect = player_quieto_red.get_rect(center = (400,200))

# TIMER

enemigos_timer= pygame.USEREVENT + 1 # ponemos el +1 para evitar conflictos con eventos predeterminados por pygame
pygame.time.set_timer(enemigos_timer, 1400)


# MAIN LOOP 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #para cerrar la ventana, es contrario al .init
            exit()
            
        if game_active:
            if event.type == enemigos_timer:
                enemigos_grupo.add(Enemigos(choice(['enemigo2', 'enemigo1', 'enemigo1', 'enemigo1'])))
       
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time= int(pygame.time.get_ticks() / 1000)  # Para resetear el timer
        
    if game_active: 
    # SCREEN BLITS   
        
        screen.blit(sky_surface, (0,0))  #blit nos deja poner una surface sobre la display y en que posicion
        screen.blit(ground_surface, (0,330))
        score = display_score()         
        
        
        #MODIFICACIONES JUGADOR

        player.draw(screen)
        player.update()
        
        
        enemigos_grupo.draw(screen)
        enemigos_grupo.update()
        
        #COLISIONES
        game_active = colisiones_sprite()
        
        
    else:
        screen.fill((94,129,162))
        screen.blit(player_quieto_red, player_quieto_rect)
        
        
        
        punt_surface = instr_font.render(f'Puntuación: {score}', False, (64,64,64))
        punt_rect = punt_surface.get_rect(midbottom = (400, 100))
        screen.blit(titulo_surface, titulo_rect)
        screen.blit(inst_surface, inst_rect)
        screen.blit(punt_surface, punt_rect)
        # podriamos aplicar un if statement para que en la pantalla de inicio, si la puntuacion es 0 te diga las instrucciones para jugar, y cunado no que te ponga el resultado
        

        #dibujar todos nuestros elementos y actualizar todo
    pygame.display.update()
    clock.tick(60) # el 60 te indica que el while true loop no corra mas que 60 fps