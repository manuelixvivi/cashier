"""
Prompt Builder for Online Mode
"""


class PromptBuilder:
    """Builds prompts for different POS intents"""

    @staticmethod
    def build_sale_prompt(products_context=""):
        return f"""You are a POS system parser. Parse the cashier command into JSON.
Available products context: {products_context}

Return JSON with fields: intent, product, qty, unit, total_price
Intent must be: sale
"""

    @staticmethod
    def build_stock_prompt():
        return """Parse stock check command. Return JSON: {"intent": "check_stock", "product": "..."}"""

    @staticmethod
    def build_price_prompt():
        return """Parse price check command. Return JSON: {"intent": "check_price", "product": "...", "qty": number, "unit": "..."}"""

    @staticmethod
    def build_unit_prompt():
        return """Parse unit addition command. Return JSON: {"intent": "add_unit", "product": "...", "unit": "...", "ratio": number}"""

    @staticmethod
    def build_product_prompt():
        return """Parse product addition command. Return JSON: {"intent": "add_product", "name": "...", "sku": "...", "base_unit": "...", "price": number}"""
