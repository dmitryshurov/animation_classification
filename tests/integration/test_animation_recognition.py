#  Copyright (c) 2020. Dmitry Shurov

from unittest import TestCase
from animation import Animation, np
from animation_library import AnimationLibrary
from animation_recognition import AnimationRecognition
from score_space_element import ScoreSpaceElement


class TestAnimationRecognition(TestCase):

    def test_equal_length_single_animation_comparison(self):
        rec_anim = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        lib_anim1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        lib_anim2 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 3]]
        ))

        lib_anim3 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 2.5]]
        ))

        lib_anim4 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 2.5],
             [1, 2, 2.5]]
        ))

        ar = AnimationRecognition()

        score = ar.compare_equal_length_single_animations(rec_anim, lib_anim1)
        self.assertEqual(score, ScoreSpaceElement(0, anim=lib_anim1))

        score = ar.compare_equal_length_single_animations(rec_anim, lib_anim2)
        self.assertEqual(score, ScoreSpaceElement(1, anim=lib_anim2))

        score = ar.compare_equal_length_single_animations(lib_anim2, rec_anim)
        self.assertEqual(score, ScoreSpaceElement(1, anim=rec_anim))

        score = ar.compare_equal_length_single_animations(rec_anim, lib_anim3)
        self.assertEqual(score, ScoreSpaceElement(1.5, anim=lib_anim3))

        score = ar.compare_equal_length_single_animations(lib_anim3, rec_anim)
        self.assertEqual(score, ScoreSpaceElement(1.5, anim=rec_anim))

        # Check that assertion is raised if animation sizes are not equal
        with self.assertRaises(ValueError):
            ar.compare_equal_length_single_animations(rec_anim, lib_anim4)

    def test_equal_length_animation_library_comparison(self):
        rec_anim = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        lib_anim1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        lib_anim2 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 3]]
        ))

        lib_anim3 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 2.5]]
        ))

        lib_anim4 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 2.5],
             [1, 2, 2.5]]
        ))

        lib_anim5 = Animation(np.array(
            [[2, 3],
             [1, 2]]
        ))

        ar = AnimationRecognition()

        anim_lib = AnimationLibrary()
        scores = ar.compare_equal_length_library_animations(rec_anim, anim_lib)
        self.assertListEqual(scores, [])

        anim_lib = AnimationLibrary([lib_anim3])
        scores = ar.compare_equal_length_library_animations(rec_anim, anim_lib)
        self.assertListEqual(scores, [ScoreSpaceElement(1.5, anim=lib_anim3)])

        anim_lib = AnimationLibrary([lib_anim1, lib_anim2, lib_anim3])
        scores = ar.compare_equal_length_library_animations(rec_anim, anim_lib)
        self.assertListEqual(scores, [ScoreSpaceElement(0, anim=lib_anim1), ScoreSpaceElement(1, anim=lib_anim2), ScoreSpaceElement(1.5, anim=lib_anim3)])

        # Test with List[Animation]
        scores = ar.compare_equal_length_library_animations(rec_anim, [])
        self.assertListEqual(scores, [])

        scores = ar.compare_equal_length_library_animations(rec_anim, [lib_anim3])
        self.assertListEqual(scores, [ScoreSpaceElement(1.5, anim=lib_anim3)])

        scores = ar.compare_equal_length_library_animations(rec_anim, [lib_anim1, lib_anim2, lib_anim3])
        self.assertListEqual(scores, [ScoreSpaceElement(0, anim=lib_anim1), ScoreSpaceElement(1, anim=lib_anim2), ScoreSpaceElement(1.5, anim=lib_anim3)])

        # The animation with different size
        with self.assertRaises(ValueError):
            ar.compare_equal_length_library_animations(rec_anim, [lib_anim4])

        # The animation with different num_features
        with self.assertRaises(ValueError):
            ar.compare_equal_length_library_animations(rec_anim, [lib_anim5])

    def test_single_animation_moving_window_no_scale(self):
        """
        Take a single recorded animation and single library animation.
        Slide the library animation through the recorded animation.
        Return the resulting scores.
        """
        rec_anim = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3],
             [1, 2, 2],
             [1, 2, 1],
             [1, 2, 1]]
        ))

        lib_anim = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        wrong_length_lib_anim = Animation(np.array(
            [[2, 3],
             [1, 2]]
        ))

        ar = AnimationRecognition()

        desired_scores = [ScoreSpaceElement(0, 0,lib_anim), ScoreSpaceElement(3, 1, lib_anim), ScoreSpaceElement(5, 2, lib_anim), ScoreSpaceElement(6, 3, lib_anim)]
        calculated_scores = ar.get_single_anim_moving_window_scores(rec_anim, lib_anim)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [ScoreSpaceElement(0, 0,lib_anim), ScoreSpaceElement(3, 1, lib_anim), ScoreSpaceElement(5, 2, lib_anim), ScoreSpaceElement(6, 3, lib_anim)]
        calculated_scores = ar.get_single_anim_moving_window_scores(rec_anim, lib_anim, window_step=1)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [ScoreSpaceElement(0, 0, lib_anim), ScoreSpaceElement(5, 2, lib_anim)]
        calculated_scores = ar.get_single_anim_moving_window_scores(rec_anim, lib_anim, window_step=2)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [ScoreSpaceElement(0, 0, lib_anim)]
        calculated_scores = ar.get_single_anim_moving_window_scores(rec_anim, lib_anim, window_step=5)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [ScoreSpaceElement(0, 0, rec_anim)]
        calculated_scores = ar.get_single_anim_moving_window_scores(rec_anim, rec_anim, window_step=5)
        self.assertEqual(desired_scores, calculated_scores)

        # The length of rec_anim is less than anim - raise ValueError
        with self.assertRaises(ValueError):
            ar.get_single_anim_moving_window_scores(rec_anim=lib_anim, anim=rec_anim)

        # The animations with different num_features - raise ValueError
        with self.assertRaises(ValueError):
            ar.compare_equal_length_library_animations(rec_anim, [wrong_length_lib_anim])

    def test_single_library_animation_moving_window_no_scale(self):
        """
        Take a single recorded animation and a single library animation.
        Slide the library animation through the recorded animation.
        Return the resulting scores.
        """
        rec_anim = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3],
             [1, 2, 2],
             [1, 2, 1],
             [1, 2, 1]]
        ))

        lib_anim1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        anim_lib = AnimationLibrary([lib_anim1])

        ar = AnimationRecognition()

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1), ScoreSpaceElement(3, 1, lib_anim1), ScoreSpaceElement(5, 2, lib_anim1), ScoreSpaceElement(6, 3, lib_anim1)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1), ScoreSpaceElement(3, 1, lib_anim1), ScoreSpaceElement(5, 2, lib_anim1), ScoreSpaceElement(6, 3, lib_anim1)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib, window_step=1)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1), ScoreSpaceElement(5, 2, lib_anim1)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib, window_step=2)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib, window_step=5)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib, window_step=5)
        self.assertEqual(desired_scores, calculated_scores)

        # TODO Test for errors

    def test_multiple_library_animations_moving_window_no_scale(self):
        """
        Take a single recorded animation and several library animations.
        Slide the library animations through the recorded animation.
        Return the resulting scores.
        """
        rec_anim = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3],
             [1, 2, 2],
             [1, 2, 1],
             [1, 2, 1]]
        ))

        lib_anim1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        lib_anim2 = Animation(np.array(
            [[1, 2, 4],
             [1, 2, 3]]
        ))

        lib_anim3 = Animation(np.array(
            [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]]
        ))

        anim_lib = AnimationLibrary([lib_anim1, lib_anim2, lib_anim3])

        ar = AnimationRecognition()

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1), ScoreSpaceElement(3, 1, lib_anim1), ScoreSpaceElement(5, 2, lib_anim1), ScoreSpaceElement(6, 3, lib_anim1)],
                          [ScoreSpaceElement(1, 0, lib_anim2), ScoreSpaceElement(2, 1, lib_anim2), ScoreSpaceElement(4, 2, lib_anim2), ScoreSpaceElement(5, 3, lib_anim2)],
                          [ScoreSpaceElement(10, 0, lib_anim3), ScoreSpaceElement(6, 1, lib_anim3), ScoreSpaceElement(4, 2, lib_anim3)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1), ScoreSpaceElement(3, 1, lib_anim1), ScoreSpaceElement(5, 2, lib_anim1), ScoreSpaceElement(6, 3, lib_anim1)],
                          [ScoreSpaceElement(1, 0, lib_anim2), ScoreSpaceElement(2, 1, lib_anim2), ScoreSpaceElement(4, 2, lib_anim2), ScoreSpaceElement(5, 3, lib_anim2)],
                          [ScoreSpaceElement(10, 0, lib_anim3), ScoreSpaceElement(6, 1, lib_anim3), ScoreSpaceElement(4, 2, lib_anim3)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib, window_step=1)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1), ScoreSpaceElement(5, 2, lib_anim1)],
                          [ScoreSpaceElement(1, 0, lib_anim2), ScoreSpaceElement(4, 2, lib_anim2)],
                          [ScoreSpaceElement(10, 0, lib_anim3), ScoreSpaceElement(4, 2, lib_anim3)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib, window_step=2)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1)],
                          [ScoreSpaceElement(1, 0, lib_anim2)],
                          [ScoreSpaceElement(10, 0, lib_anim3)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib, window_step=5)
        self.assertEqual(desired_scores, calculated_scores)

        desired_scores = [[ScoreSpaceElement(0, 0, lib_anim1)],
                          [ScoreSpaceElement(1, 0, lib_anim2)],
                          [ScoreSpaceElement(10, 0, lib_anim3)]]
        calculated_scores = ar.get_anim_library_moving_window_scores(rec_anim, anim_lib, window_step=5)
        self.assertEqual(desired_scores, calculated_scores)

        # lib_anim4 has wrong num features - raise ValueError
        lib_anim4 = Animation(np.array(
            [[1, 1],
             [1, 1],
             [1, 1]]
        ))

        anim_lib = AnimationLibrary([lib_anim1, lib_anim2, lib_anim3, lib_anim4])
        with self.assertRaises(ValueError):
            ar.get_anim_library_moving_window_scores(rec_anim, anim_lib)

        # lib_anim5 is longer than rec_anim - raise ValueError
        lib_anim5 = Animation(np.array(
            [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1],
             [1, 1, 1],
             [1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]]
        ))

        anim_lib = AnimationLibrary([lib_anim1, lib_anim2, lib_anim3, lib_anim5])
        with self.assertRaises(ValueError):
            ar.get_anim_library_moving_window_scores(rec_anim, anim_lib)
