"""Contains the traffic light grid scenario class."""

from flow.networks.base import Network
from flow.core.params import InitialConfig
from flow.core.params import TrafficLightParams
from collections import defaultdict
import numpy as np

'''
ADDITIONAL_NET_PARAMS = {
    # dictionary of traffic light grid array data
    "grid_array": {
        # number of horizontal rows of edges
        "row_num": 3,
        # number of vertical columns of edges
        "col_num": 2,
        # length of inner edges in the traffic light grid network
        "inner_length": None,
        # length of edges where vehicles enter the network
        "short_length": None,
        # length of edges where vehicles exit the network
        "long_length": None,
        # number of cars starting at the edges heading to the top
        "cars_top": 20,
        # number of cars starting at the edges heading to the bottom
        "cars_bot": 20,
        # number of cars starting at the edges heading to the left
        "cars_left": 20,
        # number of cars starting at the edges heading to the right
        "cars_right": 20,
    },
    # number of lanes in the horizontal edges
    "horizontal_lanes": 1,
    # number of lanes in the vertical edges
    "vertical_lanes": 1,
    # speed limit for all edges, may be represented as a float value, or a
    # dictionary with separate values for vertical and horizontal lanes
    "speed_limit": {
        "horizontal": 35,
        "vertical": 35
    }
}
'''
section_length = 100
class DaYuanNetwork(Network):
    """Traffic Light Grid network class.

    The traffic light grid network consists of m vertical lanes and n
    horizontal lanes, with a total of nxm intersections where the vertical
    and horizontal edges meet.

    Requires from net_params:

    * **grid_array** : dictionary of grid array data, with the following keys

      * **row_num** : number of horizontal rows of edges
      * **col_num** : number of vertical columns of edges
      * **inner_length** : length of inner edges in traffic light grid network
      * **short_length** : length of edges that vehicles start on
      * **long_length** : length of final edge in route
      * **cars_top** : number of cars starting at the edges heading to the top
      * **cars_bot** : number of cars starting at the edges heading to the
        bottom
      * **cars_left** : number of cars starting at the edges heading to the
        left
      * **cars_right** : number of cars starting at the edges heading to the
        right

    * **horizontal_lanes** : number of lanes in the horizontal edges
    * **vertical_lanes** : number of lanes in the vertical edges
    * **speed_limit** : speed limit for all edges. This may be represented as a
      float value, or a dictionary with separate values for vertical and
      horizontal lanes.

    Usage
    -----
    >>> from flow.core.params import NetParams
    >>> from flow.core.params import VehicleParams
    >>> from flow.core.params import InitialConfig
    >>> from flow.networks import TrafficLightGridNetwork
    >>>
    >>> network = DaYuanNetwork(
    >>>     name='dayuan',
    >>>     vehicles=VehicleParams(),
    >>>     net_params=NetParams(
    >>>         additional_params={
    >>>             'grid_array': {
    >>>             },
    >>>             }
    >>>         },
    >>>     )
    >>> )
    """

    def __init__(self,
                 name,
                 vehicles,
                 net_params,
                 initial_config=InitialConfig(),
                 traffic_lights=TrafficLightParams()):
        optional = ["tl_logic"]
        # retrieve all additional parameters
        # refer to the ADDITIONAL_NET_PARAMS dict for more documentation

        self.use_traffic_lights = net_params.additional_params.get(
            "traffic_lights", True)
        # radius of the inner nodes (ie of the intersections)
        self.inner_nodes_radius = 6.2

        # total number of edges in the network
        self.num_edges = 8

        # name of the network (DO NOT CHANGE)
        self.name = "BobLoblawsLawBlog"
        super().__init__(name, vehicles, net_params, initial_config,
                         traffic_lights)

    def specify_nodes(self, net_params):
        """See parent class."""
        return self._inner_nodes + self._outer_nodes

    def specify_edges(self, net_params):
        """See parent class."""
        return self._inner_edges + self._outer_edges

    def specify_routes(self, net_params):
        """See parent class."""
        routes = defaultdict(list)

        '''
                          |                |                |                |
                    out1_{0,1}          out2_{0,1}     out3_{0,1}      out4_{0,1}
                          |                |                |                |
            --out0_{0,1}--x--inner0_{0,1}--x--inner1_{0,1}--x--inner2_{0,1}--x--out5_{0,1}

            note: {0,1} indicates the direction, where 0 is rigth/down,  1 is left/top
        '''

        routes["out0_0"] = [
                ( ["out0_0", "out1_1"], 0.1 ),
                ( ["out0_0", "inner0_0", "out2_1"], 0.1 ),
                ( ["out0_0", "inner0_0", "inner1_0", "out3_1"], 0.1 ),
                ( ["out0_0", "inner0_0", "inner1_0", "inner2_0", "out4_1"], 0.3 ),
                ( ["out0_0", "inner0_0", "inner1_0", "inner2_0", "out5_0"], 0.4 )
            ]

        routes["out1_0"] = [
                ( ["out1_0", "out0_1"], 0.1 ),
                ( ["out1_0", "inner0_0", "out2_1"], 0.1 ),
                ( ["out1_0", "inner0_0", "inner1_0", "out3_1"], 0.1 ),
                ( ["out1_0", "inner0_0", "inner1_0", "inner2_0", "out4_1"], 0.3 ),
                ( ["out1_0", "inner0_0", "inner1_0", "inner2_0", "out5_0"], 0.4 )
            ]

        routes["out2_0"] = [
                ( ["out2_0", "inner0_1", "out0_1"], 0.1 ),
                ( ["out2_0", "inner0_1", "out1_1"], 0.1 ),
                ( ["out2_0", "inner1_0", "out3_1"], 0.1 ),
                ( ["out2_0", "inner1_0", "inner2_0", "out4_1"], 0.3 ),
                ( ["out2_0", "inner1_0", "inner2_0", "out5_0"], 0.4 )
            ]

        routes["out3_0"] = [
                ( ["out3_0", "inner1_1", "inner0_1", "out0_1"], 0.1 ),
                ( ["out3_0", "inner1_1", "inner0_1", "out1_1"], 0.1 ),
                ( ["out3_0", "inner1_1", "out2_1"], 0.1 ),
                ( ["out3_0", "inner2_0", "out4_1"], 0.3 ),
                ( ["out3_0", "inner2_0", "out5_0"], 0.4 )
            ]

        routes["out4_0"] = [
                ( ["out4_0", "inner2_1", "inner1_1", "inner0_1", "out0_1"], 0.1 ),
                ( ["out4_0", "inner2_1", "inner1_1", "inner0_1", "out1_1"], 0.1 ),
                ( ["out4_0", "inner2_1", "inner1_1", "out2_1"], 0.1 ),
                ( ["out4_0", "inner2_1", "out3_1"], 0.3 ),
                ( ["out4_0", "out5_0"], 0.4 )
            ]

        routes["out5_1"] = [
                ( ["out5_1", "inner2_1", "inner1_1", "inner0_1", "out0_1"], 0.2 ),
                ( ["out5_1", "inner2_1", "inner1_1", "inner0_1", "out1_1"], 0.2 ),
                ( ["out5_1", "inner2_1", "inner1_1", "out2_1"], 0.2 ),
                ( ["out5_1", "inner2_1", "out3_1"], 0.2 ),
                ( ["out5_1", "out4_1"], 0.2 )
            ]

        return routes

    # ===============================
    # ============ UTILS ============
    # ===============================

    @property
    def _inner_nodes(self):
        """Build out the inner nodes of the network.

            |     |     |     |
        --- 0 --- 1 --- 2 --- 3 ---

        The id of a node is then "center{index}", for instance "center0" for
        node 0, "center1" for node 1 etc.

        Returns
        -------
        list <dict>
            List of inner nodes
        """
        node_type = "traffic_light" if self.use_traffic_lights else "priority"

        nodes = []
        for i in range(4):
            nodes.append({
                "id": "inner{}".format(i),
                "x": ( i + 1 ) * section_length,
                "y": 0,
                "type": node_type,
                "radius": self.inner_nodes_radius 
            })

        return nodes

    @property
    def _outer_nodes(self):
        """Build out the outer nodes of the network.

                 1     2     3     4
                 |     |     |     |
        (0) *---------------------------5

        For example, at extremity (*):
        - the id of the output node is "out{*}"

        Returns
        -------
        list <dict>
            List of outer nodes
        """
        nodes = []

        def new_node(x, y, name):
            return [{"id": name, "x": x, "y": y, "type": "priority"}]

        nodes += new_node( 0, 0, "out0" )
        nodes += new_node( section_length, section_length, "out1" )
        nodes += new_node( 2 * section_length, section_length, "out2" )
        nodes += new_node( 3 * section_length, section_length, "out3" )
        nodes += new_node( 4 * section_length, section_length, "out4" )
        nodes += new_node( 5 * section_length, 0, "out5" )

        return nodes

    @property
    def _inner_edges(self):
        """Build out the inner edges of the network.

        The inner edges are the edges joining the inner nodes to each other.

                 |     |     |     |
            *----x--0--x--1--x--2--x----

        id: inner{index}_{lane}

        Returns
        -------
        list <dict>
            List of inner edges
        """
        edges = []

        def new_edge(index, from_node, to_node, orientation, lane):
            return [{
                "id": "inner{}_{}".format( index, lane),
              #  "type": orientation,
                "priority": 78,
                "from": "inner" + str(from_node),
                "to": "inner" + str(to_node),
                "length": section_length
            }]

        for i in range(3):
            edges += new_edge( i, i, i+1, "horizontal", 0 )
            edges += new_edge( i, i+1, i, "horizontal", 1 )

        return edges

    @property
    def _outer_edges(self):
        """Build out the outer edges of the network.

                 1     2     3     4
                 |     |     |     |
            --0--x-----x-----x-----x--5--

        Returns
        -------
        list <dict>
            List of outer edges
        """
        edges = []

        def new_edge(index, from_node, to_node, orientation, lane):
            return [{
                "id": "out{}_{}".format( index, lane),
              #  "type": orientation,
                "priority": 78,
                "from": from_node,
                "to": to_node,
                "length": section_length
            }]

        out_node = "out0"
        inner_node = "inner0"
        edges += new_edge( 0, out_node, inner_node, "horizontal", 0 )
        edges += new_edge( 0, inner_node, out_node, "horizontal", 1 )

        out_node = "out1"
        edges += new_edge( 1, out_node, inner_node, "vertical", 0 )
        edges += new_edge( 1, inner_node, out_node, "vertical", 1 )

        out_node = "out2"
        inner_node = "inner1"
        edges += new_edge( 2, out_node, inner_node, "vertical", 0 )
        edges += new_edge( 2, inner_node, out_node, "vertical", 1 )

        out_node = "out3"
        inner_node = "inner2"
        edges += new_edge( 3, out_node, inner_node, "vertical", 0 )
        edges += new_edge( 3, inner_node, out_node, "vertical", 1 )
        
        out_node = "out4"
        inner_node = "inner3"
        edges += new_edge( 4, out_node, inner_node, "vertical", 0 )
        edges += new_edge( 4, inner_node, out_node, "vertical", 1 )

        out_node = "out5"
        edges += new_edge( 5, out_node, inner_node, "horizontal", 1 )
        edges += new_edge( 5, inner_node, out_node, "horizontal", 0 )

        return edges

    def specify_connections(self, net_params):
        """Build out connections at each inner node.
        """
 
        '''
                          |                |                |                |
                    out1_{0,1}          out2_{0,1}     out3_{0,1}      out4_{0,1}
                          |                |                |                |
            --out0_{0,1}--x--inner0_{0,1}--x--inner1_{0,1}--x--inner2_{0,1}--x--out5_{0,1}

            note: {0,1} indicates the direction, where 0 is rigth/down,  1 is left/top
        '''

        con_dict = {}

        def new_con( from_id, to_id, lane, signal_group):
            return [{
                "from": from_id,
                "to": to_id,
                "fromLane": str(lane-1),
                "toLane": str(lane-1),
                "signal_group": signal_group
            }]

        conn = []
        conn += new_con( "out0_0", "out1_1", 1, 1 )
        conn += new_con( "out0_0", "inner0_0", 1, 1 )
        conn += new_con( "out1_0", "out0_1", 1, 1 )
        conn += new_con( "out1_0", "inner0_0", 1, 1 )
        conn += new_con( "inner0_1", "out0_1", 1, 1 )
        conn += new_con( "inner0_1", "out1_1", 1, 1 )
        con_dict["inner0"] = conn

        conn = []
        conn += new_con( "inner0_0", "out2_1", 1, 1 )
        conn += new_con( "inner0_0", "inner1_0", 1, 1 )
        conn += new_con( "out2_0", "inner0_1", 1, 1 )
        conn += new_con( "out2_0", "inner1_0", 1, 1 )
        conn += new_con( "inner1_1", "out2_1", 1, 1 )
        conn += new_con( "inner1_1", "inner0_1", 1, 1 )
        con_dict["inner1"] = conn

        conn = []
        conn += new_con( "inner1_0", "out3_1", 1, 1 )
        conn += new_con( "inner1_0", "inner2_0", 1, 1 )
        conn += new_con( "out3_0", "inner1_1", 1, 1 )
        conn += new_con( "out3_0", "inner2_0", 1, 1 )
        conn += new_con( "inner2_1", "out3_1", 1, 1 )
        conn += new_con( "inner2_1", "inner1_1", 1, 1 )
        con_dict["inner2"] = conn
 
        conn = []
        conn += new_con( "inner2_0", "out4_1", 1, 1 )
        conn += new_con( "inner2_0", "out5_0", 1, 1 )
        conn += new_con( "out4_0", "inner2_1", 1, 1 )
        conn += new_con( "out4_0", "out5_0", 1, 1 )
        conn += new_con( "out5_1", "out4_1", 1, 1 )
        conn += new_con( "out5_1", "inner2_1", 1, 1 )
        con_dict["inner3"] = conn

        return con_dict

    @staticmethod
    def gen_custom_start_pos(cls, net_params, initial_config, num_vehicles):
        start_pos = []
        start_lanes = []

        start_pos = [ ("out0_0", 0), ("out1_0", 0), ("out2_0", 0), ("out3_0", 0), ("out4_0", 0), ("out5_1", 0) ]
        start_lanes = [ 0,0,0,0,0,0 ]

        return start_pos, start_lanes











