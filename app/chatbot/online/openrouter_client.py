import os
import json
import re
import requests


class OpenRouterClient:

    name = "openrouter"

    def __init__(self):

        self.api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

    def is_available(self):

        return self.api_key is not None

    def parse_pos_command(self, text):

        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers={

                "Authorization":
                f"Bearer {self.api_key}",

                "Content-Type":
                "application/json"

            },

            json={

                "model":
                "qwen/qwen3-8b:free",

                "messages": [

                    {
                        "role": "system",
                        "content":
                        "Return ONLY valid JSON."
                    },

                    {
                        "role": "user",
                        "content": text
                    }

                ]

            }

        )

        content = (
            response.json()
            ["choices"][0]
            ["message"]["content"]
        )

        try:

            cleaned = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(
                cleaned
            )

        except Exception:

            match = re.search(
                r"\{.*\}",
                content,
                re.DOTALL
            )

            if match:

                return json.loads(
                    match.group()
                )

            raise Exception(
                f"OpenRouter invalid JSON: {content}"
            )