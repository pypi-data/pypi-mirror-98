import json
import pprint
import time
import copy
import jsbeautifier
from pyproj import Transformer


class Rescale:
    def __init__(self, multiply_lon=None, multiply_lat=None, add_lon=None, add_lat=None, multiply_y=None, multiply_x=None, add_x=None, add_y=None):
        if (multiply_lon != None or multiply_lat != None or add_lon != None or add_lat != None):
            if (multiply_x != None or multiply_y != None or add_x != None or add_y != None):
                raise "unexpectedly specified both lan/lon and x/y"
        if (multiply_lon == None and multiply_lat == None and add_lon == None and add_lat == None):
            multiply_lon = multiply_x
            multiply_lat = multiply_y
            add_lon = add_x
            add_lat = add_y
        if multiply_lon == None:
            raise "unexpected None for multiply lon / x"
        if multiply_lat == None:
            raise "unexpected None for multiply lat / y"
        if add_lon == None:
            raise "unexpected None for add lon / x"
        if add_lat == None:
            raise "unexpected None for add lat / y"
        self.multiply_lon = multiply_lon
        self.multiply_lat = multiply_lat
        self.add_lon = add_lon
        self.add_lat = add_lat


class Point():
    def __init__(self, lat=None, lon=None, x=None, y=None):
        if (lat != None or lon != None) and (x != None or y != None):
            raise "unexpectedly specified both lan/lon and x/y"
        if lat == None and lon == None:
            lat = y
            lon = x
        if lat == None:
            raise "unexpected None for lat / y"
        if lon == None:
            raise "unexpected None for lon / x"
        self.lat = lat
        self.lon = lon
    
    def rescale(self, changer):
        self.lon = self.lon * changer.multiply_lon + changer.add_lon
        self.lat = self.lat * changer.multiply_lat + changer.add_lat

    def to_geojson(self, rescale=None):
        if rescale == None:
            rescale = Rescale(multiply_lon=1, multiply_lat=1, add_lon=0, add_lat=0)
        lon = self.lon * rescale.multiply_lon + rescale.add_lon
        lat = self.lat * rescale.multiply_lat + rescale.add_lat
        return [lon, lat]

class LinearRing:
    def __init__(self, coordinate_list):
        self.coordinate_list = coordinate_list
    
    def rescale(self, changer):
        for element in self.coordinate_list:
            element.rescale(changer)

    def to_geojson(self, rescale=None):
        returned = []
        for element in self.coordinate_list:
            returned.append(element.to_geojson(rescale))
        return returned

class Polygon:
    def __init__(self, outer_ring, inner_rings_list=[], properties={}):
        self.outer_ring = outer_ring
        self.inner_rings_list = inner_rings_list
        self.properties = properties
    
    def rescale(self, changer):
        self.outer_ring.rescale(changer)
        for element in self.inner_rings_list:
            element.rescale(changer)

    def to_geojson(self, rescale=None):
        coordinates = [self.outer_ring.to_geojson(rescale)]
        for inner in self.inner_rings_list:
            coordinates.append(inner.to_geojson(rescale))
        return {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": coordinates,
            },
            "properties": self.properties
        }

class Collection:
    def __init__(self, element_list):
        self.element_list = []
        self.merge_in_list(element_list)

    def features(self):
        return self.element_list
    
    def append(self, new_element):
        self.element_lista.append(new_element)

    def merge_in_list(self, new_elements_list):
        self.element_list += new_elements_list

    def rescale(self, changer):
        for element in self.element_list:
            element.rescale(changer)

    def to_geojson(self, rescale=None):
        features = []
        for element in self.element_list:
            features.append(element.to_geojson(rescale))
        return {
            "type": "FeatureCollection",
            "features": features,
            }

def pretty_geojson_string(geojson):
    return jsbeautifier.beautify(json.dumps(geojson))

def projection_code(meaning):
    meanings = {
        "wgs84": "EPSG:4326",
        "wgs 84": "EPSG:4326",
        "internal": "EPSG:4326", # everything internally is in WGS 84
        "geojson": "EPSG:4326",
        "openstreetmap": "EPSG:4326",
        "osm": "EPSG:4326",

        "winkel tripel": "EPSG:54042", # private QGIS code?

        "web mercator": "EPSG:3857",
        "aaaargh": "EPSG:3857",
    }
    return meanings[meaning.lower()]

