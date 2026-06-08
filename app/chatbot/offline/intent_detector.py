"""
Intent Detector - Detect intent from text
"""

import re


class IntentDetector:
    """Detect intent from natural language"""

    INTENTS = {
        'sale': [
            r'jual', r'jualan', r'beli', r'transaksi',
            r'checkout'
        ],
        'check_stock': [
            r'stok', r'cek\s+stok', r'sisa', r'tersedia'
        ],
        'check_price': [
            r'harga', r'cek\s+harga', r'berapa\s+harga'
        ],
        'add_unit': [
            r'tambah\s+unit', r'unit\s+baru', r'bisa\s+dijual\s+per'
        ],
        'add_product': [
            r'tambah\s+produk', r'produk\s+baru', r'input\s+barang'
        ],
        'report': [
            r'laporan', r'report', r'penjualan\s+hari\s+ini'
        ]
    }

    @classmethod
    def detect(cls, text):
        """Detect intent from text"""
        text_lower = text.lower()

        scores = {}
        for intent, patterns in cls.INTENTS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    score += 1
            scores[intent] = score

        # Get intent with highest score
        if scores:
            best_intent = max(scores, key=scores.get)
            if scores[best_intent] > 0:
                return best_intent

        return 'unknown'

    @classmethod
    def detect_with_confidence(cls, text):
        """Detect intent with confidence score"""
        text_lower = text.lower()

        scores = {}
        for intent, patterns in cls.INTENTS.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                score += len(matches)
            scores[intent] = score

        total = sum(scores.values())
        if total == 0:
            return {'intent': 'unknown', 'confidence': 0}

        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent] / total

        return {
            'intent': best_intent,
            'confidence': round(confidence, 2),
            'all_scores': scores
        }
