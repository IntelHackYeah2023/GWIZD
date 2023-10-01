import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import numpy as np
from scipy.signal import savgol_filter

class MapVisualization:
    def __init__(self,
                 map_file = "GWIZD/os_map_krak_topo.png", 
                 top_left = (0.0 ,0.0), 
                 bottom_right=(10.0, 10.0),
                 cm=(1,0.7,0.7, 1.0)):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.map_filename = map_file
        self.img_size = (1600, 2560)
        self.cm=cm
        self.bins = (100,60)

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
        data["latitude"] = data["latitude"].apply(
            lambda x: ((x-self.top_left[0]))/((self.bottom_right[0]-self.top_left[0]))* self.img_size[1])
        data["longitude"] = data["longitude"].apply(
            lambda y: ((y-self.top_left[1]))/((self.bottom_right[1]-self.top_left[1]))* self.img_size[0])

        return data
    
    def _get_histogram2d(self, data):
        calc = np.zeros(self.img_size)
        size_x = self.img_size[1]
        size_y = self.img_size[0]

        bin_x = self.bins[0]
        bin_y = self.bins[1]

        fill_x = int(size_x // bin_x)
        fill_y = int(size_y // bin_y)

        for idx, row in data.iterrows():
            longitude = row["longitude"]
            latitude = row["latitude"]
            sidx =int(latitude//fill_x)*fill_x
            sidy =int(longitude//fill_y)*fill_y
            calc[sidx:sidx+fill_x, sidy:sidy+fill_y] += 1
            
        calc_max = calc.max()
        c = np.zeros((calc.shape[0], calc.shape[1], len(self.cm)))
        for idx, idy in np.ndindex(calc.shape):
            ratio = calc[idx, idy]/calc_max           
            if ratio > 0.5:
                c[idx, idy, :] = np.array(self.cm)*ratio
        
        c[:,:,0] = savgol_filter(c[:,:,0], 5, 2)
        return c

    def draw_map(self, data):
        map = plt.imread(self.map_filename)
        self.img_size = (map.shape[0], map.shape[1])

        coordinates = self._get_coordinates_heatmap(data)        
        f, ax = plt.subplots()
        h2d = self._get_histogram2d(coordinates)
        ax.imshow(map, extent=[0, map.shape[1], 0, map.shape[0]],  origin='upper')
        ax.imshow(h2d,  extent=[0, map.shape[1], 0, map.shape[0]], origin='upper', alpha=0.8)
        plt.axis('off')

        plt.show()
        plt.waitforbuttonpress()

    def draw_map_per_type(self, data):
        map = plt.imread(self.map_filename)
        self.img_size = (map.shape[0], map.shape[1])

        coordinates_dzik= self._get_coordinates_heatmap(data[data['type'] == 'dzik'])        
        coordinates_lasica= self._get_coordinates_heatmap(data[data['type'] == 'lasica'])        
       
        f, ax = plt.subplots()
        self.cm = (1.0,0.3,0.3,1.0)
        h2dzik = self._get_histogram2d(coordinates_dzik)

        self.cm = (0.3,0.3,1.0,1.0)
        h2lasica = self._get_histogram2d(coordinates_lasica)

        ax.imshow(map, extent=[0, map.shape[1], 0, map.shape[0]],  origin='upper')
        ax.imshow(h2dzik,  extent=[0, map.shape[1], 0, map.shape[0]], origin='upper', alpha=0.8)
        ax.imshow(h2lasica,  extent=[0, map.shape[1], 0, map.shape[0]], origin='upper', alpha=0.8)
        plt.axis('off')

        plt.show()
        plt.waitforbuttonpress()