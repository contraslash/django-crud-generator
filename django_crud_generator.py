import argparse
import os
import sys
import codecs
import string


def sanity_check():
    """
    Verify if the work folder is a django app.
    A valid django app always must have a models.py file
    :return: None
    """
    if not os.path.isfile(os.path.join(args['django_application_folder'], 'models.py')):
        print("django_application_folder is not a Django application folder")
        sys.exit(1)


def conf(args):
    """
    Create or modify the conf.py file
    :param args: command line args
    :return: 
    """

    if not os.path.isfile(os.path.join(args['django_application_folder'], 'conf.py')):
        # If conf.py does not exists, create
        conf_file = codecs.open(os.path.join(args['django_application_folder'], 'conf.py'), 'w+', encoding='UTF-8')
        print("Creating conf.py")
        conf_file.write("from base import conf\n")
    else:
        # If file exists, just load the file
        conf_file = codecs.open(os.path.join(args['django_application_folder'], 'conf.py'), 'a+', encoding='UTF-8')

    # Load content from template
    conf_template = "".join(codecs.open('conf.py.tmpl', encoding='UTF-8').readlines())
    template_rendered = string.Template(conf_template).safe_substitute(model_prefix=args['model_prefix'])

    # Put content on file
    conf_file.write(template_rendered)
    conf_file.close()


def views(args):
    """
    Create the view file    
    :param args: command line args 
    :return: 
    """
    if not os.path.isdir(os.path.join(args['django_application_folder'], 'views')):
        os.mkdir(os.path.join(args['django_application_folder'], 'views'))
        codecs.open(os.path.join(args['django_application_folder'], 'views', '__init__.py'), 'w+')

    view_file = codecs.open(
        os.path.join(
            args['django_application_folder'],
            'views',
            '{}.py'.format(args['model_name'].lower())
        ),
        'w+',
        encoding='UTF-8'
    )

    view_template = "".join(codecs.open('view.py.tmpl', encoding='UTF-8').readlines())
    template_rendered = string.Template(view_template).safe_substitute(
        model_name=args['model_name'],
        model_prefix=args['model_prefix']
    )
    view_file.write(template_rendered)
    view_file.close()


def urls(args):
    """
    Create or modify the urls_file 
    :param args: 
    :return: 
    """

    if not os.path.isfile(os.path.join(args['django_application_folder'], 'urls.py')):
        # If conf.py does not exists, create
        urls_file = codecs.open(os.path.join(args['django_application_folder'], 'urls.py'), 'w+', encoding='UTF-8')
        print("Creating urls.py")
        urls_initial_template = "".join(codecs.open('urls_initial.py.tmpl', encoding='UTF-8').readlines())
        urls_file.write(urls_initial_template)
    else:
        # If file exists, just load the file
        urls_file = codecs.open(os.path.join(args['django_application_folder'], 'urls.py'), 'a+', encoding='UTF-8')

    # Load content from template
    urls_template = "".join(codecs.open('urls.py.tmpl', encoding='UTF-8').readlines())
    template_rendered = string.Template(urls_template).safe_substitute(
        model_prefix=args['model_prefix'],
        url_pattern=args['url_pattern'],
        view_file=args['model_name'].lower()
    )

    # Put content on file
    urls_file.write(template_rendered)
    urls_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create a simple CRUD Structure based contraslash django application structure")

    parser.add_argument('--django_application_folder', default=".")

    parser.add_argument('--model_name', type=str, help="Name of model for make the crud", required=True)

    parser.add_argument('--model_prefix', type=str, help="Prefix name for conf variable")

    parser.add_argument('--url_pattern', type=str, help="Pattern for url")

    args = vars(parser.parse_args())

    # If model prefix is not defined, we'll going to define model_prefix as model_name in uppercase
    if args['model_prefix'] is None:
        args['model_prefix'] = args['model_name'].upper()

    if args['url_pattern'] is None:
        args['url_pattern'] = args['model_name'].lower()

    sanity_check()

    conf(args)

    views(args)

    urls(args)




