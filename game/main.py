import pygame
from _1systems.inspector_debugging_canvas_system import InspectorDebuggingCanvas
from _1systems.input_manager_system import InputManager
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _1systems.game_time_system import GameTime
from scene import Scene


class Game:

    def __init__(self):

        pygame.init()

        RES_NHD = [640, 360]
        RES_FWVGA = [854, 480]
        RES_HD = [1280, 720]
        RES_HD_PLUS = [1600, 900]
        RES_FULL_HD = [1920, 1080]
        RES_2K_QHD = [2560, 1440]
        ScalableGameScreen.init_screens(RES_FULL_HD, [2000, 1300], RES_FULL_HD)

        # important stuff
        self.clock = pygame.time.Clock()
        self.scene_example = Scene(self)
        self.delta_time = 0

        # it is not used for much, just holds the total amount of update elapsed
        self.elapsed_updates = 0

        # should be the one of the last things to be instantiated
        self.inspector_debugging_canvas = InspectorDebuggingCanvas(self.scene_example, font_size=10)

    def run_game_loop(self):
        while True:
            self.elapsed_updates += 1
            GameTime.DeltaTime = self.clock.tick() / 1000
            InputManager.update()
            self.scene_example.update()
            self.scene_example.render()
            self.inspector_debugging_canvas.render_inspector_debugging_text()
            ScalableGameScreen.render_final_scaled_result()


game = Game()
game.run_game_loop()
