# MongoDB Schema Documentation

## Collections

### users
```json
{
  "_id": ObjectId,
  "username": "string (unique)",
  "email": "string (unique)",
  "password_hash": "string",
  "full_name": "string",
  "role": "string (admin|manager|cashier|inventory_staff)",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime",
  "last_login": "datetime"
}
```

### products
```json
{
  "_id": ObjectId,
  "name": "string",
  "sku": "string (unique)",
  "category": "string",
  "description": "string",
  "barcode": "string (unique, sparse)",
  "base_unit": "string (default: pcs)",
  "conversions": {
    "dus": 12,
    "slop": 120
  },
  "pricing_rules": [
    {
      "unit": "batang",
      "tiers": [
        {"min_qty": 1, "price": 3000},
        {"min_qty": 2, "price": 2500}
      ]
    }
  ],
  "cost_price": "number",
  "stock": "number",
  "min_stock": "number",
  "max_stock": "number",
  "supplier_id": "ObjectId",
  "is_active": "boolean",
  "custom_fields": {},
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### sales
```json
{
  "_id": ObjectId,
  "transaction_code": "string (unique)",
  "items": [
    {
      "product_id": "string",
      "product_name": "string",
      "qty": "number",
      "unit": "string",
      "unit_price": "number",
      "total": "number"
    }
  ],
  "subtotal": "number",
  "discount_amount": "number",
  "tax_amount": "number",
  "total_amount": "number",
  "payment_method": "string",
  "customer_id": "ObjectId",
  "cashier_id": "ObjectId",
  "status": "string (completed|cancelled|refunded)",
  "notes": "string",
  "created_at": "datetime"
}
```

### inventory_movements
```json
{
  "_id": ObjectId,
  "product_id": "ObjectId",
  "movement_type": "string (goods_receipt|stock_out|stock_adjustment|stock_transfer|sale)",
  "quantity": "number",
  "unit": "string",
  "reference_id": "ObjectId",
  "reference_type": "string",
  "notes": "string",
  "warehouse_location": "string",
  "created_by": "ObjectId",
  "created_at": "datetime"
}
```

### Dynamic Schema
Products collection supports dynamic fields via `custom_fields`:
```json
{
  "custom_fields": {
    "expiry_date": "2025-12-31",
    "batch_number": "B12345",
    "shelf_location": "A-12-3"
  }
}
```

Units can be added dynamically:
```json
{
  "conversions": {
    "bungkus": 12,
    "slop": 120,
    "dus": 240
  }
}
```
