import os
import json
import re

from groq import Groq


class GroqClient:

    name = "groq"

    def __init__(self):

        self.api_key = os.getenv(
            "GROQ_API_KEY"
        )

        self.model = (
            os.getenv("GROQ_MODEL")
            or "llama-3.1-8b-instant"
        )

        self.client = (
            Groq(api_key=self.api_key)
            if self.api_key
            else None
        )

    def is_available(self):

        return self.client is not None

    def parse_pos_command(self, text):

        system_prompt = """
Return ONLY valid JSON.

Supported intents:
sale
check_stock
check_price
add_unit
unknown
"""

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": text
                }
            ],

            temperature=0.1

        )

        content = (
            response
            .choices[0]
            .message.content
        )

        try:

            cleaned = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(cleaned)

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
                f"Groq invalid JSON: {content}"
            )