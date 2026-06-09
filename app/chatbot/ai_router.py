"""
AI Router - Route between online and offline mode
"""

import os
from app.chatbot.online.gemini_client import GeminiClient
from app.chatbot.online.groq_client import GroqClient
from app.chatbot.online.openrouter_client import OpenRouterClient
from app.chatbot.offline.regex_parser import RegexParser
from app.chatbot.offline.entity_extractor import EntityExtractor
from app.chatbot.offline.rule_engine import RuleEngine
from app.chatbot.offline.intent_detector import IntentDetector


class AIRouter:
    """Router for AI chatbot - online/offline mode"""

    def __init__(self):

        self.mode = os.getenv(
            'AI_MODE',
            'hybrid'
        )

        self.providers = [

            GeminiClient(),

            GroqClient(),

            OpenRouterClient()

        ]

    def is_online_available(self):

        return any(
            provider.is_available()
            for provider in self.providers
        )

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

            try:

                return self._process_online(
                    text
                )

            except Exception as e:

                return {

                    'success': True,

                    'mode':
                    'offline_fallback',

                    'reason':
                    str(e),

                    'fallback':
                    self._process_offline(text)

                }

        else:  # offline
            return self._process_offline(text)

    def _process_online(self, text):
        """
        Try providers sequentially:
        Gemini
        Groq
        OpenRouter
        """

        last_error = None

        for provider in self.providers:

            try:

                if not provider.is_available():
                    continue

                parsed = provider.parse_pos_command(text)

                intent = parsed.get(
                    'intent',
                    'unknown'
                )

                print(
                    f"[AI] Using provider: {provider.name}"
                )

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
                    'provider': provider.name,
                    'parsed': parsed
                }

            except Exception as e:

                print(
                    f"[AI] {provider.name} failed: {e}"
                )

                last_error = str(e)

                continue

        raise Exception(
            f"All providers failed. Last error: {last_error}"
        )

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
