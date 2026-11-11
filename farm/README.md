# Django Farm Management System

Course: Object-Oriented Programming using Python
Repository: <https://github.com/will-mub/OPP.git>
Language: Python
Database: SQLite

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

This project is a browser-based farm record-keeping system built with Django. It brings produce stock, customers, suppliers, sales, expenses and reports into one database, with pages and forms for viewing and updating each of them.

The problem behind it is a simple one. Farm records kept in separate notebooks or spreadsheets are hard to search and hard to compare. Which items are running low? What was spent this month against what was sold? Having everything connected in one place makes those questions easier to answer.

The project also serves as a practical case study for the course. Each part of the farm (a produce item, a customer, a sale) maps naturally onto a Python class, which lets us show classes, objects, inheritance and encapsulation in code that does something real.

This is an academic prototype. It has not been tested or hardened for day-to-day use on an actual farm (see Limitations).

## Objectives

- Store farm-related records in a single database.
- Provide forms and pages for viewing and updating those records.
- Use Django models, URLs, views, templates and migrations as intended.
- Show how classes, objects and relationships support a working application.
- Document the setup and structure so another person can run and review the project.

## Scope and features

The system is divided into Django apps, one per business area.

| App | What it handles |
|---|---|
| produce | Inventory records: name, category, unit, selling price, quantity in stock and reorder level. |
| customers | Customer names and contact details, used when recording sales. |
| suppliers | Supplier and contact information. Suppliers no longer in use can be deactivated instead of removed. |
| sales | Sales and the individual items in each sale. Recording a valid sale reduces stock for the produce sold. |
| expenses | Farm costs. Incorrect entries are marked void rather than deleted, so the history is kept. |
| reports | Summaries of recorded sales and expenses, low-stock items and best-selling produce. |

Some screens and actions may be more complete than others in the current local build. Check what works before relying on a particular feature.

## How it works

Django follows a Model-View-Template (MVT) pattern. A request passes through four steps before the browser gets a page back. Take the produce list as the example:

1. The browser opens `/produce/`.
2. The URL router matches the path to a pattern in `produce/urls.py`, which points to the `produce_list` view.
3. The view asks the database for `Produce` records through the Django ORM.
4. A template loops through the records and renders them as an HTML table.

```python
# produce/urls.py
urlpatterns = [
    path("", views.produce_list, name="produce_list"),
]

# produce/views.py
def produce_list(request):
    items = Produce.objects.all()
    return render(request, "produce/produce_list.html", {"items": items})
```

The URL chooses the view, the view fetches the data, and the template decides how it is shown.

## Database and models

Each model is a Python class that describes a database table. The core of the `Produce` model:

```python
class Produce(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_in_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=2, default=10)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level
```

SQLite is used for local development. When a model changes, the workflow is:

1. Edit the model in `models.py`.
2. Run `python manage.py makemigrations` to generate a migration file.
3. Run `python manage.py migrate` to apply it to the database.

A migration is a record of a schema change, so the database can be updated consistently.

## Object-oriented concepts in the code

All four examples below come from `produce/models.py`.

**Class.** `Produce` is the blueprint. It defines what every produce record stores, and Django uses it to build the matching database table.

**Object.** A single record is an object created from that class. For example, `Produce.objects.get(name="Maize")` returns one `Produce` object with its own stock quantity and price. It shares its structure with every other produce item but holds different values.

**Inheritance.** `Produce` inherits from Django's `models.Model`. That gives it database mapping and methods such as `save()` and `delete()` without us writing them. The Customer, Supplier, Sale and Expense models follow the same pattern.

**Encapsulation.** The `is_low_stock` property keeps the reorder rule inside the class, next to the data it depends on. Other code can check `produce.is_low_stock` instead of repeating the comparison. Python fields are not private, so what this shows is related data and behaviour being kept together, not hidden.

## Repository structure

```
farm/
├── manage.py
├── config/
│   ├── settings.py        # Installed apps, database, templates, other settings
│   ├── urls.py            # Project-level URL routing
│   └── wsgi.py
├── produce/
│   ├── models.py          # Database-backed classes
│   ├── views.py           # Request handling
│   ├── forms.py
│   ├── urls.py            # App-level URL routing
│   └── templates/
├── customers/
├── suppliers/
├── sales/
├── expenses/
├── reports/
├── templates/             # Shared HTML files
└── static/
    └── css/               # Stylesheets and other static assets
```

`config/` holds project-wide configuration. Every other folder is an app that keeps the code for one business area together.

## Installation

Use Python 3 in a virtual environment. These steps are for the local Windows setup we developed on. From the project root:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS or Linux, activate with `source venv/bin/activate` instead.

Install the dependencies:

```bash
pip install django pillow
```

Django is the web framework. Pillow handles images where needed.

If you are building the project from scratch rather than using the existing code, the project and first app were created with:

```bash
django-admin startproject config .
python manage.py startapp produce
```

## Running the project

Apply the migrations, then start the development server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ in a browser. Press `Ctrl + C` in the terminal to stop the server.

To add records through Django's admin site, create an account first with `python manage.py createsuperuser`.

The development server is for local testing and demonstration only. It should not be used for public hosting.

## Demonstration checklist

For a walkthrough of the project, the sequence we follow is:

1. Activate the virtual environment and start the server.
2. Open the dashboard and go to the Produce page.
3. Show at least three existing produce records.
4. Add a new produce item and confirm it appears in the list.
5. Open `urls.py`, `views.py`, the template and the `Produce` model to explain how they connect.
6. Explain `makemigrations`, `migrate` and the SQLite database.

## Limitations

- This is a prototype built for a course, not a finished product.
- Workflows have not been tested at length with realistic data.
- There are no role-based permissions, so every user has the same access.
- Audit trails, validation, error handling and backups are basic or incomplete.
- The project uses SQLite and the Django development server, so it is not set up for secure multi-user deployment.

## Future improvements

- Test every workflow with realistic sample data.
- Add role-based permissions and stronger audit trails.
- Improve backup, validation and error handling.
- Prepare a secure deployment for multi-user use.

## Authors and academic context

Prepared by Group 8 for the Object-Oriented Programming using Python course, as a collaborative group project. Team membership and registration numbers are listed above.