#  Copyright (c) 2020. Dmitry Shurov

from typing import Tuple
import numpy as np


class RetimeParms:

    def __init__(self, min_percent: float, max_percent: float, num_steps: int):
        self.min_percent = min_percent
        self.max_percent = max_percent
        self.num_steps = num_steps

    def get_window_scales(self) -> Tuple:
        return np.linspace(self.min_percent, self.max_percent, self.num_steps)
