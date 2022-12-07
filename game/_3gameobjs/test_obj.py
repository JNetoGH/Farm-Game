import pygame
from _2components.collider.collider import Collider
from _2components.single_sprite.single_sprite import SingleSprite
from _3gameobjs.game_object_base_class import GameObject


class TestObj(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        # animation_clip = AnimationClip("clip_test", "_0engine_resources/graphics/character/down_axe")
        # self.animationController = AnimationController([animation_clip], self)
        self.single_sprite = SingleSprite("game_res/graphics/character/down_axe/0.png", self)
        self.single_sprite.scale_itself(2)
        self.transform.move_world_position(pygame.Vector2(200, 200))

        self.collider = Collider(0,0,400,400,self)

    # called every frame
    def game_object_update(self) -> None:
        #increment = pygame.Vector2(1, 1)
        #self.transform.translate(increment)
        # self.animationController.animate()
        pass

    def get_inspector_debugging_status(self) -> str:
        return super(TestObj, self).get_inspector_debugging_status()
