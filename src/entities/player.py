"""Jugador de Rayman"""

import pygame
import os
import sys
from src.entities.entity import Entity
from src.config import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_POWER,
    PLAYER_MAX_FALL_SPEED, GRAVITY, WHITE, YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT
)
from src.utils.collision import CollisionManager


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


class Player(Entity):
    """Clase del jugador Rayman"""
    
    def __init__(self, x: float, y: float):
        """Inicializa al jugador"""
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.is_jumping = False
        self.is_falling = False
        self.is_on_ground = False
        self.direction = 1  # 1 para derecha, -1 para izquierda
        self.can_jump = True
        self.jump_count = 0  # Para doble salto
        # Salud y respawn
        self.max_health = 3
        self.health = self.max_health
        self.spawn_x = x
        self.spawn_y = y

        # Invencibilidad temporal tras recibir daño (ms)
        self.invincible = False
        self.invincible_time = 1000
        self.invincible_timer = 0
        
        # Animaciones
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # frames por actualización
        
        # Sprites (se cargarán después de inicializar display)
        self.sprites = None
        self.has_sprites = False
        self.sprites_loaded = False
    
    def load_sprites(self):
        """Carga la imagen completa de Rayman desde rayman_a1.png"""
        if self.sprites_loaded:
            return
        
        base_path = get_base_path()
        sprite_path = os.path.join(base_path, "assets/sprites/Rayman")
        
        self.sprites = {
            "idle": None,
            "run": [],
            "jump": None,
            "fall": None,
            "dead": None
        }
        
        self.has_sprites = False
        
        try:
            # Cargar rayman_a1.png como imagen completa
            sprite_full_path = os.path.join(sprite_path, "rayman_a1.png")
            if os.path.exists(sprite_full_path):
                try:
                    # Cargar imagen
                    img = pygame.image.load(sprite_full_path).convert()
                    
                    # Obtener color del fondo (esquina superior izquierda)
                    background_color = img.get_at((0, 0))
                    img.set_colorkey(background_color)
                    img = img.convert_alpha()
                    
                    # NO escalar, usar tamaño original
                    print(f"Imagen cargada: {img.get_width()}x{img.get_height()} píxeles")
                    
                    # Usar la misma imagen para todos los estados
                    self.sprites["idle"] = img
                    self.sprites["jump"] = img
                    self.sprites["fall"] = img
                    self.sprites["run"] = [img]
                    self.has_sprites = True
                    
                    # Actualizar el tamaño del jugador al tamaño de la imagen
                    self.width = img.get_width()
                    self.height = img.get_height()
                    self.update_rect()
                    
                    print(f"Sprite Rayman cargado exitosamente")
                    print(f"Tamaño del jugador actualizado a: {self.width}x{self.height}")
                    
                except Exception as e:
                    print(f"Error cargando rayman_a1.png: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"Archivo no encontrado: {sprite_full_path}")
                
        except Exception as e:
            print(f"Advertencia: No se pudo cargar sprite ({e})")
            import traceback
            traceback.print_exc()
            self.has_sprites = False
    
    def get_current_sprite(self):
        """Retorna el sprite actual según el estado"""
        if not self.has_sprites or not self.sprites["idle"]:
            return None
        
        try:
            # Determinar animación
            if self.invincible and int(self.invincible_timer / 100) % 2 == 0:
                # Parpadeo de invencibilidad
                return None
            
            # Usar la imagen de Rayman siempre (sin cambios de pose)
            return self.sprites["idle"]
        except Exception as e:
            print(f"Error en get_current_sprite: {e}")
            return None
    
    def handle_input(self, keys):
        """Maneja la entrada del jugador"""
        # Movimiento horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED
            self.direction = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED
            self.direction = 1
        else:
            self.velocity_x = 0
        
        # Salto
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.can_jump:
            self.is_on_ground = False
            self.can_jump = False
            self.jump_count += 1
    
    def update(self, dt: float, platforms: list = None):
        """Actualiza el estado del jugador"""
        # Cargar sprites en la primera actualización (después de inicializar display)
        if not self.sprites_loaded:
            self.load_sprites()
            self.sprites_loaded = True
        
        # Actualizar temporizador de invencibilidad
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
                self.invincible_timer = 0
        # Aplicar gravedad
        self.velocity_y += GRAVITY
        
        # Limitar velocidad de caída
        if self.velocity_y > PLAYER_MAX_FALL_SPEED:
            self.velocity_y = PLAYER_MAX_FALL_SPEED
        
        # Aplicar velocidad
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.update_rect()
        
        # Colisiones con plataformas
        if platforms:
            self.handle_platform_collisions(platforms)
        
        # Permitir saltar de nuevo si está en el suelo
        if self.is_on_ground:
            self.can_jump = True
            self.jump_count = 0
            if self.velocity_y > 0:
                self.velocity_y = 0
        
        # Detección de caída
        if self.y > 800:  # Fuera de pantalla
            self.on_fall()

    def take_damage(self, amount: int = 1):
        """Aplica daño al jugador y maneja invencibilidad"""
        if self.invincible:
            return
        self.health -= amount
        # Activar invencibilidad temporal
        self.invincible = True
        self.invincible_timer = self.invincible_time

        # Efecto de retroceso
        self.velocity_y = -6

        if self.health <= 0:
            self.on_death()

    def on_death(self):
        """Se llama cuando el jugador pierde toda la salud"""
        # Reiniciar posición al spawn y restaurar salud
        self.set_position(self.spawn_x, self.spawn_y)
        self.health = self.max_health
        self.invincible = True
        self.invincible_timer = 1500
    
    def handle_platform_collisions(self, platforms):
        """Maneja colisiones con plataformas"""
        self.is_on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                direction = CollisionManager.get_collision_direction(self.rect, platform.rect)
                
                if direction == "top" and self.velocity_y >= 0:
                    self.y = platform.rect.top - self.height
                    self.velocity_y = 0
                    self.is_jumping = False
                    self.is_on_ground = True
                    self.update_rect()
                
                elif direction == "bottom" and self.velocity_y < 0:
                    self.y = platform.rect.bottom
                    self.velocity_y = 0
                    self.update_rect()
                
                elif direction == "left":
                    self.x = platform.rect.left - self.width
                    self.velocity_x = 0
                    self.update_rect()
                
                elif direction == "right":
                    self.x = platform.rect.right
                    self.velocity_x = 0
                    self.update_rect()
    
    def on_fall(self):
        """Se llama cuando el jugador cae fuera de pantalla"""
        self.set_position(100, 100)  # Reiniciar posición
    
    def draw(self, surface: pygame.Surface):
        """Dibuja al jugador"""
        try:
            sprite = self.get_current_sprite()
            
            if sprite:
                # Voltear sprite según dirección
                if self.direction == -1:
                    sprite = pygame.transform.flip(sprite, True, False)
                
                # Dibujar sprite
                surface.blit(sprite, (self.x, self.y))
                return
        except Exception as e:
            print(f"Error dibujando sprite: {e}")
        
        # Fallback: dibujo original si no hay sprites o error
        if self.invincible and (pygame.time.get_ticks() // 120) % 2 == 0:
            return
        
        pygame.draw.circle(surface, YELLOW, (self.x + self.width // 2, self.y + 10), 8)
        pygame.draw.rect(surface, YELLOW, (self.x + 8, self.y + 18, 16, 20))
        arm_y = self.y + 22
        pygame.draw.line(surface, YELLOW, (self.x + 8, arm_y), (self.x, arm_y), 3)
        pygame.draw.line(surface, YELLOW, (self.x + 24, arm_y), (self.x + 32, arm_y), 3)
