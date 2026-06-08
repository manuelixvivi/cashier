"""
Product Service - Business Logic Layer
"""

from app.products.model import Product, ProductCategory
from app.products.repository import ProductRepository, ProductCategoryRepository
from app.core.exceptions import NotFoundException, ConflictException, ValidationException


class ProductService:
    """Product management service"""

    @classmethod
    def create_product(cls, data):
        if ProductRepository.find_by_sku(data['sku']):
            raise ConflictException(
                f"Product with SKU '{data['sku']}' already exists"
            )

        if data.get('barcode') and ProductRepository.find_by_barcode(data['barcode']):
            raise ConflictException(
                f"Product with barcode '{data['barcode']}' already exists"
            )

        # =====================================================
        # NORMALISASI STOCK KE BASE UNIT
        # =====================================================

        stock = data.get('stock', 0)
        stock_unit = data.get('stock_unit')
        base_unit = data.get('base_unit', 'pcs')
        conversions = data.get('conversions', {})

        if stock_unit and stock_unit != base_unit:

            if stock_unit not in conversions:
                raise ValidationException(
                    f"Unit '{stock_unit}' not found in conversions"
                )

            stock = stock * conversions[stock_unit]

        # =====================================================
        # CREATE PRODUCT
        # =====================================================

        product = Product(
            name=data['name'],
            sku=data['sku'],
            category=data.get('category', ''),
            description=data.get('description', ''),
            barcode=data.get('barcode'),
            base_unit=base_unit,
            conversions=conversions,
            pricing_rules=data.get('pricing_rules', []),
            cost_price=data.get('cost_price', 0),
            stock=stock,
            min_stock=data.get('min_stock', 0),
            max_stock=data.get('max_stock', 0),
            supplier_id=data.get('supplier_id'),
            is_active=data.get('is_active', True),
            custom_fields=data.get('custom_fields', {})
        )

        ProductRepository.create(product)

        return product.to_dict()
    @classmethod
    def get_product(cls, product_id):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')
        return product.to_dict()

    @classmethod
    def get_product_by_sku(cls, sku):
        product = ProductRepository.find_by_sku(sku)
        if not product:
            raise NotFoundException('Product not found')
        return product.to_dict()

    @classmethod
    def search_products(cls, query, page=1, per_page=20):
        products = ProductRepository.find_by_name(query)
        total = len(products)
        start = (page - 1) * per_page
        end = start + per_page
        paginated = products[start:end]
        total_pages = (total + per_page - 1) // per_page
        return {
            'products': [p.to_dict() for p in paginated],
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        }

    @classmethod
    def list_products(cls, page=1, per_page=20, category=None, is_active=None, sort_by=None):
        filters = {}
        if category:
            filters['category'] = category
        if is_active is not None:
            filters['is_active'] = is_active

        skip = (page - 1) * per_page
        products, total = ProductRepository.list_all(skip=skip, limit=per_page, filters=filters, sort_by=sort_by)
        total_pages = (total + per_page - 1) // per_page

        return {
            'products': [p.to_dict() for p in products],
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        }

    @classmethod
    def update_product(cls, product_id, data):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        if 'sku' in data and data['sku'] != product.sku:
            if ProductRepository.find_by_sku(data['sku']):
                raise ConflictException(f"SKU '{data['sku']}' already exists")

        if 'barcode' in data and data['barcode'] and data['barcode'] != product.barcode:
            if ProductRepository.find_by_barcode(data['barcode']):
                raise ConflictException(f"Barcode '{data['barcode']}' already exists")

        ProductRepository.update(product_id, data)
        return cls.get_product(product_id)

    @classmethod
    def delete_product(cls, product_id):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')
        ProductRepository.soft_delete(product_id)
        return True

    @classmethod
    def add_unit_conversion(cls, product_id, unit, ratio):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')
        if unit == product.base_unit:
            raise ValidationException('Unit cannot be the same as base unit')
        ProductRepository.add_unit_conversion(product_id, unit, ratio)
        return cls.get_product(product_id)

    @classmethod
    def add_pricing_rule(cls, product_id, unit, tiers):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')
        if unit != product.base_unit and unit not in product.conversions:
            raise ValidationException(f"Unit '{unit}' not found. Add conversion first.")

        from config.database import get_db
        db_conn = get_db()
        db_conn[ProductRepository.COLLECTION].update_one(
            {'_id': __import__('bson').ObjectId(product_id)},
            {'$pull': {'pricing_rules': {'unit': unit}}}
        )

        pricing_rule = {'unit': unit, 'tiers': tiers}
        ProductRepository.add_pricing_rule(product_id, pricing_rule)
        return cls.get_product(product_id)

    @classmethod
    def add_custom_field(cls, product_id, field_name, field_value):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')
        ProductRepository.add_dynamic_field(product_id, field_name, field_value)
        return cls.get_product(product_id)

    @classmethod
    def get_product_price(cls, product_id, unit, qty):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')
        price = product.get_price(unit, qty)
        return {
            'product_id': product_id,
            'unit': unit,
            'quantity': qty,
            'price': price,
            'total': price * qty
        }

    @classmethod
    def get_low_stock_products(cls):
        products = ProductRepository.get_low_stock()
        return [p.to_dict() for p in products]

    @classmethod
    def convert_unit(cls, product_id, from_unit, to_unit, qty):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')
        base_qty = product.convert_to_base(from_unit, qty)
        result_qty = product.convert_from_base(to_unit, base_qty)
        return {
            'product_id': product_id,
            'from_unit': from_unit,
            'to_unit': to_unit,
            'input_qty': qty,
            'result_qty': round(result_qty, 4)
        }


class ProductCategoryService:
    @classmethod
    def create_category(cls, data):
        category = ProductCategory(
            name=data['name'],
            description=data.get('description', ''),
            parent_id=data.get('parent_id')
        )
        ProductCategoryRepository.create(category)
        return category.to_dict()

    @classmethod
    def list_categories(cls):
        categories = ProductCategoryRepository.list_all()
        return [c.to_dict() for c in categories]
