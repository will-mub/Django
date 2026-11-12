# Django Farm Management System

- Course: Object-Oriented Programming using Python
- Repository: https://github.com/will-mub/Django.git
- Language: Python
- Database: SQLite

## Project team

| No. | Team member | Registration number |
|---|---|---|
| 1 | Apio Lewis Ruth | S25B38/006 |
| 2 | Mugoya Arthur | M25B38/006 |
| 3 | Nakamatte Ann | S25B38/029 |
| 4 | Kasujja John Baker Hall | M25B38/042 |
| 5 | Kirabo Favour Cynthia | M25B38/018 |
| 6 | Mubbale Wilson | M25B38/027 |

## Overview

This is a web app for keeping a farm's records in one place. It tracks produce stock, customers, suppliers, sales and expenses, and it has a reports page that pulls the numbers together: total sales, total expenses, estimated profit, low-stock items and best sellers.

The idea came from a simple problem. When records live in separate notebooks or spreadsheets, it's slow to answer basic questions like "what are we running out of?" or "did we spend more this month than we earned?". Here, everything sits in one database and the pages are linked, so recording a sale also updates the stock automatically.

It's also our project for the Object-Oriented Programming course. A farm has natural "things" in it (a produce item, a customer, a sale), and each one is a Python class in the code, so the project doubles as a worked example of classes, objects, inheritance and encapsulation.

This is an academic prototype. It hasn't been hardened for use on a real farm (see Limitations).

## Objectives

- Keep farm records in a single database instead of scattered files.
- Give staff pages and forms to add, view, search and update those records.
- Make sales update stock automatically and refuse sales the stock can't cover.
- Summarise sales, expenses and stock in a reports page.
- Use Django's models, URLs, views, templates and migrations the way they're meant to be used.
- Show where the four main OOP ideas appear in real code.

## Features

The project is split into Django apps, one for each area of the farm.

| App | What it does |
|---|---|
| `dashboard` | The home page. Shows the number of produce items, number of customers and how many items are low on stock. |
| `produce` | Inventory. Each item has a name, category (crop, dairy, poultry, livestock, other), unit, selling price, quantity in stock and reorder level. Add, edit, delete and search by name. |
| `customers` | Customer name, phone, email and address. Add, edit, delete and search by name or phone. |
| `suppliers` | Supplier name, type (seeds, fertiliser, animal feed, equipment, veterinary, general), contact person, phone, email, address and notes. "Deleting" a supplier only marks it inactive, so it isn't lost. |
| `sales` | Record a sale with one or more produce items, a payment method (cash, mobile money, bank, other) and the amount paid. Shows a payment status of Unpaid, Partially Paid or Paid. |
| `expenses` | Record costs by category (seeds, labour, transport, utilities and so on) with an optional receipt number. Wrong entries are voided instead of deleted, and voided expenses are left out of the totals. |
| `reports` | Total sales, total expenses, estimated profit, low-stock list, top five best sellers and monthly sales and expenses for the last six months. |

Every page needs a login. Anyone who isn't signed in is sent to the Django admin login page.

### How a sale works

Recording a sale is the most involved part of the app, so it's worth explaining:

1. You pick a customer (optional), a payment method and the amount paid, then add one or more produce items with a quantity and unit price.
2. The app checks that at least one item was added and that the amount paid isn't more than the sale total.
3. Everything is saved inside one database transaction. For each item, stock is reduced only if enough is available.
4. If any item doesn't have enough stock, the whole sale is cancelled and nothing is saved, so you never end up with a half-recorded sale.

## How it works

Django follows a Model-View-Template pattern. Using the produce list as the example, when someone opens `/produce/`:

1. The URL router in `farm/urls.py` sends `produce/` to the produce app's `urls.py`.
2. That file points the empty path to the `produce_list` view.
3. The view fetches `Produce` records through the Django ORM, filtering by name if a search was entered.
4. A template renders the records as an HTML page.

```python
# produce/urls.py
urlpatterns = [
    path('', views.produce_list, name='produce_list'),
    path('add/', views.produce_create, name='produce_create'),
    path('edit/<int:pk>/', views.produce_update, name='produce_update'),
    path('delete/<int:pk>/', views.produce_delete, name='produce_delete'),
]

# produce/views.py
@login_required
def produce_list(request):
    search = request.GET.get('search', '')
    products = Produce.objects.all().order_by('-created_at')
    if search:
        products = products.filter(name__icontains=search)
    return render(request, 'produce/list.html', {
        'products': products,
        'search': search,
    })
```

The URL picks the view, the view gets the data, and the template decides how it looks.

### URL map

| Path | Page |
|---|---|
| `/` | Dashboard |
| `/produce/` | Produce list (also `add/`, `edit/<id>/`, `delete/<id>/`) |
| `/customers/` | Customer list (also `add/`, `edit/<id>/`, `delete/<id>/`) |
| `/suppliers/` | Supplier list (also `add/`, `edit/<id>/`, `delete/<id>/`) |
| `/sales/` | Sales list (also `add/` and `<id>/` for details) |
| `/expenses/` | Expense list (also `add/`, `edit/<id>/`, `void/<id>/`) |
| `/reports/` | Reports dashboard |
| `/admin/` | Django admin site |

