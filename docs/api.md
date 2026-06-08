# POS AI Backend - API Documentation

## Authentication
All endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

## Endpoints

### Auth
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/me` - Get current user

### Products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products` - List products
- `GET /api/v1/products/search?q=rokok` - Search products
- `GET /api/v1/products/<id>` - Get product
- `PUT /api/v1/products/<id>` - Update product
- `DELETE /api/v1/products/<id>` - Delete product
- `POST /api/v1/products/<id>/units` - Add unit conversion
- `POST /api/v1/products/<id>/pricing` - Add pricing rule
- `POST /api/v1/products/<id>/custom-fields` - Add custom field

### POS
- `GET /api/v1/pos/cart` - Get cart
- `POST /api/v1/pos/cart/add` - Add to cart
- `POST /api/v1/pos/cart/remove` - Remove from cart
- `POST /api/v1/pos/cart/update` - Update cart item
- `POST /api/v1/pos/cart/clear` - Clear cart
- `POST /api/v1/pos/checkout` - Checkout

### Chatbot
- `POST /api/v1/chatbot/chat` - Process chat message
- `GET /api/v1/chatbot/mode` - Get AI mode

### Reports
- `GET /api/v1/reports/daily` - Daily report
- `GET /api/v1/reports/weekly` - Weekly report
- `GET /api/v1/reports/monthly` - Monthly report
- `GET /api/v1/reports/yearly` - Yearly report
- `GET /api/v1/reports/profit` - Profit report

### Analytics
- `GET /api/v1/analytics/dashboard` - Dashboard data
- `GET /api/v1/analytics/top-products` - Top products
- `GET /api/v1/analytics/slow-products` - Slow moving products
- `GET /api/v1/analytics/sales-trend` - Sales trend

### Forecasting
- `GET /api/v1/forecasting/sales` - Sales forecast
- `GET /api/v1/forecasting/stock/<id>` - Stock forecast
- `GET /api/v1/forecasting/demand/<id>` - Demand forecast
