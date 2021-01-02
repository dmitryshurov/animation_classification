#  Copyright (c) 2020. Dmitry Shurov

from animation import Animation
from typing import List, Iterator


class AnimationLibrary:
    def __init__(self, anim_list: List[Animation] = None):
        if anim_list is None:
            anim_list = list()

        if not isinstance(anim_list, (list, tuple)):
            raise ValueError(f"Wrong anim_list type `{type(anim_list)}`: must be list or tuple")

        for anim in anim_list:
            if not isinstance(anim, Animation):
                raise ValueError(f"Wrong element type `{type(anim)}` in anim_list: must be Animation")

        self.anim_list = anim_list

    def __iter__(self) -> Iterator[Animation]:
        for anim in self.anim_list:
            yield anim

    def __getitem__(self, item) -> Animation:
        return self.anim_list[item]

    def animations(self) -> List[Animation]:
        return self.anim_list

    def size(self) -> int:
        return len(self.anim_list)

    def append(self, anim: Animation):
        self.anim_list.append(anim)
