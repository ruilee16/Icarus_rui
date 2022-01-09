import rtree
from shapely.geometry import shape, Point
import geopandas as gpd

__all__ = ['_get_idx', '_get_idx_rtree']


def _get_idx(point: Point, idx_rtree: rtree.index.Index, idx_rtree_factory: dict) -> int:
    point_in_shapes = [n.id for n in idx_rtree.intersection((point.x, point.y, point.x, point.y), objects=True)]
    for i in point_in_shapes:
        if idx_rtree_factory[i]:
            if idx_rtree_factory[i].contains(point):
                return i


def _get_idx_rtree(shapefile: gpd.geodataframe):
    idx_rtree = rtree.index.Index()
    idx_rtree_factory = {}
    for index, feature in shapefile.iterrows():
        geometry = shape(feature['geometry'])
        idx_rtree.insert(index, geometry.bounds)
        idx_rtree_factory[index] = geometry
    return idx_rtree, idx_rtree_factory