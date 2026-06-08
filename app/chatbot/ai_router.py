"""
AI Router - Route between online and offline mode
"""

import os
from app.chatbot.online.gemma_client import GemmaClient
from app.chatbot.offline.regex_parser import RegexParser
from app.chatbot.offline.entity_extractor import EntityExtractor
from app.chatbot.offline.rule_engine import RuleEngine
from app.chatbot.offline.intent_detector import IntentDetector


class AIRouter:
    """Router for AI chatbot - online/offline mode"""

    def __init__(self):
        self.mode = os.getenv('AI_MODE', 'offline')
        self.gemma_client = GemmaClient()

    def is_online_available(self):
        """Check if online mode is available"""
        return self.gemma_client.is_available()

    def process(self, text, force_mode=None):
        """Process user input with appropriate mode"""
        mode = force_mode or self.mode

        # Try online first if hybrid mode
        if mode == 'hybrid':
            if self.is_online_available():
                try:
                    return self._process_online(text)
                except Exception:
                    pass  # Fallback to offline
            return self._process_offline(text)

        elif mode == 'online':
            if not self.is_online_available():
                return {
                    'success': False,
                    'error': 'Online mode not available. API key not configured.',
                    'fallback': self._process_offline(text)
                }
            return self._process_online(text)

        else:  # offline
            return self._process_offline(text)

    def _process_online(self, text):
        """Process using online AI (Gemma via Groq)"""
        parsed = self.gemma_client.parse_pos_command(text)

        # Apply rules to validate
        intent = parsed.get('intent', 'unknown')
        if intent == 'sale':
            return RuleEngine.process_sale(parsed)
        elif intent == 'check_stock':
            return RuleEngine.process_check_stock(parsed)
        elif intent == 'check_price':
            return RuleEngine.process_check_price(parsed)
        elif intent == 'add_unit':
            return RuleEngine.process_add_unit(parsed)

        return {
            'success': True,
            'mode': 'online',
            'parsed': parsed
        }

    def _process_offline(self, text):
        """Process using offline engine (regex + rules)"""
        # Step 1: Detect intent
        intent_result = IntentDetector.detect_with_confidence(text)
        intent = intent_result['intent']

        # Step 2: Parse with regex
        parsed = RegexParser.parse(text)

        # Override intent if regex found something specific
        if parsed.get('intent') != 'unknown':
            intent = parsed['intent']

        # Step 3: Extract entities
        entities = EntityExtractor.extract_all(text)

        # Step 4: Apply rules based on intent
        result = {
            'success': True,
            'mode': 'offline',
            'intent': intent,
            'confidence': intent_result['confidence'],
            'parsed': parsed,
            'entities': entities
        }

        if intent == 'sale':
            rule_result = RuleEngine.process_sale(parsed)
            result['action_result'] = rule_result
        elif intent == 'check_stock':
            rule_result = RuleEngine.process_check_stock(parsed)
            result['action_result'] = rule_result
        elif intent == 'check_price':
            rule_result = RuleEngine.process_check_price(parsed)
            result['action_result'] = rule_result
        elif intent == 'add_unit':
            rule_result = RuleEngine.process_add_unit(parsed)
            result['action_result'] = rule_result

        return result
