import pandas as pd
import numpy as np

class Bootstrap:
    def __init__(self, db_name="GWIZD/main_db.json"):
        self.db_name = db_name

        self.dist_limit = 0.001
        self.augment_count = 100

    def load_db(self, fname = None) -> pd.DataFrame:
        if fname is None:
            fname = self.db_name
        return pd.read_json(fname)

    def augment_db(self, database) -> pd.DataFrame:
        rows = len(database)
        mu = self.dist_limit/2
        sigma = self.dist_limit
        augmentation_data = ( 
            np.random.normal(mu, sigma, size= (rows*self.augment_count, 2))
        )
        database = database.loc[database.index.repeat(self.augment_count)].copy()
        
        database[['longitude', 'latitude']] += augmentation_data
        print(database)
        return database

    def bootstrap(self):
        return self.augment_db(
                    self.load_db()
                    )
