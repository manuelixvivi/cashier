"""
Supplier Service
"""

from app.suppliers.model import Supplier
from app.suppliers.repository import SupplierRepository
from app.core.exceptions import NotFoundException


class SupplierService:
    @classmethod
    def create_supplier(cls, data):
        supplier = Supplier(
            name=data['name'],
            contact_person=data.get('contact_person', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            address=data.get('address', ''),
            tax_id=data.get('tax_id', ''),
            notes=data.get('notes', '')
        )
        SupplierRepository.create(supplier)
        return supplier.to_dict()

    @classmethod
    def get_supplier(cls, supplier_id):
        supplier = SupplierRepository.find_by_id(supplier_id)
        if not supplier:
            raise NotFoundException('Supplier not found')
        return supplier.to_dict()

    @classmethod
    def list_suppliers(cls, page=1, per_page=20):
        skip = (page - 1) * per_page
        suppliers, total = SupplierRepository.list_all(skip=skip, limit=per_page)
        total_pages = (total + per_page - 1) // per_page
        return {
            'suppliers': [s.to_dict() for s in suppliers],
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        }

    @classmethod
    def update_supplier(cls, supplier_id, data):
        supplier = SupplierRepository.find_by_id(supplier_id)
        if not supplier:
            raise NotFoundException('Supplier not found')
        SupplierRepository.update(supplier_id, data)
        return cls.get_supplier(supplier_id)

    @classmethod
    def delete_supplier(cls, supplier_id):
        supplier = SupplierRepository.find_by_id(supplier_id)
        if not supplier:
            raise NotFoundException('Supplier not found')
        SupplierRepository.update(supplier_id, {'is_active': False})
        return True
