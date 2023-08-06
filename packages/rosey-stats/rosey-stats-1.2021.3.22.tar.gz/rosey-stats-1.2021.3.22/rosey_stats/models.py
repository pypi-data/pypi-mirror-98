import warnings
import numpy as np
import pandas as pd
from rich import print
from tqdm import tqdm, trange
from sklearn.utils import resample
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.feature_selection import f_regression, f_classif
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, log_loss
from glmnet import ElasticNet


def vec_to_array(a: np.ndarray):
    return a.reshape((len(a), 1))


# noinspection PyPep8Naming
class Blooper(BaseEstimator, RegressorMixin):
    """
    Boostrap Lasso with Partial Ridge Regression
    https://arxiv.org/pdf/1706.02150v1.pd
    """
    def __init__(
            self,
            n_lams: int = 50,
            eps: float = 1e-3,
            draws: int = 100,
            cv: int = 10,
            domain: str = None,
            best_lam=None,
            ridge_penalty=None,
            fit_intercept=False,
            verbose=False
    ):
        """
        Boostrap Lasso with Partial Ridge Regression
        https://arxiv.org/pdf/1706.02150v1.pdf

        :param n_lams:
        :param eps: The ratio between the max lambda and the min lambda
        :param draws: Number of sample to draw form the posterior distribution
        :param cv:
        :param domain: {None, 'all', 'pos', 'neg'}
        :param best_lam:
        :param ridge_penalty: Only override if you know what you're doing
        :param fit_intercept:
        :param verbose:
        """
        self.n_lams = n_lams
        self.eps = eps
        self.draws = draws
        self.cv = cv
        self.domain = domain
        self.best_lam_ = best_lam
        self.ridge_penalty = ridge_penalty
        self.fit_intercept = fit_intercept
        self.verbose = verbose

        self.coef_trace_ = None
        self.intercept_trace_ = None
        self.coef_mle_ = None
        self.intercept_mle_ = None

        if domain not in {None, 'all', 'pos', 'neg'}:
            raise ValueError('`domain` must be one of the following None, "all", "pos", "neg"')

    def fit(self, X: np.ndarray, y: np.ndarray):
        # Do any preprocessing needed
        X, y = X.astype(float), y.astype(float)
        if self.ridge_penalty is None:
            self.ridge_penalty = 1 / len(X)

        # This is the paired BLPR algorithm
        self._fit_paired_blpr(X, y)

        return self

    def predict(self, X):
        return X @ self.coef_mle_ + self.intercept_mle_

    def _get_glmnet_limits_from_domain(self) -> dict:
        limits = {
            'upper_limits': np.inf,
            'lower_limits': -np.inf
        }
        if self.domain == 'pos':
            limits['lower_limits'] = 0
        if self.domain == 'neg':
            limits['upper_limits'] = 0

        return limits

    @staticmethod
    def _get_glmnet_lambda_path(lam):
        return np.array([lam * 0.98, lam])

    def _fit_paired_blpr(self, x, y):
        warnings.simplefilter('ignore')
        n, p = x.shape

        m_trace, b_trace = [], []
        progressor = trange(self.draws, desc='Bootstrap Iterations') if self.verbose else range(self.draws)
        for b in progressor:
            # 1. Create bootstrap samples of x -> x_boot & y -> y_boot
            x_boot, y_boot = resample(x, y, replace=True, random_state=b)

            # 2. Find the best λ
            if self.best_lam_ is None:
                best_lam_finder = ElasticNet(
                    alpha=1,
                    n_splits=self.cv,
                    n_lambda=self.n_lams,
                    min_lambda_ratio=self.eps,
                    fit_intercept=self.fit_intercept,
                    **self._get_glmnet_limits_from_domain()
                )
                best_lam_finder.fit(x, y)  # TODO (15-Mar-21) add weights later
                self.best_lam_ = best_lam_finder.lambda_best_[0]
                if self.verbose:
                    print(f'Optimal λ => {self.best_lam_:.3f}')

            boot_l1_model = ElasticNet(
                alpha=1,
                n_splits=self.cv,
                lambda_path=self._get_glmnet_lambda_path(self.best_lam_),
                fit_intercept=self.fit_intercept,
                **self._get_glmnet_limits_from_domain()
            )
            boot_l1_model.fit(x_boot, y_boot)
            m_boot_l1 = boot_l1_model.coef_

            partial_ridge_selector = np.ones(p)
            partial_ridge_selector[m_boot_l1.nonzero()] = 0

            # 4. Solve m_boot_blpr
            blpr = ElasticNet(
                alpha=0,
                n_splits=self.cv,
                lambda_path=self._get_glmnet_lambda_path(self.ridge_penalty / 2),
                fit_intercept=self.fit_intercept,
                **self._get_glmnet_limits_from_domain()
            )
            blpr.fit(
                x_boot, y_boot,
                relative_penalties=partial_ridge_selector
            )
            m_trace.append(blpr.coef_)
            b_trace.append(blpr.intercept_)
        m_trace = np.vstack(m_trace)
        b_trace = np.array(b_trace)
        self.coef_trace_ = m_trace.copy()
        self.intercept_trace_ = b_trace.copy()
        self.coef_mle_ = self.coef_trace_.mean(axis=0)
        self.intercept_mle_ = b_trace.mean(axis=0)
        warnings.simplefilter('default')


