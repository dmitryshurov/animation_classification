#  Copyright (c) 2020. Dmitry Shurov

from animation import Animation, np


class ScalingParms:
    def __init__(self):
        self.scale = None


class ScaledAnimation(Animation):
    def __init__(self,
                 source_anim: Animation,      # Animation that was used as the basics
                 scaling_parms:ScalingParms,  # Scaling parameters
                 matrix: np.ndarray           # Data after scaling
                 ):
        super().__init__(matrix)
        self.source_anim = source_anim
        self.scaling_parms = scaling_parms