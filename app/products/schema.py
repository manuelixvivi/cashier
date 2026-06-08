"""
Product Schemas with Dynamic Field Support
"""

from marshmallow import Schema, fields, validate


class PricingTierSchema(Schema):
    """Pricing tier schema"""
    min_qty = fields.Float(required=True, validate=validate.Range(min=0))
    price = fields.Float(required=True, validate=validate.Range(min=0))


class PricingRuleSchema(Schema):
    """Pricing rule schema"""
    unit = fields.String(required=True)
    tiers = fields.List(fields.Nested(PricingTierSchema))


class ProductSchema(Schema):
    """Product schema with dynamic fields"""
    _id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    sku = fields.String(required=True, validate=validate.Length(min=1, max=50))
    category = fields.String(validate=validate.Length(max=100))
    description = fields.String(validate=validate.Length(max=1000))
    barcode = fields.String(allow_none=True, load_default=None, validate=validate.Length(max=100))
    base_unit = fields.String(load_default='pcs', validate=validate.Length(max=50))
    conversions = fields.Dict(keys=fields.String(), values=fields.Float(), load_default={})
    pricing_rules = fields.List(fields.Nested(PricingRuleSchema), load_default=[])
    cost_price = fields.Float(load_default=0, validate=validate.Range(min=0))
    stock = fields.Float(load_default=0, validate=validate.Range(min=0))
    min_stock = fields.Float(load_default=0, validate=validate.Range(min=0))
    max_stock = fields.Float(load_default=0, validate=validate.Range(min=0))
    supplier_id = fields.String(allow_none=True)
    is_active = fields.Boolean(load_default=True)
    custom_fields = fields.Dict(load_default={})
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    stock_unit = fields.String(load_default=None)


class ProductUpdateSchema(Schema):
    """Product update schema (partial)"""
    name = fields.String(validate=validate.Length(min=1, max=200))
    category = fields.String(validate=validate.Length(max=100))
    description = fields.String(validate=validate.Length(max=1000))
    barcode = fields.String(validate=validate.Length(max=100))
    base_unit = fields.String(validate=validate.Length(max=50))
    conversions = fields.Dict(keys=fields.String(), values=fields.Float())
    pricing_rules = fields.List(fields.Nested(PricingRuleSchema))
    cost_price = fields.Float(validate=validate.Range(min=0))
    stock = fields.Float(validate=validate.Range(min=0))
    min_stock = fields.Float(validate=validate.Range(min=0))
    max_stock = fields.Float(validate=validate.Range(min=0))
    supplier_id = fields.String(allow_none=True)
    is_active = fields.Boolean()
    custom_fields = fields.Dict()


class ProductCategorySchema(Schema):
    """Product category schema"""
    _id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=255))
    parent_id = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
