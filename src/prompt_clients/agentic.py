from typing import List, Generator

from prompt_clients.models import (
    PromptClient,
    ChatArtifact,
    LlmModelId,
    PromptResponse,
)
from prompt_clients.prompt_templates.agentic import (
    Agentic as AgenticTemplate,
)


class Agentic:
    def __init__(self, prompt_client: PromptClient):
        self._template = AgenticTemplate()
        self._prompt_client = prompt_client
        self._stop_sequences = ["PAUSE", "<|eot_id|>"]

    def prompt(
        self,
        current_artifact: ChatArtifact,
        history: List[ChatArtifact] = None,
        stream: bool = False,
    ) -> PromptResponse | Generator[PromptResponse, None, None]:
        prompt = self._template.make_prompt(
            current_artifact=current_artifact,
            history=history,
            model_id=LlmModelId.MISTRAL_LARGE,
        )
        res = self._prompt_client.prompt(
            prompt=prompt,
            min_token=1,
            max_token=900,
            stop_sequences=self._stop_sequences,
            model_id=LlmModelId.MISTRAL_LARGE,
            stream=stream,
        )

        return res
