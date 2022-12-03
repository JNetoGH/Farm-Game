from _1systems.time.time import Time
from _2components.animation.animation_clip import AnimationClip
from _2components.component_base_class.component import Component
from _3gameobjs.game_obj import GameObject


# sets the current animation in a animation list and the current frame of the animation according to a speed
class AnimationController(Component):

    def __init__(self, animation_clips, game_object_owner: GameObject):
        super().__init__(game_object_owner)
        self.game_object_owner = game_object_owner

        self.animation_clips_list = animation_clips
        self.current_animation_clip: AnimationClip = self.animation_clips_list[0]
        self.current_animation_clip_name = self.current_animation_clip.name

        self.current_frame_index = 0  # the current img of the animation clip
        self.animation_speed = 4
        self.stop_animation_clip = False

    def add_animation(self, *animations: AnimationClip) -> None:
        for animation in animations:
            self.animation_clips_list.append(animation)

    def remove_animation(self, *animations: AnimationClip) -> None:
        for animation in animations:
            self.animation_clips_list.remove(animation)

    def set_current_animation(self, animation_clip_name) -> None:
        for animation_clip in self.animation_clips_list:
            if animation_clip.name == animation_clip_name and self.current_animation_clip != animation_clip:
                self.current_animation_clip = animation_clip
                self.current_animation_clip_name = animation_clip_name


    def stop_animation(self, true_false):
        self.stop_animation_clip = true_false

    def animate(self) -> None:
        if not self.stop_animation_clip and self.animation_clips_list != []:
            # jump from frame to frame
            self.current_frame_index += self.animation_speed * Time.DeltaTime
            # sets back to the first frame if it's bigger than the size of the animation
            if self.current_frame_index >= len(self.current_animation_clip.images):
                self.current_frame_index = 0
            self.game_object_owner.image = self.current_animation_clip.images[int(self.current_frame_index)]

