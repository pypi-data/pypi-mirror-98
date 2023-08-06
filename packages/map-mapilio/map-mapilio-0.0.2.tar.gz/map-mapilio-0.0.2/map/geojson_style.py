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
    def get_geo_json(value: Dict) -> Dict:
        """
        Geo json Features format
        """
        geo_json = Dict(
            {
                "type": "Feature",
                "properties": {
                    "average_score": value['avg_score'],
                    "class_name": value['classname'],
                    "camera_model": None,
                    "captured_at": None,
                    "key": None,
                    "pano": None,
                    "sequence_key": None,
                    "user_key": None,
                    "username": None,
                    "quality_score": None
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        value['Lat_center'],
                        value['Lon_center']
                    ]
                }
            })
        return geo_json

    @staticmethod
    def export_geojson(points: Dict):
        """
        Export geo json format
        """
        with open(os.path.join('Exports', 'detected_points.json'), 'w') as f:
            json.dump(points, f)