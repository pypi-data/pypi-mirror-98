# MP-Flatpages

Django flatpages app.

### Installation

Install with pip:

```
pip install django-mp-flatpages
```

Add flatpages to urls.py:

```
urlpatterns = [

    path('', include('flatpages.urls'))
    
]
```

Run migrations:
```
python manage.py migrate
```
