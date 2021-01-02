#  Copyright (c) 2020. Dmitry Shurov

from animation_reader import AnimationReader
from animation_library import AnimationLibrary


class AnimationLibraryReader:
    @staticmethod
    def read_chan_folder(folder):
        import os

        anim_lib = AnimationLibrary()

        for fname in sorted(os.listdir(folder)):
            if not fname.endswith('.chan'):
                continue

            fpath = os.path.join(folder, fname)
            anim_lib.append(AnimationReader.read_from_chan_file(fpath))

        return anim_lib
