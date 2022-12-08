import pygame

from JNetoProductions_pygame_game_engine.components.key_tracker.key_tracker import KeyTracker
from JNetoProductions_pygame_game_engine.components.single_sprite.single_sprite import SingleSprite
from JNetoProductions_pygame_game_engine.components.text_render.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.components.timer.timer import Timer
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from our_game.game_objects.player import Resource


class MiddleBlock(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        #self.stop_rendering_this_game_object()

        self.single_sprite = SingleSprite("our_game/game_res/graphics/ui/buying_phase.png", self)
        self.single_sprite.scale_itself(4)
        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth,
                                                      ScalableGameScreen.HalfDummyScreenHeight))


class RepresentationOfTheCurrentItemAtBuyingPhase(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        #self.stop_rendering_this_game_object()
        self.single_sprite = SingleSprite("our_game/game_res/graphics/crafting_resources/bronze.png", self)
        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth-5, 280))
        self.single_sprite.scale_itself(8)


class BuyingPhaseTextHolder(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        #self.stop_rendering_this_game_object()

        self.image = pygame.Surface((0,0))
        self.fix_game_object_on_screen(self.transform.world_position)

        # money and amount texts
        self.text_render_of_purchase_price = TextRenderComponent("$0000000", 30, pygame.Color(0, 0, 0), -5, 165, self)
        self.text_render_of_purchase_amount = TextRenderComponent("00000000", 30, pygame.Color(0, 0, 0), -5, 40, self)

        # labels
        self.text_render_purchase_status = TextRenderComponent("Default", 30, pygame.Color(0, 0, 0), -5, -100, self)

        # + an - buttons
        self.pressing_time_in_ms = 500
        self.unpressed_button_color = pygame.Color(177, 78, 5)
        self.pressed_button_color = pygame.Color(91, 43, 42)
        self.text_render_of_option_minus = TextRenderComponent("-", 40, self.unpressed_button_color, -113, 37, self)
        self.text_render_of_option_plus = TextRenderComponent("+", 40, self.unpressed_button_color, 107, 37, self)

    def press_plus_button(self):
        self.text_render_of_option_plus.change_color(self.pressed_button_color)
        pressing_time = Timer(self.pressing_time_in_ms, self, self.change_plus_button_color)
        pressing_time.activate()

    def press_minus_button(self):
        self.text_render_of_option_minus.change_color(self.pressed_button_color)
        pressing_time = Timer(self.pressing_time_in_ms, self, self.change_minus_button_color)
        pressing_time.activate()

    def change_plus_button_color(self):
        self.text_render_of_option_plus.change_color(self.unpressed_button_color)

    def change_minus_button_color(self):
        self.text_render_of_option_minus.change_color(self.unpressed_button_color)


class BuyingPhase(GameObject):

    def __init__(self, name: str, player, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        #self.stop_rendering_this_game_object()

        self.image = pygame.Surface((0, 0))
        self.text_render = TextRenderComponent("BUYING PHASE", 60, pygame.Color(255, 255, 255), 0, 0, self)

        self.fixed_position_on_screen = pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth, 50)
        self.fix_game_object_on_screen(self.fixed_position_on_screen)

        self.key_tracker_arrow_left = KeyTracker(pygame.K_LEFT, self)
        self.key_tracker_arrow_right = KeyTracker(pygame.K_RIGHT, self)
        self.key_tracker_arrow_up = KeyTracker(pygame.K_UP, self)
        self.key_tracker_arrow_down = KeyTracker(pygame.K_DOWN, self)
        self.key_tracker_enter = KeyTracker(pygame.K_RETURN, self)
        self.key_tracker_k = KeyTracker(pygame.K_k, self)

        self.current_item_index = 0
        self.purchase_amount = 1

        self.max_allowed_amount_for_purchase = 100

        self.player = player
        self.is_running = False

        self.middle_block = MiddleBlock("buying_phase_middle_block", self.scene, self.rendering_layer)
        self.representation_of_the_current_item_at_buying_phase = RepresentationOfTheCurrentItemAtBuyingPhase(
            "representation_of_the_current_item_at_buying_phase", self.scene, self.rendering_layer)
        self.buying_phase_text_holder = BuyingPhaseTextHolder("buying_phase_text_holder", self.scene, self.rendering_layer)

    def run_phase(self):
        self.is_running = True
        self.current_item_index = 0
        self.purchase_amount = 1
        self.start_rendering_this_game_object()
        self.middle_block.start_rendering_this_game_object()
        self.representation_of_the_current_item_at_buying_phase.start_rendering_this_game_object()
        self.buying_phase_text_holder.start_rendering_this_game_object()

    def stop_phase(self):
        self.is_running = False
        self.stop_rendering_this_game_object()
        self.middle_block.stop_rendering_this_game_object()
        self.representation_of_the_current_item_at_buying_phase.stop_rendering_this_game_object()
        self.buying_phase_text_holder.stop_rendering_this_game_object()

    def game_object_update(self) -> None:
        if self.is_running:

            current_item: Resource = self.player.res_inventory.resources[self.current_item_index]
            purchase_value: float = current_item.price * self.purchase_amount
            has_enough_money = self.player.money >= purchase_value

            # item image
            self.representation_of_the_current_item_at_buying_phase.single_sprite.change_image(current_item.single_sprite.get_img_path())
            self.representation_of_the_current_item_at_buying_phase.single_sprite.scale_itself(8)

            # purchase price
            self.buying_phase_text_holder.text_render_of_purchase_price.change_text(f"${purchase_value}")
            # purchase amount
            self.buying_phase_text_holder.text_render_of_purchase_amount.change_text(f"{self.purchase_amount}")

            print(f"available money: {self.player.money}")
            print(f"has enough money: {has_enough_money}")
            print(f"{current_item.name}")
            print(f"amount: {self.purchase_amount}")
            print(f"price: {purchase_value}\n")

            # switch between resources
            if self.key_tracker_arrow_right.has_key_been_fired_at_this_frame:
                if not self.current_item_index == len(self.player.res_inventory.resources)-1:
                    self.current_item_index += 1
                    self.purchase_amount = 1
            elif self.key_tracker_arrow_left.has_key_been_fired_at_this_frame:
                if not self.current_item_index <= 0:
                    self.current_item_index -= 1
                    self.purchase_amount = 1

            # increase the amount for purchase
            elif self.key_tracker_arrow_up.has_key_been_fired_at_this_frame:
                if not self.purchase_amount >= self.max_allowed_amount_for_purchase:
                    self.buying_phase_text_holder.press_plus_button()
                    self.purchase_amount += 1
            elif self.key_tracker_arrow_down.has_key_been_fired_at_this_frame:
                if not self.purchase_amount <= 1:
                    self.buying_phase_text_holder.press_minus_button()
                    self.purchase_amount -= 1

            # try to make the purchase
            elif self.key_tracker_enter.has_key_been_fired_at_this_frame:
                if has_enough_money:
                    self.player.money -= purchase_value
                    current_item.amount += self.purchase_amount

            # quit the phase
            elif self.key_tracker_k.has_key_been_fired_at_this_frame:
                self.stop_phase()