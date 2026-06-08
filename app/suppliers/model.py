"""
Supplier Models
"""

from datetime import datetime
from bson import ObjectId


class Supplier:
    """Supplier model"""
    COLLECTION = 'suppliers'

    def __init__(self, name, contact_person='', phone='', email='',
                 address='', tax_id='', notes='', is_active=True, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.contact_person = contact_person
        self.phone = phone
        self.email = email
        self.address = address
        self.tax_id = tax_id
        self.notes = notes
        self.is_active = is_active
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'contact_person': self.contact_person,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'tax_id': self.tax_id,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
