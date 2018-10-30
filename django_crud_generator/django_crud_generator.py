import argparse
import codecs
import os
import re
import sys
import string

BASE_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
print(BASE_TEMPLATES_DIR)

def convert(name):
    """
    This function converts a Camel Case word to a underscore word
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def render_template_with_args_in_file(file, template_file_name, **kwargs):
    """
    Get a file and render the content of the template_file_name with kwargs in a file
    :param file: A File Stream to write
    :param template_file_name: path to route with template name
    :param **kwargs: Args to be rendered in template
    """
    template_file_content = "".join(
        codecs.open(
            template_file_name,
            encoding='UTF-8'
        ).readlines()
    )
    template_rendered = string.Template(template_file_content).safe_substitute(**kwargs)
    file.write(template_rendered)


def create_or_open(file_name, initial_template_file_name, args):
    """
    Creates a file or open the file with file_name name
    :param file_name: String with a filename
    :param initial_template_file_name: String with path to initial template
    :param args: from console to determine path to save the files
    """
    file = None
    if not os.path.isfile(
        os.path.join(
            args['django_application_folder'],
            file_name
        )
    ):
        # If file_name does not exists, create
        file = codecs.open(
            os.path.join(
                args['django_application_folder'],
                file_name
            ),
            'w+',
            encoding='UTF-8'
        )
        print("Creating {}".format(file_name))
        if initial_template_file_name:
            render_template_with_args_in_file(file, initial_template_file_name, **{})
    else:
        # If file exists, just load the file
        file = codecs.open(
                os.path.join(args['django_application_folder'], 
                file_name
            ),
            'a+',
            encoding='UTF-8'
        )

    return file


def generic_insert_module(module_name, args, **kwargs):
    """
    In general we have a initial template and then insert new data, so we dont repeat the schema for each module
    :param module_name: String with module name
    :paran **kwargs: Args to be rendered in template
    """
    file = create_or_open(
        '{}.py'.format(module_name), 
        os.path.join(
            BASE_TEMPLATES_DIR, 
            '{}_initial.py.tmpl'.format(module_name)
        ), 
        args
    )
        
    render_template_with_args_in_file(
        file, 
        os.path.join(
            BASE_TEMPLATES_DIR, 
            '{}.py.tmpl'.format(module_name)
        ), 
        **kwargs
        )
    file.close()


def sanity_check(args):
    """
    Verify if the work folder is a django app.
    A valid django app always must have a models.py file
    :return: None
    """
    if not os.path.isfile(
        os.path.join(
            args['django_application_folder'],
            'models.py'
        )
    ):
        print("django_application_folder is not a Django application folder")
        sys.exit(1)


def generic_insert_with_folder(folder_name, file_name, template_name, args):
    """
    In general if we need to put a file on a folder, we use this method
    """
    # First we make sure views are a package instead a file
    if not os.path.isdir(
        os.path.join(
            args['django_application_folder'],
            folder_name
        )
    ):
        os.mkdir(os.path.join(args['django_application_folder'], folder_name))
        codecs.open(
            os.path.join(
                args['django_application_folder'],
                folder_name,
                '__init__.py'
            ),
            'w+'
        )

    view_file = create_or_open(
        os.path.join(
            folder_name,
            '{}.py'.format(file_name)
        ), 
        '', 
        args
    )
    # Load content from template
    render_template_with_args_in_file(
        view_file, 
        os.path.join(
            BASE_TEMPLATES_DIR, 
            template_name
        ),
        model_name=args['model_name'],
        model_prefix=args['model_prefix'],
        model_name_lower=args['model_name'].lower(),
        application_name=args['django_application_folder'].split("/")[-1]
    )
    view_file.close()


def api(args):
    pass

def execute_from_command_line():
    parser = argparse.ArgumentParser(
        "Create a simple CRUD Structure based contraslash django application "
        "structure"
    )

    parser.add_argument(
        '--django_application_folder',
        default="."
    )

    parser.add_argument(
        '--model_name',
        type=str,
        help="Name of model for make the crud",
        required=True
    )

    parser.add_argument(
        '--model_prefix',
        type=str,
        help="Prefix name for conf variable"
    )

    parser.add_argument('--url_pattern', type=str, help="Pattern for url")

    parser.add_argument('--create_api', action='store_true', help="Create a api using Django Rest Framework")

    parser.add_argument('--add_mixins', action='store_true', help="Add mixins to manage nested urls")

    parser.add_argument('--slug', action='store_true', help="Use slug instad pk on urls")
    
    args = vars(parser.parse_args())    
    
    # If model prefix is not defined, we'll going to define model_prefix as
    # model_name in uppercase
    if args['model_prefix'] is None:
        args['model_prefix'] = args['model_name'].upper()

    if args['url_pattern'] is None:
        args['url_pattern'] = args['model_name'].lower()

    if args['django_application_folder'].endswith("/"):
        args['django_application_folder'] = args[
            'django_application_folder'
        ][:-1]

    sanity_check(args)

    # Views has an specific logic, so we don't touch it
    simplified_file_name = convert(args['model_name'].strip())

    generic_insert_with_folder("views", simplified_file_name, "view.py.tmpl", args)
    # Seems like tests also has the same logic
    generic_insert_with_folder("tests", "test_{}".format(simplified_file_name), "tests.py.tmpl", args)

    modules_to_inject = [
        'conf',
        'forms'
    ]

    if args['slug']:
        modules_to_inject.append('urls_slug')
    else:
        modules_to_inject.append('urls')
    
    if args['create_api']:
        modules_to_inject += [
            'serializers',
            'viewsets',
            'urls_api'
        ]

    # If mixins flag is present, we add mixins to the `modules to inject`
    if args['add_mixins']:
        modules_to_inject.append('mixins')

    for module in modules_to_inject:
        generic_insert_module(
            module, 
            args,
            model_name=args['model_name'],
            model_prefix=args['model_prefix'],
            url_pattern=args['url_pattern'],
            view_file=simplified_file_name,
            model_name_lower=args['model_name'].lower()
        )

    # This is just a fix to link api_urls with urls
    if args['create_api']:
        render_template_with_args_in_file(
            create_or_open(
                os.path.join(
                    BASE_TEMPLATES_DIR, 
                    'urls.py'
                ), 
                "", 
                args
            ), 
            os.path.join(
                BASE_TEMPLATES_DIR, 
                "urls_api_urls_patch.py.tmpl"
            )
        )
    


if __name__ == '__main__':
    execute_from_command_line()
