# 📚 Documentación Técnica - Rayman Engine

## Arquitectura General

El engine sigue un patrón **Entity-Component-Scene** donde:
- **Entities**: Son objetos del juego (jugador, plataformas, etc.)
- **Scenes**: Son niveles o pantallas que contienen entidades
- **Engine**: Gestiona las escenas y el bucle principal

## Diagrama de Clases

```
Entity (abstracta)
├── Player
├── Platform
├── Wall
├── Spike
└── Collectible

Scene (abstracta)
└── LevelScene

GameEngine
└── Scenes[]
```

## Flujo de Actualización

```
Engine.run()
├── handle_events()
├── update(dt)
│   └── Scene.update(dt)
│       └── Entity.update(dt)
└── draw()
    └── Scene.draw()
        └── Entity.draw()
```

## Sistema de Colisiones (AABB)

El sistema usa colisiones Axis-Aligned Bounding Box (AABB) rectangulares:

1. **Detección**: Se verifica si dos rectángulos se solapan
2. **Resolución**: Se determina la dirección de colisión
3. **Respuesta**: Se ajusta la posición del objeto

```python
# Dirección de colisión posibles:
- "top"    (desde arriba)
- "bottom" (desde abajo)
- "left"   (desde izquierda)
- "right"  (desde derecha)
```

## Física del Jugador

### Gravedad
- Aplicada en cada frame: `velocity_y += GRAVITY`
- Límite de caída: `PLAYER_MAX_FALL_SPEED`

### Salto
- Presionar ESPACIO: `velocity_y = -PLAYER_JUMP_POWER`
- Solo salta si está en el suelo: `is_on_ground == True`

### Movimiento
- Izquierda/Derecha: Cambia `velocity_x` de -PLAYER_SPEED a +PLAYER_SPEED
- Velocidad constante (sin aceleración)

## Estados del Jugador

```python
Player
├── is_jumping   # Está en el aire después de saltar
├── is_falling   # Está cayendo
├── is_on_ground # Está en contacto con una plataforma
├── direction    # -1 (izquierda) o 1 (derecha)
└── jump_count   # Contador de saltos (para doble salto)
```

## Sistema de Animaciones

La clase `Animation` maneja secuencias de frames:

```python
animation = Animation(
    frames=[frame1, frame2, frame3],
    frame_duration=10,  # ms por frame
    loop=True           # ¿se repite?
)
```

## Cómo Extender el Engine

### Crear una Entidad Personalizada

```python
from src.entities.entity import Entity
import pygame

class MiEnemigo(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
        self.health = 100
        self.speed = 2
    
    def update(self, dt):
        # Movimiento
        self.x += self.speed
        self.update_rect()
        
        # Lógica especial
        if self.x > 1280:
            self.x = 0
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.active = False
```

### Crear una Escena Personalizada

```python
from src.scenes.scene import Scene
from src.entities.world import Platform

class BossScene(Scene):
    def setup(self):
        # Crear el jefe
        self.boss = MiBoss(640, 100)
        self.add_entity(self.boss)
        
        # Crear plataformas
        platform = Platform(0, 600, 1280, 50)
        self.add_entity(platform)
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
    
    def update(self, dt):
        # Lógica de escena
        for entity in self.entities:
            entity.update(dt)
    
    def draw(self, surface):
        surface.fill((100, 100, 100))
        for entity in self.entities:
            entity.draw(surface)
```

## Optimización y Rendimiento

### Tips de Optimización

1. **Culling**: Solo actualiza entidades visibles
2. **Pooling**: Reutiliza objetos en lugar de crear/destruir
3. **Caché**: Precalcula valores que no cambian frecuentemente
4. **Batching**: Agrupa dibujos similares

### Monitoreo de Rendimiento

```python
import time

start = time.time()
# código
end = time.time()
print(f"Tiempo: {(end - start) * 1000:.2f}ms")
```

## Debugging

### Mostrar Rectángulos de Colisión

```python
# En LevelScene.draw()
for entity in self.entities:
    entity.draw(surface)
    pygame.draw.rect(surface, (255, 0, 0), entity.rect, 1)  # Debug
```

### Mostrar Velocidades

```python
font = pygame.font.Font(None, 24)
debug_text = font.render(
    f"VX: {player.velocity_x:.2f} VY: {player.velocity_y:.2f}", 
    True, 
    (255, 255, 255)
)
surface.blit(debug_text, (10, 50))
```

## Configuración de Niveles

### Crear un Nivel Procedural

```python
class ProceduralLevel(LevelScene):
    def setup(self):
        super().setup()
        
        # Generar plataformas aleatorias
        import random
        for i in range(10):
            x = random.randint(100, 1100)
            y = 200 + i * 80
            platform = Platform(x, y, 150, 20)
            self.platforms.append(platform)
            self.add_entity(platform)
```

## Conversión de Assets

Para usar sprites reales del juego:

1. **Formato**: Usa PNG con transparencia
2. **Tamaño**: Mantén proporciones consistentes
3. **Carga**:

```python
sprite = pygame.image.load("assets/sprites/player.png")
sprite = pygame.transform.scale(sprite, (32, 48))
```

---

**Nota**: Este documento se actualizará conforme el engine evolucione.
