import json
import io
import random
from PIL import Image
import folium
from typing import List, Dict, Optional
import argparse
from pathlib import Path

random.seed(39)

# Default value for the animal data file
DEFAULT_ANIMAL_DATA_FILE = "animals_locations.json"

# Default map center location is set to Cracow
CRACOW_LATITUDE = 50.049683
CRACOW_LONGITUDE = 19.944544

class AnimalMap:
    def __init__(self, map_location: Optional[Dict[str, float]] = None, animal_data_file: Optional[str] = None):
        self.coordinates = map_location
        self.groups = {}
        self.map = folium.Map(location=[self.coordinates["latitude"], self.coordinates["longitude"]],
                             zoom_start=self.coordinates["zoom_level"])
        self.animal_data = self.load_animal_locations(animal_data_file)

    def load_animal_locations(self, data_file: str) -> List[Dict[str, str]]:
        with open(data_file) as f:
            locations = json.load(f)
        return locations

    def get_feature_group(self, animal_type: str) -> folium.FeatureGroup:
        if animal_type in self.groups:
            return self.groups[animal_type]
        else:
            group = folium.FeatureGroup(name=f"{animal_type}")
            group.add_to(self.map)
            self.groups[animal_type] = group
            return group

    def add_polygon(self, latitude: float, longitude: float, face_id: str, animal_type: str) -> folium.Polygon:
        # Latitude/longitude difference is set to cover a distance of up to 4 square kilometers
        random_range = 2 * 0.009
        polygon_coordinates = []

        polygon_coordinates.append([latitude - random.uniform(0, random_range),
                                    longitude + random.uniform(0, random_range)])

        polygon_coordinates.append([latitude - random.uniform(0, random_range),
                                    longitude - random.uniform(0, random_range)])

        polygon_coordinates.append([latitude + random.uniform(0, random_range),
                                    longitude - random.uniform(0, random_range)])

        polygon_coordinates.append([latitude + random.uniform(0, random_range),
                                    longitude + random.uniform(0, random_range)])

        def random_color() -> str:
            return "#{:02X}{:02X}{:02X}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        random_polygon_color = random_color()

        def lighter_color(color: str, factor: float = 0.5) -> str:
            r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
            new_r = int(r + (255 - r) * factor)
            new_g = int(g + (255 - g) * factor)
            new_b = int(b + (255 - b) * factor)
            return "#{:02X}{:02X}{:02X}".format(new_r, new_g, new_b)

        lighter_polygon_color = lighter_color(random_polygon_color, factor=0.7)

        popup_content = f"""
        <div style="width: 200px; height: 100px; background-color: #ffffff;">
            <h4>Know animal: {animal_type}</h4>
            <p>Identifier: {face_id}</p>
            <p>The available habitat for animals in the past 48 hours.</p>
        </div>
        """

        return folium.Polygon(
            locations=polygon_coordinates,
            color=random_polygon_color,
            fill=True,
            fill_color=lighter_polygon_color,
            fill_opacity=0.6,
            popup=folium.Popup(popup_content)
        )

    def add_icons(self) -> None:
        for location in self.animal_data:
            latitude = float(location["latitude"])
            longitude = float(location["longitude"])
            animal_type = location["type"]
            face_id = location.get("faceId", None)
            info = location.get("info", None)
            is_confirmed = location.get("confirmed", None)

            img_base_path = Path("./images")
            icon_name = f"{animal_type}_confirmed.png" if is_confirmed else f"{animal_type}.png"
            img_path = img_base_path / icon_name
            custom_icon = folium.CustomIcon(
                icon_image=str(img_path),
                icon_size=(40, 40),
                icon_anchor=(20, 40)
            )

            group = self.get_feature_group(animal_type)

            text = "Animal already reported" if is_confirmed else info
            popup_content = f"""
            <div style="width: 200px; height: 100px; background-color: #ffffff;">
                <h4>Information on: {animal_type}</h4>
                <p>{text}</p>
            </div>
            """

            group.add_child(folium.Marker(
                location=[latitude, longitude],
                icon=custom_icon,
                popup=folium.Popup(popup_content)
            ))

            if face_id is not None:
                group.add_child(self.add_polygon(latitude, longitude, face_id, animal_type))

    def add_control_panel(self) -> None:
        folium.LayerControl().add_to(self.map)

    def save_as_png(self, file_name: str) -> None:
        img_data = self.map._to_png(5)
        img = Image.open(io.BytesIO(img_data))
        img.save(file_name)

    def save_as_html(self, file_name: str) -> None:
        self.map.save(file_name)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate an animal map.")
    parser.add_argument(
        "--latitude", type=float, default=CRACOW_LATITUDE, help="Custom latitude for map location."
    )
    parser.add_argument(
        "--longitude", type=float, default=CRACOW_LONGITUDE, help="Custom longitude for map location."
    )
    parser.add_argument(
        "--zoom", type=int, default=13, help="Custom zoom level for map location."
    )
    parser.add_argument(
        "--data-file", type=str, default=DEFAULT_ANIMAL_DATA_FILE, help="Animal data file."
    )
    parser.add_argument(
        "--save-png", action="store_true", help="Save the map as a PNG image."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    custom_map_location = {
        "latitude": args.latitude,
        "longitude": args.longitude,
        "zoom_level": args.zoom
    }

    animal_map = AnimalMap(custom_map_location, args.data_file)
    animal_map.add_icons()
    animal_map.add_control_panel()
    animal_map.save_as_html("map.html")

    if args.save_png:
        animal_map.save_as_png("map.png")



if __name__ == "__main__":
    main()