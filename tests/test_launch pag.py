import pytest
from ..model import * 

def test_count_launchpads():
    LAUNCH_PADS = [LaunchPadConfig(0,0,2), LaunchPadConfig(1,1,1)]
    GRID_SIZE = 5
    model = UAVModel(GRID_SIZE, GRID_SIZE, LAUNCH_PADS)