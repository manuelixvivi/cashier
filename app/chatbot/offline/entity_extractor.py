"""
Entity Extractor - Extract entities from text
"""

import re


class EntityExtractor:
    """Extract entities from natural language text"""

    @staticmethod
    def extract_product_name(text):
        """Extract product name from text"""
        # Remove common command words
        clean = re.sub(r'(jual|jualan|beli|cek|stok|harga|tambah|unit|baru|bisa|dijual|per)', '', text.lower())
        clean = re.sub(r'\d+', '', clean)
        clean = re.sub(r'(pcs|dus|renteng|slop|batang|bungkus|pack|botol|kaleng|sachet|box|karton|rp)', '', clean)
        return clean.strip()

    @staticmethod
    def extract_quantity(text):
        """Extract quantity from text"""
        # Look for number followed by unit
        match = re.search(r'(\d+(?:\.\d+)?)\s+(?:pcs|dus|renteng|slop|batang|bungkus|pack|botol|kaleng|sachet|box|karton)', text.lower())
        if match:
            return float(match.group(1))

        # Look for standalone number
        match = re.search(r'(\d+(?:\.\d+)?)', text)
        if match:
            return float(match.group(1))

        return 1

    @staticmethod
    def extract_unit(text):
        """Extract unit from text"""
        units = ['pcs', 'dus', 'renteng', 'slop', 'batang', 'bungkus', 
                 'pack', 'botol', 'kaleng', 'sachet', 'box', 'karton']
        for unit in units:
            if unit in text.lower():
                return unit
        return 'pcs'

    @staticmethod
    def extract_price(text):
        """Extract price from text"""
        # Match "Rp 5000" or "5000" or "5.000"
        match = re.search(r'(?:rp\.?\s*)?(\d[\d.,]*)', text.lower())
        if match:
            price_str = match.group(1).replace('.', '').replace(',', '')
            try:
                return float(price_str)
            except:
                pass
        return None

    @staticmethod
    def extract_all(text):
        """Extract all entities at once"""
        return {
            'product': EntityExtractor.extract_product_name(text),
            'qty': EntityExtractor.extract_quantity(text),
            'unit': EntityExtractor.extract_unit(text),
            'price': EntityExtractor.extract_price(text)
        }
