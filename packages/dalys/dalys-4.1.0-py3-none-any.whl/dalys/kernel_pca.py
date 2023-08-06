from sklearn.decomposition import KernelPCA
from dalys.base_estimator import BaseEstimator


class KPCATool(BaseEstimator):
    def __init__(self, samples, labels, n_components=2, style=None, labels_unique_name=None, kernel='rbf',
                 fit_inverse_transform=True, gamma=1, preprocessing='std', scaled=False):
        super().__init__(samples, labels, n_components, style, labels_unique_name,
                         preprocessing, scaled)
        self._ca = KernelPCA(n_components=n_components, kernel=kernel, fit_inverse_transform=fit_inverse_transform,
                             gamma=gamma)
        self._reduce = self._ca.fit_transform(self._scaled_data)
        self._fill_components()
        self._extract_classes()

    def set_params(self, n_components, kernel='rbf', fit_inverse_transform=True,
                   gamma=1, preprocessing='std', scaled=False):
        self.__init__(self._samples, self._labels, n_components=n_components, style=self._style,
                      labels_unique_name=self._labels_unique_name, kernel=kernel,
                      fit_inverse_transform=fit_inverse_transform, gamma=gamma,
                      preprocessing=preprocessing, scaled=scaled)

    def inverse_transform(self, x):
        return self._ca.inverse_transform(x)