# noinspection PyPep8Naming
class BairSupervisedPCA(BaseEstimator, TransformerMixin):
    """
    Supervised Principal Components Analysis
    This is the one as described by 'Prediction by Supervised Principal Components' (Eric Bair, Trevor Hastie et al)
    https://stats.stackexchange.com/a/767/91928
    NOTE -> Use sklearn LinearRegression over statsmodels OLS because it is ~3x faster.
    Example below
    >>> from sklearn.datasets import load_boston, load_breast_cancer
    >>> require_dims = 3
    >>> data, target = load_boston(True)
    >>> bspca = BairSupervisedPCA(n_components=require_dims)
    >>> trans_a = bspca.fit_transform(data, target)
    >>> trans_b = bspca.transform(data)
    >>> trans_a.ndim
    2
    >>> trans_a.shape[1]
    3
    >>> np.isclose(trans_a, trans_b).all()
    True
    >>> data, target = load_breast_cancer(True)
    >>> lspca = BairSupervisedPCA(require_dims)
    >>> trans_a = lspca.fit_transform(data, target)
    >>> trans_b = lspca.transform(data)
    >>> trans_a.ndim
    2
    >>> trans_a.shape[1]
    3
    >>> np.isclose(trans_a, trans_b).all()
    True
    >>> print('Done')
    Done
    """

    def __init__(self, n_components=None, is_regression=True, cv=5,
                 threshold_samples=25, use_pvalues=False, verbose=False):
        self.pca = PCA(n_components=n_components, whiten=True)
        self.conditioner_model_ = LinearRegression() if is_regression else LogisticRegression()
        self.cv, self.n_thres = cv, threshold_samples
        self.n_components = n_components
        self.is_regression, self.use_pvalues = is_regression, use_pvalues
        self.cv_results, self.indices, self.best = 3 * [None]
        self.verbose = verbose

        if use_pvalues:
            warnings.warn('Using p-values could select spurious features as important!')

    def _check_is_fitted(self):
        if self.indices is None or self.best is None:
            raise NotFittedError

    def plot_learning_curve(self, show_graph=False):
        import matplotlib.pyplot as graph
        try:
            from rosey_graph import plot_learning_curve as plc
        except ImportError:
            raise ImportError('You need have rosey-graph installed to call this function')
        self._check_is_fitted()

        plc(self.cv_results['mean'], self.cv_results['std'], self.cv_results['theta'], n=self.cv)
        graph.ylabel('R2 Score' if self.is_regression else 'Log loss')
        graph.xlabel(r'$\theta$')
        if show_graph:
            graph.show()

    def _univariate_regression(self, x, y):
        def model(x_i):
            lm_i = LinearRegression() if self.is_regression else LogisticRegression()
            lm_i.fit(vec_to_array(x_i), y)
            return lm_i.coef_[0]

        iterator = range(x.shape[1])
        if self.verbose and tqdm:
            iterator = tqdm(iterator, desc='Computing Coefs')
        return np.array([model(x[:, i]) for i in iterator])

    def fit(self, X, y):
        # Step 1 -> Compute (univariate) standard regression coefficient for each feature
        if self.use_pvalues:
            _, thetas = f_regression(X, y) if self.is_regression else f_classif(X, y)
            grid_sweep = np.linspace(thetas.min(), 1, self.n_thres)
        else:
            # Compute the regression coef like it says in the paper
            if self.is_regression:
                y_centered = y - np.mean(y)
                thetas = self._univariate_regression(X, y_centered)
            else:
                thetas = self._univariate_regression(X, y)
            # noinspection PyTypeChecker
            grid_sweep = np.percentile(np.abs(thetas), np.linspace(0.01, 1, self.n_thres)[::-1] * 100)

        # Step 2 -> Form a reduced data matrix
        thetas = (thetas if self.use_pvalues else np.abs(thetas)).flatten()
        cv_results = []
        for thres in grid_sweep:
            select = np.squeeze(np.argwhere(thetas <= thres) if self.use_pvalues else np.argwhere(thetas >= thres))
            x_selected = X[:, select]
            try:
                comps = float('inf') if self.n_components is None else self.n_components
                u_selected = PCA(min(x_selected.shape[1], comps), whiten=True).fit_transform(x_selected)
            except (ValueError, IndexError):
                u_selected = x_selected

            kf, scores = KFold(n_splits=self.cv, shuffle=True), []
            for train_ind, val_ind in kf.split(u_selected):
                # Split
                x_train, x_val = u_selected[train_ind], u_selected[val_ind]
                y_train, y_val = y[train_ind], y[val_ind]

                # Fit
                if x_train.ndim == 1:
                    x_train, x_val = vec_to_array(x_train), vec_to_array(x_val)

                if self.is_regression:
                    lm = LinearRegression().fit(x_train, y_train)
                else:
                    lm = LogisticRegression().fit(x_train, y_train)

                # Score
                y_hat = lm.predict(x_val)
                score = mean_squared_error(y_val, y_hat) if self.is_regression else log_loss(y_val, y_hat)

                # Test
                scores.append(score)

            # Score threshold
            scores = np.array(scores)
            cv_results.append((scores.mean(), scores.std()))
            if self.verbose:
                print(f'Theta -> {thres}', cv_results[-1])

        # Get best results
        self.cv_results = pd.DataFrame(cv_results, columns=['mean', 'std'])
        self.cv_results['theta'] = grid_sweep
        self.cv_results = self.cv_results.tail(len(self.cv_results) - 1)

        self.best = self.cv_results.sort_values(by='mean', ascending=False if self.is_regression else True).head(1)
        if self.use_pvalues:
            best_select = np.argwhere(thetas <= self.best['theta'].values)
        else:
            best_select = np.argwhere(thetas >= self.best['theta'].values)
        self.indices = np.squeeze(best_select)

        X = vec_to_array(X[:, self.indices]) if X[:, self.indices].shape[1] == 1 else X[:, self.indices]
        self.pca.fit(X)
        self.conditioner_model_.fit(self.pca.transform(X), y)

        return self

    def transform(self, X, y=None, **fit_params):
        self._check_is_fitted()

        # Step 3 -> Reduce X and then perform PCA
        x_reduced = X[:, self.indices]
        self.n_components = min(x_reduced.shape[1], float('inf') if self.n_components is None else self.n_components)
        return self.pca.transform(x_reduced)

    def fit_transform(self, X, y=None, **fit_params):
        assert y is not None
        if X.ndim == 1:
            raise ValueError('X cannot be a vector')
        elif X.shape[1] == 1:
            raise ValueError('X must have more than 1 feature')

        self.fit(X, y)
        return self.transform(X)

    def precondition(self, X):
        """
        This returns the preconditioned target variable (It predicts y from the input data)
        :param X:
        :return:
        """
        return self.conditioner_model_.predict(self.pca.transform(X[:, self.indices]))


