import requests
import pandas as pd

from . import config


class LogicPlum:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_project(self, name, description):
        url: str = f"{config.HOST_NAME}{config.PROJECT_CREATE}"

        headers: dict = {
            'Authorization': self.api_key,
            'version': '100',
        }

        data: dict = {
            'name': name,
            'description': description,
        }

        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 500: return "Server Error"
        if response.status_code != 201: return response.json().get('detail', None)

        return response.json().get('project_id', None)


    def train(self, project_id, df, target):
        url: str = f"{config.HOST_NAME}{config.MODEL_TRAIN}"

        headers: dict = {
            'Authorization': self.api_key,
            'version': '100',
        }

        json_df = df.to_json(orient='records')

        data: dict = {
            'project_id': project_id,
            'target': target,
            'data': json_df,
        }
 
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 500: return "Server Error"

        return response.json().get('detail', None)

    def train_status(self, project_id):
        url: str = f"{config.HOST_NAME}{config.MODEL_TRAIN_STATUS}"

        headers: dict = {
            'Authorization': self.api_key,
            'version': '100',
        }

        params: dict = {
            'project_id': project_id,
        }

        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 500: return "Server Error"

        return response.json().get('detail', None)

    def model_list(self, project_id):
        url: str = f"{config.HOST_NAME}{config.MODEL_LIST}"

        headers: dict = {
            'Authorization': self.api_key,
            'version': '100',
        }

        params: dict = {
            'project_id': project_id,
        }

        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 500: return "Server Error"

        return response.json().get('detail', None)

    def deployment_list(self, project_id):
        url: str = f"{config.HOST_NAME}{config.DEPLOY_LIST}"

        headers: dict = {
            'Authorization': self.api_key,
            'version': '100',
        }

        params: dict = {
            'project_id': project_id,
        }

        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 500: return "Server Error"

        return response.json().get('detail', None)

    def deploy(self, project_id, model_id):
        url: str = f"{config.HOST_NAME}{config.DEPLOY}"

        headers: dict = {
            'Authorization': self.api_key,
            'version': '100',
        }

        data: dict = {
            'project_id': project_id,
            'model_id': model_id,
        }
 
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 500: return "Server Error"

        return response.json().get('detail', None)

    def score(self, deployment_id, df):
        url: str = f"{config.HOST_NAME}{config.MODEL_SCORE}"

        headers: dict = {
            'Authorization': self.api_key,
            'version': '100',
        }

        json_df = df.to_json(orient='records')

        data: dict = {
            'deployment_id': deployment_id,
            'data': json_df,
        }

        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 500: return "Server Error"
        if response.status_code != 200: return response.json().get('detail', None)

        return pd.read_json(response.json().get('prediction', None), orient='records')

    def blueprint(self, project_id, model_id):
        url: str = f"{config.HOST_NAME}{config.MODEL_BLUEPRINT}"

        headers: dict = {
            'Authorization': self.api_key,
            'version': '100',
        }

        data: dict = {
            'project_id': project_id,
            'model_id': model_id,
        }
 
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 500: return "Server Error"

        return response.json().get('detail', None)
