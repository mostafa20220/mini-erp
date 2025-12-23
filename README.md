# Mini ERP System

A comprehensive Enterprise Resource Planning (ERP) system built with Django REST Framework for managing products, orders, customers, and inventory operations with role-based access control.

## 🔗 Related Repositories

**Frontend Application**: [Mini ERP Frontend](https://github.com/mostafa20220/mini-erp-front-end)  
The bootstrap-based frontend application that consumes this API.

## 🚀 Features

### User Management
- **Role-Based Access Control (RBAC)**
  - Admin: Full system access
  - Sales: View-only access to products, full order management
  - Customer: Order placement and tracking
- **JWT Authentication** with access and refresh tokens
- **Customer Management** with unique customer codes and opening balances
- **User Profile Management** with avatar support

### Product Management
- **Comprehensive Product Catalog**
  - SKU-based inventory tracking
  - Product categorization
  - Cost and selling price management
  - Stock quantity monitoring with automatic updates
  - Product image uploads
- **Stock Status Tracking**
  - Real-time stock level monitoring
  - Low stock alerts (customizable threshold)
  - Automatic stock updates on order confirmation/cancellation
- **Stock Change Logging**
  - Complete audit trail for all stock changes
  - Tracks previous and new quantities
  - Records change reasons and timestamps
  - Maintains product information even after deletion

### Order Management
- **Sales Order Processing**
  - Auto-generated order numbers
  - Customer association with order tracking
  - Multiple order statuses (Pending, Confirmed, Cancelled)
  - Automatic total amount calculation
- **Order Items**
  - Product-wise quantity and pricing
  - Line item totals
  - Bulk creation support for efficiency
- **Business Logic**
  - Automatic stock reduction on order confirmation
  - Stock restoration on order cancellation
  - Validation to prevent overselling
  - Stock change logging for all inventory movements

### Dashboard & Analytics
- **Business Insights**
  - Total customer count
  - Today's sales total
  - Low stock product alerts
- **Real-time Metrics** for business decision-making

## 🏗️ Architecture

This project follows **SOLID principles** and implements a clean, layered architecture:

```
┌─────────────────┐
│   API Views     │  ← Request handling, authentication, permissions
├─────────────────┤
│  Serializers    │  ← Data validation, transformation
├─────────────────┤
│   Services      │  ← Business logic layer
├─────────────────┤
│  Querysets      │  ← Database queries, custom managers
├─────────────────┤
│    Models       │  ← Data models, validators
└─────────────────┘
```

### Key Design Patterns
- **Service Layer Pattern**: Business logic separated from views
- **Custom QuerySets & Managers**: Reusable, optimized database queries
- **Dedicated Serializers**: One serializer per operation (create, update, list, retrieve)
- **Django Filters**: Advanced filtering capabilities with `django-filter`
- **Cursor Pagination**: Efficient pagination for large datasets

## 📋 Requirements

- Python 3.10+
- Django 5.1.2
- Django REST Framework 3.15.2
- PostgreSQL/SQLite (SQLite for development)

### Key Dependencies
```
Django==5.1.2
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
drf-spectacular==0.27.2
django-filter==24.3
django-phonenumber-field
phonenumbers==8.13.47
pillow==10.4.0
python-decouple
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mini-erp
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements
```

### 4. Environment Configuration
Create a `.env` file in the project root (use `example.env` as template):

```env
# JWT Configuration
JWT_ACCESS_EXPIRES_IN_MINUTES=120
JWT_REFRESH_EXPIRES_IN_DAYS=7

# Django Settings
DEBUG=1
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS="localhost, 127.0.0.1"
CSRF_TRUSTED_ORIGINS="http://localhost:8000, http://127.0.0.1:8000"
DEFAULT_PAGINATION_PAGE_SIZE=10
```

### 5. Database Setup
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive API Documentation
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### API Endpoints

#### Authentication
```
POST   /api/v1/auth/register/          # User registration
POST   /api/v1/auth/login/             # Login (get JWT tokens)
POST   /api/v1/auth/refresh/           # Refresh access token
POST   /api/v1/auth/logout/            # Logout (blacklist token)
GET    /api/v1/auth/me/                # Get current user profile
PUT    /api/v1/auth/me/                # Update current user profile
```

#### Customers
```
GET    /api/v1/customers/              # List all customers
POST   /api/v1/customers/              # Create new customer
GET    /api/v1/customers/{id}/         # Retrieve customer details
PUT    /api/v1/customers/{id}/         # Update customer
PATCH  /api/v1/customers/{id}/         # Partial update customer
DELETE /api/v1/customers/{id}/         # Delete customer
```

#### Products
```
GET    /api/v1/products/               # List all products
POST   /api/v1/products/               # Create new product (Admin only)
GET    /api/v1/products/{id}/          # Retrieve product details
PUT    /api/v1/products/{id}/          # Update product (Admin only)
PATCH  /api/v1/products/{id}/          # Partial update (Admin only)
DELETE /api/v1/products/{id}/          # Delete product (Admin only)
GET    /api/v1/products/stock-changes/ # View stock change logs
```

#### Orders
```
GET    /api/v1/orders/                 # List all orders
POST   /api/v1/orders/                 # Create new order
GET    /api/v1/orders/{id}/            # Retrieve order details
PUT    /api/v1/orders/{id}/            # Update order
DELETE /api/v1/orders/{id}/            # Delete order
POST   /api/v1/orders/{id}/confirm/    # Confirm order (reduces stock)
POST   /api/v1/orders/{id}/cancel/     # Cancel order (restores stock)
```

#### Dashboard
```
GET    /api/v1/dashboard/insights/     # Get business insights
```

### Filtering & Search

#### Products
```
GET /api/v1/products/?sku=PROD-001
GET /api/v1/products/?category=Electronics
GET /api/v1/products/?stock_status=low_stock
GET /api/v1/products/?min_price=100&max_price=500
GET /api/v1/products/?search=laptop
```

#### Orders
```
GET /api/v1/orders/?status=confirmed
GET /api/v1/orders/?customer=1
GET /api/v1/orders/?order_date=2025-12-23
GET /api/v1/orders/?min_total=1000
```

#### Customers
```
GET /api/v1/customers/?customer_code=CUST-001
GET /api/v1/customers/?role=customer
GET /api/v1/customers/?search=john
```

## 🔐 Permissions

### Admin
- **Products**: Full CRUD access (Create, Read, Update, Delete)
- **Orders**: Full CRUD access with update/delete capabilities
- **Customers**: Full CRUD access
- **Dashboard**: Can view business insights and analytics
- **Stock History**: Can view all stock change logs

### Sales User
- **Products**: Read-only access (List and Retrieve)
- **Orders**: Can create and view orders (Create, Read)
- **Customers**: Can create customers
- **Dashboard**: Can view business insights and analytics
- **Stock History**: Can view all stock change logs


## 💾 Database Schema

### Users
```
- id (PK)
- email (unique)
- customer_code (unique, nullable)
- phone (unique, nullable)
- role (admin/sales/customer)
- first_name, last_name
- opening_balance
- address
- avatar
- is_active
- created_at, modified_at
- created_by, modified_by
```

### Products
```
- id (PK)
- sku (unique)
- name
- category
- cost_price
- selling_price
- stock_qty
- image
- created_at, modified_at
- created_by, modified_by
```

### Orders
```
- id (PK)
- order_number (unique, auto-generated)
- customer (FK → User)
- order_date
- status (pending/confirmed/cancelled)
- total_amount (calculated)
- created_at, modified_at
- created_by, modified_by
```

### Order Items
```
- id (PK)
- order (FK → Order)
- product (FK → Product)
- product_name (snapshot)
- product_sku (snapshot)
- quantity
- unit_price
- total_price (calculated)
```

### Stock Change Logs
```
- id (PK)
- product (FK → Product, nullable)
- product_name, product_category, product_sku
- customer (FK → User, nullable)
- previous_qty
- new_qty
- change_reason
- created_at
- created_by (FK → User)
```

## 🧪 Testing

### Example Test Payloads

#### Create Product
```json
{
  "sku": "PROD-001",
  "name": "Laptop Dell XPS 13",
  "category": "Electronics",
  "cost_price": "800.00",
  "selling_price": "1200.00",
  "stock_qty": 50
}
```

#### Create Order
```json
{
  "customer_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": "1200.00"
    },
    {
      "product_id": 2,
      "quantity": 1,
      "unit_price": "500.00"
    }
  ]
}
```

#### Register User
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "role": "customer"
}
```

## 📁 Project Structure

```
mini-erp/
├── common/                 # Shared utilities and base models
│   ├── models.py          # BaseModel with audit fields
│   ├── urls.py            # Dashboard endpoints
│   └── views.py           # Dashboard insights view
├── miniERP/               # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL configuration
│   └── pagination.py      # Custom pagination classes
├── orders/                # Order management module
│   ├── models.py          # Order, OrderItem, StockChangeLog
│   ├── serializers.py     # Order serializers
│   ├── services.py        # Order business logic
│   ├── querysets.py       # Custom query managers
│   ├── views.py           # Order API views
│   ├── filters.py         # Order filtering
│   └── constants.py       # Order status constants
├── products/              # Product management module
│   ├── models.py          # Product model
│   ├── serializers.py     # Product serializers
│   ├── services.py        # Product business logic
│   ├── querysets.py       # Product query managers
│   ├── views.py           # Product API views
│   ├── filters.py         # Product filtering
│   └── constants.py       # Product constants
├── users/                 # User & authentication module
│   ├── models.py          # Custom User model
│   ├── serializers.py     # User & auth serializers
│   ├── views.py           # User API views
│   ├── permissions.py     # Custom permissions
│   ├── querysets.py       # User query managers
│   └── urls/              # User URL configurations
│       ├── auth.py        # Authentication routes
│       └── customers.py   # Customer routes
├── media/                 # User-uploaded files
│   └── products/images/   # Product images
├── db.sqlite3             # SQLite database (dev)
├── manage.py              # Django CLI
├── requirements           # Python dependencies
└── example.env            # Environment template
```

## 🔧 Configuration

### Key Settings

#### Pagination
Default page size: 10 (configurable via `DEFAULT_PAGINATION_PAGE_SIZE`)

#### JWT Tokens
- Access Token: 120 minutes (default)
- Refresh Token: 7 days (default)

#### Stock Thresholds
- Low Stock: < 10 units (configurable in `products/constants.py`)

#### Media Files
- Products: `media/products/images/`
- Profiles: `media/profile/`



---

**Built with ❤️ using Django REST Framework**

