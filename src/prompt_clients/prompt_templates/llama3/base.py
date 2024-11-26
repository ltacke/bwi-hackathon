from typing import List

from app.infrastructure.prompt_clients.models import ChatArtifact, TooManyTokenException


class LlamaBase:
    template: str = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{{ system_prompt }}<|eot_id|>{{ shot_examples }}<|start_header_id|>user<|end_header_id|>
{{ user_message }}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

    MAX_TOKEN: int = 127000

    @staticmethod
    def make_prompt(
        system_prompt: str,
        current_artifact: ChatArtifact,
        ignore_length: bool = False,
        history: List[ChatArtifact] = None,
    ) -> str:
        if history is None:
            history = []
        prompt = (
            __class__()
            .template.replace("{{ user_message }}", current_artifact.text.strip())
            .replace("{{ system_prompt }}", system_prompt.strip())
        )

        if history is None:
            prompt = prompt.replace("{{ shot_examples }}", "")
        else:
            history_string = ""
            for chat_message in history:
                history_string += f"<|start_header_id|>{chat_message.sender}<|end_header_id|>{chat_message.text}<|eot_id|>"

            prompt = prompt.replace("{{ shot_examples }}", history_string)

        if not ignore_length and (len(prompt) / 2.7) > __class__().MAX_TOKEN:
            raise TooManyTokenException(
                f"Prompt is {len(prompt)} which divided by 2.7 is roughly {len(prompt) / 2.7} token. May be too long for llama3. Should be less than {__class__().MAX_TOKEN} tokens.\n{prompt}"
            )

        return prompt
