import json
from pathlib import Path
import folium
from main import AnimalMap

# Sample test data
TEST_MAP_LOCATION = {
    "latitude": 51.049683,
    "longitude": 20.944544,
    "zoom_level": 12,
}

TEST_DATA_FILE = "test_animals_locations.json"

TEST_DATA = [
    {
        "latitude": 51.049683,
        "longitude": 20.944544,
        "type": "Boar",
        "info": "TestInfo",
        "confirmed": True,
    }
]

def setup_module(module):
    # Create a test data file
    with open(TEST_DATA_FILE, "w") as f:
        json.dump(TEST_DATA, f)

def test_create_animal_map():
    animal_map = AnimalMap(TEST_MAP_LOCATION, TEST_DATA_FILE)
    assert isinstance(animal_map, AnimalMap)

def test_load_animal_locations():
    animal_map = AnimalMap(TEST_MAP_LOCATION, TEST_DATA_FILE)
    locations = animal_map.load_animal_locations(TEST_DATA_FILE)
    assert isinstance(locations, list)
    assert len(locations) == 1
    assert locations[0]["type"] == "Boar"

def test_add_icons():
    animal_map = AnimalMap(TEST_MAP_LOCATION, TEST_DATA_FILE)
    animal_map.add_icons()
    assert isinstance(animal_map.map, folium.Map)

def test_save_as_html():
    animal_map = AnimalMap(TEST_MAP_LOCATION, TEST_DATA_FILE)
    animal_map.add_icons()
    animal_map.save_as_html("test_map.html")
    assert Path("test_map.html").is_file()