## Database and models

Each model is a Python class that Django turns into a database table. The `Produce` model:

```python
class Produce(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_in_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=2, default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level
```

The models are connected to each other:

- A `Sale` can belong to a `Customer` (optional) and to the user who recorded it.
- A `Sale` has many `SaleItem` records, and each `SaleItem` points to a `Produce` item.
- A `Customer` or `Produce` item that already appears in a sale can't be deleted (`on_delete=models.PROTECT`), which keeps sales history intact.
- An `Expense` records who entered it and has an `is_void` flag.

The `Sale` model also works out its own figures with properties: `total_amount` adds up the line totals of its items, `balance` is the total minus what's been paid, and `payment_status` turns that into Unpaid, Partially Paid or Paid.

SQLite is the database, stored in `db.sqlite3`. When a model changes, the workflow is to run `makemigrations` to create a migration file, then `migrate` to apply it.

## Object-oriented concepts in the code

**Class.** `Produce`, `Customer`, `Supplier`, `Sale`, `SaleItem` and `Expense` are classes. Each one is a blueprint for one kind of record, and Django uses it to build the matching database table.

**Object.** A single record is an object made from a class. `Produce.objects.get(name="Maize")` returns one `Produce` object with its own price and stock level. Every produce item has the same structure but different values.

**Inheritance.** All the models inherit from Django's `models.Model`, which gives them database behaviour such as `save()` and `delete()` for free. We only add the farm-specific fields and rules on top.

**Encapsulation.** Rules live inside the class that owns the data. `Produce.is_low_stock` keeps the reorder rule next to the stock fields, and `Sale.payment_status` keeps the payment logic inside `Sale`. The rest of the app just reads `produce.is_low_stock` or `sale.payment_status` instead of repeating the logic. Python doesn't make these fields private, so this is about keeping related data and behaviour together, not hiding it.

## Repository structure

```
OPP/
├── README.md
└── farm/
    ├── manage.py
    ├── db.sqlite3
    ├── farm/                 # Project settings and root URLs
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── dashboard/            # Home page
    ├── produce/              # Inventory
    ├── customers/            # Customer records
    ├── suppliers/            # Supplier records
    ├── sales/                # Sales and sale items
    ├── expenses/             # Expenses and voiding
    ├── reports/              # Totals, low stock, best sellers
    ├── templates/            # Shared base template and admin branding
    └── static/css/           # farm.css and admin-custom.css
```

Each app folder holds its own `models.py`, `views.py`, `urls.py`, `forms.py`, `admin.py`, `migrations/` and a `templates/` folder.

## Installation

You need Python 3.12 or newer (the project was generated with Django 6.1). The steps below are for Windows; on macOS or Linux, use `source venv/bin/activate` to activate the environment.

```bash
git clone https://github.com/will-mub/Django.git
cd OPP/farm

python -m venv venv
venv\Scripts\activate

pip install django
```

## Creating and Running the project
```bash
django-admin startproject farm

```

From inside the `farm` folder:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/ and sign in with the account you just created. Press `Ctrl + C` in the terminal to stop the server.

The repository includes a `db.sqlite3` file that already has a few sample records, so the pages aren't empty on first run. You'll still want to create your own superuser, since you won't know the passwords for the accounts already in that file.

The development server is for testing and demos only, not public hosting.

## Demonstration walkthrough

1. Start the server and sign in.
2. On the dashboard, point out the produce count, customer count and low-stock count.
3. Open Produce, add an item, and set its reorder level above its stock to see it flagged as low.
4. Add a customer, then record a sale for them. Go back to Produce and show that stock went down.
5. Try selling more than what's in stock and show that the sale is refused.
6. Record an expense, then void it and show that it disappears from the list and the totals.
7. Open Reports for the sales total, expense total, estimated profit and best sellers.
8. Open `urls.py`, `views.py`, a template and `models.py` to show how the pieces connect.

## Limitations

- Anyone with a login has full access. There are no roles or permissions.
- The test files are empty, so nothing is covered by automated tests yet.
- Settings are in development mode: `DEBUG = True`, an exposed secret key and empty `ALLOWED_HOSTS`. This isn't safe to deploy as is.
- Sales can be created and viewed, but not edited or cancelled afterwards.
- The currency isn't fixed in the data fields. Expenses are displayed in UGX, but sales and produce prices are plain numbers.
- Customers and produce are deleted for real (unless they're linked to a sale), while suppliers and expenses are only deactivated or voided.
- Reports use a simple profit figure (sales total minus expenses), which ignores stock purchase costs.

## Future improvements

- Add automated tests for the models and views, especially the sale and stock logic.
- Add user roles so different staff can do different things.
- Allow sales to be edited or cancelled, with stock restored.
- Move secrets and debug settings into environment variables before any real deployment.
- Add backups and better error handling.

## Authors and academic context

Prepared by Group 8 for the Object-Oriented Programming using Python course, as a collaborative group project. Team membership and registration numbers are listed above.
