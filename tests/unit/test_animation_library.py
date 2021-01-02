#  Copyright (c) 2020. Dmitry Shurov

from unittest import TestCase
from animation import Animation, np
from animation_library import AnimationLibrary


class TestAnimationLibrary(TestCase):

    def test_constructor(self):
        # Test empty library
        a = AnimationLibrary()
        self.assertEqual(a.size(), 0)

        a = AnimationLibrary([])
        self.assertEqual(a.size(), 0)

        # Test with a single argument
        a = AnimationLibrary([Animation()])
        self.assertEqual(a.size(), 1)

        # Test with multiple arguments
        a = AnimationLibrary([Animation(), Animation()])
        self.assertEqual(a.size(), 2)
        self.assertEqual(a.animations()[0], a.animations()[1])

        # Test for value errors
        with self.assertRaises(ValueError):
            AnimationLibrary("wrong_type")

        with self.assertRaises(ValueError):
            AnimationLibrary(["wrong_type"])

        with self.assertRaises(ValueError):
            AnimationLibrary([Animation(), "wrong_type"])

        library_animation1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        library_animation2 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 3]]
        ))

        library_animation3 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 2.5]]
        ))

        AnimationLibrary([library_animation1, library_animation2, library_animation3])

    def test_iter(self):
        library_animation1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        library_animation2 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 3]]
        ))

        library_animation3 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 2.5]]
        ))

        anim_library = AnimationLibrary([library_animation1])

        for anim in anim_library:
            self.assertEqual(anim, library_animation1)

        anim_library = AnimationLibrary([library_animation1, library_animation2, library_animation3])

        i = 0
        for anim in anim_library:
            if i == 0:
                self.assertEqual(anim, library_animation1)
            elif i == 1:
                self.assertEqual(anim, library_animation2)
            elif i == 2:
                self.assertEqual(anim, library_animation3)
            i += 1

    def test_getitem(self):
        library_animation1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        library_animation2 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 3]]
        ))

        library_animation3 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 2.5]]
        ))

        anim_library = AnimationLibrary([library_animation1, library_animation2, library_animation3])

        self.assertEqual(anim_library[0], library_animation1)
        self.assertEqual(anim_library[1], library_animation2)
        self.assertEqual(anim_library[2], library_animation3)

    def test_add_animation(self):
        anim1 = Animation(np.array(
            [[1, 3, 4],
             [1, 2, 3]]
        ))

        anim2 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 3]]
        ))

        anim3 = Animation(np.array(
            [[2, 3, 4],
             [1, 2, 2.5]]
        ))

        anim_library = AnimationLibrary()

        anim_library.append(anim1)
        self.assertEqual(1, anim_library.size())
        self.assertEqual(anim1, anim_library[0])

        anim_library.append(anim2)
        self.assertEqual(2, anim_library.size())
        self.assertEqual(anim2, anim_library[1])
