# Django CRUD Generator

This is a simpls script to automate CRUD operations based on [Base Django](https://git.contraslash.com/ma0/base-django) 
by [contraslash](https://contraslash.com)
 
This script asume that you already have created a model and want to create a CRUD
based on this model
 
You should invoque this script using simethin like this

```bash
python crud_generator.py --model_name Budget  --django_application_folder ../django_app_folder/applications/budget/
```

You can specify a model_prefix using `--model_prefix`

The First capital in `--model_name` is important

Also remember that contraslash based models needs to have an `url_name` that links to `conf.<MODEL_NAME>_DETAIL_URL_NAME`