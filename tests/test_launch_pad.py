import pytest
from src.model import UAVModel, LaunchPadConfig

# Run with python -m pytest tests


def test_count_launchpads():
    LAUNCH_PADS = [LaunchPadConfig(0,0,1), LaunchPadConfig(1,1,1)]
    GRID_SIZE = 5
    model = UAVModel(GRID_SIZE, GRID_SIZE, LAUNCH_PADS)
    
    assert len(model.launch_pads) == 2


def test_position_launchpads():
    LAUNCH_PADS = [LaunchPadConfig(0,10,1), LaunchPadConfig(15,5,1)]
    GRID_SIZE = 20
    model = UAVModel(GRID_SIZE, GRID_SIZE, LAUNCH_PADS)
    
    assert model.launch_pads[0].pos == (0,10)
    assert model.launch_pads[1].pos == (15,5)


def test_count_uavs():
    NUM_UAVS = 3
    LAUNCH_PADS = [LaunchPadConfig(0,0,NUM_UAVS), LaunchPadConfig(1,1,NUM_UAVS*2)]
    GRID_SIZE = 5
    model = UAVModel(GRID_SIZE, GRID_SIZE, LAUNCH_PADS)
    
    assert model.launch_pads[0].num_uavs == NUM_UAVS
    assert model.launch_pads[1].num_uavs == NUM_UAVS*2
    assert len(model.agents) ==  NUM_UAVS + (NUM_UAVS*2)


def test_zero_uavs():
    NUM_UAVS = 0
    LAUNCH_PADS = [LaunchPadConfig(0,0,NUM_UAVS)]
    GRID_SIZE = 5
    model = UAVModel(GRID_SIZE, GRID_SIZE, LAUNCH_PADS)
    
    assert model.launch_pads[0].num_uavs == NUM_UAVS
    assert len(model.agents) ==  NUM_UAVS
