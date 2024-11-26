from typing import List

from app.infrastructure.prompt_clients.models import (
    ChatArtifact,
    TooManyTokenException,
    UnknownChatArtifactException,
)


class MistralBase:
    template: str = """<s>[INST]{{ system_prompt }}[/INST]</s>{{ shot_examples }}"""

    MAX_TOKEN: int = 31500

    @staticmethod
    def make_prompt(
        system_prompt: str,
        current_artifact: ChatArtifact,
        ignore_length: bool = False,
        history: List[ChatArtifact] = None,
    ) -> str:
        if history is None:
            history = []
        current_history_queue = history.copy()
        current_history_queue.append(current_artifact)
        prompt = (
            __class__()
            .template.replace("{{ system_prompt }}", system_prompt.strip())
            .replace(
                "{{ shot_examples }}", ""
            )  # TODO try out shot examples outside system prompt
        )

        history_string = ""
        for chat_message in current_history_queue:
            if chat_message.sender == "user":
                history_string += f"[INST]{chat_message.text}[/INST]"
            elif chat_message.sender == "assistant":
                history_string += f"{chat_message.text}</s>"
            elif chat_message.sender == "answer":
                history_string += f"{chat_message.text}</s>"
            elif chat_message.sender == "toolcall":
                history_string += f"[INST]{chat_message.text}[/INST]"
            else:
                raise UnknownChatArtifactException(
                    f"Unknown chat artifact sender: {chat_message.sender}"
                )

        prompt += history_string

        if not ignore_length and (len(prompt) / 2.7) > __class__().MAX_TOKEN:
            raise TooManyTokenException(
                f"Prompt is {len(prompt)} which divided by 2.7 is roughly {len(prompt) / 2.7} token. May be too long for mistral large. Should be less than {__class__().MAX_TOKEN} tokens.\n{prompt}"
            )

        return prompt
