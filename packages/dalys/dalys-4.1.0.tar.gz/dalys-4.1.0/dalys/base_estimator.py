import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import combinations_with_replacement
from dalys.utils.utils import marker_dict, colors, scalers
from abc import ABC, abstractmethod


class BaseEstimator(ABC):
    def __init__(self, samples, labels, n_components, style, labels_unique_name, preprocessing, scaled):
        self._markers = [key for key in marker_dict.keys()]
        self._samples = samples
        self._labels = labels
        self._unique_labels = np.unique(labels)
        self._labels_unique_name = labels_unique_name
        self._legend = labels_unique_name if labels_unique_name else self._unique_labels
        self._n_classes = len(self._unique_labels)
        self._preprocessing = preprocessing
        self._scaled = scaled
        self._n_components = n_components
        self._title = self.__class__.__name__
        self._style = style
        self._scaler = None
        self._ca = None
        self._scaled_data = None
        self._reduce = None
        self._get_scale_data()
        self._generate_styles()

    @abstractmethod
    def set_params(self, *args):
        pass

    def set_style(self, style):
        if len(style) != len(self._unique_labels):
            raise ValueError('inappropriate list size')
        self._style = style

    def get_reduce_data(self):
        return self._reduce

    def _generate_styles(self):
        if self._style:
            return
        self._style, previous = list(), list()
        while len(self._style) != self._n_classes:
            color = np.random.choice(colors)
            marker = np.random.choice(self._markers)
            if color not in previous:
                previous.append(color)
                self._style.append((color, marker))

    def _get_scale_data(self):
        self._scaler = next(item[1] for item in scalers if item[0] == self._preprocessing)
        self._scaled_data = self._scaler.fit_transform(
            [item.flatten() for item in self._samples]) if not self._scaled else self._samples

    def _fill_components(self):
        self._components_list = list([list() for i in range(self._n_components)])
        for i in range(len(self._scaled_data)):
            for j in range(self._n_components):
                self._components_list[j].append(self._reduce[i][j])

    def _extract_classes(self):
        self._class_list = list([[list() for i in range(self._n_components)]
                                 for j in range(self._n_classes)])
        for i in range(len(self._labels)):
            for j in range(self._n_components):
                self._class_list[self._labels[i]][j].append(self._components_list[j][i])

    def projections_plot(self, grid=None, fontsize=8):
        fig = plt.figure(0)
        if len(self._reduce[0]) > 1:
            perms = list(item for item in combinations_with_replacement(range(len(self._reduce[0])), 2)
                         if item[0] != item[1])
            for i in range(len(perms)):
                k, j = perms[i][0], perms[i][1]
                if grid:
                    fig.add_subplot(int(str(grid) + str(i + 1)))
                else:
                    fig = plt.figure(i)
                    fig.canvas.set_window_title(self._title + ' 2D plot')
                for m in range(self._n_classes):
                    item = self._class_list[m]
                    color, marker = self._style[m]
                    plt.scatter(item[k], item[j], c=color, marker=marker)
                plt.xlabel('component {0}'.format(k), fontsize=fontsize)
                plt.ylabel('component {0}'.format(j), fontsize=fontsize)
                if not grid:
                    plt.legend(self._legend)
            if grid:
                fig.canvas.set_window_title(self._title + ' 2D subplot')
            plt.show()
            return
        for m in range(self._n_classes):
            item = self._class_list[m]
            color, marker = self._style[m]
            plt.scatter(item[0], np.zeros(len(item[0])), c=color, marker=marker)
            plt.legend(self._legend)
        fig.canvas.set_window_title(self._title + ' 2D plot (1 dimensional data)')
        plt.xlabel('component 0')
        plt.ylabel('component 1')
        plt.show()

    def projections_plot_3d(self, components=(0, 1, 2)):
        if len(self._reduce[0]) < 3:
            raise ValueError('the number of components should be 3 or more')
        fig = plt.figure()
        fig.canvas.set_window_title(self._title + ' 3D plot')
        ax = fig.add_subplot(111, projection='3d')
        i, j, k = components
        for m in range(self._n_classes):
            item = self._class_list[m]
            color, marker = self._style[m]
            ax.scatter(item[i], item[j], item[k], c=color, marker=marker)
        ax.set_xlabel('component {0}'.format(i))
        ax.set_ylabel('component {0}'.format(j))
        ax.set_zlabel('component {0}'.format(k))
        ax.legend(self._legend)
        plt.show()
