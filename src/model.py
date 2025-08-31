import mesa
import numpy as np
from collections import namedtuple


LaunchPadConfig = namedtuple('LaunchPadConfig', ('x', 'y', 'num_uavs'))

def compute_coverage(model):
    """Fraction of cells visited at least once"""
    return np.count_nonzero(model.coverage > 0) / model.coverage.size

def compute_redundancy(model):
    visited_cells = model.coverage[model.coverage > 0]
    if len(visited_cells) == 0:
        return 0
    return visited_cells.mean()

class UAVModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, width, height, launch_pads):
        super().__init__()
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Coverage": compute_coverage,
                "Redundancy": compute_redundancy}
        )
        
        self.grid = mesa.space.MultiGrid(width, height, torus=False) # creates space
        self.coverage = np.zeros((height, width), dtype=int) # coverage matrix to track visits per cell
        self.launch_pads = self.create_launchpads(launch_pads=launch_pads)
        for pad in self.launch_pads:
            pad.spawn_uavs(model=self)
        

    def create_launchpads(self, launch_pads):
        """Creates launchpad on the grid"""
        pads = []
        for p in launch_pads:
            pads.append(LaunchPad((p.x, p.y), p.num_uavs))
        return pads


    def step(self):
        self.agents.do("move")
        self.agents.do("inspect")
        self.datacollector.collect(self)


class LaunchPad():
    """A location for start and landing of UAVs"""

    def __init__(self, pos, num_uavs):
        self.pos = pos
        self.num_uavs = num_uavs
        

    def spawn_uavs(self, model):
        """Spawns n UAVs on the launch pad"""
        self.uavs = UAVAgent.create_agents(model=model, n=self.num_uavs)
        for a in self.uavs:
            model.grid.place_agent(a, self.pos)
            a.track_position()
            a.inspect()



class UAVAgent(mesa.Agent):
    """A model with UAV agents exploring a 2D grid and recording coverage"""

    def __init__(self, model):
        super().__init__(model) 
        self.track = []

    def track_position(self):
        """Keeps track of the trajectory of a UAV"""
        self.track.append(self.pos)

    def move(self):
        """Moves the drone to another cell"""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.track_position()

    def inspect(self):
        """Drone inspects the cell"""
        y, x = self.pos
        self.model.coverage[y][x] += 1