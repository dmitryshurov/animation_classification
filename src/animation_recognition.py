#  Copyright (c) 2020. Dmitry Shurov

from typing import List, Union

from animation import Animation
from animation_library import AnimationLibrary
from retime_parms import RetimeParms
from score_space_element import ScoreSpaceElement


class AnimationRecognition:
    """
    The responsibility of this class is to run recognition scoring algorithm over the animations
    and return the score space (which, in case it's linear, is just an array of scores),
    which is then processed with the ScoreSpaceAnalyzer to retrieve animation candidates.
    """

    def __init__(self, retime_parms: RetimeParms = None):
        self.retime_parms = retime_parms

    def compare_equal_length_single_animations(self, rec_anim: Animation, lib_anim: Animation) -> ScoreSpaceElement:
        """
        Compare 2 animations with equal length and return score

        Parameters
        ----------
        rec_anim: Animation
            First animation to compare
        lib_anim: Animation
            Second animation to compare

        Returns
        -------
        score: ScoreSpaceElement
            The comparison score (0 is equal), the higher the score - the bigger the difference
        """

        score = rec_anim.diff_score(lib_anim, diff_type="abs", score_type="sum")
        return ScoreSpaceElement(score, anim=lib_anim)

    def compare_equal_length_library_animations(self, rec_anim: Animation, anim_lib: Union[AnimationLibrary, List[Animation]]) -> List[ScoreSpaceElement]:
        """
        Compare animations with all the animations in library (which must have equal length) and return score

        Parameters
        ----------
        rec_anim: Animation
            Animation to compare
        anim_lib: AnimationLibrary
            Animation library to compare

        Returns
        -------
        scores: List[ScoreSpaceElement]

        """
        scores = list()  # List[ScoreSpaceElement]

        for library_anim in anim_lib:
            score = self.compare_equal_length_single_animations(rec_anim, library_anim)
            scores.append(score)

        return scores

    def get_single_anim_moving_window_scores(self, rec_anim: Animation, anim: Animation, window_step=1) -> List[ScoreSpaceElement]:
        # TODO Write the doc
        """
        Slide the moving window with lib_anim through the rec_anim and collect scores

        Parameters
        ----------
        rec_anim:

        anim:

        window_step:


        Returns
        -------


        """
        scores = list()  # List[ScoreSpaceElement]

        if anim.num_frames() > rec_anim.num_frames():
            raise ValueError("Length or lib_anim can't be greater than length of rec_anim")

        for win_start in range(0, rec_anim.num_frames() - anim.num_frames() + 1, window_step):
            cut_anim = rec_anim.cut_window(win_start, anim.num_frames())

            score_space_el = self.compare_equal_length_single_animations(cut_anim, anim)
            score_space_el.window_start_frame = win_start

            scores.append(score_space_el)

        return scores

    def get_anim_library_moving_window_scores(self, rec_anim: Animation, anim_lib: AnimationLibrary, window_step=1) -> List[List[ScoreSpaceElement]]:
        scores = []  # List[List[ScoreSpaceElement]]

        for anim in anim_lib:
            scores.append(self.get_single_anim_moving_window_scores(rec_anim, anim, window_step=window_step))

        return scores

    # def run_library_comparison(self, recorded_animation: Animation, animation_library: AnimationLibrary):
    #     """
    #     Run animation comparison through the library and return the ScoreSpace.
    #     Here we assume that the recorded animation is long and the library animations are short
    #     so we slide the library animations through the recorded animation and find the score
    #     then we find the best fitting candidates based on the score
    #
    #     Parameters
    #     ----------
    #     recorded_animation : AnimationLibrary
    #         Recorded animation, where the patterns from animation library are searched
    #     animation_library : AnimationLibrary
    #         The collection of animations that are locally compared with our recorded animation
    #
    #     Returns
    #     -------
    #     score_space: ScoreSpace
    #         The calculated score space to search for candidates using retrieve_candidates_from_score_space()
    #
    #     See Also
    #     --------
    #     retrieve_candidates_from_score_space()
    #
    #     """
    #
    #     # This score tensor is static by library_animation, window_scale dimensions
    #     # But may be dynamic by window_start dimension
    #     score_space = self.init_score_space(space_type="linear")
    #
    #     # For each animation in library
    #     # TODO Check if we need enumerate here
    #     for library_animation_idx, library_animation in enumerate(animation_library.animations()):
    #
    #         # Get the window scales range
    #         # TODO Check if we need enumerate here
    #         for window_scale_idx, window_scale in enumerate(self.retime_parms.get_window_scales()):
    #
    #             # Scale the animation
    #             scaled_library_animation = library_animation.retime(window_scale)
    #
    #             # Slide the moving window and get score for each window position as a list of ScoreSpaceElement
    #             scores_list = self.get_single_anim_moving_window_scores(
    #                 recorded_animation, scaled_library_animation,  self.get_window_step()
    #             )
    #
    #             score_space.insert_list(scores_list)
    #
    #     return score_space

    # def get_window_step(self):
    #     """
    #     Returns the step of a moving window
    #
    #     TODO Implement more complex way to calculate step
    #
    #     Returns
    #     -------
    #
    #     """
    #     return 1

    # def init_score_space(self, space_type) -> ScoreSpace:
    #     """
    #     This function is intended to be just a wrapper to create a desired type of score space.
    #
    #     """
    #     if space_type == "linear":
    #         return LinearScoreSpace()
    #     else:
    #         raise NotImplementedError(f"space_type {space_type} not implemented")

    # def compare_and_score_animations(self, anim1: Animation, anim2: Animation) -> Score:
    #     pass