"""
returns {'scale_lat': num, 'scale_lon': num} that when applied will
keep shape of a pattern when projected into new projection

useful when you treat geometry as a pattern, rather than as a shape of
something real 
"""
def get_recommended_scaling(lat, lon, projection_to, projection_from=None):
    if projection_from == None:
        projection_from = projection_code("internal")
    transformer = Transformer.from_crs(projection_from, projection_to)
    point = transformer.transform(lat, lon)
    right = transformer.transform(lat, lon + 0.1)
    up = transformer.transform(lat + 0.1, lon)
    lon_distance = right[0] - point[0]
    lat_distance = up[1] - point[1]

    lat_oversize = lat_distance / lon_distance

    return {'scale_lat': 1.0 / lat_oversize, 'scale_lon': 1.0 }

def main():
    outer = LinearRing([
            Point(x=0, y=0),
            Point(x=1, y=0),
            Point(x=1, y=1),
            Point(x=0, y=1),
            Point(x=0, y=0),
        ])
    polygon = Polygon(outer)
    collection = Collection([polygon])
    #rint(pretty_geojson_string(collection.to_geojson()))

    pattern = maze_under_construction_pattern(30, 30)
    lat = 50.05518
    lon = 19.92757
    base_scaling = 0.000001
    projection_scale = get_recommended_scaling(lat, lon, projection_code("web mercator"))
    scale_lat = projection_scale['scale_lat'] * base_scaling
    scale_lon = projection_scale['scale_lon'] * base_scaling
    pattern.rescale(Rescale(multiply_lat=scale_lat, multiply_lon=scale_lon, add_lon=lon, add_lat=lat))
    print(pretty_geojson_string(pattern.to_geojson()))

def maze_under_construction_pattern(repetition_x, repetition_y):
    """
                        v
                        2
    l1.l1.l1.l1.        .
                        v
         v              2
         1
         .        l2.l2.l2.l2
         v
         1






    """
    multiplier = 8
    central_point_x = multiplier/2 
    central_point_y = multiplier* 3/2 
    width = multiplier
    height = 1
    l1 = LinearRing([
            Point(x=central_point_x - width/2, y=central_point_y - height/2),
            Point(x=central_point_x + width/2, y=central_point_y - height/2),
            Point(x=central_point_x + width/2, y=central_point_y + height/2),
            Point(x=central_point_x - width/2, y=central_point_y + height/2),
            Point(x=central_point_x - width/2, y=central_point_y - height/2),
        ])
    central_point_x = multiplier/2 
    central_point_y = multiplier/2 
    width = 1
    height = multiplier
    v1 = LinearRing([
            Point(x=central_point_x - width/2, y=central_point_y - height/2),
            Point(x=central_point_x + width/2, y=central_point_y - height/2),
            Point(x=central_point_x + width/2, y=central_point_y + height/2),
            Point(x=central_point_x - width/2, y=central_point_y + height/2),
            Point(x=central_point_x - width/2, y=central_point_y - height/2),
        ])
    l2 = copy.deepcopy(l1)
    l2.rescale(Rescale(multiply_x=1, multiply_y=1, add_x=multiplier, add_y=-multiplier))
    v2 = copy.deepcopy(v1)
    v2.rescale(Rescale(multiply_x=1, multiply_y=1, add_x=multiplier, add_y=multiplier))
    l1 = Polygon(l1)
    l2 = Polygon(l2)
    v1 = Polygon(v1)
    v2 = Polygon(v2)
    features = [l1, l2, v1, v2]
    collection_group = Collection(features)
    returned = Collection([])
    for x in range(0, repetition_x):
        for y in range(0, repetition_y):
            x_move = (x - repetition_x/2) * multiplier * 2
            y_move = (y - repetition_y/2) * multiplier * 2
            added = copy.deepcopy(collection_group)
            added.rescale(Rescale(multiply_x=1, multiply_y=1, add_x=x_move, add_y=y_move))
            returned.merge_in_list(added.features())
    return returned

if __name__ == "__main__":
    main()
