#  Copyright (c) 2020. Dmitry Shurov

from unittest import TestCase

from animation import Animation, np
from animation_library import AnimationLibrary
from animation_recognition_processor import AnimationRecognitionProcessor
from animation_recognition_processor_input_data import AnimationRecognitionProcessorInputData
from score_space_element import ScoreSpaceElement
from timeline import Timeline


class TestAnimationRecognitionProcessor(TestCase):
    def setUp(self) -> None:
        # Prepare data for processing
        self.anim = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3],
             [1, 2, 2],
             [1, 2, 1],
             [1, 2, 1]]
        ))

        self.lib_anim1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        self.lib_anim2 = Animation(np.array(
            [[1, 2, 4],
             [1, 2, 3]]
        ))

        self.lib_anim3 = Animation(np.array(
            [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]]
        ))

        self.lib = AnimationLibrary([self.lib_anim1, self.lib_anim2, self.lib_anim3])

        # Pack the data into the AnimationRecognitionProcessorInputData structure
        self.data = AnimationRecognitionProcessorInputData(self.anim, self.lib)

    def test_process_and_get_scores(self):
        # Process data and get scores
        p = AnimationRecognitionProcessor()
        p.process(self.data)

        scores = p.get_best_scores(num_scores=10)
        desired_scores = [[ScoreSpaceElement(0, 0, self.lib_anim1), ScoreSpaceElement(3, 1, self.lib_anim1), ScoreSpaceElement(5, 2,  self.lib_anim1), ScoreSpaceElement(6, 3, self.lib_anim1)],
                          [ScoreSpaceElement(1, 0, self.lib_anim2), ScoreSpaceElement(2, 1, self.lib_anim2), ScoreSpaceElement(4, 2,  self.lib_anim2), ScoreSpaceElement(5, 3, self.lib_anim2)],
                          [ScoreSpaceElement(4, 2, self.lib_anim3), ScoreSpaceElement(6, 1, self.lib_anim3), ScoreSpaceElement(10, 0,self.lib_anim3)]]
        self.assertEqual(desired_scores, scores)

        scores = p.get_best_scores(num_scores=2)
        desired_scores = [[ScoreSpaceElement(0, 0, self.lib_anim1), ScoreSpaceElement(3, 1, self.lib_anim1)],
                          [ScoreSpaceElement(1, 0, self.lib_anim2), ScoreSpaceElement(2, 1, self.lib_anim2)],
                          [ScoreSpaceElement(4, 2, self.lib_anim3), ScoreSpaceElement(6, 1, self.lib_anim3)]]
        self.assertEqual(desired_scores, scores)

        scores = p.get_best_scores(num_scores=0)
        desired_scores = [[],
                          [],
                          []]
        self.assertEqual(desired_scores, scores)

    def test_process_and_get_timeline(self):
        p = AnimationRecognitionProcessor()
        p.process(self.data)
        timeline = p.get_timeline_with_placed_animations()

        desired_timeline = Timeline(length=5,
                                    elements=[
                                        ScoreSpaceElement(0, 0, self.lib_anim1),
                                        ScoreSpaceElement(4, 2, self.lib_anim2)
                                    ]
        )

        self.assertEqual(desired_timeline, timeline)
    #
    # def test_process_and_get_animation(self):
    #     # TODO Do we really need this
    #     p = AnimationRecognitionProcessor()
    #     p.process(self.data)
    #     timeline = p.get_animation()