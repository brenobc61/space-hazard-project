import pygame
import os
import random
pygame.font.init()

# configurando janela do jogo
WINDOW_WIDTH, WINDOW_HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Hazard")

# carregando imagens das entidades
ASTEROID_IMAGE = pygame.image.load(os.path.join("assets", "asteroid.png"))
GREAT_ASTEROID_IMAGE = pygame.image.load(os.path.join("assets", "great_asteroid.png"))
ALIEN_IMAGE = pygame.image.load(os.path.join("assets", "alien.png"))
ENEMY_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "enemy_ship.png"))
ELITE_ENEMY_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "elite_enemy_ship.png"))
MOTHER_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "mother_ship.png"))
PLAYER_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "player_ship.png"))

# carregando imagens dos lasers
ELITE_ENEMY_SHIP_LASER_IMAGE = pygame.image.load(os.path.join("assets", "elite_enemy_ship_laser.png"))
ENEMY_SHIP_LASER_IMAGE = pygame.image.load(os.path.join("assets", "enemy_ship_laser.png"))
MOTHER_SHIP_LASER_IMAGE = pygame.image.load(os.path.join("assets", "mother_ship_laser.png"))
PLAYER_LASER_IMAGE = pygame.image.load(os.path.join("assets", "player_laser.png"))

# carregando imagens de fundo
BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets", "background.png"))
TITLE_BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets", "title_background.png"))

# redimensionando as imagens de fundo para ficarem compatíveis com a janela do jogo
SCALED_BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
SCALED_TITLE_BACKGROUND_IMAGE = pygame.transform.scale(TITLE_BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))

