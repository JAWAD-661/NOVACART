# NovaCart - E-commerce Store

NovaCart is a complete Django-based e-commerce demo built for internship and portfolio presentation. It includes a customer-facing storefront, shopping cart, checkout system, user authentication, order history, and an admin dashboard.


### Customer storefront
![Featured product section](images/Featured%20prodcut%20section.png)

### Login page
![NovaCart login page](images/novacart%20login%20page.png)

### Admin views
| Admin panel | Admin order dashboard |
| --- | --- |
| ![Django admin panel](images/admin%20pannel%20django.png) | ![Admins order dashboard](images/Admins%20order%20dashboard.png) |

## What this project includes

### Customer-facing features
- Product catalog with featured items
- Product detail page
- Shopping cart with add/remove/update actions
- User registration and login
- Checkout flow with shipping details
- Order confirmation page
- Personal order history page for logged-in users
- Search bar for finding products quickly
- Responsive UI for desktop and mobile

### Admin features
- Django admin panel for managing products and orders
- Staff dashboard to view all orders
- Ability to update order status
- Manage users and order data from one place

## Tech stack
- Backend: Django 6.0.6
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Authentication: Django built-in auth system

## Project structure

```text
novacart/
├── ecomstore/              # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI entry point
├── shop/                   # Main app
│   ├── models.py           # Product, Order, OrderItem models
│   ├── views.py            # Storefront logic and views
│   ├── admin.py            # Admin registration
│   ├── templates/          # HTML templates
│   └── static/             # CSS and JS files
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── setup.py                # Optional setup helper script
└── README.md               # Project documentation
```

## How to run locally

### 1. Install Python
Make sure Python 3.10+ is installed.

### 2. Create and activate a virtual environment
On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

### 6. Start the server

```bash
python manage.py runserver
```

### 7. Open the site
- Home page: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/login/
- Register: http://127.0.0.1:8000/register/
- My orders: http://127.0.0.1:8000/my-orders/
- Admin panel: http://127.0.0.1:8000/admin/

## User flow

### Normal user
1. Register an account or log in
2. Browse products on the home page
3. Open a product detail page
4. Add items to the cart
5. Checkout and submit shipping details
6. View the order in “My Orders”

### Admin / staff user
1. Log in to the Django admin panel
2. Manage products, orders, and users
3. Visit the custom admin orders dashboard at /admin-orders/
4. Update the status of orders

## Sample credentials
If you create a superuser during setup, you can use those credentials to access the admin panel.

Example:
- Username: admin
- Password: your chosen password

## Testing
Run the test suite with:

```bash
python manage.py test
```

Current test coverage includes:
- Homepage loading
- Cart page loading
- User order history
- Staff order dashboard
- Logout flow


