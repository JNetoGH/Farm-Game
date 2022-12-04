import pygame
from _2components.component_base_class.component import Component


class SingleSprite(Component):

    def __init__(self, img_path, game_object_owner):
        super().__init__(game_object_owner)
        self._img_path = img_path
        self.sprite_img_as_surface = pygame.image.load(self._img_path).convert_alpha()
        self._game_object_owner.image = self.sprite_img_as_surface
        self._game_object_owner.rect = self._game_object_owner.image.get_rect(center=self._game_object_owner.transform.position_read_only)

    def change_image(self, new_img_path):
        self._img_path = new_img_path
        self.sprite_img_as_surface = pygame.image.load(self._img_path).convert_alpha()

    # scaled like 0.8 = 80%
    def scale_itself(self, scale):
        _scaled_sprite_as_surface = SingleSprite._return_scaled_image_surface(self.sprite_img_as_surface, scale)
        self._game_object_owner.image = _scaled_sprite_as_surface
        self._game_object_owner.rect = self._game_object_owner.image.get_rect(center=self._game_object_owner.transform.position_read_only)

    # scaled like 0.8 = 80%
    @staticmethod
    def _return_scaled_image_surface(surface_img, scale):
        return pygame.transform.scale(surface_img, (surface_img.get_width() * scale, surface_img.get_height() * scale))

    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(SingleSprite)\n" \
               f"path: {self._img_path}\n"
