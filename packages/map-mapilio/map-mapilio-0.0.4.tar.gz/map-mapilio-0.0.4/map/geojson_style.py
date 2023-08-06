from addict import Dict
import os
import json


class Geojson:
    """
     Get geo json format
    """
    common_json = Dict({
        "type": "FeatureCollection",
        "features": []
    })

    @staticmethod
    def get_geo_json(**kwargs) -> Dict:
        """
        Geo json Features format
        value: Dict,
        area: float,
        height: float, width: float,
        type: str
        """
        params = Dict(kwargs)

        if params.type == "Point":
            geom_type = {
                "type": params.type,
                "coordinates": [
                    params.lon,
                    params.lat
                ]
            }
        if params.type == "Polygon":
            geom_type = {
                "type": params.type,
                "coordinates": params.segmentation
            }
        geom = "POINT({} {})".format(params.lon, params.lat)
        geo_json = Dict(
            {
                "type": "Feature",
                "properties": {
                    "average_score": params.score,
                    "class_name": params.classname,
                    "camera_model": None,
                    "captured_at": None,
                    "key": params.key if params.key else None,
                    "pano": None,
                    "area": params.area if params.area else None,
                    "height": params.height if params.height else None,
                    "width": params.width if params.width else None,
                    "geom": geom
                },
                "geometry": geom_type
            })
        return geo_json

    @staticmethod
    def convert_dict_to_geojson(params: Dict, type: str) -> json:
        for key, value in params.items():
            value = Dict(value)
            ff = Geojson.get_geo_json(lat=value.lat, lon=value.lon,
                                      classname=value.classname,
                                      area=value.area,
                                      score=value.average_score,
                                      key=key,
                                      type=type)
            Geojson.common_json.features.append(ff)

        return Geojson.common_json

    @staticmethod
    def export_geojson(points: Dict):
        """
        Export geo json format
        """
        with open(os.path.join('Exports', 'detected_points.json'), 'w') as f:
            json.dump(points, f)