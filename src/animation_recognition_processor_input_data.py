#  Copyright (c) 2020. Dmitry Shurov

from animation import Animation
from animation_library import AnimationLibrary


class AnimationRecognitionProcessorInputData:
    """
    Data structure containing data for AnimationRecognitionProcessor
    """
    def __init__(self, anim: Animation, lib: AnimationLibrary):
        self.anim = anim  # Animation where the library animations will be recognized
        self.lib = lib    # AnimationLibrary containing animations to recognize
