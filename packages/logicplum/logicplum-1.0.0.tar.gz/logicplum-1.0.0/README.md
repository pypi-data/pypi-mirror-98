# LogicPlum
LogicPlum is a client library for working with the LogicPlum platform APIs.


Example
------------
```
>>> import pandas as pd
>>> from logicplum import LogicPlum
>>>
>>>
>>> lp = LogicPlum("YOUR-API-KEY")
>>>
>>> # New Project
>>> project_id = lp.create_project("PROJECT-NAME", "PROJECT-DESCRIPTION")
>>> print(project_id)
>>>
>>> # Data Training
>>> train_df = pd.read_csv("datatotrain.csv")
>>> target = "TARGET-COLUMN-NAME"
>>> x = lp.train(project_id, train_df, target)
>>> print(x)
>>>
>>> # Check data training status
>>> training_status = lp.train_status(project_id)
>>> print(training_status)
>>>
>>> # List models
>>> models = lp.model_list(project_id)
>>> print(models)
>>>
>>> # Deploy a model
>>> model_id = "MODEL-ID-TO-DEPLOY"
>>> deployment_id = lp.deploy(project_id, model_id)
>>> print(deployment_id)
>>> 
>>> # List deployed models
>>> deployments = lp.deployment_list(project_id)
>>> print(deployments)
>>>
>>> # Predictions
>>> score_df = pd.read_csv('datatoscore.csv')
>>> scores = lp.score(deployment_id, score_df)
>>> print(scores)
>>>
```
