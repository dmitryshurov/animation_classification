#  Copyright (c) 2020. Dmitry Shurov

import copy
from typing import List
from score_space import ScoreSpace
from score_space_element import ScoreSpaceElement

class NoElementsAvailableError(Exception):
    pass

class ScoreSpaceSimple2D(ScoreSpace):

    def __init__(self, elements: List[List[ScoreSpaceElement]] = None):
        super().__init__()

        self.elements = copy.deepcopy(elements) if elements else list()

    def empty(self):
        # If any sublist has at least one element = not empty
        for e in self.elements:
            if len(e) > 0:
                return False

        # If there's no sublist or each sublist is empty = empty
        return True

    def get_best_score_element(self, remove=False):
        # TODO Refactor!
        mins = [(min(x), x) for x in self.elements if len(x) > 0]

        if len(mins) == 0:
            raise NoElementsAvailableError('No elements available in the Score Space')

        min_el = min(mins, key=lambda x: x[0])

        if remove:
            min_el[1].remove(min_el[0])

        return min_el[0]
