import json
import io

import folium
import io
from PIL import Image

coordinates = {
        "cracow":
            {
                "latitude": 50.049683,
                "longitude": 19.944544,
                "zoom_level": 14
            }
}


def load_dzik_location():
    with open("dziki.json") as f:
        data = json.load(f)

def add_icons(map):
    custom_icon = folium.CustomIcon(
        icon_image="dzik.png",  # Path to your custom marker image
        icon_size=(40, 40),  # Adjust the size as needed
        icon_anchor=(20, 40),  # Adjust the anchor point if necessary
    )

    folium.Marker(
        location=[coordinates["cracow"]["latitude"],
                  coordinates["cracow"]["longitude"]],  # Location of the marker
        icon=custom_icon,  # Custom icon
        tooltip="Custom Marker",  # Tooltip text (optional)
    ).add_to(map)

def save_as_png(map):
    img_data = map._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save('map1.png')

map = folium.Map(location=[coordinates["cracow"]["latitude"],
                           coordinates["cracow"]["longitude"]],
                 zoom_start=coordinates["cracow"]["zoom_level"])

add_icons(map)
map.save("map.html")


