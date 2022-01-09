from abc import ABC, abstractmethod



class link:
    # the identifier of links will be the nodes tuple a link connected
    __slots__ = ['node_list', 'osm_id', 'geometry', 'length',
                 'daymet_list', 'mrt_list', 'tree_ratio']

    class link_1():
        __slots__ = ['node_list', 'osm_id', 'length', 'mrtid', 'daymetid']

        def __init__(self, nodes: tuple, length: float, osm_id: int, *mrtid = None : int)

        None: int, *daymetid = None: int):
        self.node_list = nodes
        self.length = length
        # self.length = geodesic((node[0].geometry.y, node[0].geometry.x), (node[1].geometry.y, node[1].geometry.x)).kilometers*1000
        self.osm_id = osm_id

    def to_dict(self):
        return {
            'length': self.length,
            'osm': self.osm_id,
            'geometry': self.geometry
        }