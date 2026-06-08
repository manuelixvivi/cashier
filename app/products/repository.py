"""
Product Repository - Data Access Layer
"""

from datetime import datetime
from bson import ObjectId
from config.database import get_db
from app.products.model import Product, ProductCategory


class ProductRepository:
    """Product data repository"""
    COLLECTION = 'products'

    @classmethod
    def find_by_id(cls, product_id):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'_id': ObjectId(product_id)})
        return Product.from_dict(data) if data else None

    @classmethod
    def find_by_sku(cls, sku):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'sku': sku})
        return Product.from_dict(data) if data else None
    
    @classmethod
    def decrease_stock(cls, product_id, qty):
        db = get_db()

        return db.products.update_one(
            {"_id": ObjectId(product_id)},
            {
                "$inc": {
                    "stock": -qty
                }
            }
        )

    @classmethod
    def find_by_barcode(cls, barcode):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'barcode': barcode})
        return Product.from_dict(data) if data else None

    @classmethod
    def find_by_name(cls, name):
        db = get_db()
        cursor = db[cls.COLLECTION].find({
            'name': {'$regex': name, '$options': 'i'},
            'is_active': True
        })
        return [Product.from_dict(data) for data in cursor]

    @classmethod
    def create(cls, product):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': product._id,
            'name': product.name,
            'sku': product.sku,
            'category': product.category,
            'description': product.description,
            'barcode': product.barcode,
            'base_unit': product.base_unit,
            'conversions': product.conversions,
            'pricing_rules': product.pricing_rules,
            'cost_price': product.cost_price,
            'stock': product.stock,
            'min_stock': product.min_stock,
            'max_stock': product.max_stock,
            'supplier_id': product.supplier_id,
            'is_active': product.is_active,
            'custom_fields': product.custom_fields,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        })
        return product

    @classmethod
    def update(cls, product_id, update_data):
        db = get_db()
        update_data['updated_at'] = datetime.utcnow()
        result = db[cls.COLLECTION].update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0

    @classmethod
    def update_stock(cls, product_id, quantity_delta):
        db = get_db()
        result = db[cls.COLLECTION].update_one(
            {'_id': ObjectId(product_id)},
            {'$inc': {'stock': quantity_delta}, '$set': {'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, product_id):
        db = get_db()
        result = db[cls.COLLECTION].delete_one({'_id': ObjectId(product_id)})
        return result.deleted_count > 0

    @classmethod
    def soft_delete(cls, product_id):
        db = get_db()
        result = db[cls.COLLECTION].update_one(
            {'_id': ObjectId(product_id)},
            {'$set': {'is_active': False, 'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0

    @classmethod
    def list_all(cls, skip=0, limit=20, filters=None, sort_by=None):
        db = get_db()
        query = filters or {}
        sort_field = sort_by or [('created_at', -1)]
        cursor = db[cls.COLLECTION].find(query).sort(sort_field).skip(skip).limit(limit)
        total = db[cls.COLLECTION].count_documents(query)
        products = [Product.from_dict(data) for data in cursor]
        return products, total

    @classmethod
    def get_low_stock(cls):
        db = get_db()
        cursor = db[cls.COLLECTION].find({
            '$expr': {'$lt': ['$stock', '$min_stock']},
            'is_active': True
        })
        return [Product.from_dict(data) for data in cursor]

    @classmethod
    def add_dynamic_field(cls, product_id, field_name, field_value):
        db = get_db()
        result = db[cls.COLLECTION].update_one(
            {'_id': ObjectId(product_id)},
            {'$set': {f'custom_fields.{field_name}': field_value, 'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0

    @classmethod
    def add_unit_conversion(cls, product_id, unit, ratio):
        db = get_db()
        result = db[cls.COLLECTION].update_one(
            {'_id': ObjectId(product_id)},
            {'$set': {f'conversions.{unit}': ratio, 'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0

    @classmethod
    def add_pricing_rule(cls, product_id, pricing_rule):
        db = get_db()
        result = db[cls.COLLECTION].update_one(
            {'_id': ObjectId(product_id)},
            {'$push': {'pricing_rules': pricing_rule}, '$set': {'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0


class ProductCategoryRepository:
    """Product category repository"""
    COLLECTION = 'product_categories'

    @classmethod
    def find_by_id(cls, category_id):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'_id': ObjectId(category_id)})
        return ProductCategory.from_dict(data) if data else None

    @classmethod
    def create(cls, category):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': category._id,
            'name': category.name,
            'description': category.description,
            'parent_id': category.parent_id,
            'created_at': category.created_at
        })
        return category

    @classmethod
    def list_all(cls):
        db = get_db()
        cursor = db[cls.COLLECTION].find()
        return [ProductCategory.from_dict(data) for data in cursor]
