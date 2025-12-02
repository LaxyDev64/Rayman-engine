"""Definición de enemigos para el engine"""

import pygame
from src.entities.entity import Entity
from typing import Optional


class Enemy(Entity):
    """Clase base para enemigos"""

    def __init__(self, x: float, y: float, width: int, height: int, health: int = 1):
        super().__init__(x, y, width, height)
        self.health = health
        self.active = True
        self.velocity_x = 0
        self.velocity_y = 0

    def take_damage(self, amount: int = 1):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.active = False

    def update(self, dt: float):
        if not self.active:
            return
        # Movimiento por defecto (override en subclases)
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.update_rect()

    def draw(self, surface: pygame.Surface):
        # Dibujo por defecto (rectángulo rojo)
        if not self.active:
            return
        pygame.draw.rect(surface, (180, 30, 30), self.rect)


class SimpleEnemy(Enemy):
    """Enemigo simple que patrulla horizontalmente"""

    def __init__(self, x: float, y: float, width: int = 32, height: int = 32, patrol_range: int = 150, speed: float = 2.0):
        super().__init__(x, y, width, height, health=1)
        self.start_x = x
        self.patrol_range = patrol_range
        self.speed = speed
        self.direction = 1
        self.velocity_x = self.speed * self.direction

    def update(self, dt: float):
        if not self.active:
            return
        # Patrullar
        self.x += self.speed * self.direction
        if abs(self.x - self.start_x) > self.patrol_range:
            self.direction *= -1
            self.x += self.speed * self.direction
        self.update_rect()

    def draw(self, surface: pygame.Surface):
        if not self.active:
            return
        # Dibujo simple: cuerpo y ojo
        pygame.draw.rect(surface, (200, 40, 40), self.rect)
        # Ojo
        eye_x = int(self.x + (self.width * 0.7) if self.direction > 0 else self.x + (self.width * 0.3))
        pygame.draw.circle(surface, (255, 255, 255), (eye_x, int(self.y + self.height * 0.3)), 3)
