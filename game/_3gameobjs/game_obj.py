import numpy
import pygame
from _2components.transform.transform import Transform


class GameObject(pygame.sprite.Sprite):

    def __init__(self, pos: pygame.Vector2, level):
        super().__init__(level.all_sprites)

        self.level = level

        self.transform = Transform(self)
        self.transform.position = pos

        # adds itself to the level game object list
        level.all_game_obj.append(self)
        # calls its start() method
        self.start()

        # makes a default img to the object
        self.image = pygame.Surface((64, 32))
        self.image.fill((255, 255, 255))

        # - The rectangle that holds the game object's image
        # - The center pos of the rect is the same of the gm obj pos by default, but needs to be set back to the
        #   object pos at every movement, it's automatically made by the transform bia the move_position method
        self.rect = self.image.get_rect(center=self.transform.position)

    def get_index_in_level_list(self) -> int:
        for i in range(0, len(self.level.all_game_obj)):
            if self.level.all_game_obj[i] == self:
                return i

    def start(self) -> None:
        pass

    def tick(self) -> None:
        pass

    def render(self) -> None:
        pass

    def debug_render(self) -> None:
        # img rect
        pygame.draw.rect(self.level.game.screen, "red", self.rect, 1)