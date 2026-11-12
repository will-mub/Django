# Django Farm Management System

A Django web application for managing farm produce, customers, suppliers, sales and expenses, with a dashboard and reports. This academic prototype was developed for the Object-Oriented Programming using Python course.

- **Language:** Python
- **Framework:** Django
- **Database:** SQLite
- **Repository:** https://github.com/will-mub/Django.git

## Run the application

The repository already contains the Django project and its apps. You do not need to run `django-admin startproject` or recreate the apps. Follow these steps from a terminal.

### 1. Clone the repository and enter the project directory

```bash
git clone https://github.com/will-mub/Django.git
cd Django/farm
```

The `farm` directory contains `manage.py` and is the working directory for the commands below.

### 2. Create and activate a virtual environment

**Windows (Command Prompt):**

```bat
python -m venv venv
venv\Scripts\activate
```

**macOS or Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Use Python 3.12 or newer.

### 3. Install Django

```bash
python -m pip install django
```

### 4. Create or update the database

```bash
python manage.py migrate
```

The repository includes `db.sqlite3` with sample records. If you are starting with a fresh database, migrations create its tables.

### 5. Create the demo superuser

Create the account when it does not already exist in your local database:

```bash
python manage.py createsuperuser --username wilz --email wilz@example.com
```

At the prompts, enter **`122333`** for the password and confirm it. This short password is intentionally weak and only for local demonstration/testing. Django may warn that it fails password validation; confirm the bypass when prompted to use this demo password. Do not use these credentials on a public or production deployment.

### 6. Start the development server and sign in

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> and sign in with:

- **Username:** `wilz`
- **Password:** `122333`

Stop the server with `Ctrl+C`. The development server and demo credentials are for local testing only, not public hosting.

## Demonstration walkthrough

1. Sign in and point out the dashboard's produce count, customer count and low-stock count.
2. Add a produce item and set its reorder level above its current stock to see it flagged as low.
3. Add a customer and record a sale for them. Check that the produce stock decreases.
4. Try selling more than the available stock; the sale should be refused.
5. Record an expense, then void it and check that it is excluded from the list and totals.
6. Open Reports to view sales, expenses, estimated profit and best sellers.
7. To explain the implementation, follow a URL, view, template and model.

## Features

The project is split into Django apps for the main areas of farm management.

| App | What it does |
|---|---|
| `dashboard` | Home page with produce count, customer count and low-stock count. |
| `produce` | Inventory with categories, units, prices, stock quantities and reorder levels. Supports adding, editing, deleting and searching by name. |
| `customers` | Customer contact records, with add, edit, delete and search by name or phone. |
| `suppliers` | Supplier details and type. Deleting a supplier marks it inactive rather than removing its record. |
| `sales` | Sales with one or more produce items, payment method and amount paid. Displays unpaid, partially paid or paid status. |
| `expenses` | Expenses by category, with an optional receipt number. Incorrect entries are voided instead of deleted. |
| `reports` | Sales and expense totals, estimated profit, low-stock list, top five best sellers and monthly totals for the last six months. |

Every page requires login. Users who are not signed in are redirected to the Django admin login page.

### How a sale works

1. Choose an optional customer, payment method and amount paid, then add one or more produce items with quantities and unit prices.
2. The app checks that at least one item was added and that the amount paid does not exceed the sale total.
3. The sale is saved in a database transaction. Stock is reduced only when enough is available.
4. If any item has insufficient stock, the entire transaction is cancelled; no partial sale is saved.

## How the application works

Django follows a Model-View-Template pattern. For example, when someone opens `/produce/`:

1. `farm/urls.py` routes the request to the produce app's `urls.py`.
2. The app URL configuration selects the `produce_list` view.
3. The view queries `Produce` records through the Django ORM and filters by name when a search term is provided.
4. A template renders the records as an HTML page.

The URL selects the view, the view retrieves the data, and the template controls its presentation.

### URL map

