#  Copyright (c) 2020. Dmitry Shurov

from unittest import TestCase

from score_space_element import ScoreSpaceElement
from score_space_simple_2d import ScoreSpaceSimple2D, NoElementsAvailableError


class TestScoreSpaceSimple2D(TestCase):
    def test_constructor(self):
        scores = [
            [ScoreSpaceElement(0, 0), ScoreSpaceElement(3, 1), ScoreSpaceElement(5, 2), ScoreSpaceElement(6, 3)],
            [ScoreSpaceElement(1, 0), ScoreSpaceElement(2, 1), ScoreSpaceElement(4, 2), ScoreSpaceElement(5, 3)],
            [ScoreSpaceElement(4, 2), ScoreSpaceElement(6, 1), ScoreSpaceElement(10, 0)]
        ]

        score_space = ScoreSpaceSimple2D(scores)
        self.assertListEqual(score_space.elements, scores)

        score_space = ScoreSpaceSimple2D()
        self.assertListEqual(score_space.elements, [])

        score_space = ScoreSpaceSimple2D([])
        self.assertListEqual(score_space.elements, [])

    def test_empty(self):
        scores = [
            [ScoreSpaceElement(0, 0), ScoreSpaceElement(3, 1), ScoreSpaceElement(5, 2), ScoreSpaceElement(6, 3)],
            [ScoreSpaceElement(1, 0), ScoreSpaceElement(2, 1), ScoreSpaceElement(4, 2), ScoreSpaceElement(5, 3)],
            [ScoreSpaceElement(4, 2), ScoreSpaceElement(6, 1), ScoreSpaceElement(10, 0)]
        ]

        self.assertFalse(ScoreSpaceSimple2D(scores).empty())
        self.assertFalse(ScoreSpaceSimple2D([[ScoreSpaceElement(0, 0)], []]).empty())

        self.assertTrue(ScoreSpaceSimple2D().empty())
        self.assertTrue(ScoreSpaceSimple2D([]).empty())
        self.assertTrue(ScoreSpaceSimple2D([[]]).empty())
        self.assertTrue(ScoreSpaceSimple2D([[], []]).empty())

    def test_get_best_score_element(self):
        scores = [
            [ScoreSpaceElement(0, 0), ScoreSpaceElement(3, 1), ScoreSpaceElement(5, 2), ScoreSpaceElement(6, 3)],
            [ScoreSpaceElement(1, 0), ScoreSpaceElement(2, 1), ScoreSpaceElement(4, 2), ScoreSpaceElement(5, 3)],
            [ScoreSpaceElement(4, 2), ScoreSpaceElement(6, 1), ScoreSpaceElement(10, 0)]
        ]

        s = ScoreSpaceSimple2D(scores)
        self.assertEqual(ScoreSpaceElement(0, 0), s.get_best_score_element())
        self.assertEqual(ScoreSpaceElement(0, 0), s.get_best_score_element(remove=True))
        self.assertEqual(ScoreSpaceElement(1, 0), s.get_best_score_element())
        self.assertEqual(ScoreSpaceElement(1, 0), s.get_best_score_element(remove=True))
        self.assertEqual(ScoreSpaceElement(2, 1), s.get_best_score_element(remove=True))
        self.assertEqual(ScoreSpaceElement(3, 1), s.get_best_score_element())

        s = ScoreSpaceSimple2D([[ScoreSpaceElement(0, 0)], []])
        self.assertEqual(ScoreSpaceElement(0, 0), s.get_best_score_element(remove=True))

        with self.assertRaises(NoElementsAvailableError):
            s.get_best_score_element()
