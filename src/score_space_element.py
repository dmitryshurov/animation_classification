#  Copyright (c) 2020. Dmitry Shurov

from __future__ import annotations

from animation import Animation


class ScoreSpaceElement:
    def __init__(self,
                 score: float,
                 window_start_frame: int = None,
                 anim: Animation = None,
                 # window_scale: float = None,
                 ):

        self.score = score
        self.anim = anim
        # self.window_scale = window_scale
        self.window_start_frame = window_start_frame

    def __eq__(self, other: ScoreSpaceElement):
        return self.score == other.score and self.anim == other.anim and self.window_start_frame == other.window_start_frame

    def __lt__(self, other: ScoreSpaceElement):
        return self.score < other.score

    def __repr__(self):
        res = '{:.2f}'.format(self.score)

        if self.window_start_frame is not None:
            res += ' @ {:d}'.format(self.window_start_frame)

        if self.anim is not None:
            res += ' ({:d},{:d})'.format(self.anim.num_frames(), self.anim.num_features())

            if self.anim.name is not None:
                res += ' "{:s}"'.format(self.anim.name)

        # if self.window_scale is not None:
        #     res += ' s {:.2f}'.format(self.window_scale)

        return res
