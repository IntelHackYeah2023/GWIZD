import pandas as pd
import numpy as np

class Bootstrap:
    def __init__(self, db_name="GWIZD/main_db.json"):
        self.db_name = db_name

        self.dist_limit_x = 0.005
        self.dist_limit_y = 0.0005
        self.augment_count = 500

    def load_db(self, fname = None) -> pd.DataFrame:
        if fname is None:
            fname = self.db_name
        return pd.read_json(fname)

    def augment_db(self, database) -> pd.DataFrame:
        rows = len(database)
        mux, muy = self.dist_limit_x/2, self.dist_limit_y/2
        sigmax, sigmay = self.dist_limit_x, self.dist_limit_y
        augmentation_data_x = ( 
            np.random.normal(mux, sigmax, size= (rows*self.augment_count))
        )
        augmentation_data_y = ( 
            np.random.normal(muy, sigmay, size= (rows*self.augment_count))
        )
        database = database.loc[database.index.repeat(self.augment_count)].copy()
        
        database['longitude'] += augmentation_data_x
        database['latitude'] += augmentation_data_y
        print(database)
        return database

    def bootstrap(self):
        return self.augment_db(
                    self.load_db()
                    )