| Path | Page |
|---|---|
| `/` | Dashboard |
| `/produce/` | Produce list; also `add/`, `edit/<id>/` and `delete/<id>/` |
| `/customers/` | Customer list; also `add/`, `edit/<id>/` and `delete/<id>/` |
| `/suppliers/` | Supplier list; also `add/`, `edit/<id>/` and `delete/<id>/` |
| `/sales/` | Sales list; also `add/` and `<id>/` for details |
| `/expenses/` | Expense list; also `add/`, `edit/<id>/` and `void/<id>/` |
| `/reports/` | Reports dashboard |
| `/admin/` | Django admin site |

## Database and models

Each model is a Python class that Django maps to a database table. For example, `Produce` stores an item's name, category, description, unit, selling price, stock quantity, reorder level and creation time. Its `is_low_stock` property compares the stock quantity with the reorder level.

The models are related to preserve farm records:

- A `Sale` can optionally belong to a `Customer` and is associated with the user who recorded it.
- A `Sale` has multiple `SaleItem` records, each linked to a `Produce` item.
- A customer or produce item already used in a sale cannot be deleted (`on_delete=models.PROTECT`), preserving sales history.
- An `Expense` records who entered it and has an `is_void` flag.
- Sale properties calculate the total, outstanding balance and payment status.

SQLite data is stored in `db.sqlite3`. When models change, run `python manage.py makemigrations` to create migration files, then `python manage.py migrate` to apply them.

## Object-oriented concepts

- **Classes:** `Produce`, `Customer`, `Supplier`, `Sale`, `SaleItem` and `Expense` define the structure and behaviour of farm records.
- **Objects:** A record such as a produce item retrieved with `Produce.objects.get(name="Maize")` is an instance of the `Produce` class.
- **Inheritance:** The models inherit from Django's `models.Model`, which provides database operations such as `save()` and `delete()`.
- **Encapsulation:** Rules are kept with the data they govern. For example, `Produce.is_low_stock` contains the stock warning rule, and `Sale` properties calculate payment information.

## Repository structure

```text
Django/
├── README.md
└── farm/
    ├── manage.py
    ├── db.sqlite3
    ├── farm/                 # Project settings and root URLs
    ├── dashboard/            # Home page
    ├── produce/              # Inventory
    ├── customers/            # Customer records
    ├── suppliers/            # Supplier records
    ├── sales/                 # Sales and sale items
    ├── expenses/              # Expenses and voiding
    ├── reports/               # Totals, low stock and best sellers
    ├── templates/             # Shared templates and admin branding
    └── static/css/            # Stylesheets
```

Each app folder contains its own models, views, URLs, forms, admin configuration, migrations and templates.

## Limitations and future improvements

- Anyone with an account has full access; there are no roles or permissions.
- Automated tests are not yet implemented.
- Development settings include `DEBUG = True`, an exposed secret key and empty `ALLOWED_HOSTS`; this configuration is not safe for deployment.
- Sales can be created and viewed, but not edited or cancelled.
- Currency is not consistently represented in data fields. Expenses are displayed in UGX, while sale and produce prices are plain numbers.
- Customers and produce are permanently deleted unless linked to a sale; suppliers and expenses are deactivated or voided instead.
- The simple estimated profit calculation subtracts expenses from sales and does not account for stock purchase costs.
- Future work could add tests, user roles, sale cancellation with stock restoration, environment-based settings, backups and improved error handling.

## Project team and academic context

Prepared by Group 8 for the Object-Oriented Programming using Python course.

| No. | Team member | Registration number |
|---|---|---|
| 1 | Apio Lewis Ruth | S25B38/006 |
| 2 | Mugoya Arthur | M25B38/006 |
| 3 | Nakamatte Ann | S25B38/029 |
| 4 | Kasujja John Baker Hall | M25B38/042 |
| 5 | Kirabo Favour Cynthia | M25B38/018 |
| 6 | Mubbale Wilson | M25B38/027 |
