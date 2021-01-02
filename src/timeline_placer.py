#  Copyright (c) 2020. Dmitry Shurov

from typing import List

from timeline import Timeline, FramesAlreadyReservedError
from score_space_element import ScoreSpaceElement


class TimelinePlacer:
    @staticmethod
    def layout_score_space_on_timeline(score_space: List[List[ScoreSpaceElement]], timeline: Timeline) -> Timeline:
        # TODO Replace List[List[ScoreSpaceElement]] with LinearScoreSpace or smth. everywhere

        """
        Grab elements from the score space and drop them onto the timeline using some algorithm,
        that may (and will) change. So consider it to be sort of a callback or mixin or...

        
        So, the algorithm is:
        1. Find the highest score through all the ScoreSpaceElements
        
        2. If each of its frames is not reserved on the timeline
           2.1. Add it to the timeline
           2.2. Add the frames occupied by the animation to the reserved frames list
           
        3. Drop it from the list
        
        4. Repeat step 1 till the timeline is full or till the score list is empty.
        - 
        """

        # This is a temporary trick while I don't use the ScoreSpace everywhere in the code
        # instead of list of lists
        from score_space_simple_2d import ScoreSpaceSimple2D
        score_space = ScoreSpaceSimple2D(score_space)

        while not score_space.empty():
            score_element = score_space.get_best_score_element(remove=True)

            try:
                timeline.add_element(score_element)
                print(f"Added {score_element} to timeline")
            except FramesAlreadyReservedError:
                # Just drop the elements which can't be placed to the Timeline and move on
                pass

        return timeline
