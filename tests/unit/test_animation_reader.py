#  Copyright (c) 2020. Dmitry Shurov

from unittest import TestCase

from animation import Animation, np
from animation_reader import AnimationReader, LineLengthDoesNotMatchError, EmptyInputError, ParsingLineFailedError


class TestAnimationReader(TestCase):
    def test_read_single_line(self):
        line = ""
        self.assertEqual([], AnimationReader.read_single_line(line))

        line = "1.2 0.5 0"
        self.assertEqual([1.2, 0.5, 0], AnimationReader.read_single_line(line))

        with self.assertRaises(ParsingLineFailedError):
            line = "a 1"
            AnimationReader.read_single_line(line)

    def test_read_multiline(self):
        """
        Test reading animation from string
        """

        string1 = """
        1.2 0.5 0
        7 4 6
        """

        string2 = """
        # rx ry rz
        1.2 0.5 0
        7 4 6
        """

        expected = [[1.2, 0.5, 0],
                    [7, 4, 6]]

        self.assertEqual(expected, AnimationReader.read_multiple_lines(string1))
        self.assertEqual(expected, AnimationReader.read_multiple_lines(string2))

        string3 = """
        1.2 0.5 0
        7 4
        """

        expected = [[1.2, 0.5, 0],
                    [7, 4]]

        self.assertEqual(expected, AnimationReader.read_multiple_lines(string3))

    def test_read_from_string(self):
        """
        Test reading animation from string
        """

        string = """
        # rx ry rz
        1.2 0.5 0
        7 4 6
        """

        expected = Animation(np.array(
            [[1.2, 0.5, 0],
             [7, 4, 6]]
        ))

        result = AnimationReader.read_from_string(string)
        self.assertEqual(expected, result)

        string = """
        1.2 0.5 0
        7 4
        """

        with self.assertRaises(LineLengthDoesNotMatchError):
            AnimationReader.read_from_string(string)

        # Empty string should throw EmptyInputError
        string = """  """

        with self.assertRaises(EmptyInputError):
            AnimationReader.read_from_string(string)

        # String with only header should also throw EmptyInputError
        string = """
        # a b c
        """

        with self.assertRaises(EmptyInputError):
            AnimationReader.read_from_string(string)

        string = """
        1.2 0.5 0
        7 4 A
        """

        with self.assertRaises(ParsingLineFailedError):
            AnimationReader.read_from_string(string)

    def test_read_from_file(self):
        """
        Test reading animation from file
        """

        import os

        expected = Animation(np.array(
            [[1.2, 0.5, 0],
             [7, 4, 6]]
        ))

        this_folder = os.path.dirname(__file__)

        result = AnimationReader.read_from_chan_file(this_folder + "/data/test_data1.chan")
        self.assertEqual(expected, result)

        with self.assertRaises(EmptyInputError):
            AnimationReader.read_from_chan_file(this_folder + "/data/test_data_empty.chan")

        # Read a more complex chan file exported from Maya using Chan Exporter
        anim = AnimationReader.read_from_chan_file(this_folder + '/data/VideoPose3D_output_demo.chan')
        self.assertEqual(1391, anim.num_frames())
        self.assertEqual(39, anim.num_features())
