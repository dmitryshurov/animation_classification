#  Copyright (c) 2020. Dmitry Shurov

from __future__ import annotations

from animation_reader import AnimationReader
from animation_library_reader import AnimationLibraryReader
from animation_recognition_processor_input_data import AnimationRecognitionProcessorInputData


class AnimationRecognitionProcessorInputDataReader:

    @staticmethod
    def load_from_chan_files(chan_path: str, folder_path: str) -> AnimationRecognitionProcessorInputData:
        """
        Load an animation from a chan file and an animation library from a folder containing chan files

        Args:
            chan_path: a single chan path
            folder_path: a path to a folder containing chan files

        Returns:
            AnimationRecognitionProcessorInputData filled with Animation and AnimationLibrary
        """

        anim = AnimationReader.read_from_chan_file(chan_path)
        lib = AnimationLibraryReader.read_chan_folder(folder_path)

        return AnimationRecognitionProcessorInputData(anim, lib)
