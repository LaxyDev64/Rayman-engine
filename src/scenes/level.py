"""Escena de nivel del juego"""

import pygame
import os
import glob
import sys
from src.scenes.scene import Scene
from src.entities.player import Player
from src.entities.world import Platform, Wall, Spike, Collectible
from src.entities.enemy import SimpleEnemy
from src.utils.collision import CollisionManager
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_JUMP_POWER


def get_base_path():
    """Obtiene la ruta base de la aplicacion (compatible con PyInstaller)"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Ejecutable PyInstaller - usa MEIPASS
        return sys._MEIPASS
    elif getattr(sys, 'frozen', False):
        # Ejecutable PyInstaller sin MEIPASS
        return os.path.dirname(sys.executable)
    else:
        # Ejecucion desde script
        return os.getcwd()


class LevelScene(Scene):
    """Escena de un nivel del juego"""
    
    def __init__(self, width: int, height: int):
        """Inicializa la escena de nivel"""
        super().__init__(width, height)
        self.player = None
        self.platforms = []
        self.enemies = []
        self.collectibles = []
        self.score = 0
        self.background = None
        self.background_loaded = False
        self.ui_bar = None
        self.ui_bar_loaded = False
        self.setup()
    
    def load_background(self):
        """Carga el fondo del nivel"""
        if self.background_loaded:
            return
        
        base_path = get_base_path()
        # Buscar el archivo de fondo con wildcard
        bg_patterns = [
            os.path.join(base_path, "assets", "sprites", "PC*Castle*Background.png"),
            os.path.join(base_path, "assets", "sprites", "PC _ Computer - Rayman Legends - Levels - Outside Castle Background.png")
        ]
        
        bg_path = None
        for pattern in bg_patterns:
            matches = glob.glob(pattern)
            if matches:
                bg_path = matches[0]
                break
        
        if bg_path and os.path.exists(bg_path):
            try:
                self.background = pygame.image.load(bg_path).convert_alpha()
                self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print(f"Fondo cargado: {bg_path}")
            except Exception as e:
                print(f"Advertencia: No se pudo cargar fondo ({e})")
                self.background = None
        else:
            print(f"Advertencia: Archivo de fondo no encontrado")
            self.background = None
        
        self.background_loaded = True
    
    def load_ui_bar(self):
        """Carga la barra UI de Rayman"""
        if self.ui_bar_loaded:
            return
        
        base_path = get_base_path()
        ui_path = os.path.join(base_path, "assets", "sprites", "Rayman", "ui_bar_rayman_a1.png")
        if os.path.exists(ui_path):
            try:
                self.ui_bar = pygame.image.load(ui_path).convert_alpha()
                # Escalar la barra UI
                self.ui_bar = pygame.transform.scale(self.ui_bar, (280, 110))
                print("Barra UI cargada exitosamente")
            except Exception as e:
                print(f"Advertencia: No se pudo cargar barra UI ({e})")
                self.ui_bar = None
        else:
            print(f"Advertencia: Archivo UI no encontrado: {ui_path}")
            self.ui_bar = None
        
        self.ui_bar_loaded = True
    
    def setup(self):
        """Configura el nivel"""
        # Crear jugador
        self.player = Player(100, 100)
        self.add_entity(self.player)
        
        # Crear plataformas (suelo)
        ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, (100, 150, 100))
        self.platforms.append(ground)
        self.add_entity(ground)
        
        # Crear plataformas flotantes
        platform1 = Platform(300, SCREEN_HEIGHT - 200, 150, 20, (100, 150, 100))
        platform2 = Platform(600, SCREEN_HEIGHT - 300, 150, 20, (100, 150, 100))
        platform3 = Platform(900, SCREEN_HEIGHT - 250, 150, 20, (100, 150, 100))
        
        for p in [platform1, platform2, platform3]:
            self.platforms.append(p)
            self.add_entity(p)
        
        # Crear paredes
        wall_left = Wall(0, 0, 20, SCREEN_HEIGHT)
        wall_right = Wall(SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT)
        self.add_entity(wall_left)
        self.add_entity(wall_right)
        self.platforms.append(wall_left)
        self.platforms.append(wall_right)
        
        # Crear púas
        spike1 = Spike(250, SCREEN_HEIGHT - 70)
        spike2 = Spike(400, SCREEN_HEIGHT - 250)
        self.add_entity(spike1)
        self.add_entity(spike2)
        
        # Crear objetos coleccionables
        for i in range(5):
            collectible = Collectible(200 + i * 80, SCREEN_HEIGHT - 120)
            self.collectibles.append(collectible)
            self.add_entity(collectible)

        # Crear enemigos simples
        enemy1 = SimpleEnemy(500, SCREEN_HEIGHT - 82, patrol_range=200, speed=1.6)
        enemy2 = SimpleEnemy(650, SCREEN_HEIGHT - 332, patrol_range=120, speed=1.2)
        self.enemies.append(enemy1)
        self.enemies.append(enemy2)
        self.add_entity(enemy1)
        self.add_entity(enemy2)
    
    def handle_input(self, event: pygame.event.Event):
        """Maneja la entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
    
    def update(self, dt: float):
        """Actualiza la escena"""
        # Cargar fondo y UI en la primera actualización
        if not self.background_loaded:
            self.load_background()
        if not self.ui_bar_loaded:
            self.load_ui_bar()
        
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # Actualizar entidades
        for entity in self.entities:
            if isinstance(entity, Player):
                entity.update(dt, self.platforms)
            else:
                entity.update(dt)
        
        # Revisar colisiones con coleccionables
        for collectible in self.collectibles:
            if not collectible.collected and self.player.rect.colliderect(collectible.rect):
                collectible.collected = True
                self.score += collectible.value
        
        # Revisar colisiones con púas
        spikes = self.get_entities_by_type(Spike)
        for spike in spikes:
            if self.player.rect.colliderect(spike.rect):
                self.player.on_fall()

        # Revisar colisiones con enemigos
        enemies = self.get_entities_by_type(SimpleEnemy)
        for enemy in enemies:
            if not enemy.active:
                continue
            if self.player.rect.colliderect(enemy.rect):
                direction = CollisionManager.get_collision_direction(self.player.rect, enemy.rect)
                # Si el jugador cae sobre el enemigo, lo mata
                if direction == "top" and self.player.velocity_y > 0:
                    enemy.take_damage(1)
                    # Rebote del jugador
                    self.player.velocity_y = -PLAYER_JUMP_POWER / 2
                else:
                    # El jugador recibe daño
                    self.player.take_damage(1)
    
    def draw(self, surface: pygame.Surface):
        """Dibuja la escena"""
        try:
            # Dibujar fondo si existe
            if self.background:
                surface.blit(self.background, (0, 0))
            else:
                surface.fill(self.background_color)
                # Dibujar cielo (gradiente simulado)
                pygame.draw.rect(surface, (135, 206, 235), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        except Exception as e:
            print(f"Error dibujando fondo: {e}")
            surface.fill(self.background_color)
        
        # Dibujar todas las entidades
        for entity in self.entities:
            try:
                entity.draw(surface)
            except Exception as e:
                print(f"Error dibujando entidad: {e}")
        
        # Dibujar UI Bar si existe
        if self.ui_bar:
            try:
                surface.blit(self.ui_bar, (10, 10))
                # Dibujar puntuación sobre la barra UI
                font_large = pygame.font.Font(None, 36)
                font_small = pygame.font.Font(None, 28)
                
                score_text = font_large.render(f"{self.score}", True, (255, 215, 0))
                surface.blit(score_text, (50, 25))
                
                # Salud
                health_text = font_small.render(f"{self.player.health}/{self.player.max_health}", True, (255, 100, 100))
                surface.blit(health_text, (50, 65))
            except Exception as e:
                print(f"Error dibujando UI bar: {e}")
        else:
            # Fallback a HUD simple sin barra UI
            try:
                font_large = pygame.font.Font(None, 40)
                font_small = pygame.font.Font(None, 32)
                
                # Panel HUD de fondo semitransparente
                hud_surface = pygame.Surface((250, 100))
                hud_surface.set_alpha(200)
                hud_surface.fill((0, 0, 0))
                surface.blit(hud_surface, (10, 10))
                
                # Puntuación
                score_text = font_large.render(f"Score: {self.score}", True, (255, 215, 0))
                surface.blit(score_text, (20, 20))
                
                # Salud
                health_text = font_small.render(f"Health: {self.player.health}/{self.player.max_health}", True, (255, 100, 100))
                surface.blit(health_text, (20, 60))
            except Exception as e:
                print(f"Error dibujando HUD: {e}")
