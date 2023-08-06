import pandas as pd
import sourcedefender
from mAdvisor.bi.master import MadvisorAutoMl
from mAdvisor.bi.preprocessing import preprocessing
import pandas as pd

class automl:
    """
    Parameters
    ----------

    target:
    Variable that needs to be predicted by AutoML. It can be a discrete for classification or it can be continuous for regression.

    train_data:
    Data set to be used for training AutoML models, must have a target column.
    Provide path to the train data or pass the data-frame itself.

    test_data:
    Data set for which model has to do the prediction, target variable should not be present.
    Provide path to the test data or pass the data-frame itself.

    label_level:
    Target variable sub-level to calculate model evaluation metrics, not required in case of regression. Sub-level with maximum number of occurance is selected by default value.

    app_type:
    Whether it is a "classification" or "regression" problem. AutoML automatically tags the app_type in case of no user input.

    prediction_algorithm:
    algorithm to be used for prediction. Best algorithm in selected by default.
    for "classification" use,
    'Random Forest', 'Logistic Regression', 'XGBoost', 'Naive Bayes', 'Neural Network (Sklearn)', 'Neural Network (TensorFlow)' or 'Neural Network (PyTorch)'

    for "regression" use,
    'Linear Regression', 'GBT Regression', 'DTREE Regression' or 'RF Regression'

    token:
    Licence key from marlabs

    """

    def __init__(self, target, train_data, test_data, token, label_level=None, app_type=None,
                 prediction_algorithm=None):
        self.label_level = label_level
        self.target = target
        self.app_type = app_type
        self.prediction_algorithm = prediction_algorithm
        self.test_data = test_data
        self.train_data = train_data
        self.token = token

    def fit(self):
        model = MadvisorAutoMl(target=self.target,
                               training_slug=None,
                               label_level=self.label_level,
                               app_type=self.app_type,
                               prediction_algorithm=self.prediction_algorithm,
                               train_data=self.train_data,
                               test_data=self.test_data,
                               token=self.token
                               )
        response = model.fit()
        print(pd.DataFrame(response['model result']['model_evaluation_results']))
        model_slug = response['model result']['model_slug']
        prediction_rules = response['score result']['prediction rules']
        predicted_data = pd.DataFrame(response['score result']['predicted data'])
        return model_slug, prediction_rules, predicted_data


class train:
    """
    Parameters
    ----------

    target:
    Variable that needs to be predicted by AutoML. It can be a discrete for classification or it can be continuous for regression.

    train_data:
    Data set to be used for training AutoML models, must have a target column.
    Provide path to the train data or pass the data-frame itself.

    label_level:
    Target variable sub-level to calculate model evaluation metrics, not required in case of regression. Sub-level with maximum number of occurance is selected by default value.

    app_type:
    Whether it is a "classification" or "regression" problem. AutoML automatically tags the app_type in case of no user input.

    token:
    Licence key from marlabs

    """

    def __init__(self, target, train_data, token, label_level=None, app_type=None):
        self.label_level = label_level
        self.target = target
        self.app_type = app_type
        self.train_data = train_data
        self.token = token

    def fit(self):
        model = MadvisorAutoMl(target=self.target,
                               training_slug=None,
                               label_level=self.label_level,
                               app_type=self.app_type,
                               prediction_algorithm=None,
                               train_data=self.train_data,
                               test_data=None,
                               token=self.token
                               )
        response = model.fit()
        print(pd.DataFrame(response['model result']['model_evaluation_results']))
        model_slug = response['model result']['model_slug']
        return model_slug

class score:
    """
    Parameters
    ----------

    test_data:
    Data set for which model has to do the prediction, target variable should not be present.
    Provide path to the test data or pass the data-frame itself.

    prediction_algorithm:
    algorithm to be used for prediction. Best algorithm in selected by default.
    for "classification" use,
    'Random Forest', 'Logistic Regression', 'XGBoost', 'Naive Bayes', 'Neural Network (Sklearn)', 'Neural Network (TensorFlow)' or 'Neural Network (PyTorch)'

    for "regression" use,
    'Linear Regression', 'GBT Regression', 'DTREE Regression' or 'RF Regression'

    training_slug:
    Training slug is the unique name given to the model while training. Provide training slug if running score alone.

    token:
    Licence key from marlabs

    """

    def __init__(self, test_data, training_slug, token, prediction_algorithm=None):
        self.prediction_algorithm = prediction_algorithm
        self.test_data = test_data
        self.training_slug = training_slug
        self.token = token

    def fit(self):
        model = MadvisorAutoMl(training_slug=self.training_slug,
                               prediction_algorithm=self.prediction_algorithm,
                               test_data=self.test_data,
                               token=self.token
                               )
        response = model.fit()
        prediction_rules = response['score result']['prediction rules']
        predicted_data = pd.DataFrame(response['score result']['predicted data'])
        return prediction_rules, predicted_data


class AutoFE:
    """
    Parameters
    ----------
    target:
    Variable that needs to be predicted by AutoML. It can be a discrete for classification or it can be continuous for regression.

    train_df:
    train dataframe to be used.

    app_type:
    Whether it is a "classification" or "regression" problem. AutoML automatically tags the app_type in case of no user input.

    token:
    Licence key from marlabs

    """
    def __init__(self, target, train_df, token, app_type=None):
        self.target = target
        self.app_type = app_type
        self.df = train_df
        self.token = token

    def fit(self):
        model = preprocessing(df=self.df,
                                    target= self.target,
                                    token=self.token,
                                    app_type= self.app_type)

        linear_df, tree_df, slug_string = model.auto_feature_engineering()
        return linear_df, tree_df, slug_string

class AutoFE_Test:
    """
    Parameters
    ----------
    test_df:
    test dataframe to be used.

    fe-slug:
        Unique slug value received from train data feature engineering

    token:
    Licence key from marlabs

    """
    def __init__(self,test_df,fe_slug, token):
        self.df = test_df
        self.fe_slug = fe_slug
        self.token = token

    def fit(self):
        model = preprocessing(df=self.df,
                                    fe_slug= self.fe_slug,
                                    token=self.token)

        linear_df, tree_df = model.auto_feature_engineering_test()
        return linear_df, tree_df
