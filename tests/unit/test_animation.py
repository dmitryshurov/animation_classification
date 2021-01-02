#  Copyright (c) 2020. Dmitry Shurov

from unittest import TestCase
from animation import Animation, np


# Test Animation class
class TestAnimation(TestCase):

    # Test the Animation class construction
    def test_construct_ndarray_type(self):

        # Construction of Animation with np.ndarray type is OK
        Animation(np.ndarray((10, 5)))
        Animation(np.ndarray((2, 3)))
        Animation(np.ndarray((0, 0)))
        Animation()

        # Other object types must raise TypeError
        with self.assertRaises(TypeError):
            Animation(1)

        with self.assertRaises(TypeError):
            Animation([[]])

        # Matrix dimensions other than 2 must raise ValueError
        with self.assertRaises(ValueError):
            Animation(np.ndarray((2,)))

        with self.assertRaises(ValueError):
            Animation(np.ndarray((2, 3, 4)))

    # Test num_frames() and num_features() method after Animation class construction
    def test_num_frames_num_features(self):
        a0 = Animation(np.ndarray((3, 2)))

        self.assertEqual(a0.num_frames(), 3)
        self.assertEqual(a0.num_features(), 2)

        # Test empty shape
        a1 = Animation(np.ndarray((4, 5)))

        self.assertEqual(a1.num_frames(), 4)
        self.assertEqual(a1.num_features(), 5)

        # Test empty shape
        a2 = Animation(np.ndarray((0, 0)))

        self.assertEqual(a2.num_frames(), 0)
        self.assertEqual(a2.num_features(), 0)

        # Test empty shape with default constructor
        a3 = Animation()

        self.assertEqual(a3.num_frames(), 0)
        self.assertEqual(a3.num_features(), 0)

    # Test matrix() method
    def test_get_matrix(self):
        orig_matrix = np.array(
                       [[1, 3, 4],
                        [1, 2, 3]]
        )
        a = Animation(orig_matrix)

        self.assertTrue(np.array_equal(orig_matrix, a.matrix()))

    # Test __eq__() method
    def test_compare_animations(self):
        a1 = Animation(np.array(
                       [[1, 3, 4],
                        [1, 2, 3]]
                       ))

        a2 = Animation(np.array(
                       [[1, 3, 4],
                        [1, 2, 3]]
                       ))

        a3 = Animation(np.array(
                       [[1, 3.5, 4],
                        [1, 2, 3]]
                       ))

        a4 = Animation(np.array(
                       [[1, 3, 4],
                        [1, 2, 3],
                        [1, 2, 3]]
                       ))

        self.assertEqual(a1, a2)

        self.assertNotEqual(a1, a3)
        self.assertNotEqual(a2, a3)
        self.assertNotEqual(a1, a4)
        self.assertNotEqual(a1, None)
        self.assertNotEqual(a1, [])

    # Test diff() method with different arguments
    def test_diff_animations(self):
        # Input animations
        a1 = Animation(np.array(
                       [[1, 2, 4],
                        [1, 2, 3]]
                       ))
        
        a2 = Animation(np.array(
                       [[1, 3, 2],
                        [0.5, 2, 3]]
                       ))

        a3 = Animation(np.array(
                       [[1, 3, 2],
                        [0.5, 2, 3],
                        [0.5, 2, 3]]
                       ))
        #

        # Test simple subtraction difference (sub)
        diff = np.array(
                       [[0, -1, 2],
                        [0.5, 0, 0]]
                       )

        self.assertTrue(np.array_equal(diff, a1.diff(a2, diff_type="sub")))
        #

        # Test absolute difference (abs)
        diff_abs = np.array(
            [[0, 1, 2],
             [0.5, 0, 0]]
        )
        self.assertTrue(np.array_equal(diff_abs, a1.diff(a2, diff_type="abs")))
        #

        # Test square difference (square)
        diff_square = np.array(
            [[0, 1, 4],
             [0.25, 0, 0]]
        )
        self.assertTrue(np.array_equal(diff_square, a1.diff(a2)))
        self.assertTrue(np.array_equal(diff_square, a1.diff(a2, diff_type="square")))
        #

        # Test that diff() throws exception if diff_type argument is wrong
        with self.assertRaises(ValueError):
            self.assertTrue(np.array_equal(diff, a1.diff(a2, diff_type="wrong_arg")))
        #

        # Test that args of other types raise error
        with self.assertRaises(TypeError):
            a1.diff([])

        with self.assertRaises(TypeError):
            a1.diff(None)

        with self.assertRaises(TypeError):
            a1.diff(a2, diff_type=1)

        # Check that with the different matrix sizes we have ValueError
        with self.assertRaises(ValueError):
            self.assertTrue(np.array_equal(diff, a1.diff(a3)))

    def test_diff_score(self):
        a1 = Animation(np.array(
            [[1, 2, 4],
             [1, 2, 3]]
        ))

        a2 = Animation(np.array(
            [[1, 2, 4],
             [1, 2, 3]]
        ))

        a3 = Animation(np.array(
            [[1, 2, 3],
             [1, 2, 3]]
        ))

        a4 = Animation(np.array(
            [[1.5, 2, 3],
             [1, 2, 3]]
        ))

        self.assertEqual(a1.diff_score(a2, diff_type="square", score_type="sum"), 0)
        self.assertEqual(a1.diff_score(a3, diff_type="square", score_type="sum"), 1)
        self.assertEqual(a2.diff_score(a3, diff_type="square", score_type="sum"), 1)
        self.assertEqual(a3.diff_score(a2, diff_type="square", score_type="sum"), 1)
        self.assertEqual(a3.diff_score(a1, diff_type="square", score_type="sum"), 1)

        self.assertEqual(a1.diff_score(a4, diff_type="square", score_type="sum"), 1.25)
        self.assertEqual(a4.diff_score(a1, diff_type="square", score_type="sum"), 1.25)
        self.assertEqual(a1.diff_score(a4), 1.25)
        self.assertEqual(a4.diff_score(a1), 1.25)

        self.assertEqual(a4.diff_score(a1, diff_type="abs", score_type="sum"), 1.5)
        self.assertEqual(a1.diff_score(a4, diff_type="abs", score_type="sum"), 1.5)

        self.assertEqual(a1.diff_score(a4, diff_type="sub", score_type="sum"), 0.5)
        self.assertEqual(a4.diff_score(a1, diff_type="sub", score_type="sum"), -0.5)
        self.assertEqual(a1.diff_score(a4, diff_type="sub"), 0.5)
        self.assertEqual(a4.diff_score(a1, diff_type="sub"), -0.5)

        # Check the type errors
        with self.assertRaises(TypeError):
            a1.diff_score(1)

        with self.assertRaises(TypeError):
            a1.diff_score(a4, diff_type=1)

        with self.assertRaises(TypeError):
            a1.diff_score(a4, diff_type="sub", score_type=1)

    def test_cut_window(self):
        recorded_animation = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3],
             [1, 2, 2],
             [1, 2, 1],
             [1, 2, 0],
             [1, 2, -1],
             [1, 2, 0],
             [1, 2, 1]]
        ))

        anim1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        anim2 = Animation(np.array(
            [[1, 2, 3],
             [1, 2, 2]]
        ))

        anim3 = Animation(np.array(
            [[1, 2, 0],
             [1, 2, 1]]
        ))

        anim4 = Animation(np.array(
            [[1, 2, 0]]
        ))

        anim5 = Animation(np.array(
            [[1, 2, 1],
             [1, 2, 0],
             [1, 2, -1]]
        ))

        self.assertEqual(recorded_animation.cut_window(0, 2), anim1)
        self.assertEqual(recorded_animation.cut_window(1, 2), anim2)
        self.assertEqual(recorded_animation.cut_window(6, 2), anim3)
        self.assertEqual(recorded_animation.cut_window(6, 1), anim4)
        self.assertEqual(recorded_animation.cut_window(3, 3), anim5)

        with self.assertRaises(ValueError):
            recorded_animation.cut_window(7, 0)

        with self.assertRaises(ValueError):
            recorded_animation.cut_window(7, 2)

        with self.assertRaises(ValueError):
            recorded_animation.cut_window(-1, 2)
