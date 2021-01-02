#  Copyright (c) 2020. Dmitry Shurov


class ScoreSpace:
    def __init__(self):
        pass

    # def insert(self, element: ScoreSpaceElement):
    #     pass
    #
    # def insert_list(self, elements: List[ScoreSpaceElement]):
    #     pass

    def deepcopy(self):
        pass

    def empty(self):
        pass

    def get_best_score_element(self, remove=False):
        pass


#
#
# class LinearScoreSpace(ScoreSpace):
#     """
#     The storage for all ScoreSpaceElement objects
#     TODO: Use more efficient data structure
#     """
#     def __init__(self):
#         ScoreSpace.__init__(self)
#         self.elements = list()
#
#     def insert(self, element: ScoreSpaceElement):
#         self.elements.append(element)
#
#     def insert_list(self, elements: List[ScoreSpaceElement]):
#         self.elements.extend(elements)
#
#     # def get_candidates(self, num_candidates: int, min_distance: float) -> List[AnimationCandidate]:
#     #     pass

