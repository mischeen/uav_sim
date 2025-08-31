import mesa
import numpy as np
from collections import namedtuple
import random


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

    def __init__(self, width, height, launch_pads, p_tree=0.9):
        super().__init__()
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Coverage": compute_coverage,
                "Redundancy": compute_redundancy}
        )
        
        self.grid = mesa.space.MultiGrid(width, height, torus=False) # creates space
        self.create_landscape(p_tree)
        self.ignite_cell((width//2, height//2))
        self.coverage = np.zeros((height, width), dtype=int) # coverage matrix to track visits per cell        
        self.launch_pads = self.create_launchpads(launch_pads=launch_pads)
        for pad in self.launch_pads:
            pad.spawn_uavs(model=self)
                    

    def create_landscape(self, p_tree):
        for _, pos in self.grid.coord_iter():
            state = "tree" if random.random() < p_tree else "empty"
            cell = CellAgent(self, state=state)
            self.grid.place_agent(cell, pos)

    def ignite_cell(self, pos):
        cell = next(a for a in self.grid.get_cell_list_contents([pos]) if isinstance(a, CellAgent))
        cell.set_state("burning")


    def create_launchpads(self, launch_pads):
        """Creates launchpad on the grid"""
        pads = []
        for p in launch_pads:
            pads.append(LaunchPad((p.x, p.y), p.num_uavs))
        return pads

    def step(self):
        cells = self.agents.select(agent_type=CellAgent)   
        cells.do('update_state')
        cells.do('advance')
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


class CellAgent(mesa.Agent):

    def __init__(self, model, state):
        super().__init__(model)
        self.valid_states = ["empty", "tree", "burning"]
        self.set_state(state)
        self.next_state = None
        
    def set_state(self, state):
        if state in self.valid_states:
            self.state = state
            self._set_color(state)

        else:
            raise ValueError(f'Provided state "{state}" is not a valid cell state. Choose from {self.valid_states}.') 

    def _set_color(self, state):
        if state == "tree":
            self.color = 'green'
        elif state == "burning":
            self.color = 'orange'
        else:
            self.color = 'black'

    def update_state(self):
        if self.state == "tree":
            neighbors = self.model.grid.get_neighbors(
                self.pos, moore=True, include_center=False
            ) 
            burning_neighbors = [n for n in neighbors if isinstance(n, CellAgent) and n.state == "burning"]
            if burning_neighbors:
                if random.random() < self.ignite_prob(burning_neighbors):
                    self.next_state = "burning"
                else:
                    self.next_state = "tree"
            else:
                self.next_state = "tree"   
        elif self.state == "burning":
            self.next_state = "empty"    
        else:
            self.next_state = "empty"         


    def ignite_prob(self, burning_neighbors): 
        base=0.4
        x, _ = self.pos
        for n in burning_neighbors:
            nx, _ = n.pos
            if x > nx:
                return base + 0.5
        else:
            return base


    def advance(self):
        """Apply the state update."""
        self.set_state(self.next_state)


