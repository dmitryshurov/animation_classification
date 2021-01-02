#  Copyright (c) 2020. Dmitry Shurov

from typing import List
import os
from animation import Animation, np


class LineLengthDoesNotMatchError(ValueError):
    pass


class EmptyInputError(ValueError):
    pass


class ParsingLineFailedError(ValueError):
    pass


class AnimationReader:
    @staticmethod
    def read_single_line(line: str) -> List[float]:
        try:
            return [float(x) for x in line.split()]
        except ValueError:
            raise ParsingLineFailedError('Failed to parse line: "{0}"'.format(line))

    @staticmethod
    def read_multiple_lines(string: str) -> List[List[float]]:
        result = list()
        lines = string.splitlines()

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                continue

            tokens = AnimationReader.read_single_line(line)
            if len(tokens) > 0:
                result.append(tokens)

        return result


    @staticmethod
    def read_from_string(string: str) -> Animation:
        if len(string.strip()) == 0:
            raise EmptyInputError("Input chan data is empty")

        parsed_lines = AnimationReader.read_multiple_lines(string)

        str_length = [len(x) for x in parsed_lines]

        if len(str_length) == 0:
            raise EmptyInputError("Input chan data is empty")

        if min(str_length) != max(str_length):
            raise LineLengthDoesNotMatchError("Lines lengths does not match")

        return Animation(np.array(parsed_lines))

    @staticmethod
    def read_from_chan_file(fname: str):
        with open(fname, 'r') as f:
            contents = f.read()

            anim = AnimationReader.read_from_string(contents)
            anim.name = os.path.basename(fname)

            return anim


    @staticmethod
    def parse_videopose3d_frame_data(frame_data: np.ndarray):
        frame_features = frame_data.flatten()

    @staticmethod
    def read_from_videopose3d_npy_file(fname: str):
        data = np.load(fname)
        num_frames = data.shape[0]

        for frame in range(num_frames):
            AnimationReader.parse_videopose3d_frame_data(data[frame])
