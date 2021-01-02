#  Copyright (c) 2020. Dmitry Shurov

from unittest import TestCase

from animation_library_reader import AnimationLibraryReader
from animation_reader import AnimationReader

import os


class TestAnimationLibraryReader(TestCase):
    def test_read(self):
        lib_folder = os.path.dirname(__file__) + '/data/anim_lib'

        lib = AnimationLibraryReader.read_chan_folder(lib_folder)

        anim1 = AnimationReader.read_from_chan_file(lib_folder + '/1.chan')
        anim2 = AnimationReader.read_from_chan_file(lib_folder + '/2.chan')

        self.assertEqual(anim1, lib[0])
        self.assertEqual(anim2, lib[1])
