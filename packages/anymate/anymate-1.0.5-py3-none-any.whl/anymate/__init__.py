import datetime
import requests
import jwt
from typing import Union
from anymate.models import *
from anymate.helpers import *


class client:
    access_token: str = None
    client_id: str = None
    client_secret: str = None
    username: str = None
    password: str = None
    on_premises_mode: bool = None
    client_uri: str = None
    auth_uri: str = None

    def __init__(self, client_id: str, client_secret: str, username: str, password: str):
        self.password = password
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.set_cloud_mode()

    def set_on_premises_mode(self, client_uri: str, auth_uri: str) -> None:
        self.on_premises_mode = True

        auth_uri = auth_uri.strip()
        if auth_uri.endswith('/'):
            auth_uri = auth_uri[:-1]
        self.auth_uri = auth_uri

        client_uri = client_uri.strip()
        if client_uri.endswith('/'):
            client_uri = client_uri[:-1]
        self.client_uri = client_uri

    def set_cloud_mode(self) -> None:
        self.on_premises_mode = False
        self.client_uri = self._get_api_url()
        self.auth_uri = self._get_auth_url()

    def _get_api_url(self) -> str:
        return f'https://{self.client_id}.anymate.app'

    def _get_auth_url(self) -> str:
        return f'https://{self.client_id}.auth.anymate.app';

    def _authenticate(self) -> str:
        auth = {'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'password',
                'username': self.username,
                'password': self.password}
        result = requests.post(f'{self.auth_uri}/connect/token', data=auth)
        response = AuthResponse(**result.json())
        self.access_token = response.access_token
        return response.access_token

    def _get_or_refresh_access_token(self) -> None:
        get_new_token = True
        if self.access_token:
            decoded_token = jwt.decode(self.access_token, options={"verify_signature": False}, algorithms=["HS256"])
            expiration_time = decoded_token.get('exp', 0)
            expiration_datetime = datetime.datetime.utcfromtimestamp(expiration_time)
            diff = expiration_datetime - datetime.datetime.utcnow()
            get_new_token = diff.total_seconds() < 5 * 60

        if not get_new_token:
            return

        self.access_token = self._authenticate()
        return

    def _api_post(self, endpoint: str, json_payload: str) -> dict:
        self._get_or_refresh_access_token()
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-type': 'application/json'}
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        if not endpoint.endswith('/'):
            endpoint = endpoint + '/'

        url = f'{self.client_uri}/{endpoint}'
        result = requests.post(url, data=json_payload, headers=headers)
        result.raise_for_status()
        json_result = result.json()
        return json_result

    def _api_get(self, endpoint: str) -> dict:
        self._get_or_refresh_access_token()
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-type': 'application/json'}
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        if not endpoint.endswith('/'):
            endpoint = endpoint + '/'

        url = f'{self.client_uri}/{endpoint}'
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        json_result = result.json()
        return json_result

    def failure(self, anymate_process_failure: Union[AnymateProcessFailure, dict, str]) -> AnymateResponse:
        endpoint = 'api/Failure'
        json_payload = anymate_process_failure if isinstance(anymate_process_failure, str) else json.dumps(
            anymate_process_failure)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def finish_run(self, anymate_finish_run: Union[AnymateFinishRun, dict, str]) -> AnymateResponse:
        endpoint = 'api/FinishRun'
        json_payload = anymate_finish_run if isinstance(anymate_finish_run, str) else json.dumps(anymate_finish_run)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def start_or_get_run(self, processKey: str) -> AnymateRunResponse:
        endpoint = f'api/StartOrGetRun/{processKey}'
        result = self._api_get(endpoint)
        response = AnymateRunResponse(**result)
        return response

    def ok_to_run(self, processKey: str) -> AnymateOkToRun:
        endpoint = f'api/OkToRun/{processKey}'
        result = self._api_get(endpoint)
        response = AnymateOkToRun(**result)
        return response

    def get_rules(self, processKey: str) -> dict:
        endpoint = f'api/GetRules/{processKey}'
        result = self._api_get(endpoint)
        return result
        # response = get_object(result)
        # return response

    def take_next(self, processKey: str) -> dict:
        endpoint = f'api/TakeNext/{processKey}'
        result = self._api_get(endpoint)
        return result
        # response = get_object(result)
        # return response

    def create_task(self, processKey: str, new_task: Union[dict, str]) -> AnymateCreateTaskResponse:
        endpoint = f'api/CreateTask/{processKey}'
        json_payload = new_task if isinstance(new_task, str) else json.dumps(new_task)
        result = self._api_post(endpoint, json_payload)
        response = AnymateCreateTaskResponse(**result)
        return response

    def create_tasks(self, processKey: str, new_tasks: Union[list, str]) -> AnymateCreateTasksResponse:
        endpoint = f'api/CreateTasks/{processKey}'
        json_payload = new_tasks if isinstance(new_tasks, str) else json.dumps(new_tasks)
        result = self._api_post(endpoint, json_payload)
        response = AnymateCreateTasksResponse(**result)
        return response

    def create_and_take_task(self, processKey: str, new_task: Union[dict, str]) -> dict:
        endpoint = f'api/CreateAndTakeTask/{processKey}'
        json_payload = new_task if isinstance(new_task, str) else json.dumps(new_task)
        result = self._api_post(endpoint, json_payload)
        return result
        # response = get_object(result)
        # return response

    def update_task(self, task: dict, str) -> AnymateResponse:
        endpoint = f'api/UpdateTask'
        json_payload = task if isinstance(task, str) else json.dumps(task)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def error(self, action: Union[AnymateTaskAction, dict, str]) -> AnymateResponse:
        endpoint = f'api/Error'
        json_payload = action if isinstance(action, str) else json.dumps(action)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def manual(self, action: Union[AnymateTaskAction, dict, str]) -> AnymateResponse:
        endpoint = f'api/Manual'
        json_payload = action if isinstance(action, str) else json.dumps(action)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def retry(self, action: Union[AnymateTaskAction, AnymateRetryTaskAction, dict, str]) -> AnymateResponse:
        endpoint = f'api/Retry'
        json_payload = action if isinstance(action, str) else json.dumps(action)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def solved(self, action: Union[AnymateTaskAction, dict, str]) -> AnymateResponse:
        endpoint = f'api/Solved'
        json_payload = action if isinstance(action, str) else json.dumps(action)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response
