from src.model import UAVModel, LaunchPadConfig
from mesa.visualization import SolaraViz, make_space_component, make_plot_component
from mesa.visualization.utils import update_counter
import matplotlib
import solara
from matplotlib.figure import Figure
import numpy as np

# Simulation parameters
LAUNCH_PADS = [LaunchPadConfig(0,0,10)]
GRID_SIZE = 20

model_params = {
    "width": GRID_SIZE,
    "height": GRID_SIZE,
    "launch_pads": LAUNCH_PADS
}

# Initialize model
model = UAVModel(GRID_SIZE, GRID_SIZE, LAUNCH_PADS)

# Custom Solara component for UAV trajectories
cmap = matplotlib.cm.get_cmap("tab20")

@solara.component
def UAVGrid(model):
    """
    Solara component that draws a 2D grid with UAV positions and trajectories.
    """
    update_counter.get() # This is required to update the counter
    # Trigger reactive update
    model.datacollector.get_model_vars_dataframe()

    fig = Figure(figsize=(10,10))
    ax = fig.subplots()
    ax.set_title("UAV Grid with Trajectories")

    height, width = model.grid.height, model.grid.width
    ax.set_xlim(-0.5, width-0.5)
    ax.set_ylim(-0.5, height-0.5)
    ax.set_xticks(np.arange(width))
    ax.set_yticks(np.arange(height))
    ax.set_aspect('equal')
    ax.grid(True)

    # Draw UAV trajectories and positions
    for i, uav in enumerate(model.agents):
        color = cmap(i % 20)
        track = np.array(uav.track)
        if len(track) > 1:
            ax.plot(track[:,0], track[:,1], color=color, alpha=0.4)
        ax.scatter(track[-1,0], track[-1,1], color=color, s=100, edgecolor=None, zorder=5)

    return solara.FigureMatplotlib(fig)

# Coverage plot component
CoveragePlot = make_plot_component("Coverage")
RedundancePlot = make_plot_component("Redundance")

# Create the Solara dashboard
page = SolaraViz(
    model,
    components=[UAVGrid, CoveragePlot, RedundancePlot],
    name="UAV Simulator",
    model_params=model_params,
)
