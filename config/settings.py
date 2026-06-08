"""
Dynamic Application Settings
Stored in MongoDB for runtime configuration
"""

from datetime import datetime
from config.database import get_db


class SettingsManager:
    """Dynamic settings manager - runtime configuration without restart"""
    COLLECTION = 'app_settings'

    @classmethod
    def get(cls, key, default=None):
        """Get setting value by key"""
        db = get_db()
        setting = db[cls.COLLECTION].find_one({'key': key})
        return setting['value'] if setting else default

    @classmethod
    def set(cls, key, value, description=None):
        """Set or update setting value"""
        db = get_db()
        data = {
            'key': key,
            'value': value,
            'updated_at': datetime.utcnow()
        }
        if description:
            data['description'] = description

        db[cls.COLLECTION].update_one(
            {'key': key},
            {'$set': data},
            upsert=True
        )
        return True

    @classmethod
    def get_all(cls):
        """Get all settings"""
        db = get_db()
        return {s['key']: s['value'] for s in db[cls.COLLECTION].find()}

    @classmethod
    def delete(cls, key):
        """Delete setting"""
        db = get_db()
        result = db[cls.COLLECTION].delete_one({'key': key})
        return result.deleted_count > 0

    @classmethod
    def initialize_defaults(cls):
        """Initialize default settings"""
        defaults = {
            'store_name': {'value': 'Toko Saya', 'description': 'Nama toko'},
            'store_address': {'value': '', 'description': 'Alamat toko'},
            'store_phone': {'value': '', 'description': 'Nomor telepon toko'},
            'currency': {'value': 'IDR', 'description': 'Mata uang'},
            'tax_rate': {'value': 0.0, 'description': 'Persentase pajak'},
            'default_page_size': {'value': 20, 'description': 'Default jumlah item per halaman'},
            'low_stock_threshold': {'value': 10, 'description': 'Batas stok rendah'},
            'ai_mode': {'value': 'offline', 'description': 'Mode AI: online/offline'},
            'receipt_footer': {'value': 'Terima kasih atas kunjungan Anda!', 'description': 'Footer struk'},
            'enable_audit_log': {'value': True, 'description': 'Aktifkan audit log'},
            'backup_enabled': {'value': True, 'description': 'Aktifkan backup otomatis'},
        }

        for key, data in defaults.items():
            if cls.get(key) is None:
                cls.set(key, data['value'], data.get('description'))
