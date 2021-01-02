#  Copyright (c) 2020. Dmitry Shurov

from unittest import TestCase

from animation import Animation, np
from score_space_element import ScoreSpaceElement
from timeline import Timeline
from timeline_placer import TimelinePlacer


class TestTimelinePlacer(TestCase):
    def test_place(self):
        a1 = Animation(np.ndarray((2, 1)))

        scores = [
            [ScoreSpaceElement(0, 0, anim=a1), ScoreSpaceElement(3, 1, anim=a1), ScoreSpaceElement(5, 2, anim=a1), ScoreSpaceElement(6, 3, anim=a1)],
            [ScoreSpaceElement(1, 0, anim=a1), ScoreSpaceElement(2, 1, anim=a1), ScoreSpaceElement(4, 2, anim=a1), ScoreSpaceElement(5, 3, anim=a1)],
            [ScoreSpaceElement(4, 2, anim=a1), ScoreSpaceElement(6, 1, anim=a1), ScoreSpaceElement(10, 0, anim=a1)]
        ]

        timeline = Timeline(10)
        TimelinePlacer.layout_score_space_on_timeline(scores, timeline)
        desired_timeline = Timeline(length=10, elements=[ScoreSpaceElement(0, 0, anim=a1), ScoreSpaceElement(4, 2, anim=a1)])

        self.assertEqual(desired_timeline, timeline)
