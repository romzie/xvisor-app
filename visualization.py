import configparser
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np


class Visualizer():


    def __init__(self):

        config = configparser.ConfigParser()
        config.read('config.ini')

        self.delimiter = config['CSV_FILE']['delimiter']
        self.csv_path = config['CSV_FILE']['path']

        # Tags defined in 'config.ini' FIXME read config file
        self.tags = ['NO_DATA', 'CORRECT', 'VALUE_ERR', 'RTE', 'DEADLOCK']
        self.cmap = colors.ListedColormap(['#FFFFFF', '#00FF00', '#FF7800', '#FF0000', '#FFFF00'])

    def create_hitmap(self):

        csvfile = open(self.csv_path, 'r')
        csvr = csv.reader(csvfile, delimiter=self.delimiter)

        # Gathering data and regroup it with adresses
        data = {}
        for row in csvr:
            try:
                data[row[0]]
            except:
                data[row[0]] = {}
            data[row[0]][row[1]] = row[2]

        csvfile.close()
        adresses = [x for x in data.keys()]

        # Retreive cycles
        cycles = []
        for ad in adresses:
            for cy in data[ad].keys():
                if int(cy) not in cycles:
                    cycles.append(int(cy))
        cycles.sort()
        adresses.sort(key=lambda x: int(x[2:], 16))

        # Building a matrix containing the index of the tags
        # To assign the proper color to the cell
        heat = np.zeros((len(adresses), len(cycles)))
        for i_ad, ad in enumerate(adresses):
            for cy in data[ad]:
                i_cy = cycles.index(int(cy))
                for j, tag in enumerate(self.tags):
                    if data[ad][cy] == tag:
                        heat[i_ad][i_cy] = j
                        break

        # Build figure
        fig, ax = plt.subplots()

        # Plot heatmap
        heatmap = ax.pcolormesh(heat, cmap=self.cmap)
        nb_ticks = len(self.tags)
        ticks = np.linspace(0, nb_ticks-1, nb_ticks+1) + 0.5
        cbar = fig.colorbar(heatmap, ticks=ticks, orientation='horizontal')

        # Add carriage return every 2 tags for readability
        for i in range(len(self.tags)):
            if i % 2 == 1:
                self.tags[i] = "\n" + self.tags[i]
        cbar.ax.set_xticklabels(self.tags)

        # Center labels
        ax.set_xticks(np.arange(len(cycles)) + 0.5, minor=False)
        ax.set_yticks(np.arange(len(adresses)) + 0.5, minor=False)

        ax.set_xticklabels(cycles, minor=False)
        ax.set_yticklabels(adresses, minor=False)

        # Adding readability
        ax.grid(False)
        ax = plt.gca()
        ax.set_ylabel("Adresses mémoires", rotation=90)
        ax.set_xlabel("Cycles d'éxecution")

        # Remove grid ticks
        for t in ax.xaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False
        for t in ax.yaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False

        plt.savefig('heatmap.jpg')


if __name__ == '__main__':
    visualizer = Visualizer()
    visualizer.create_hitmap()