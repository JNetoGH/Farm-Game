import pygame
from _1systems.input_manager_system import InputManager
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _1systems.game_time_system import GameTime
from _1systems.text_rendering_system import TextRender
from _2components.collider.collider import Collider
from scene import Scene


class InspectorDebuggingCanvas:

    def __init__(self, scene: Scene, font_size=10):
        self.current_game_object_index = 0
        self.current_scene = scene
        self.font_size = font_size

    def render_inspector_debugging_text(self):
        font = pygame.font.Font('_0resources/fonts/JetBrainsMono-Medium.ttf',
                                self.font_size)  # create a text surface object,

        msgs = "JNETO PRODUCTIONS GAME ENGINE: INSPECTOR DEBUGGING SYSTEM\n\n" \
               f"ENGINE INNER DETAILS\n" \
               f"fps: {self.current_scene.game.clock.get_fps():.1f}\n" \
               f"elapsed updates: {self.current_scene.game.elapsed_updates}\n" \
               f"delta-time: {str(GameTime.DeltaTime)}\n\n" \
               f"{ScalableGameScreen.get_inspector_debugging_status()}\n" + \
               f"{InputManager.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.all_game_obj[1].get_inspector_debugging_status()}\n"  # player is 0 in the list of objects as well

        # calls the method that displays text on the dummy screen
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth // 3,
                             msgs, (20, 20), font, color=pygame.Color("white"))

    def render_game_objects_gizmos(self):
        for gm_obj in self.current_scene.all_game_obj:
            font_size = 15
            font = pygame.font.Font('_0resources/fonts/JetBrainsMono-Medium.ttf', font_size)  # create a text surface object
            if gm_obj.transform.is_center_point_appearing_on_screen_read_only:
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_transform(gm_obj, "black", font, font_size)
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_image_rect(gm_obj, "red", font, font_size)
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_debugging_stats(gm_obj, "black", font)
            if gm_obj.has_collider:
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_colliders(gm_obj, "yellow", font, font_size)

    @staticmethod
    def _render_gizmos_of_game_obj_transform(game_obj, color: str, font: pygame.font.Font, font_size: int) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only

        description_spacing_x = 30
        description_spacing_y = 30

        # TRANSFORM GIZMOS
        # render the point
        pygame.draw.circle(ScalableGameScreen.GameScreenDummySurface, color, object_screen_pos, 5)
        # description
        text_transform = f"{game_obj.name}'s Transform.world_position\n(x:{game_obj.transform.world_position.x} | y:{game_obj.transform.world_position.y})\n" \
                         f"{game_obj.name}'s Transform.screen_position\n(x:{game_obj.transform.screen_position_read_only.x} | y:{game_obj.transform.screen_position_read_only.y})"
        # render description
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth,
                             text_transform,
                             (object_screen_pos[0] + description_spacing_x,
                              object_screen_pos[1] - font_size // 2 - description_spacing_y),
                             font, color=pygame.Color(color))

    @staticmethod
    def _render_gizmos_of_game_obj_image_rect(game_obj, color: str, font: pygame.font.Font, font_size: int) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only

        # IMAGE RECT GIZMOS
        # render the rect
        pygame.draw.rect(ScalableGameScreen.GameScreenDummySurface, color, game_obj.image_rect, 1)
        # description
        text_img_rect = "self.image.image_rect"
        # render render description
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth,
                             text_img_rect,
                             (object_screen_pos[0] - game_obj.image_rect.width // 2,
                              object_screen_pos[1] - game_obj.image_rect.height // 2 - font_size - 5),
                             font, color=pygame.Color(color))

    @staticmethod
    def _render_gizmos_of_game_obj_debugging_stats(game_obj, color: str, font: pygame.font.Font) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only

        description_spacing_x = 30
        description_spacing_y = 30

        # THE DEBUGGING STATS IS ALSO GOING TO APPEAR AS GIZMOS
        components_names = game_obj.get_this_game_object_components_list_as_string()
        # description
        game_object_stats_text = \
            f"GAME OBJECT INSPECTOR \n" \
            f"\ngame object name: {game_obj.name}\n" \
            f"class name: {type(game_obj)} \n" \
            f"should be rendered: {game_obj.should__be_rendered}\n" \
            f"index in scene game objects list: {game_obj.get_index_in_scene_all_game_objects_list()}\n" \
            f"rendering layer index: {game_obj.get_this_game_object_rendering_layer_index_in_scene_rendering_layers_list()}\n" \
            f"\ncomponents:\n[{components_names}]\n\n"
        # render description
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth,
                             game_object_stats_text,
                             (object_screen_pos[0] - game_obj.image_rect.width // 2,
                              object_screen_pos[1] + game_obj.image_rect.height // 2 + description_spacing_y),
                             font, color=pygame.Color(color))

    @staticmethod
    def _render_gizmos_of_game_obj_colliders(game_obj, color: str, font: pygame.font.Font, font_size: int) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only

        # COLLIDERS GIZMOS
        for component in game_obj.components_list:
            if isinstance(component, Collider):
                # render
                # the position of the collider is at world position,
                # so I have to treat its position for correct representation on screen
                representative_collider_rect = component.collider_rect.copy()
                representative_collider_rect.centerx = object_screen_pos.x + component.offset_from_game_object_x
                representative_collider_rect.centery = object_screen_pos.y + component.offset_from_game_object_y
                pygame.draw.rect(ScalableGameScreen.GameScreenDummySurface, color,
                                 representative_collider_rect, 1)
                # description
                collider_text = f"{component.game_object_owner_read_only.name}'s collider\n" \
                                f"offside.x: {component.offset_from_game_object_x} | offside.y: {component.offset_from_game_object_y}\n" \
                                f"width: {component.width}  |  height: {component.height}\n" \
                                f"world center position {component.collider_rect.center}"
                # render description
                TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth,
                                     collider_text,
                                     (representative_collider_rect.centerx - representative_collider_rect.width // 2,
                                      representative_collider_rect.centery - representative_collider_rect.height // 2 - font_size * 4 - 20),
                                     font, color=pygame.Color(color))
                pygame.draw.circle(ScalableGameScreen.GameScreenDummySurface, color,
                                   representative_collider_rect.center, 5)
