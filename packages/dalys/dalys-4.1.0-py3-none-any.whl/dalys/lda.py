from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from dalys.base_estimator import BaseEstimator


class LDATool(BaseEstimator):
    def __init__(self, samples, labels, n_components=3, style=None, labels_unique_name=None, preprocessing='std',
                 scaled=False):
        super().__init__(samples, labels, n_components, style, labels_unique_name, preprocessing, scaled)
        self._ca = LinearDiscriminantAnalysis(n_components=self._n_components)
        self._reduce = self._ca.fit_transform(self._scaled_data, self._labels)
        self._fill_components()
        self._extract_classes()

    def set_params(self, n_components, preprocessing='std', scaled=False):
        self.__init__(self._samples, self._labels, n_components=n_components, style=self._style,
                      labels_unique_name=self._labels_unique_name, preprocessing=preprocessing, scaled=scaled)
