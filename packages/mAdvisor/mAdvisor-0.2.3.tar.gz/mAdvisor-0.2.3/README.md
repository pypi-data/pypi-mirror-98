<div align="center">
  <img src="https://www.marlabs.com/wp-content/uploads/2017/09/marlabs_logo.png">
</div>

mAdvisor AutoML by Marlabs
==============
[![Python](https://img.shields.io/pypi/pyversions/madvisor.svg?style=plastic)](https://badge.fury.io/py/madvisor)

mAdvisor AutoML is an automated AI/ML solution from Marlabs that translates data into meaningful insights & predictions without any manual intervention. AutoML gives you the power of cognitive technologies like machine learning, machine reasoning, deep learning, natural language generation, natural language processing and expert rules systems with your limited knowledge of AI/ML, thereby enabling enterprises to identify revenue streams, enhance customer experience and productivity. This solution is designed for application and machine experts, so that machine learning models can be created with no help from a data scientist.  A 30-day trial license for mAdvisor AutoML® is issued on activation.

The solution includes the following features:
1. Ability to comprehend and monetize Big Data
2. Rapid time to insights
3. No dependency on data scientists & analysts to create briefs
4. Rapid development of predictive apps
5. Expandable and Scalable to the adoption of new use cases

--------------



Installation
--------------
### pip
```sh
$ pip install mAdvisor
```

Usage
--------------
  * A Licence Key is required to use this package
  * Register yourself to activate the 30 days free trial
  * Connect with Marlabs mAdvisor team to purchase a paid licence.

## User Registration and Plan Subscription

###  Sign Up
```sh
import requests
base_url = 'https://madvisor-dbc.marlabsai.com/automl'
url = base_url + '/account/sign-up'
data= {'email': '<email id>',
 'username':'<user name>',
 'password':'<password>'
}
response = requests.post(url, data=data)
if response.status_code != 200:
    print('Failed response code {}'.format(response.status_code))
print('Output result: {}'.format(response.json()))
```
###  Subscribe to the 30 days trial plan
```sh
url = base_url+'/subscription/subscribe-plan'
data= {'username':'<user name>',
 'password':'<password>',
 'subscription_type': 'TRIAL',
 'plan': 'FREE'
 }

response = requests.post(url, data=data)
if response.status_code != 200:
    print('Failed response code {}'.format(response.status_code))
print('Output result: {}'.format(response.json()))
```

###  Check Your Active Subscriptions
```sh
url = base_url+'/subscription/active-plans'
data= {'username':'<user name>',
 'password':'<password>'
 }

response = requests.post(url, data=data)
if response.status_code != 200:
    print('Failed response code {}'.format(response.status_code))
print('Output result: {}'.format(response.json()))
```

## Start Using the Library

### AutoML model training
This calss is used to initiate AutoML training job, user has to use the slug value returned from here while doing prediction.
```sh
from mAdvisor import train
model = train(train_data="<train dataset pass either path to the file or dataframe>",
               target="<Target Variable Name>",
               token = "<Licence Key>")
model_slug = model.fit()
```

### AutoML prediction
Train data prediction can be using this class
```sh
from mAdvisor import score
model = score(test_data="<test dataset pass either path to the file or dataframe>",
               training_slug="<model slug value received from train output>",
               token = "<Licence Key>")
prediction_rules, predicted_data = model.fit()
```
### AutoML model Training and Prediction in a single go
Used to initiate automl job, both model training and scoring can be done using this class.
```sh
from mAdvisor import automl
model = automl(train_data="<train dataset pass either path to the file or dataframe>",
               test_data="<test dataset pass either path to the file or dataframe>",
               target="<Target Variable Name>",
               token = "<Licence Key>")
model_slug, prediction_rules, predicted_data = model.fit()
```

### Automated Data Preprocessing, Feature engineering and Feature Selection for train data
Feature engineering module will return two dataframes, one for linear algorithms & second one for tree based algorithms and a slug value which is to be used while preparing test data. 
```sh
from mAdvisor import AutoFE
preprocess = AutoFE(target="<Target Variable Name>",
                    train_df = "train dataframe to be used",
                    token = "<Licence Key>")
linear_df, tree_df, fe_slug = preprocess.fit()
```

### Automated Data Preprocessing, Feature engineering and Feature Selection for test data
Feature engineering module will return two dataframes, one for linear algorithms and second one for tree based algorithms.
```sh
from mAdvisor import AutoFE_Test
preprocess_test = AutoFE_Test(test_df = "<test dataframe to be used>",
			 fe_slug="<Unique slug value received from train data feature engineering>",
                   	 token = "<Licence Key>")
linear_df_test, tree_df_test = preprocess_test.fit()
```

