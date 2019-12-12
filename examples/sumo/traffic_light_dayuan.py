"""Traffic Light Grid example."""
from flow.controllers import GridRouter
from flow.core.experiment import Experiment
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams
from flow.core.params import VehicleParams
from flow.core.params import TrafficLightParams
from flow.core.params import SumoCarFollowingParams
from flow.core.params import InFlows
from flow.envs.ring.accel import AccelEnv, ADDITIONAL_ENV_PARAMS
from flow.networks import DaYuanNetwork

def get_flow_params(additional_net_params):
    """Define the network and initial params in the presence of inflows.

    Parameters
    ----------
    additional_net_params : dict
        network-specific parameters that are unique to the traffic light grid

    Returns
    -------
    flow.core.params.InitialConfig
        parameters specifying the initial configuration of vehicles in the
        network
    flow.core.params.NetParams
        network-specific parameters used to generate the network
    """
    initial = InitialConfig(
        spacing='custom', lanes_distribution=float('inf'), shuffle=True)

    inflow = InFlows()
    outer_edges = [ "out0_0", "out1_0", "out2_0", "out3_0", "out4_0", "out5_1" ]
    for i in range(len(outer_edges)):
        inflow.add(
            veh_type='human',
            edge=outer_edges[i],
            probability=0.25,
            departLane='free',
            departSpeed=20)

    net = NetParams(
        inflows=inflow,
        additional_params=additional_net_params)

    return initial, net


def get_non_flow_params(enter_speed):
    """Define the network and initial params in the absence of inflows.

    Note that when a vehicle leaves a network in this case, it is immediately
    returns to the start of the row/column it was traversing, and in the same
    direction as it was before.

    Parameters
    ----------
    enter_speed : float
        initial speed of vehicles as they enter the network.
    add_net_params: dict
        additional network-specific parameters (unique to the traffic light grid)

    Returns
    -------
    flow.core.params.InitialConfig
        parameters specifying the initial configuration of vehicles in the
        network
    flow.core.params.NetParams
        network-specific parameters used to generate the network
    """
    additional_init_params = {'enter_speed': enter_speed}
    initial = InitialConfig(
        spacing='custom', additional_params=additional_init_params)
    net = NetParams()

    return initial, net


def da_yuan_example(render=None, use_inflows=True):
    """
    Perform a simulation of vehicles on a traffic light grid.

    Parameters
    ----------
    render: bool, optional
        specifies whether to use the gui during execution
    use_inflows : bool, optional
        set to True if you would like to run the experiment with inflows of
        vehicles from the edges, and False otherwise

    Returns
    -------
    exp: flow.core.experiment.Experiment
        A non-rl experiment demonstrating the performance of human-driven
        vehicles and balanced traffic lights on a traffic light grid.
    """
    v_enter = 10
    sim_params = SumoParams(sim_step=0.05, render=True)

    if render is not None:
        sim_params.render = render

    vehicles = VehicleParams()
    vehicles.add(
        veh_id="human",
        routing_controller=(GridRouter, {}),
        car_following_params=SumoCarFollowingParams(
            min_gap=2.5,
            decel=7.5,  # avoid collisions at emergency stops
        ),
        num_vehicles=6)

    env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)

    tl_logic = TrafficLightParams(baseline=False)
    phases = [{
        "duration": "31",
        "minDur": "8",
        "maxDur": "45",
        "state": "rrGGGG"
    }, {
        "duration": "6",
        "minDur": "3",
        "maxDur": "6",
        "state": "rryyyy"
    }, {
        "duration": "31",
        "minDur": "8",
        "maxDur": "45",
        "state": "GGrrrr"
    }, {
        "duration": "6",
        "minDur": "3",
        "maxDur": "6",
        "state": "yyrrrr"
    }]
    tl_logic.add("inner0", phases=phases, programID=1)
    tl_logic.add("inner1", phases=phases, programID=1)
    tl_logic.add("inner2", phases=phases, programID=1, tls_type="actuated")
    tl_logic.add("inner3", phases=phases, programID=1, tls_type="actuated")
    
    additional_net_params = {
        "speed_limit": 35,
        "horizontal_lanes": 1,
        "vertical_lanes": 1
    }

    if use_inflows:
        initial_config, net_params = get_flow_params(additional_net_params=additional_net_params)
    else:
        initial_config, net_params = get_non_flow_params(enter_speed=v_enter)

    network = DaYuanNetwork(
        name="grid-intersection",
        vehicles=vehicles,
        net_params=net_params,
        initial_config=initial_config,
        traffic_lights=tl_logic)

    env = AccelEnv(env_params, sim_params, network)

    return Experiment(env)


if __name__ == "__main__":
    # import the experiment variable
    exp = da_yuan_example()

    # run for a set number of rollouts / time steps
    exp.run(1, 15000)
