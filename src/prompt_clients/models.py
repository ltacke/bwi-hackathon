from enum import StrEnum
from typing import Optional, List, Protocol, Generator, Literal

from pydantic import BaseModel, ConfigDict


class TooManyTokenException(Exception):
    pass


class UnknownChatArtifactException(Exception):
    pass


class InvalidGenerationException(Exception):
    pass


class LlmModelId(StrEnum):
    MISTRAL_LARGE: str = "mistralai/mistral-large"
    LLAMA31_INSTRUCT: str = "meta-llama/llama-3-1-70b-instruct"


class GenerationInfo(BaseModel):
    generated_text: str
    generated_token_count: int
    input_token_count: int
    stop_reason: str


class ChatArtifact(BaseModel):
    sender: Literal["user", "assistant", "answer", "toolcall"]
    text: str


class PromptResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    id: Optional[str] = ""
    model_id: str
    results: List[GenerationInfo]


class PromptClient(Protocol):
    @property
    def model_id(self) -> LlmModelId: ...

    def prompt(
        self,
        prompt: str,
        min_token: int,
        max_token: int,
        model_id: str,
        stop_sequences: List[str] = None,
        stream: bool = False,
    ) -> Generator[PromptResponse, None, None] | PromptResponse: ...


class PromptExecuter(Protocol):
    def prompt(
        self, *args, **kwargs
    ) -> Generator[PromptResponse, None, None] | PromptResponse: ...
