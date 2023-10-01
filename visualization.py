import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import numpy as np
from scipy.signal import savgol_filter

class MapVisualization:
    def __init__(self,
                 map_file = "GWIZD/mapa_krak_topo.png", 
                 top_left = (0.0 ,0.0), 
                 bottom_right=(10.0, 10.0)):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.map_filename = map_file
        self.img_size = (1600, 2560)

    def _map_coordinates_to_img(self, coord) -> tuple:
        coord_x = coord[1]
        coord_y = coord[2]
        normalizedX=(coord_x-self.top_left[0])/(self.bottom_right[0]-self.top_left[0])* self.img_size[0]
        normalizedY=(coord_y-self.top_left[1])/(self.bottom_right[1]-self.top_left[1])* self.img_size[1]

        return (coord[0],
                (coord_x-self.top_left[0])/(self.bottom_right[0]-self.top_left[0])* self.img_size[0], 
                (coord_y-self.top_left[1])/(self.bottom_right[1]-self.top_left[1])* self.img_size[1])


    def _get_coordinates(self, data):
        color_dictionary = {"lasica" : [1.0, 0.0, 0.0], "dzik" : [1.0, 0.0, 0.0]}
        data["type"] = data["type"].apply(lambda x: color_dictionary[x])
        data["latitude"] = data["latitude"].apply(lambda x: (x-self.top_left[0])/(self.bottom_right[0]-self.top_left[0])* self.img_size[0])
        data["longitude"] = data["longitude"].apply(lambda y: (y-self.top_left[1])/(self.bottom_right[1]-self.top_left[1])* self.img_size[1])

        return data[["type", "latitude", "longitude"]].to_numpy()
    
    def _get_coordinates_heatmap(self, data):
        data["latitude"] = data["latitude"].apply(lambda x: (x-self.top_left[0])/(self.bottom_right[0]-self.top_left[0])* self.img_size[0])
        data["longitude"] = data["longitude"].apply(lambda y: (y-self.top_left[1])/(self.bottom_right[1]-self.top_left[1])* self.img_size[1])

        return data
    
    def _get_histogram2d(self, data, bins):
        calc = np.zeros(self.img_size)
        size_x = self.img_size[1]
        size_y = self.img_size[0]

        bin_x = bins[0]
        bin_y = bins[1]

        fill_x = int(size_x // bin_x)
        fill_y = int(size_y // bin_y)

        for idx, row in data.iterrows():
            longitude = row["longitude"]
            latitude = row["latitude"]
            sidx =int(latitude//fill_x)
            sidy =int(longitude//fill_y)
            calc[sidx:sidx+fill_x, sidy:sidy+fill_y] += 1
            print(f"X:{sidx} -> {sidx+fill_x}, Y: {sidy}+{sidy+fill_y}")
        calc_max = calc.max()
        c = np.zeros((calc.shape[0], calc.shape[1], 3))
        for idx, idy in np.ndindex(calc.shape):
            c[idx, idy, 0] =  calc[idx, idy]/calc_max
            if c[idx, idy, 0] > 0.5:
                c[idx, idy, 1] =  0.7
                c[idx, idy, 2] =  0.7
        
        c[:,:,0] = savgol_filter(c[:,:,0], 5, 2)
        return c

    def draw_map(self, data):
        coordinates= self._get_coordinates_heatmap(data)
        
        f, ax = plt.subplots()
        map = plt.imread(self.map_filename)

        h2d = self._get_histogram2d(data, (200, 320))
        ax.imshow(map, extent=[0, map.shape[1], 0, map.shape[0]],  origin='upper')
        ax.imshow(h2d,  extent=[0, map.shape[1], 0, map.shape[0]], origin='upper', alpha=0.5)
        plt.axis('off')
        plt.show()
        plt.waitforbuttonpress()