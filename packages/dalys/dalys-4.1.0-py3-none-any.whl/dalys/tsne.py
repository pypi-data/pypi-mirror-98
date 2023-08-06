from sklearn.manifold import TSNE
from dalys.base_estimator import BaseEstimator


class TSNETool(BaseEstimator):
    def __init__(self, samples, labels, n_components=2, style=None, labels_unique_name=None, perplexity=30,
                 init='random', n_iter=1000, n_iter_without_progress=300,
                 early_exaggeration=12, verbose=0, preprocessing='std', scaled=False):
        super().__init__(samples, labels, n_components, style, labels_unique_name,
                         preprocessing, scaled)
        self._ca = TSNE(n_components=self._n_components, perplexity=perplexity,
                        init=init, n_iter=n_iter, n_iter_without_progress=n_iter_without_progress,
                        early_exaggeration=early_exaggeration, verbose=verbose)
        self._reduce = self._ca.fit_transform(self._scaled_data)
        self._fill_components()
        self._extract_classes()

    def set_params(self, n_components, perplexity=30, init='random',
                   n_iter=1000, n_iter_without_progress=300, early_exaggeration=12,
                   verbose=0, preprocessing='std', scaled=False):
        self.__init__(self._samples, self._labels, n_components=n_components, style=self._style,
                      labels_unique_name=self._labels_unique_name, perplexity=perplexity,
                      init=init, n_iter=n_iter, n_iter_without_progress=n_iter_without_progress,
                      early_exaggeration=early_exaggeration, verbose=verbose,
                      preprocessing=preprocessing, scaled=scaled)
