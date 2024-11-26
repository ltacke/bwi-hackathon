from typing import List

from src.prompt_clients.models import LlmModelId, ChatArtifact
from src.prompt_clients.prompt_templates.llama3.base import LlamaBase
from src.prompt_clients.prompt_templates.mistral.base import MistralBase


class PromptFactory:
    @staticmethod
    def make_prompt(
        system_prompt: str,
        current_artifact: ChatArtifact,
        model_id: LlmModelId,
        ignore_length: bool = False,
        history: List[ChatArtifact] = None,
    ) -> str:
        if model_id == LlmModelId.LLAMA31_INSTRUCT:
            base_template = LlamaBase()
        elif model_id == LlmModelId.MISTRAL_LARGE:
            base_template = MistralBase()
        else:
            raise ValueError(f"Unknown model id: {model_id}")

        return base_template.make_prompt(
            system_prompt=system_prompt,
            current_artifact=current_artifact,
            history=history,
            ignore_length=ignore_length,
        )
