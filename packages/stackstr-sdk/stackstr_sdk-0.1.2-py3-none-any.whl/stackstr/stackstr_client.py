import requests
import json
import io
import pandas as pd
import time
import uuid
from stackstr.exception import InvalidCredentials


class StackStrClient:
    api_url = "https://api.stackstr.io"

    def __init__(self, key: str, secret: str, project_id: str):
        self.__key = key
        self.__secret = secret
        self.__oid = self.__verify_credentials()
        self.project_id = project_id

    def __auth_header(self) -> [str, str]:
        return {'Authorization': f'{self.__key}:{self.__secret}'}

    def key(self) -> str:
        return self.__key

    def secret(self) -> str:
        return self.__secret

    def __verify_credentials(self) -> str:
        credentials = {"key": self.__key, "secret": self.__secret}
        resp = requests.post(f'{self.api_url}/credential/verify', json.dumps(credentials))
        if resp.status_code == 400 or resp.status_code == 401:
            err = json.loads(resp.content)
            raise InvalidCredentials(err.get('message'))
        if resp.status_code > 401:
            err = json.loads(resp.content)
            raise Exception(err.get('message'))
        return json.loads(resp.content).get('oid')

    def log_prediction(self, features: dict, prediction: str) -> (str, int):
        pred_id = str(uuid.uuid4())
        times = int(time.time())
        prediction_event = {
            "feature_map": features,
            "project_id": self.project_id,
            "prediction": prediction,
            "prediction_id": pred_id,
            "timestamp": times
        }
        prediction_event = json.dumps(prediction_event)
        resp = requests.post(f'{self.api_url}/prediction/{self.__oid}', data=prediction_event,
                             headers=self.__auth_header())
        if resp.status_code >= 400:
            err = json.loads(resp.content)
            raise Exception(err.get('message'))
        return pred_id, int(time.time())

    def log_groundtruth(self, prediction_id: str, ground_truth: str):
        ground_truth_event = {
            "ground_truth": ground_truth,
            "prediction_id": prediction_id,
            "project_id": self.project_id,
        }
        ground_truth_event = json.dumps(ground_truth_event)

        resp = requests.post(f'{self.api_url}/prediction/{self.__oid}/ground_truth',
                             data=ground_truth_event, headers=self.__auth_header())
        if resp.status_code >= 400:
            err = json.loads(resp.content)
            raise Exception(err.get('message'))
        return resp

    def upload_training_data(self, df: pd.DataFrame):
        data_buffer = io.StringIO()
        df.to_csv(data_buffer, index=False)
        files = {'training_data': data_buffer.getvalue()}
        resp = requests.post(f'{self.api_url}/project/{self.__oid}/{self.project_id}/training_data',
                             headers=self.__auth_header(), files=files)

        return resp
