"""
Customer Service
"""

from app.customers.model import Customer
from app.customers.repository import CustomerRepository
from app.core.exceptions import NotFoundException, ConflictException


class CustomerService:
    @classmethod
    def create_customer(cls, data):
        if data.get('phone') and CustomerRepository.find_by_phone(data['phone']):
            raise ConflictException('Customer with this phone already exists')

        customer = Customer(
            name=data['name'],
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            address=data.get('address', ''),
            membership_level=data.get('membership_level', 'regular'),
            points=data.get('points', 0),
            notes=data.get('notes', '')
        )
        CustomerRepository.create(customer)
        return customer.to_dict()

    @classmethod
    def get_customer(cls, customer_id):
        customer = CustomerRepository.find_by_id(customer_id)
        if not customer:
            raise NotFoundException('Customer not found')
        return customer.to_dict()

    @classmethod
    def get_customer_by_phone(cls, phone):
        customer = CustomerRepository.find_by_phone(phone)
        if not customer:
            raise NotFoundException('Customer not found')
        return customer.to_dict()

    @classmethod
    def list_customers(cls, page=1, per_page=20, search=None):
        skip = (page - 1) * per_page
        customers, total = CustomerRepository.list_all(skip=skip, limit=per_page, search=search)
        total_pages = (total + per_page - 1) // per_page
        return {
            'customers': [c.to_dict() for c in customers],
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        }

    @classmethod
    def update_customer(cls, customer_id, data):
        customer = CustomerRepository.find_by_id(customer_id)
        if not customer:
            raise NotFoundException('Customer not found')
        CustomerRepository.update(customer_id, data)
        return cls.get_customer(customer_id)

    @classmethod
    def delete_customer(cls, customer_id):
        customer = CustomerRepository.find_by_id(customer_id)
        if not customer:
            raise NotFoundException('Customer not found')
        CustomerRepository.update(customer_id, {'is_active': False})
        return True

    @classmethod
    def add_transaction_points(cls, customer_id, amount):
        points = int(amount / 10000)
        CustomerRepository.add_points(customer_id, points, amount)
        return {'points_added': points}
