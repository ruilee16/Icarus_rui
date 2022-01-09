from recycle import AGENT, NETWORK
import networkx
from typing import Protocol

# the agent processing functions.
class agent_function(Protocol):
    def route(self, agent: AGENT.agent, nt_graph: networkx.graph):
        """Use the networkx.graph to route the ActiveTrips and will update the agent.route attributes"""

    def get_route_to_shp(self, agent: AGENT.agent, nt: NETWORK.network):
        """Use the networkx.graph to route the ActiveTrips and will update the agent.exposure attributes"""

    def get_exposure(self, agent: AGENT.agent, network_env: dict):
        """Use the networkx.graph to route the ActiveTrips and will update the agent.exposure attributes"""

    def check_vulnerable(self, agent: AGENT.agent, network_env: dict):
        """Use the networkx.graph to route the ActiveTrips and will update the agent.exposure attributes"""
