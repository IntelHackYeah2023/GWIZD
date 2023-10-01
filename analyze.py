import pandas as pd
class Analyze:
    def __init__(self, database):
        self.database = database
        self.analsysis_type_options = {
            "animals"   : self._analyze_animals,
            "costs"     : self._analyze_costs
        }
        self.animals = ["lasica", "dzik"]

    def _analyze_animals (self) -> pd.DataFrame:
        return self.database[self.database['type'].isin(self.animals)]
    def _analyze_costs (self) -> pd.DataFrame:
        return self.database[self.database['type'] == "szkoda"]

    def analyze(self, type) -> pd.DataFrame:
        return self.analsysis_type_options[type]()