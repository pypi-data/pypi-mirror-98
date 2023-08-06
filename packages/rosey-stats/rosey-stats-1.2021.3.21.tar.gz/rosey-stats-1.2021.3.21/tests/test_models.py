import numpy as np
from rosey_stats.models import BairSupervisedPCA


def test_bair_supervised_pca():
    from sklearn.datasets import load_boston, load_breast_cancer
    require_dims = 3
    data, target = load_boston(True)

    bspca = BairSupervisedPCA(n_components=require_dims)
    trans_a = bspca.fit_transform(data, target)
    trans_b = bspca.transform(data)

    assert trans_a.ndim == 2
    assert trans_a.shape[1] == 3
    assert np.isclose(trans_a, trans_b).all()

    data, target = load_breast_cancer(True)
    lspca = BairSupervisedPCA(require_dims)
    trans_a = lspca.fit_transform(data, target)
    trans_b = lspca.transform(data)

    assert trans_a.ndim == 2
    assert trans_a.shape[1] == 3
    assert np.isclose(trans_a, trans_b).all()
