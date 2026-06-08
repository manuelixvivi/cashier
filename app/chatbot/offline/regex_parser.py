"""
Regex Parser - Offline command parsing
"""

import re


class RegexParser:
    """Parse POS commands using regex patterns"""

    # Indonesian number words
    NUMBER_WORDS = {
        'satu': 1, 'dua': 2, 'tiga': 3, 'empat': 4, 'lima': 5,
        'enam': 6, 'tujuh': 7, 'delapan': 8, 'sembilan': 9, 'sepuluh': 10,
        'sebelas': 11, 'dua belas': 12, 'seratus': 100, 'seribu': 1000
    }

    # Common units
    UNITS = ['pcs', 'dus', 'renteng', 'slop', 'batang', 'bungkus', 
             'pack', 'botol', 'kaleng', 'sachet', 'box', 'karton']

    @classmethod
    def parse(cls, text):
        """Parse text using regex patterns"""
        text_lower = text.lower().strip()

        # Sale pattern: "jual [product] [qty] [unit] [price]"
        sale_match = re.match(
            r'(?:jual|jualan|beli)\s+(.+?)\s+(\d+(?:\.\d+)?)\s+(' + '|'.join(cls.UNITS) + r')\s+(\d+(?:\.\d+)?)',
            text_lower
        )
        if sale_match:
            return {
                'intent': 'sale',
                'product': sale_match.group(1).strip(),
                'qty': float(sale_match.group(2)),
                'unit': sale_match.group(3),
                'total_price': float(sale_match.group(4))
            }

        # Sale pattern with "rp" prefix: "jual [product] [qty] [unit] rp[price]"
        sale_match2 = re.match(
            r'(?:jual|jualan|beli)\s+(.+?)\s+(\d+(?:\.\d+)?)\s+(' + '|'.join(cls.UNITS) + r')\s+rp\.?\s*(\d+(?:\.\d+)?)',
            text_lower
        )
        if sale_match2:
            return {
                'intent': 'sale',
                'product': sale_match2.group(1).strip(),
                'qty': float(sale_match2.group(2)),
                'unit': sale_match2.group(3),
                'total_price': float(sale_match2.group(4))
            }

        # Simple sale: "[qty] [product] [unit]"
        simple_sale = re.match(
            r'(\d+(?:\.\d+)?)\s+(.+?)\s+(' + '|'.join(cls.UNITS) + r')',
            text_lower
        )
        if simple_sale:
            return {
                'intent': 'sale',
                'product': simple_sale.group(2).strip(),
                'qty': float(simple_sale.group(1)),
                'unit': simple_sale.group(3),
                'total_price': None  # Will be calculated
            }

        # Check stock
        stock_match = re.match(
            r'(?:cek\s+)?stok\s+(.+)',
            text_lower
        )
        if stock_match:
            return {
                'intent': 'check_stock',
                'product': stock_match.group(1).strip()
            }

        # Check price
        price_match = re.match(
            r'(?:cek\s+)?harga\s+(.+)',
            text_lower
        )
        if price_match:
            return {
                'intent': 'check_price',
                'product': price_match.group(1).strip()
            }

        # Add unit: "[product] bisa dijual per [unit]" or "tambah unit [unit] untuk [product]"
        unit_match = re.match(
            r'(?:tambah\s+unit\s+|)(.+?)\s+(?:bisa\s+dijual\s+per|unit\s+baru)\s+(' + '|'.join(cls.UNITS) + r')',
            text_lower
        )
        if unit_match:
            return {
                'intent': 'add_unit',
                'product': unit_match.group(1).strip(),
                'unit': unit_match.group(2),
                'ratio': 1  # Default ratio, should be specified
            }

        return {'intent': 'unknown', 'raw': text}

    @classmethod
    def parse_number(cls, text):
        """Parse number from text (digits or words)"""
        text = text.lower().strip()

        # Try digit parsing
        if text.isdigit():
            return int(text)

        # Try float
        try:
            return float(text)
        except ValueError:
            pass

        # Try word parsing
        return cls.NUMBER_WORDS.get(text, 1)
