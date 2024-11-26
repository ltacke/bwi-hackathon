from typing import List, Tuple

from app.infrastructure.prompt_clients.models import TooManyTokenException


class LlamaBaseDeprecatedTemplate:
    template: str = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{{ system_prompt }}<|eot_id|>{{ shot_examples }}<|start_header_id|>user<|end_header_id|>
{{ user_message }}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

    MAX_TOKEN: int = 127000

    @staticmethod
    def make_prompt(
        system_prompt: str,
        user_message: str,
        ignore_length: bool = False,
        shot_examples: List[Tuple[str, str]] = None,
    ) -> str:
        prompt = (
            __class__()
            .template.replace("{{ user_message }}", user_message.strip())
            .replace("{{ system_prompt }}", system_prompt.strip())
        )

        if not shot_examples:
            prompt = prompt.replace("{{ shot_examples }}", "")
        else:
            example = ""
            for user, assistant in shot_examples:
                example += f"<|start_header_id|>user<|end_header_id|>{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>{assistant}<|eot_id|>"

            prompt = prompt.replace("{{ shot_examples }}", example)

        if not ignore_length and (len(prompt) / 2.7) > __class__().MAX_TOKEN:
            raise TooManyTokenException(
                f"Prompt is {len(prompt)} which divided by 2.7 is roughly {len(prompt) / 2.7} token. May be too long for llama3. Should be less than {7900} tokens.\n{prompt}"
            )

        return prompt
