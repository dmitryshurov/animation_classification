#  Copyright (c) 2020. Dmitry Shurov

from typing import List

from animation_recognition import AnimationRecognition
from score_space_analyzer import ScoreSpaceAnalyzer
from animation_recognition_processor_input_data import AnimationRecognitionProcessorInputData
from score_space_element import ScoreSpaceElement
from timeline import Timeline
from timeline_placer import TimelinePlacer


class AnimationRecognitionProcessor:
    """
    Process the input animation data and return the recognized animations with scores

    Get the input data got from chans or any other source (recorded animation, animation library etc.)
    Run the selected comparison algorithm on the input data (e.g. simple moving window algorithm)
    Return the output data (best matches with scores etc.)
    """
    def __init__(self):
        self.ar = AnimationRecognition()
        self.scores = None
        self.data = None

    def process(self, data: AnimationRecognitionProcessorInputData):
        self.data = data
        self.scores = self.ar.get_anim_library_moving_window_scores(data.anim, data.lib, window_step=1)

    def get_best_scores(self, num_scores) -> List[List[ScoreSpaceElement]]:
        return ScoreSpaceAnalyzer.get_best_scores(self.scores, num_scores)

    def get_timeline_with_placed_animations(self):
        timeline = Timeline(length=self.data.anim.num_frames())
        TimelinePlacer.layout_score_space_on_timeline(self.scores, timeline)

        return timeline
