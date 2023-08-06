import umap
from dalys.base_estimator import BaseEstimator


class UMAPTool(BaseEstimator):
    def __init__(self, samples, labels, n_components=2, style=None, labels_unique_name=None,
                 n_neighbors=15, min_dist=0.1, metric='euclidean', preprocessing='std', scaled=False):
        super().__init__(samples, labels, n_components, style, labels_unique_name, preprocessing, scaled)
        self._ca = umap.UMAP(n_components=self._n_components, n_neighbors=n_neighbors, min_dist=min_dist,
                             metric=metric)
        self._reduce = self._ca.fit_transform(self._scaled_data)
        self._fill_components()
        self._extract_classes()

    def set_params(self, n_components, n_neighbors=15, min_dist=0.1, metric='euclidean', scaled=False):
        self.__init__(self._samples, self._labels, n_components=n_components, style=self._style,
                      labels_unique_name=self._labels_unique_name, n_neighbors=n_neighbors, min_dist=min_dist,
                      metric=metric, scaled=scaled)

    def transform(self, x):
        return self._ca.transform(x)
