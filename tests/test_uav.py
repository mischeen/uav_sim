import pytest
from src.model import UAVModel, LaunchPadConfig

# Run with python -m pytest tests

@pytest.fixture
def simple_model():
    X, Y, NUM_UAVS = 0, 0, 1
    LAUNCH_PADS = [LaunchPadConfig(X, Y, NUM_UAVS)]
    GRID_SIZE = 5
    model = UAVModel(GRID_SIZE, GRID_SIZE, LAUNCH_PADS)
    return model


def test_track_start(simple_model):
    model = simple_model
    uav = model.agents[0]
    assert uav.track[0] == (0,0) # Starting position


def test_track_length(simple_model):
    ITERATIONS = 5
    model = simple_model
    uav = model.agents[0]
    assert len(uav.track) == 1 # Starting position

    for _ in range(ITERATIONS):     
        model.step()
    
    assert len(uav.track) ==  ITERATIONS + 1 # Starting position + all movements


def test_track_delta(simple_model):
    model = simple_model
    uav = model.agents[0]
    model.step()

    assert uav.track[0] !=  uav.track[1]