if __name__ == '__main__':
    import matplotlib.pyplot as graph
    from sklearn.linear_model import LassoCV
    from sklearn.datasets import load_boston
    from scipy import stats
    graph.style.use('fivethirtyeight')

    N, P = 300, 30
    m_true = np.zeros(P)
    m_true[:4] = [2, -2, 2, 3]

    noise = 3 * stats.norm().rvs(N)

    data = 3*stats.norm().rvs((N, P))
    target = data @ m_true + noise

    # OR!
    # data, target = load_boston(return_X_y=True)
    # N, P = data.shape
    print(data)

    lasso_cv = LassoCV(cv=10, positive=True).fit(data, target)
    print(f'best λ = {lasso_cv.alpha_}')

    print('=== SKLearn ===')
    print(f'R2 = {lasso_cv.score(data, target):.2%}')
    graph.plot(lasso_cv.coef_, alpha=0.6, label='SKLearn')

    print('=== GLM Net ===')
    warnings.simplefilter('ignore')
    glmnet = ElasticNet(
        alpha=1,  # 0 for ridge and 1 for lasso
        # lambda_path=np.array([lasso_cv.alpha_ * 0.98, lasso_cv.alpha_]),  # Comment if you want the model to search
        n_splits=10,
        lower_limits=0
    ).fit(data, target)
    warnings.simplefilter('default')
    print(f'R2 = {glmnet.score(data, target):.2%}')
    graph.plot(glmnet.coef_, alpha=0.6, label='GLM Net')

    print('=== Blooper ===')
    # blooper = Blooper(best_lam=lasso_cv.alpha_, draws=100).fit(data, target)
    blooper = Blooper(draws=100, domain='pos', verbose=True).fit(data, target)
    print(f'R2 = {blooper.score(data, target):.2%}')
    graph.plot(blooper.coef_mle_, alpha=0.6, label='BLPR')

    graph.plot(m_true, '*', color='black', label='True')

    graph.legend()
    graph.ylabel(r'$\beta$')
    graph.xlabel('Coefficient')
    graph.show()

    for b in trange(len(blooper.coef_trace_), desc='Plotting...'):
        graph.plot(blooper.coef_trace_[b, :], color='black', lw=1, alpha=0.05)
    graph.plot(m_true, '*', markersize=5, label='True')
    graph.axhline(0, color='k', linestyle='--', linewidth=1)
    graph.show()
