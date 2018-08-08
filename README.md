# Django CRUD Generator


[![PyPI](https://img.shields.io/pypi/v/django-crud-generator.svg)](https://pypi.org/project/django-crud-generator)


This is a simple script to automate CRUD operations based on [Base Django](https://git.contraslash.com/ma0/base-django) 
by [contraslash](https://contraslash.com)
 
## Prerequisites:

- You have an existing django project with an app with a model to generate its crud
- You have a template called `base.html` and that template contains a block called `content`
- You have installed [Base Django app](https://git.contraslash.com/ma0/base-django)  and is already on `INSTALLED_APPS` on `settings.py`

## Usage:
You should invoque this script using simethin like this

```bash
cd your/app/path
python django-crud-generator.py --model_name ModelName
```

After run the script add a attribute to your model `url_name = conf.<MODEL_NAME>_DETAIL_URL_NAME`.

Be sure your `path/to/application/urls.py` is routed by the main `urls.py` file.

## Options:
- `--model_prefix`: Is used to prefix all configuration in `conf.py` variables for urls
- `--url_pattern`: Define the url pattern inside the `urls.py`
- `--create_api`: If `True` creates an api based on [Django Rest Framework](http://www.django-rest-framework.org/)
