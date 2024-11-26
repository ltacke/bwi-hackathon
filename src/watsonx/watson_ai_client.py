import functools
import json
import os
from dataclasses import dataclass
from time import sleep
from typing import Optional, List, Generator

import requests

from src.prompt_clients.models import PromptClient, PromptResponse
from src.watsonx.models import (
    WatsonXClientError,
    TooManyRequestsException,
    BadGatewayException,
    ServiceOverloadedException,
)


def retry_on_connection_error(retries=10, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.ConnectionError as e:
                    print("ConnectionError", str(e))
                    sleep(delay)
                except (
                    TooManyRequestsException,
                    BadGatewayException,
                    ServiceOverloadedException,
                ):
                    sleep(delay * 2)

            raise Exception(f"Failed after {retries} attempts")

        return wrapper

    return decorator


@dataclass
class WatsonXConfig:
    wai_api_key: str
    wai_url: str
    wai_stream_url: str
    wai_project_id: str


class WatsonXClient(PromptClient):
    _url: str
    _headers: dict
    _project_id: Optional[str] = None

    def __init__(self, config: WatsonXConfig):
        self._apikey = config.wai_api_key
        self._token = self.get_access_token(api_key=self._apikey)
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

        self._headers = headers
        self._url = config.wai_url
        self._stream_url = config.wai_stream_url
        self._project_id = config.wai_project_id

    @staticmethod
    def get_access_token(api_key: str):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}"

        resp = requests.post(
            "https://iam.cloud.ibm.com/identity/token", data=data, headers=headers
        )

        if resp.status_code != 200:
            raise WatsonXClientError(
                f"wrong client status during auth received {resp.status_code} with {resp.text}"
            )

        access_token = resp.json()["access_token"]

        return access_token

    def prompt(
        self,
        prompt: str,
        min_token: int,
        max_token: int,
        model_id: str,
        stop_sequences: List[str] = None,
        stream: bool = False,
    ) -> Generator[PromptResponse, None, None] | PromptResponse:
        parameters = {
            "min_new_tokens": min_token,
            "max_new_tokens": max_token,
            "decoding_method": "greedy",
            "repetition_penalty": 1,
            "random_seed": 67,
        }

        if stop_sequences is not None:
            parameters["stop_sequences"] = stop_sequences
            parameters["include_stop_sequence"] = True

        payload = {
            "parameters": parameters,
            "input": prompt,
            "model_id": model_id,
            "moderations": {},
            "project_id": self._project_id,
        }

        if stream:
            return self._streamed_prompt(payload)
        else:
            return self._prompt(payload)
        pass

    @retry_on_connection_error()
    def _prompt(
        self,
        payload: dict,
    ) -> PromptResponse:
        resp = requests.post(self._url, headers=self._headers, json=payload)

        if resp.status_code == 429:
            raise TooManyRequestsException(resp.text)
        if resp.status_code == 502:
            raise BadGatewayException(resp.text)
        if resp.status_code == 529:
            raise BadGatewayException(resp.text)
        if resp.status_code != 200:
            raise WatsonXClientError(
                f"wrong client status received {resp.status_code} with {resp.text}"
            )

        return PromptResponse.model_validate(resp.json())

    @retry_on_connection_error()
    def _streamed_prompt(self, payload: dict) -> Generator[PromptResponse, None, None]:
        url = self._stream_url
        resp = requests.post(url, headers=self._headers, json=payload, stream=True)

        if resp.status_code == 429:
            raise TooManyRequestsException(resp.text)
        if resp.status_code == 502:
            raise BadGatewayException(resp.text)
        if resp.status_code == 529:
            raise BadGatewayException(resp.text)
        if resp.status_code != 200:
            raise WatsonXClientError(
                f"wrong client status received {resp.status_code} with {resp.text}"
            )
        resp.encoding = "utf-8"
        for line in resp.iter_lines(decode_unicode=True):
            if line and line.startswith("data:"):
                event_data = line[5:].strip()
                yield PromptResponse.model_validate(json.loads(event_data))


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv(override=True)

    config = WatsonXConfig(
        wai_url=os.getenv("WAI_URL"),
        wai_project_id=os.getenv("WAI_PROJECT_ID"),
        wai_api_key=os.getenv("WAI_API_KEY"),
    )

    client = WatsonXClient(config)
    content = client.prompt(
        "Was ist beste pizza? Antworte  in shakespeare sonnet", 0, 1000, None, False
    )

    for c in content:
        print(c)
