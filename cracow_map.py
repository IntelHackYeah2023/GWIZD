import json
import io
from pathlib import Path
import random
random.seed(39)

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

def add_polygon(latitude, longitude, face_id, type):
    # The latitude difference required to cover a distance of 1 kilometer is approximately 0.008993216059360853 degrees.
    random_range = 2 * 0.009
    # Define the coordinates of the polygon vertices

    polygon_coordinates = []
    polygon_coordinates.append([latitude - random.uniform(0, random_range),
                                longitude + random.uniform(0, random_range)])

    polygon_coordinates.append([latitude - random.uniform(0, random_range),
                                longitude - random.uniform(0, random_range)])

    polygon_coordinates.append([latitude + random.uniform(0, random_range),
                                longitude - random.uniform(0, random_range)])

    polygon_coordinates.append([latitude + random.uniform(0, random_range),
                                longitude + random.uniform(0, random_range)])

    def random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return "#{:02X}{:02X}{:02X}".format(r, g, b)

    # Function to generate a lighter version of a color
    def lighter_color(color, factor=0.5):
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        new_r = int(r + (255 - r) * factor)
        new_g = int(g + (255 - g) * factor)
        new_b = int(b + (255 - b) * factor)
        return "#{:02X}{:02X}{:02X}".format(new_r, new_g, new_b)

    # Generate a random color for the polygon
    random_polygon_color = random_color()

    # Generate a lighter version of the random color
    lighter_polygon_color = lighter_color(random_polygon_color, factor=0.7)

    popup_content = f"""
    <div style="width: 200px; height: 100px; background-color: #ffffff;">
        <h4>Znany zwierz: {type}</h4>
        <p>Identyfikator: {face_id}</p>
        <p>Kolorem zaznaczono jego obszar zerowania w ostatnich 48h</p>
    </div>
    """

    # Create a Polygon object and add it to the map
    polygon = folium.Polygon(
        locations=polygon_coordinates,
        color=random_polygon_color,  # Outline color of the polygon
        fill=True,  # Fill the polygon with color
        fill_color=lighter_polygon_color,  # Fill color of the polygon
        fill_opacity=0.6,  # Opacity of the fill color (0 to 1)
        popup=folium.Popup(popup_content)  # Popup text
    )

    return polygon

def add_icons(map):
    for location in load_animals_location():
        latitude = float(location["latitude"])
        longitude = float(location["longitude"])
        type = location["type"]
        face_id = location.get("faceId", None)
        info = location.get("info", None)
        is_confirmed = location.get("confirmed", None)

        img_path = f"{type}_confirmed.png" if is_confirmed else f"{type}.png"
        custom_icon = folium.CustomIcon(
            icon_image=img_path,  # Path to your custom marker image
            icon_size=(40, 40),  # Adjust the size as needed
            icon_anchor=(20, 40),  # Adjust the anchor point if necessary
        )

        group = get_feature_group(type)
        group.add_to(map)

        # Create a custom HTML string for the popup
        text = "Juz zgloszono" if is_confirmed else info
        popup_content = f"""
        <div style="width: 200px; height: 100px; background-color: #ffffff;">
            <h4>Informacja o: {type}</h4>
            <p>{text}</p>
        </div>
        """

        group.add_child(folium.Marker(
            location=[latitude, longitude],  # Location of the marker
            icon=custom_icon,  # Custom icon
            popup=folium.Popup(popup_content)))

        if face_id is not None:
            group.add_child(add_polygon(latitude, longitude, face_id, type))

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
