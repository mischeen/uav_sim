from src.model import UAVModel, LaunchPadConfig
from mesa.visualization import SolaraViz, make_space_component, make_plot_component


# run with uv run solara run app.py


# Grid component with agent portrayal
def agent_portrayal(agent):
    return {
        "color": "tab:blue",
        "size": 50,
    }

LAUNCH_PADS = [LaunchPadConfig(0,0,10)]
GRID_SIZE = 20
ITERATIONS = 500

model_params = {
    "width": GRID_SIZE,
    "height": GRID_SIZE,
    "launch_pads": [LaunchPadConfig(0,0,5)]
}

model = UAVModel(GRID_SIZE,GRID_SIZE,LAUNCH_PADS) 
SpaceGraph = make_space_component(agent_portrayal)
CoveragePlot = make_plot_component("Coverage")

# Create the dashboard
page = SolaraViz(
    model,
    components=[SpaceGraph, CoveragePlot],
    name="UAV Simulator",
    model_params=model_params,
)
