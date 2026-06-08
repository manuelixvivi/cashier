"""
Response Parser for Online Mode
"""

import json
import re


class OnlineParser:
    """Parse Gemma API responses"""

    @staticmethod
    def parse_json_response(text):
        """Extract and parse JSON from text response"""
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in text
            match = re.search(r'\{[\s\S]*?\}', text)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
            return {"intent": "unknown", "raw": text}

    @staticmethod
    def validate_pos_result(result):
        """Validate parsed POS result"""
        required_intents = {
            'sale': ['product', 'qty', 'unit'],
            'check_stock': ['product'],
            'check_price': ['product'],
            'add_unit': ['product', 'unit', 'ratio'],
            'add_product': ['name', 'sku', 'base_unit']
        }

        intent = result.get('intent', 'unknown')
        if intent in required_intents:
            missing = [f for f in required_intents[intent] if f not in result]
            if missing:
                result['validation_error'] = f"Missing fields: {', '.join(missing)}"

        return result
