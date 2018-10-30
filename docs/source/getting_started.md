# Getting Started

Django Crud Generator is not intended to create a django application from the scratch, in the opposite way just scaffold 
a new structure to create basic operations based on [base-django](https://github.com/contraslash/base-django) package.

This package must be installed in the root of your project with the name base. To do so:

```bash
git clone https://github.com/contraslash/base-django base
```

> If you want to create a site from scratch please check our [create a blog in 5]()

To use [django-crud-generator](https://pypi.org/project/django-crud-generator/), first install the latest version from pip

```bash
pip install django-crud-generator
```


Now assume you have a `Post` Model under an app called `blog`, to create the structure use
 
```bash
django-crud-generator.py  --django_application_folder blog --model_name Post
```

Now you can add the `urls.py` file to your main tree.

To fully customize your templates, add `template_name` attribute to each class.

By default django-crud-generator asumes you already have a `base.html` template, like in all common django sites, with
the default schema

```html
<html>
    <head>
    </head>
    <body>
        {% block content %}
        
        {% endblock %}
    </body>
</html>
```