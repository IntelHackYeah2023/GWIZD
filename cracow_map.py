import json
import io
from pathlib import Path

import folium
from PIL import Image

coordinates = {
    "cracow":
        {
            "latitude": 50.049683,
            "longitude": 19.944544,
            "zoom_level": 13
        }
}

def load_animals_location():
    danimals_locations_path = Path("animals_locations.json")
    with open(danimals_locations_path) as f:
        locations = json.load(f)

    return locations

groups = {}

def get_feature_group(type):
    if type in groups:
        return groups[type]
    else:
        group = folium.FeatureGroup(name=f"{type}").add_to(map)
        groups[type] = group

        return group

def add_icons(map):
    for location in load_animals_location():
        latitude = float(location["latitude"])
        longitude = float(location["longitude"])
        type = location["type"]

        custom_icon = folium.CustomIcon(
            icon_image=f"{type}.png",  # Path to your custom marker image
            icon_size=(40, 40),  # Adjust the size as needed
            icon_anchor=(20, 40),  # Adjust the anchor point if necessary
        )

        group = get_feature_group(type)
        group.add_to(map)

        group.add_child(folium.Marker(
            location=[latitude, longitude],  # Location of the marker
            icon=custom_icon,  # Custom icon
            popup="Zadzwon do najblizszej placowki - 0700 xxx yyy"
            #tooltip="Custom Marker",  # Tooltip text (optional)
        ))

def save_as_png(map):
    img_data = map._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save('map.png')


map = folium.Map(location=[coordinates["cracow"]["latitude"],
                           coordinates["cracow"]["longitude"]],
                 zoom_start=coordinates["cracow"]["zoom_level"])

add_icons(map)

folium.LayerControl().add_to(map)

map.save("map.html")
