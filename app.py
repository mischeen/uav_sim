from src.model import UAVModel, LaunchPadConfig, UAVAgent, CellAgent
from mesa.visualization import SolaraViz, make_plot_component, Slider

from mesa.visualization.utils import update_counter
import matplotlib
import matplotlib.patches as patches
import solara
from matplotlib.figure import Figure
import numpy as np

# Simulation parameters: uv run solara run app.py
LAUNCH_PADS = [LaunchPadConfig(9,0,1)]
GRID_SIZE = 50

model_params = {
    "width": GRID_SIZE,
    "height": GRID_SIZE,
    "launch_pads": LAUNCH_PADS,
    "p_tree": Slider(
            "Tree density",
            value=0.9,       # default
            min=0.0,
            max=1.0,
            step=0.05,
        ),
}

# Initialize model
model = UAVModel(GRID_SIZE, GRID_SIZE, LAUNCH_PADS)

# Custom Solara component for UAV trajectories
uav_cmap = matplotlib.colormaps.get_cmap("tab20")

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
    height, width = model.grid.height, model.grid.width
    ax.set_xlim(-0.5, width-0.5)
    ax.set_ylim(-0.5, height-0.5)
    ax.set_xticks(np.arange(width))
    ax.set_yticks(np.arange(height))
    ax.set_aspect('equal')
    ax.grid(True)

    # Draw Calls
    cell_size = 1.0
    for cell in (a for a in model.agents if isinstance(a, CellAgent)):
        x, y = cell.pos
        rect = patches.Rectangle(
            (x, y),                # (lower-left corner)
            cell_size, cell_size,  # width, height
            facecolor=cell.color,
            edgecolor="black",     # optional grid lines
            linewidth=0.5,
            zorder=5,
        )
        ax.add_patch(rect)

    # Draw UAV trajectories and positions
    for i, uav in enumerate(a for a in model.agents if isinstance(a, UAVAgent)):
            color = uav_cmap(i % 20)
            track = np.array(uav.track)
            if len(track) > 1:
                ax.plot(track[:,0], track[:,1], color=color, linewidth=4, alpha=0.8, zorder=6)
            ax.scatter(track[-1,0], track[-1,1], color=color, s=200, edgecolor=None, zorder=7)

    return solara.FigureMatplotlib(fig)

# Coverage plot component
CoveragePlot = make_plot_component("Coverage")
RedundancePlot = make_plot_component("Redundancy")


# Wrap your plots/components into a custom dashboard layout
@solara.component
def UAVDashboard(model):
    with solara.Column():
        # Top row: the grid
        with solara.Card("Simulation Grid"):
            UAVGrid(model)

        # Bottom row: coverage + redundance side by side
        with solara.Row():
            with solara.Card("Coverage Over Time", style={"width": "50%"}):
                CoveragePlot(model)
            with solara.Card("Redundancy Over Time", style={"width": "50%"}):
                RedundancePlot(model)

# Now tell SolaraViz to use your custom dashboard
page = SolaraViz(
    model,
    components=[UAVDashboard],   
    name="UAV Simulator",
    model_params=model_params,
)
