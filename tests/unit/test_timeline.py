#  Copyright (c) 2020. Dmitry Shurov

from unittest import TestCase

from animation import Animation, np
from timeline import Timeline, IncompleteScoreSpaceElementError, FramesAlreadyReservedError, FramesOutOfRangeError, EmptyAnimationError
from score_space_element import ScoreSpaceElement


class TestTimeline(TestCase):
    def test_construct(self):
        with self.assertRaises(ValueError):
            Timeline(length=-1)

        t = Timeline()
        self.assertListEqual([], t.elements)
        self.assertEqual(t.length, 0)

        t = Timeline(length=5)
        self.assertListEqual([], t.elements)
        self.assertEqual(t.length, 5)

        t = Timeline(elements=[])
        self.assertListEqual([], t.elements)
        self.assertEqual(t.length, 0)

        els = [ScoreSpaceElement(0), ScoreSpaceElement(1)]
        t = Timeline(elements=els)
        self.assertListEqual(els, t.elements)

    def test_eq(self):
        t1 = Timeline(elements=[ScoreSpaceElement(0), ScoreSpaceElement(1)])
        t2 = Timeline(elements=[ScoreSpaceElement(0)])
        t3 = Timeline()
        t4 = Timeline(elements=[ScoreSpaceElement(0), ScoreSpaceElement(1)])
        t5 = Timeline(elements=[ScoreSpaceElement(1), ScoreSpaceElement(1)])

        self.assertEqual(t1, t4)
        self.assertNotEqual(t1, t2)
        self.assertNotEqual(t1, t3)
        self.assertNotEqual(t2, t3)
        self.assertNotEqual(t4, t5)

    def test_free_frames_set(self):
        t = Timeline()
        self.assertEqual(set(), t.free_frames_set())

        t = Timeline(length=5)
        self.assertEqual(set(range(5)), t.free_frames_set())

        anim1 = Animation(np.ndarray((2, 1)))  # Anim with 2 frames
        se1 = ScoreSpaceElement(0, anim=anim1, window_start_frame=0)

        t.add_element(se1)  # Must reserve frames 0 and 1
        self.assertEqual(set(range(2, 5)), t.free_frames_set())

    def test_reserve_frames(self):
        t = Timeline(length=7)
        self.assertEqual({0, 1, 2, 3, 4, 5, 6}, t.free_frames_set())
        self.assertEqual(False, t.full())

        t._reserve_frames(1, 2)
        self.assertEqual({0, 3, 4, 5, 6}, t.free_frames_set())

        with self.assertRaises(FramesAlreadyReservedError):
            t._reserve_frames(0, 2)

        t._reserve_frames(3, 3)
        self.assertEqual({0, 6}, t.free_frames_set())

        with self.assertRaises(FramesAlreadyReservedError):
            t._reserve_frames(3, 3)

        t._reserve_frames(0, 0)
        self.assertEqual({0, 6}, t.free_frames_set())

        t._reserve_frames(0, 1)
        self.assertEqual({6}, t.free_frames_set())
        self.assertEqual(False, t.full())

        t._reserve_frames(6, 1)
        self.assertEqual(set(), t.free_frames_set())
        self.assertEqual(True, t.full())

    def test_add_element(self):
        # ========== PART 1 ========== #

        t = Timeline(length=3)

        # Check for various forms of incomplete instances of ScoreSpaceElement
        with self.assertRaises(IncompleteScoreSpaceElementError):
            t.add_element(ScoreSpaceElement(0))

        with self.assertRaises(IncompleteScoreSpaceElementError):
            t.add_element(ScoreSpaceElement(0, anim=Animation(np.ndarray((2, 1)))))

        with self.assertRaises(IncompleteScoreSpaceElementError):
            t.add_element(ScoreSpaceElement(0, window_start_frame=1))

        # ========== PART 2 ========== #

        t = Timeline(length=3)

        # Create 2 valid instances of ScoreSpaceElement
        el1 = ScoreSpaceElement(0, anim=Animation(), window_start_frame=0)
        el2 = ScoreSpaceElement(1, anim=Animation(np.ndarray((2, 1))), window_start_frame=1)

        # Animation with 0 frames raises error
        with self.assertRaises(EmptyAnimationError):
            t.add_element(el1)

        # Nothing added, just check it
        self.assertEqual([], t.elements)
        self.assertEqual({0, 1, 2}, t.free_frames_set())

        # Animation with 2 frames starting at frame 1
        t.add_element(el2)
        self.assertEqual([el2], t.elements)
        self.assertEqual({0}, t.free_frames_set())
        self.assertEqual(False, t.full())

        # ========== PART 3 ========== #
        t = Timeline(length=1)

        # Adding an animation that exceeds the timeline length raises error
        with self.assertRaises(FramesOutOfRangeError):
            t.add_element(ScoreSpaceElement(0, window_start_frame=0, anim=Animation(np.ndarray((2, 1)))))

        # ========== PART 4 ========== #
        t = Timeline(length=5)

        # Add a valid ScoreSpaceElement with 2 frames starting at frame 1
        t.add_element(ScoreSpaceElement(1, anim=Animation(np.ndarray((2, 1))), window_start_frame=1))
        self.assertEqual({0, 3, 4}, t.free_frames_set())

        # Check for various forms of adding ScoreSpaceElement to the reserved timeline frames
        with self.assertRaises(FramesAlreadyReservedError):
            t.add_element(ScoreSpaceElement(1, anim=Animation(np.ndarray((2, 1))), window_start_frame=2))

        with self.assertRaises(FramesAlreadyReservedError):
            t.add_element(ScoreSpaceElement(1, anim=Animation(np.ndarray((2, 1))), window_start_frame=0))

        # Check for various forms of incomplete instances of ScoreSpaceElement. Again.
        with self.assertRaises(FramesOutOfRangeError):
            t.add_element(ScoreSpaceElement(1, anim=Animation(np.ndarray((5, 1))), window_start_frame=2))

