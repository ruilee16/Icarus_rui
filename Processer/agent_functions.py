import agent_fuction_interface
import networkx as nx

class process_agent(agent_fuction_interface):

    def route(self, agent, nt_graph):
        temp_routes = []
        for _ in agent.trips:
            trip = agent.trips[_]
            if trip.mode in ['WALK', 'BIKE']:
                orig, dest = trip.act_start.apn.near_node, trip.act_end.apn.near_node
                try:
                    trip.routes = nx.shortest_path(nt_graph, orig, dest, weight='weight')
                    temp_routes.append({'agentid': agent.id, 'tripid': _, 'routes': trip.routes})
                except:
                    pass
                    # rip.length = 0
        return temp_routes


    def get_route_to_shp(self, agent, network):
        pass

    def get_exposure(self, agent, network_env):
        for trip_idx in agent.trips:
            dur = (agent.trips[trip_idx].abm_end - agent.trips[trip_idx].abm_start) / 60  # duration in minutes
            start_step = agent.trips[trip_idx].abm_start / 60 // 15 * 15

            if agent.trips[trip_idx].mode in ('walk', 'bike'):
                link_list = list(zip(agent.trips[trip_idx].routes[0:-1], agent.trips[trip_idx].routes[1:]))
                # steps = dur//15
                link_list = set([tuple(sorted(i)) for i in link_list])
                _temp_length = [network_env.links[i].length for i in link_list]
                try:
                    temperature = agent_class.Exposure()
                    temperature.daymet = statistics.mean([daymet[daymet_dict[i]][start_step] for i in link_list])
                    sum([a * b for a, b in zip(_temp_temperatue, _temp_length)]) / sum(
                        _temp_length)

                    try:
                        _temp_temperatue = [mrt_link[mrt_dict[i]].temp[start_step] for i in link_list]

                        temperature.mrt = sum([a * b for a, b in zip(_temp_temperatue, _temp_length)]) / sum(
                            _temp_length)
                        temperature.Cal_WBGT(0.2, 3.2)
                        temperature.duration = dur
                        agent.trips[trip_idx].exp = temperature
                    except:
                        temperature.mrt = temperature.daymet
                        temperature.duration = dur

                        temperature.Cal_WBGT(0.2, 3.2)
                        agent.trips[trip_idx].exp = temperature
                except:
                    agent.trips[trip_idx].exp = None