import numbers
import numpy as np
import pandas as pd
import random
from collections import Counter
from mlxtend.frequent_patterns import fpgrowth
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.multiclass import check_classification_targets
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

from imodels.rule_list.bayesian_rule_list.brl_util import *
from imodels.rule_list.rule_list import RuleList
from imodels.util.discretization.mdlp import MDLP_Discretizer, BRLDiscretizer
from imodels.util.extract import extract_fpgrowth


class BayesianRuleListClassifier(BaseEstimator, RuleList, ClassifierMixin):
    """
    This is a scikit-learn compatible wrapper for the Bayesian Rule List
    classifier developed by Benjamin Letham. It produces a highly
    interpretable model (a list of decision rules) by sampling many different
    rule lists, trying to optimize for compactness and predictive performance.

    Parameters
    ----------
    listlengthprior : int, optional (default=3)
        Prior hyperparameter for expected list length (excluding null rule)

    listwidthprior : int, optional (default=1)
        Prior hyperparameter for expected list width (excluding null rule)
        
    maxcardinality : int, optional (default=2)
        Maximum cardinality of an itemset
        
    minsupport : float, optional (default=0.1)
        Minimum support (fraction between 0 and 1) of an itemset

    alpha : array_like, shape = [n_classes]
        prior hyperparameter for multinomial pseudocounts

    n_chains : int, optional (default=3)
        Number of MCMC chains for inference

    max_iter : int, optional (default=50000)
        Maximum number of iterations
        
    class1label: str, optional (default="class 1")
        Label or description of what the positive class (with y=1) means
        
    verbose: bool, optional (default=True)
        Verbose output
        
    random_state: int
        Random seed
    """

    def __init__(self, listlengthprior=3, listwidthprior=1, maxcardinality=2, minsupport=0.1, alpha=np.array([1., 1.]),
                 n_chains=3, max_iter=50000, class1label="class 1", verbose=False, random_state=42):
        self.listlengthprior = listlengthprior
        self.listwidthprior = listwidthprior
        self.maxcardinality = maxcardinality
        self.minsupport = minsupport
        self.alpha = alpha
        self.n_chains = n_chains
        self.max_iter = max_iter
        self.class1label = class1label
        self.verbose = verbose
        self._zmin = 1

        self.thinning = 1  # The thinning rate
        self.burnin = self.max_iter // 2  # the number of samples to drop as burn-in in-simulation

        self.discretizer = None
        self.d_star = None
        self.random_state = random_state
        self.seed()

    def seed(self):
        if self.random_state is not None:
            random.seed(self.random_state)
            np.random.seed(self.random_state)

    def _setlabels(self, X, feature_labels=[]):
        if len(feature_labels) == 0:
            if type(X) == pd.DataFrame and ('object' in str(X.columns.dtype) or 'str' in str(X.columns.dtype)):
                feature_labels = X.columns
            else:
                feature_labels = ["ft" + str(i + 1) for i in range(len(X[0]))]
        self.feature_labels = feature_labels

    def fit(self, X, y, feature_labels: list = None, undiscretized_features=[], verbose=False):
        """Fit rule lists to data

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            Training data 

        y : array_like, shape = [n_samples]
            Labels
            
        feature_labels : array_like, shape = [n_features], optional (default: [])
            String labels for each feature.
            If empty and X is a DataFrame, column labels are used.
            If empty and X is not a DataFrame, then features are simply enumerated
            
        undiscretized_features : array_like, shape = [n_features], optional (default: [])
            String labels for each feature which is NOT to be discretized. If empty, all numeric features are discretized
            
        verbose : bool
            Currently doesn't do anything

        Returns
        -------
        self : returns an instance of self.
        """
        self.seed()

        if len(set(y)) != 2:
            raise Exception("Only binary classification is supported at this time!")

        X, y = check_X_y(X, y)
        check_classification_targets(y)
        self.n_features_in_ = X.shape[1]

        itemsets, self.discretizer = extract_fpgrowth(X, y,
                                                      feature_labels=feature_labels,
                                                      minsupport=self.minsupport,
                                                      maxcardinality=self.maxcardinality,
                                                      undiscretized_features=undiscretized_features,
                                                      verbose=verbose)

        self.feature_labels = self.discretizer.feature_labels
        X_df_onehot = self.discretizer.onehot_df

        # Now form the data-vs.-lhs set
        # X[j] is the set of data points that contain itemset j (that is, satisfy rule j)
        for c in X_df_onehot.columns:
            X_df_onehot[c] = [c if x == 1 else '' for x in list(X_df_onehot[c])]
        X = [{}] * (len(itemsets) + 1)
        X[0] = set(range(len(X_df_onehot)))  # the default rule satisfies all data
        for (j, lhs) in enumerate(itemsets):
            X[j + 1] = set([i for (i, xi) in enumerate(X_df_onehot.values) if set(lhs).issubset(xi)])

        # now form lhs_len
        lhs_len = [0]
        for lhs in itemsets:
            lhs_len.append(len(lhs))
        nruleslen = Counter(lhs_len)
        lhs_len = array(lhs_len)
        itemsets_all = ['null']
        itemsets_all.extend(itemsets)

        Xtrain, Ytrain, nruleslen, lhs_len, self.itemsets = (
            X, np.vstack((1 - np.array(y), y)).T.astype(int), nruleslen, lhs_len, itemsets_all
        )

        permsdic = defaultdict(default_permsdic)  # We will store here the MCMC results
        # Do MCMC
        res, Rhat = run_bdl_multichain_serial(self.max_iter, self.thinning, self.alpha, self.listlengthprior,
                                              self.listwidthprior, Xtrain, Ytrain, nruleslen, lhs_len,
                                              self.maxcardinality, permsdic, self.burnin, self.n_chains,
                                              [None] * self.n_chains, verbose=self.verbose, seed=self.random_state)

        # Merge the chains
        permsdic = merge_chains(res)

        ###The point estimate, BRL-point
        self.d_star = get_point_estimate(permsdic, lhs_len, Xtrain, Ytrain, self.alpha, nruleslen, self.maxcardinality,
                                         self.listlengthprior, self.listwidthprior,
                                         verbose=self.verbose)  # get the point estimate

        if self.d_star:
            # Compute the rule consequent
            self.theta, self.ci_theta = get_rule_rhs(Xtrain, Ytrain, self.d_star, self.alpha, True)

        self.complexity_ = self._get_complexity()

        return self

    def _get_complexity(self):
        final_itemsets = np.array(self.itemsets, dtype=object)[self.d_star]
        complexity = 0
        for itemset in final_itemsets:
            complexity += 1
            if len(itemset) > 1 and type(itemset) != str:
                complexity += 0.5 * (len(itemset) - 1)
        return complexity

    def __str__(self, decimals=1):
        if self.d_star:
            detect = ""
            if self.class1label != "class 1":
                detect = "for detecting " + self.class1label
            header = "Trained RuleListClassifier " + detect + "\n"
            separator = "".join(["="] * len(header)) + "\n"
            s = ""
            for i, j in enumerate(self.d_star):
                if self.itemsets[j] != 'null':
                    condition = "ELSE IF " + (
                        " AND ".join([str(self.itemsets[j][k]) for k in range(len(self.itemsets[j]))])) + " THEN"
                else:
                    condition = "ELSE"
                s += condition + " probability of " + self.class1label + ": " + str(
                    np.round(self.theta[i] * 100, decimals)) + "% (" + str(
                    np.round(self.ci_theta[i][0] * 100, decimals)) + "%-" + str(
                    np.round(self.ci_theta[i][1] * 100, decimals)) + "%)\n"
            return header + separator + s[5:] + separator[1:]
        else:
            return "(Untrained RuleListClassifier)"

    def _to_itemset_indices(self, data):
        X_colname_removed = data.copy()
        for i in range(len(data)):
            X_colname_removed[i] = list(map(lambda s: s.split(' : ')[1], X_colname_removed[i]))
        X_df_categorical = pd.DataFrame(X_colname_removed, columns=self.feature_labels)
        X_df_onehot = pd.get_dummies(X_df_categorical)

        # X[j] is the set of data points that contain itemset j (that is, satisfy rule j)
        for c in X_df_onehot.columns:
            X_df_onehot[c] = [c if x == 1 else '' for x in list(X_df_onehot[c])]
        X = [set() for j in range(len(self.itemsets))]
        X[0] = set(range(len(data)))  # the default rule satisfies all data
        for (j, lhs) in enumerate(self.itemsets):
            if j > 0:
                X[j] = set([i for (i, xi) in enumerate(X_df_onehot.values) if set(lhs).issubset(xi)])
        return X

    def predict_proba(self, X):
        """Compute probabilities of possible outcomes for samples in X.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]

        Returns
        -------
        T : array-like, shape = [n_samples, n_classes]
            Returns the probability of the sample for each class in
            the model. The columns correspond to the classes in sorted
            order, as they appear in the attribute `classes_`.
        """
        if self.discretizer:
            D = self.discretizer.apply_discretization(X)
        else:
            D = X

        # deal with pandas data
        if type(D) in [pd.DataFrame, pd.Series]:
            D = D.values

        N = len(D)
        X2 = self._to_itemset_indices(D[:])
        P = preds_d_t(X2, np.zeros((N, 1), dtype=int), self.d_star, self.theta)
        return np.vstack((1 - P, P)).T

    def predict(self, X, threshold=0.1):
        """Perform classification on samples in X.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]

        Returns
        -------
        y_pred : array, shape = [n_samples]
            Class labels for samples in X.
        """
        # deal with pandas data
        if type(X) in [pd.DataFrame, pd.Series]:
            X = X.values
        # print('predicting!')
        # print('preds_proba', self.predict_proba(X)[:, 1])
        return 1 * (self.predict_proba(X)[:, 1] >= threshold)
