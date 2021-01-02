#  Copyright (c) 2020. Dmitry Shurov

from score_space_element import ScoreSpaceElement
from typing import List


class ScoreSpaceAnalyzer:
    """
    This one actually should take the be
    """

    def __init__(self):
        pass

    @staticmethod
    def get_sorted_from_library_recognition(score_space: List[List[ScoreSpaceElement]]):
        return [sorted(x) for x in score_space]

    @staticmethod
    def get_best_scores(score_space: List[List[ScoreSpaceElement]], num_scores: int):
        """
        Returns no more than num_scores of best scores sorted by score.
        The lower score the better, so lowest scores come first.

        Args:
            num_scores: Maximum number of best scores to collect

        Returns:

        """
        sorted_scores = ScoreSpaceAnalyzer.get_sorted_from_library_recognition(score_space)

        return [x[:num_scores] for x in sorted_scores]


    # @staticmethod
    # def retrieve_candidates_from_score_space(self, score_space: ScoreSpace,
    #                                          num_candidates: int,
    #                                          min_distance: int) -> List[AnimationCandidate]:
    #     # This functions should do some sort of clustering and
    #     # select the candidates with highest scores, but not too similar
    #
    #     # Candidates should be a score-ordered vector of structures that contain data about the animations
    #     candidates = score_space.get_candidates(num_candidates, min_distance)
    #
    #     return candidates
