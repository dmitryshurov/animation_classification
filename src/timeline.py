#  Copyright (c) 2020. Dmitry Shurov

from __future__ import annotations
from typing import Set, List
from animation import Animation
from score_space_element import ScoreSpaceElement


class IncompleteScoreSpaceElementError(Exception):
    pass


class FramesOutOfRangeError(Exception):
    pass


class FramesAlreadyReservedError(Exception):
    pass


class EmptyAnimationError(Exception):
    pass


class Timeline:
    """
    This class serves as a timeline for placing time-aligned animations
    recognized with animation_recognition.

    This is basically a container for ScoreSpaceElement structures.
    """
    def __init__(self, length: int = 0, elements: List[ScoreSpaceElement] = None):
        if length < 0:
            raise ValueError('length must be >= 0')

        self.elements = elements or list()
        self.length = length
        self.free_frames = set(range(self.length))

    def __eq__(self, other: Timeline):
        return self.elements == other.elements

    def __repr__(self):
        return str(self.elements)

    def add_element(self, e: ScoreSpaceElement):
        if e.anim is None or e.window_start_frame is None:
            raise IncompleteScoreSpaceElementError("ScoreSpaceElement has no Animation or window_start_frame assigned")

        if e.anim.num_frames() == 0:
            raise EmptyAnimationError("ScoreSpaceElement Animation has num_frames() == 0")

        self._reserve_frames(e.window_start_frame, e.anim.num_frames())
        self.elements.append(e)

    def can_reserve_frames(self, frames_to_reserve: Set[int]) -> bool:
        return (self.free_frames & frames_to_reserve) == frames_to_reserve

    def _reserve_frames(self, start_frame: int, num_frames: int):
        end_frame = start_frame + num_frames

        if end_frame > self.length:
            raise FramesOutOfRangeError(f'End frame {end_frame} is more than timeline length {self.length}')

        frames_to_reserve = set(range(start_frame, end_frame))

        if not self.can_reserve_frames(frames_to_reserve):
            raise FramesAlreadyReservedError('Some frames are already reserved')

        self.free_frames -= frames_to_reserve

    # def to_animation(self) -> Animation:
    #     """
    #     Flatten the layed out ScoreSpaceElements to a simple animation
    #     """
    #     pass

    def free_frames_set(self) -> Set[int]:
        return self.free_frames

    def full(self):
        return len(self.free_frames) == 0