class Entity():
    LASER_INTERVAL = 8

    def __init__(self, x, y, hp=1):
        self.x = x
        self.y = y
        self.health = hp
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.interval_counter = 0   
        self.speed = 1.5
        self.enemy_laser_speed = 7

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, obj, window_height):
        self.cooldown()
        for laser in self.lasers:
            laser.move(self.enemy_laser_speed)
            if laser.off_screen(window_height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 1
                self.lasers.remove(laser)

    def cooldown(self):
        if self.interval_counter >= self.LASER_INTERVAL:
            self.interval_counter = 0
        elif self.interval_counter > 0:
            self.interval_counter += 1

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()  
    
    def move(self):
        self.y += self.speed

class Player(Entity):
    def __init__(self, x, y, hp=5):
        super().__init__(x, y, hp)
        self.ship_image = PLAYER_SHIP_IMAGE
        self.laser_image = PLAYER_LASER_IMAGE
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.laser_speed = -30

    def move_lasers(self, objs, window_height):
        self.cooldown()
        pontos = 0
        for laser in self.lasers:
            laser.move(self.laser_speed)
            if laser.off_screen(window_height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= 1
                        if obj.health <= 0:
                            objs.remove(obj)
                            pontos = 10
                        if laser in self.lasers:
                            self.lasers.remove(laser)
        return pontos
    
    def shoot(self):
        if self.interval_counter == 0:
            laser = Laser(self.x, self.y, self.laser_image)
            self.lasers.append(laser)
            self.interval_counter = 1

class Asteroid(Entity):
    def __init__(self, x, y, hp=1):
        super().__init__(x, y, hp)
        self.ship_image = ASTEROID_IMAGE
        self.mask = pygame.mask.from_surface(self.ship_image)

class GreatAsteroid(Entity):
    def __init__(self, x, y, hp=5):
        super().__init__(x, y, hp)
        self.ship_image = GREAT_ASTEROID_IMAGE
        self.mask = pygame.mask.from_surface(self.ship_image)

class Alien(Entity):
    def __init__(self, x, y, hp=2):
        super().__init__(x, y, hp)
        self.ship_image = ALIEN_IMAGE
        self.mask = pygame.mask.from_surface(self.ship_image)

class EnemyShip(Entity):
    def __init__(self, x, y, hp=5):
        super().__init__(x, y, hp)
        self.ship_image = ENEMY_SHIP_IMAGE
        self.laser_image = ENEMY_SHIP_LASER_IMAGE
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.enemy_laser_speed = 7

    def shoot(self):
        if self.interval_counter == 0:
            laser = Laser(self.x-5, self.y, self.laser_image)
            self.lasers.append(laser)
            self.interval_counter = 1

class EliteEnemyShip(Entity):  
    def __init__(self, x, y, hp=5):
        super().__init__(x, y, hp)
        self.ship_image = ELITE_ENEMY_SHIP_IMAGE
        self.laser_image = ELITE_ENEMY_SHIP_LASER_IMAGE
        self.mask = pygame.mask.from_surface(self.ship_image)

    def shoot(self):
        if self.interval_counter == 0:
            laser = Laser(self.x-5, self.y, self.laser_image)
            self.lasers.append(laser)
            self.interval_counter = 1

class MotherShip(Entity):    
    def __init__(self, x, y, hp=35):
        super().__init__(x, y, hp)
        self.ship_image = MOTHER_SHIP_IMAGE
        self.laser_image = MOTHER_SHIP_LASER_IMAGE
        self.mask = pygame.mask.from_surface(self.ship_image)

    def shoot(self):
        if self.interval_counter == 0:
            laser = Laser(self.x+54, self.y, self.laser_image)
            self.lasers.append(laser)
            self.interval_counter = 1

class Laser:
    def __init__(self, x, y, laser_image):
        self.x = x
        self.y = y
        self.laser_image = laser_image
        self.mask = pygame.mask.from_surface(self.laser_image)
        
    def draw(self, window):
        window.blit(self.laser_image, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(obj, self)

# função para verificar se uma entidade do jogo colidiu com outra
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def game():
    FPS = 60
    game_runnig = True
    stage = 0
    player_speed = 8
    victory = False
    enemies = []
    score = 0
    game_over = False
    game_over_count = 0
    player = Player(300, 650)
    clock = pygame.time.Clock()

    # definindo as fontes da interface do jogo
    main_font = pygame.font.SysFont("simsun", 30)
    score_font = pygame.font.SysFont("simsun", 20)
    lost_font = pygame.font.SysFont("simsun", 60)

    # função para desenhar a tela
    def redraw_window():

        # função para transformar as vidas do jogador em barras verticais
        def get_player_health_in_bars(player_hp):
            health_in_bars = ""
            for i in range(0, player_hp):
                health_in_bars += '|'
            return health_in_bars
    
        # desenhando a interface do jogador
        health_label = main_font.render(f"{get_player_health_in_bars(player.health)}", 1 , (255, 255, 255))
        level_label = main_font.render(f"Fase: {stage}/3", 1 , (255, 255, 255))
        score_label = score_font.render(f"Pontos: {score}/1300", 1 , (255, 255, 255))

        WINDOW.blit(SCALED_BACKGROUND_IMAGE, (0, 0))
        WINDOW.blit(health_label, (10, 10))
        WINDOW.blit(level_label, (WINDOW_WIDTH - level_label.get_width() - 10, 10))
        WINDOW.blit(score_label, (WINDOW_WIDTH - score_label.get_width() - 10, 50))

        # desenhando os inimigos
        for enemy in enemies:
            enemy.draw(WINDOW)

        # desenhando mensagem de game over (fim de jogo)
        if game_over:
            lost_label = lost_font.render("VOCÊ PERDEU", 1, (255, 255, 255))
            WINDOW.blit(lost_label, (WINDOW_WIDTH/2 - lost_label.get_width()/2, 350))

        # desenhando mensagem de vitória (jogo concluído)
        if victory:
            lost_label = lost_font.render("VITÓRIA", 1, (255, 255, 255))
            WINDOW.blit(lost_label, (WINDOW_WIDTH/2 - lost_label.get_width()/2, 350))

        # desenhando jogador
        player.draw(WINDOW)

        # atualizando a tela
        pygame.display.update()
    
    while game_runnig:
        clock.tick(FPS)
        redraw_window()

        # checando se o jogador venceu o jogo
        if stage == 3:
            if len(enemies) == 0:
                game_over_count += 1
                victory = True

        # checando se o jogador perdeu o jogo
        if player.health <= 0:
            game_over = True
            game_over_count += 1

        # finalizando o jogo caso o jogador tenha ganhado ou perdido
        if game_over or victory:
            if game_over_count > FPS * 3:
                game_runnig = False
            else:
                continue

        # posicionando os inimigos de acordo com a fase
        if len(enemies) == 0 and victory == False:
            stage += 1
            if stage == 1:             
                enemies.append(Asteroid(130, -200))
                enemies.append(Asteroid(500, -300))
                enemies.append(GreatAsteroid(320, -550))
                enemies.append(Asteroid(110, -590))
                enemies.append(Asteroid(280, -630))
                enemies.append(Asteroid(130, -700))
                enemies.append(Asteroid(190, -780))
                enemies.append(Asteroid(550, -800))
                enemies.append(Asteroid(430, -830))
                enemies.append(Alien(180, -1100))
                enemies.append(Alien(330, -1100))
                enemies.append(Alien(480, -1100))
                enemies.append(Asteroid(550, -1200))
                enemies.append(Asteroid(260, -1400))
                enemies.append(Asteroid(130, -1480))
                enemies.append(GreatAsteroid(500, -1500))
                enemies.append(GreatAsteroid(150, -1600))
                enemies.append(Asteroid(500, -1650))
                enemies.append(Asteroid(530, -1700))
                enemies.append(EnemyShip(330, -1710))
                enemies.append(Asteroid(240, -1780))
                enemies.append(Alien(120, -1900))
                enemies.append(EnemyShip(210, -2000))
                enemies.append(Alien(440, -2100))
                enemies.append(Alien(530, -2100))
                enemies.append(Asteroid(360, -2220))
                enemies.append(EnemyShip(490, -2300))
                enemies.append(Asteroid(190, -2500))
                enemies.append(GreatAsteroid(220, -2700))
                enemies.append(Asteroid(110, -2800))
                enemies.append(Asteroid(170, -2900))
                enemies.append(Asteroid(490, -3000))
                enemies.append(Asteroid(450, -3100))
                enemies.append(Alien(180, -3200))
                enemies.append(Alien(240, -3200))
                enemies.append(Alien(210, -3300))
                enemies.append(Asteroid(330, -3400))
                enemies.append(Alien(380, -3600))
                enemies.append(Alien(440, -3600))
                enemies.append(Alien(410, -3700))
                enemies.append(GreatAsteroid(210, -3720))
                enemies.append(Asteroid(130, -3850))
                enemies.append(Asteroid(520, -3850))
                enemies.append(EnemyShip(180, -4100))
                enemies.append(EnemyShip(330, -4100))
                enemies.append(EnemyShip(480, -4100))
            elif stage == 2:
                enemies.append(Asteroid(80, -190))
                enemies.append(Asteroid(610, -180))
                enemies.append(GreatAsteroid(150, -200))
                enemies.append(Asteroid(580, -300))
                enemies.append(Asteroid(620, -340))
                enemies.append(EliteEnemyShip(350, -400))
                enemies.append(Alien(150, -700))
                enemies.append(Alien(250, -700))
                enemies.append(Alien(200, -750))
                enemies.append(Asteroid(310, -840))
                enemies.append(Alien(450, -900))
                enemies.append(Alien(550, -900))
                enemies.append(Alien(500, -950))
                enemies.append(EnemyShip(150, -1100))
                enemies.append(EnemyShip(350, -1100))
                enemies.append(Asteroid(440, -1200))
                enemies.append(Asteroid(410, -1350))
                enemies.append(EnemyShip(500, -1500))
                enemies.append(EnemyShip(350, -1500))
                enemies.append(GreatAsteroid(130, -1580))
                enemies.append(GreatAsteroid(240, -1750))
                enemies.append(Asteroid(480, -1850))
                enemies.append(Asteroid(510, -1950))
                enemies.append(EnemyShip(180, -2200))
                enemies.append(EnemyShip(480, -2200))
                enemies.append(EliteEnemyShip(330, -2250))
                enemies.append(GreatAsteroid(240, -2500))
                enemies.append(Asteroid(180, -2700))
                enemies.append(Asteroid(330, -2700))
                enemies.append(Asteroid(480, -2700))
                enemies.append(GreatAsteroid(330, -2900))
                enemies.append(EliteEnemyShip(180, -2900))
                enemies.append(EliteEnemyShip(480, -2900))
            elif stage == 3:
                enemies.append(Asteroid(50, -200))
                enemies.append(Asteroid(100, -200))
                enemies.append(Asteroid(150, -200))
                enemies.append(Asteroid(200, -200))
                enemies.append(Asteroid(250, -200))
                enemies.append(Asteroid(300, -200))
                enemies.append(Asteroid(350, -200))
                enemies.append(Asteroid(400, -200))
                enemies.append(Asteroid(450, -200))
                enemies.append(Asteroid(500, -200))
                enemies.append(Asteroid(550, -200))
                enemies.append(Asteroid(600, -200))
                enemies.append(Asteroid(650, -200))
                enemies.append(Alien(150, -410))
                enemies.append(Alien(250, -410))
                enemies.append(Alien(350, -410))
                enemies.append(Alien(450, -410))
                enemies.append(GreatAsteroid(500, -600))
                enemies.append(Asteroid(360, -720))
                enemies.append(Asteroid(410, -790))
                enemies.append(EliteEnemyShip(190, -810))
                enemies.append(EnemyShip(250, -1000))
                enemies.append(EnemyShip(380, -1000))
                enemies.append(EnemyShip(350, -1200))
                enemies.append(EnemyShip(480, -1200))
                enemies.append(Asteroid(550, -1300))
                enemies.append(Asteroid(260, -1350))
                enemies.append(EliteEnemyShip(250, -1600))
                enemies.append(EliteEnemyShip(400, -1600))
                enemies.append(GreatAsteroid(150, -1800))
                enemies.append(GreatAsteroid(300, -1800))
                enemies.append(GreatAsteroid(450, -1800))
                enemies.append(EnemyShip(150, -2000))
                enemies.append(EnemyShip(250, -2000))
                enemies.append(EnemyShip(450, -2000))
                enemies.append(EnemyShip(550, -2000))
                enemies.append(EnemyShip(550, -2000))
                enemies.append(Alien(150, -2300))
                enemies.append(EnemyShip(450, -2300))
                enemies.append(EnemyShip(550, -2300))
                enemies.append(EliteEnemyShip(150, -2600))
                enemies.append(Alien(450, -2600))
                enemies.append(Alien(550, -2600))
                enemies.append(EnemyShip(250, -2800))
                enemies.append(EliteEnemyShip(350, -2800))
                enemies.append(EliteEnemyShip(150, -3200))
                enemies.append(EliteEnemyShip(250, -3200))
                enemies.append(EliteEnemyShip(450, -3200))
                enemies.append(EliteEnemyShip(550, -3200))
                enemies.append(EliteEnemyShip(550, -3200))
                enemies.append(MotherShip(150, -3800))

        # verificando se o jogador fechou a aplicação     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # movimentação do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_speed > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x + player_speed + player.get_width() < WINDOW_WIDTH:
            player.x += player_speed
        if keys[pygame.K_SPACE]:
            player.shoot()

        # controlando ações das entidades do jogo
        for enemy in enemies[:]:
            enemy.move()

            # movendo os lasers dos inimigos
            if isinstance(enemy, EnemyShip) or isinstance(enemy, EliteEnemyShip) or isinstance(enemy, MotherShip):
                enemy.move_lasers(player, WINDOW_HEIGHT)

            # fazendo os inimigos atirarem de forma aleatória
            if random.randrange(0, 150) == 1:
                if isinstance(enemy, EnemyShip) or isinstance(enemy, EliteEnemyShip):
                    enemy.shoot()

            # fazendo o inimigo final atirar de forma aleatória com frequência maior do que inimigos normais
            if random.randrange(0, 50) == 1:
                if isinstance(enemy, MotherShip):
                    enemy.shoot()
                    
            # verificando se os inimigos estão colidindo com o jogador ou se ultrapassaram o jogador
            if collide(enemy, player):
                player.health -= 1 
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > WINDOW_HEIGHT:
                if isinstance(enemy, MotherShip):
                    player.health = 0
                else:
                    player.health -= 1
                    enemies.remove(enemy)

        # movendo o laser do jogador e calculando a pontuação dele caso acerte um inimigo
        score += player.move_lasers(enemies, WINDOW_HEIGHT)

def main():
    game_running = True

    # definindo as fontes do menu do jogo
    description_font = pygame.font.SysFont("simsun", 40)
    controls_font = pygame.font.SysFont("simsun", 30)
    
    # desenhando a janela de menu do jogo
    while game_running:
        controls_label1 = controls_font.render("CONTROLES:", 1, (255, 255, 255))
        controls_label2 = controls_font.render("->: ir para esquerda", 1, (255, 255, 255))
        controls_label3 = controls_font.render("<-: ir para direita", 1, (255, 255, 255))
        controls_label4 = controls_font.render("ESPAÇO: Atirar", 1, (255, 255, 255))
        description_label = description_font.render("> Aperte ESPAÇO para começar <", 1, (255, 255, 255))

        WINDOW.blit(SCALED_TITLE_BACKGROUND_IMAGE, (0, 0))
        WINDOW.blit(controls_label1, (WINDOW_WIDTH/2 - controls_label1.get_width()/2, 300))
        WINDOW.blit(controls_label2, (WINDOW_WIDTH/2 - controls_label2.get_width()/2, 350))
        WINDOW.blit(controls_label3, (WINDOW_WIDTH/2 - controls_label3.get_width()/2, 400))
        WINDOW.blit(controls_label4, (WINDOW_WIDTH/2 - controls_label4.get_width()/2, 450))
        WINDOW.blit(description_label, (WINDOW_WIDTH/2 - description_label.get_width()/2, 550))

        # verificando se o jogador inicia ou sai do jogo
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game()
    pygame.quit()

main()