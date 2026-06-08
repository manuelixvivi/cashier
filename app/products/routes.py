"""
Product Routes - API Endpoints
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.core.response import APIResponse
from app.products.service import ProductService, ProductCategoryService
from app.products.schema import ProductSchema, ProductUpdateSchema, ProductCategorySchema

products_bp = Blueprint('products', __name__)
product_schema = ProductSchema()
product_update_schema = ProductUpdateSchema()
category_schema = ProductCategorySchema()


@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = product_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )
    result = ProductService.create_product(data)
    return APIResponse.success(data=result, message='Product created', status_code=201)


@products_bp.route('/', methods=['GET'])
@jwt_required()
def list_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    is_active = request.args.get('is_active')
    if is_active is not None:
        is_active = is_active.lower() == 'true'
    result = ProductService.list_products(
        page=page, per_page=per_page, 
        category=category, is_active=is_active
    )
    return APIResponse.paginated(
        data=result['products'],
        page=result['page'],
        per_page=result['per_page'],
        total=result['total'],
        total_pages=result['total_pages']
    )


@products_bp.route('/search', methods=['GET'])
@jwt_required()
def search_products():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    result = ProductService.search_products(query, page=page, per_page=per_page)
    return APIResponse.paginated(
        data=result['products'],
        page=result['page'],
        per_page=result['per_page'],
        total=result['total'],
        total_pages=result['total_pages']
    )


@products_bp.route('/<product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    result = ProductService.get_product(product_id)
    return APIResponse.success(data=result)


@products_bp.route('/sku/<sku>', methods=['GET'])
@jwt_required()
def get_product_by_sku(sku):
    result = ProductService.get_product_by_sku(sku)
    return APIResponse.success(data=result)


@products_bp.route('/<product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        data = product_update_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )
    result = ProductService.update_product(product_id, data)
    return APIResponse.success(data=result, message='Product updated')


@products_bp.route('/<product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    ProductService.delete_product(product_id)
    return APIResponse.success(message='Product deleted')


@products_bp.route('/<product_id>/units', methods=['POST'])
@jwt_required()
def add_unit_conversion(product_id):
    data = request.get_json()
    unit = data.get('unit')
    ratio = data.get('ratio')
    if not unit or ratio is None:
        return APIResponse.error(
            message='Unit and ratio are required',
            error_code='VALIDATION_ERROR'
        )
    result = ProductService.add_unit_conversion(product_id, unit, float(ratio))
    return APIResponse.success(data=result, message='Unit conversion added')


@products_bp.route('/<product_id>/pricing', methods=['POST'])
@jwt_required()
def add_pricing_rule(product_id):
    data = request.get_json()
    unit = data.get('unit')
    tiers = data.get('tiers', [])
    if not unit or not tiers:
        return APIResponse.error(
            message='Unit and tiers are required',
            error_code='VALIDATION_ERROR'
        )
    result = ProductService.add_pricing_rule(product_id, unit, tiers)
    return APIResponse.success(data=result, message='Pricing rule added')


@products_bp.route('/<product_id>/custom-fields', methods=['POST'])
@jwt_required()
def add_custom_field(product_id):
    data = request.get_json()
    field_name = data.get('field_name')
    field_value = data.get('field_value')
    if not field_name:
        return APIResponse.error(
            message='Field name is required',
            error_code='VALIDATION_ERROR'
        )
    result = ProductService.add_custom_field(product_id, field_name, field_value)
    return APIResponse.success(data=result, message='Custom field added')


@products_bp.route('/<product_id>/price', methods=['GET'])
@jwt_required()
def get_product_price(product_id):
    unit = request.args.get('unit', 'pcs')
    qty = request.args.get('qty', 1, type=float)
    result = ProductService.get_product_price(product_id, unit, qty)
    return APIResponse.success(data=result)


@products_bp.route('/<product_id>/convert', methods=['GET'])
@jwt_required()
def convert_unit(product_id):
    from_unit = request.args.get('from')
    to_unit = request.args.get('to')
    qty = request.args.get('qty', 1, type=float)
    if not from_unit or not to_unit:
        return APIResponse.error(
            message='from and to units are required',
            error_code='VALIDATION_ERROR'
        )
    result = ProductService.convert_unit(product_id, from_unit, to_unit, qty)
    return APIResponse.success(data=result)


@products_bp.route('/low-stock', methods=['GET'])
@jwt_required()
def get_low_stock():
    result = ProductService.get_low_stock_products()
    return APIResponse.success(data=result)


@products_bp.route('/categories', methods=['GET'])
@jwt_required()
def list_categories():
    result = ProductCategoryService.list_categories()
    return APIResponse.success(data=result)


@products_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    try:
        data = category_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )
    result = ProductCategoryService.create_category(data)
    return APIResponse.success(data=result, message='Category created', status_code=201)
