"""
Gemini Client - Online AI using Google Gemini API
"""

import os
import json
import re
import google.generativeai as genai

class GeminiClient:

    name = "gemini"
    def __init__(self, api_key=None, model=None):

        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")

        self.model_name = (
            model
            or os.getenv("GEMINI_MODEL")
            or "gemini-2.5-flash"
        )

        self.client = None

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(
                    self.model_name
                )
            except Exception as e:
                print(f"Gemini initialization failed: {e}")

    def is_available(self):
        """
        Check if Gemini is available
        """
        return self.client is not None

    def chat(
        self,
        message,
        system_prompt=None,
        temperature=0.3,
        max_tokens=1024
    ):
        """
        Send chat message to Gemini
        """

        if not self.is_available():
            raise Exception(
                "Gemini API not configured"
            )

        prompt = ""

        if system_prompt:
            prompt += system_prompt + "\n\n"

        prompt += message

        try:

            generation_config = genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )

            response = self.client.generate_content(
                prompt,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:

            error_text = str(e)

            if "429" in error_text:

                raise Exception(
                    "Gemini quota exceeded"
                )

            raise Exception(
                f"Gemini API error: {error_text}"
            )

    def parse_pos_command(self, text):
        """
        Parse POS command using Gemini
        """

        system_prompt = """
    ```

    You are a POS (Point of Sale) parser for an Indonesian minimarket.

    Return ONLY valid JSON.

    Supported intents:

    * sale
    * add_unit
    * add_product
    * check_stock
    * check_price
    * stock_in
    * stock_out
    * update_pricing_rule
    * unknown

    Rules:

    * "jual" => sale
    * "stok" => check_stock
    * "harga" => check_price
    * "barang masuk" => stock_in
    * "barang keluar" => stock_out
    * "tambah unit" => add_unit

    Product names must be lowercase.

    Units:
    pcs, dus, renteng, slop,
    batang, bungkus, pack,
    botol, kaleng, sachet.

    Prices are Indonesian Rupiah.

    Return JSON ONLY.

    Examples:

    Input:
    jual rokok 2 batang 5000

    Output:
    {
    "intent":"sale",
    "product":"rokok",
    "qty":2,
    "unit":"batang",
    "total_price":5000
    }

    Input:
    cek stok royco

    Output:
    {
    "intent":"check_stock",
    "product":"royco"
    }

    Input:
    rokok sekarang bisa dijual per batang

    Output:
    {
    "intent":"add_unit",
    "product":"rokok",
    "unit":"batang",
    "ratio":1
    }

    Input:
    barang masuk royco 10 dus

    Output:
    {
    "intent":"stock_in",
    "product":"royco",
    "qty":10,
    "unit":"dus"
    }

    Input:
    rokok 1 batang 3000, 2 batang 5000

    Output:
    {
    "intent":"update_pricing_rule",
    "product":"rokok",
    "unit":"batang",
    "tiers":[
    {
    "min_qty":1,
    "price":3000
    },
    {
    "min_qty":2,
    "price":2500
    }
    ]
    }
    """
        response = self.chat(
            text,
            system_prompt=system_prompt,
            temperature=0.1,
            max_tokens=512
        )

        print("\n===== GEMINI RAW RESPONSE =====")
        print(response)
        print("===== END RESPONSE =====\n")

        try:

            cleaned = response.strip()

            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]

            if cleaned.startswith("```"):
                cleaned = cleaned[3:]

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            return json.loads(
                cleaned.strip()
            )

        except Exception:

            json_match = re.search(
                r'\{.*\}',
                response,
                re.DOTALL
            )

            if json_match:
                try:
                    return json.loads(
                        json_match.group()
                    )
                except Exception:
                    pass

            raise Exception(
                f"Gemini returned invalid JSON: {response}"
            )