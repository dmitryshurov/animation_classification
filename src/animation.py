#  Copyright (c) 2020. Dmitry Shurov

from __future__ import annotations
import numpy as np


class Animation:
    def __init__(self, matrix: np.ndarray = None, name: str = None):
        """
        Create the animation from a numpy array
        Initialized with (0, 0) shape by default

        Parameters
        ----------
        matrix : np.ndarray
            Feature matrix to create the animation from. 0 axis is time in frames, 1 axis is skeleton features

        Examples
        --------
        Animation(np.ndarray((num_frames, num_features)))
        """

        if matrix is None:
            matrix = np.ndarray(shape=(0, 0))

        if not isinstance(matrix, np.ndarray):
            raise TypeError('Wrong input type for npy_matrix. Must be numpy.ndarray.')

        if len(matrix.shape) != 2:
            raise ValueError('Wrong number of dimensions for matrix. Must be 2-dimensional.')

        self._matrix = matrix
        self.name = name

    def __eq__(self, other: Animation):
        return isinstance(other, Animation) and np.array_equal(self.matrix(), other.matrix())

    def __repr__(self):
        return str(self.matrix())

    def matrix(self) -> np.ndarray:
        """
        Returns the underlying numpy matrix
        """
        return self._matrix

    def num_frames(self) -> int:
        """
        Returns length of the animation in frames
        """
        return self._matrix.shape[0]

    def num_features(self) -> int:
        """
        Returns the length of the feature vector for this animation
        """
        return self._matrix.shape[1]

    def diff(self, other: Animation, diff_type: str = "square") -> np.ndarray:
        """
        Returns the difference matrix between this and other matrix (may be a non-symmetrical operation).

        Parameters
        ----------
        other : Animation
            Animation to calculate difference with.
        diff_type : str
            Type of difference function.
                - "sub" - simple subtraction (non-symmetric)
                - "abs" - absolute of simple subtraction
                - "square" - square difference

        Returns
        -------
        result : np.ndarray
            Resulting difference matrix

        """

        if not isinstance(other, Animation):
            raise TypeError("Argument `other` must be of `Animation` type")

        if not isinstance(diff_type, str):
            raise TypeError("Argument `diff_type` must be of `str` type")

        if self.matrix().shape != other.matrix().shape:
            raise ValueError("Matrices must have equal shapes")

        if diff_type == "sub":
            return np.subtract(self.matrix(), other.matrix())

        elif diff_type == "abs":
            return np.abs(self.diff(other, diff_type="sub"))

        elif diff_type == "square":
            return np.square(self.diff(other, diff_type="sub"))

        else:
            raise ValueError("Wrong `diff_type` value: {0}. Must be on of: [sub, abs, square]".format(diff_type))

    def diff_score(self, other: Animation, diff_type: str = "square", score_type: str = "sum") -> float:
        diff = self.diff(other, diff_type=diff_type)

        if not isinstance(score_type, str):
            raise TypeError("Argument `score_type` must be of `str` type")

        if score_type == "sum":
            return float(np.sum(diff))
        else:
            raise ValueError("Wrong `score_type` value: {0}. Must be on of: [sum]".format(score_type))

    def cut_window(self, window_start_frame: int, window_width: int) -> Animation:
        start = window_start_frame
        end = window_start_frame + window_width

        if start < 0 or end > self.num_frames():
            raise ValueError("Out of bounds")

        if window_width < 1:
            raise ValueError("window_width must be >= 1")

        return Animation(self.matrix()[start:end, :])

    # def retime(self, window_scale: float) -> Animation:
    #     pass
    #
