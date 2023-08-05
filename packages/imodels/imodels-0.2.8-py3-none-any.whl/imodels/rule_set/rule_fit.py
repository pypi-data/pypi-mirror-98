"""Linear model of tree-based decision rules based on the rulefit algorithm from Friedman and Popescu.

The algorithm can be used for predicting an output vector y given an input matrix X. In the first step a tree ensemble
is generated with gradient boosting. The trees are then used to form rules, where the paths to each node in each tree
form one rule. A rule is a binary decision if an observation is in a given node, which is dependent on the input features
that were used in the splits. The ensemble of rules together with the original input features are then being input in a
L1-regularized linear model, also called Lasso, which estimates the effects of each rule on the output target but at the
same time estimating many of those effects to zero.
"""
import numpy as np
import pandas as pd
from scipy.special import softmax
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.base import TransformerMixin
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.utils.multiclass import check_classification_targets
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from typing import List, Tuple

from imodels.rule_set.rule_set import RuleSet
from imodels.util.convert import tree_to_rules
from imodels.util.extract import extract_rulefit
from imodels.util.rule import get_feature_dict, replace_feature_name, Rule
from imodels.util.score import score_lasso
from imodels.util.transforms import Winsorizer, FriedScale


class RuleFit(BaseEstimator, TransformerMixin, RuleSet):
    """Rulefit class. Rather than using this class directly, should use RuleFitRegressor or RuleFitClassifier


    Parameters
    ----------
    tree_size:      Number of terminal nodes in generated trees. If exp_rand_tree_size=True, 
                    this will be the mean number of terminal nodes.
    sample_fract:   fraction of randomly chosen training observations used to produce each tree. 
                    FP 2004 (Sec. 2)
    max_rules:      total number of terms included in the final model (both linear and rules)
                    approximate total number of candidate rules generated for fitting also is based on this
                    Note that actual number of candidate rules will usually be lower than this due to duplicates.
    memory_par:     scale multiplier (shrinkage factor) applied to each new tree when 
                    sequentially induced. FP 2004 (Sec. 2)
    lin_standardise: If True, the linear terms will be standardised as per Friedman Sec 3.2
                    by multiplying the winsorised variable by 0.4/stdev.
    lin_trim_quantile: If lin_standardise is True, this quantile will be used to trim linear 
                    terms before standardisation.
    exp_rand_tree_size: If True, each boosted tree will have a different maximum number of 
                    terminal nodes based on an exponential distribution about tree_size. 
                    (Friedman Sec 3.3)
    include_linear: Include linear terms as opposed to only rules
    random_state:   Integer to initialise random objects and provide repeatability.
    tree_generator: Optional: this object will be used as provided to generate the rules. 
                    This will override almost all the other properties above. 
                    Must be GradientBoostingRegressor or GradientBoostingClassifier, optional (default=None)

    Attributes
    ----------
    rule_ensemble: RuleEnsemble
        The rule ensemble

    feature_names: list of strings, optional (default=None)
        The names of the features (columns)

    """

    def __init__(self,
                 tree_size=4,
                 sample_fract='default',
                 max_rules=2000,
                 memory_par=0.01,
                 tree_generator=None,
                 lin_trim_quantile=0.025,
                 lin_standardise=True,
                 exp_rand_tree_size=True,
                 include_linear=True,
                 alphas=None,
                 cv=3,
                 random_state=None):
        self.tree_size = tree_size
        self.sample_fract = sample_fract
        self.max_rules = max_rules
        self.memory_par = memory_par
        self.tree_generator = tree_generator
        self.lin_trim_quantile = lin_trim_quantile
        self.lin_standardise = lin_standardise
        self.exp_rand_tree_size = exp_rand_tree_size
        self.include_linear = include_linear
        self.alphas = alphas
        self.cv = cv
        self.random_state = random_state

        self.winsorizer = Winsorizer(trim_quantile=self.lin_trim_quantile)
        self.friedscale = FriedScale(self.winsorizer)
        self.stddev = None
        self.mean = None

        self._init_prediction_task()  # decides between regressor and classifier

    def _init_prediction_task(self):
        """
        RuleFitRegressor and RuleFitClassifier override this method
        to alter the prediction task. When using this class directly,
        it is equivalent to RuleFitRegressor
        """
        self.prediction_task = 'regression'

    def fit(self, X, y=None, feature_names=None):
        """Fit and estimate linear combination of rule ensemble

        """
        X, y = check_X_y(X, y)
        self.n_features_in_ = X.shape[1]

        self.n_features_ = X.shape[1]
        self.feature_dict_ = get_feature_dict(X.shape[1], feature_names)
        self.feature_placeholders = list(self.feature_dict_.keys())
        self.feature_names = list(self.feature_dict_.values())

        extracted_rules = self._extract_rules(X, y)
        self.rules_without_feature_names_, self.coef, self.intercept = self._score_rules(X, y, extracted_rules)
        self.rules_ = [
            replace_feature_name(rule, self.feature_dict_) for rule in self.rules_without_feature_names_
        ]
        self.complexity_ = self._get_complexity()

        return self

    def predict_continuous_output(self, X):
        """Predict outcome of linear model for X
        """
        if type(X) == pd.DataFrame:
            X = X.values.astype(np.float32)

        y_pred = np.zeros(X.shape[0])
        y_pred += self.eval_weighted_rule_sum(X)

        if self.include_linear:
            if self.lin_standardise:
                X = self.friedscale.scale(X)
            y_pred += X @ self.coef[:X.shape[1]]
        return y_pred + self.intercept

    def predict(self, X):
        '''Predict. For regression returns continuous output.
        For classification, returns discrete output.
        '''
        if self.prediction_task == 'regression':
            return self.predict_continuous_output(X)
        else:
            return np.argmax(self.predict_proba(X), axis=1)

    def predict_proba(self, X):
        continuous_output = self.predict_continuous_output(X)
        logits = np.vstack((1 - continuous_output, continuous_output)).transpose()
        return softmax(logits, axis=1)

    def transform(self, X=None, rules=None):
        """Transform dataset.

        Parameters
        ----------
        X : array-like matrix, shape=(n_samples, n_features)
            Input data to be transformed. Use ``dtype=np.float32`` for maximum
            efficiency.

        Returns
        -------
        X_transformed: matrix, shape=(n_samples, n_out)
            Transformed data set
        """
        df = pd.DataFrame(X, columns=self.feature_placeholders)
        X_transformed = np.zeros([X.shape[0], 0])

        for r in rules:
            curr_rule_feature = np.zeros(X.shape[0])
            curr_rule_feature[list(df.query(r).index)] = 1
            curr_rule_feature = np.expand_dims(curr_rule_feature, axis=1)
            X_transformed = np.concatenate((X_transformed, curr_rule_feature), axis=1)

        return X_transformed

    def get_rules(self, exclude_zero_coef=False, subregion=None):
        """Return the estimated rules

        Parameters
        ----------
        exclude_zero_coef: If True (default), returns only the rules with an estimated
                           coefficient not equalt to  zero.

        subregion: If None (default) returns global importances (FP 2004 eq. 28/29), else returns importance over 
                           subregion of inputs (FP 2004 eq. 30/31/32).

        Returns
        -------
        rules: pandas.DataFrame with the rules. Column 'rule' describes the rule, 'coef' holds
               the coefficients and 'support' the support of the rule in the training
               data set (X)
        """
        n_features = len(self.coef) - len(self.rules_)
        rule_ensemble = list(self.rules_without_feature_names_)
        output_rules = []
        ## Add coefficients for linear effects
        for i in range(0, n_features):
            if self.lin_standardise:
                coef = self.coef[i] * self.friedscale.scale_multipliers[i]
            else:
                coef = self.coef[i]
            if subregion is None:
                importance = abs(coef) * self.stddev[i]
            else:
                subregion = np.array(subregion)
                importance = sum(abs(coef) * abs([x[i] for x in self.winsorizer.trim(subregion)] - self.mean[i])) / len(
                    subregion)
            output_rules += [(self.feature_names[i], 'linear', coef, 1, importance)]

        ## Add rules
        for i in range(0, len(self.rules_)):
            rule = rule_ensemble[i]
            coef = self.coef[i + n_features]

            if subregion is None:
                importance = abs(coef) * (rule.support * (1 - rule.support)) ** (1 / 2)
            else:
                rkx = self.transform(subregion, [rule])[:, -1]
                importance = sum(abs(coef) * abs(rkx - rule.support)) / len(subregion)

            output_rules += [(self.rules_[i].rule, 'rule', coef, rule.support, importance)]
        rules = pd.DataFrame(output_rules, columns=["rule", "type", "coef", "support", "importance"])
        if exclude_zero_coef:
            rules = rules.ix[rules.coef != 0]
        return rules

    def visualize(self):
        rules = self.get_rules()
        rules = rules[rules.coef != 0].sort_values("support", ascending=False)
        pd.set_option('display.max_colwidth', -1)
        return rules[['rule', 'coef']].round(3)

    def _extract_rules(self, X, y) -> List[Rule]:
        return extract_rulefit(X, y,
                               feature_names=self.feature_placeholders,
                               tree_size=self.tree_size,
                               max_rules=self.max_rules,
                               memory_par=self.memory_par,
                               tree_generator=self.tree_generator,
                               exp_rand_tree_size=self.exp_rand_tree_size,
                               random_state=self.random_state)

    def _score_rules(self, X, y, rules) -> Tuple[List[Rule], List[float], float]:
        X_concat = np.zeros([X.shape[0], 0])

        # standardise linear variables if requested (for regression model only)
        if self.include_linear:

            # standard deviation and mean of winsorized features
            self.winsorizer.train(X)
            winsorized_X = self.winsorizer.trim(X)
            self.stddev = np.std(winsorized_X, axis=0)
            self.mean = np.mean(winsorized_X, axis=0)

            if self.lin_standardise:
                self.friedscale.train(X)
                X_regn = self.friedscale.scale(X)
            else:
                X_regn = X.copy()
            X_concat = np.concatenate((X_concat, X_regn), axis=1)

        X_rules = self.transform(X, rules)
        if X_rules.shape[0] > 0:
            X_concat = np.concatenate((X_concat, X_rules), axis=1)

        return score_lasso(X_concat, y, rules, alphas=self.alphas, cv=self.cv,
                           prediction_task=self.prediction_task,
                           max_rules=self.max_rules, random_state=self.random_state)


class RuleFitRegressor(RuleFit, RegressorMixin):
    def _init_prediction_task(self):
        self.prediction_task = 'regression'


class RuleFitClassifier(RuleFit, ClassifierMixin):
    def _init_prediction_task(self):
        self.prediction_task = 'classification'
