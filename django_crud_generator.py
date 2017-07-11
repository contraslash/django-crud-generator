import argparse
import os
import sys
import codecs
import string

from pprint import pprint


def sanity_check():
    if not os.path.isfile(os.path.join(args['django_application_folder'], 'models.py')):
        print("django_application_folder is not a Django application folder")
        sys.exit(1)


def conf(args):
    print(os.path.join(args['django_application_folder'], 'conf.py'))
    if not os.path.isfile(os.path.join(args['django_application_folder'], 'conf.py')):
        conf_file = codecs.open(os.path.join(args['django_application_folder'], 'conf.py'), 'w+', encoding='UTF-8')
        print("Creating conf.py")
        conf_file.write("from base import conf\n")
    else:
        conf_file = codecs.open(os.path.join(args['django_application_folder'], 'conf.py'), 'r+', encoding='UTF-8')
        print("".join(conf_file.readlines()))

    conf_template = "".join(codecs.open('conf.py.tmpl', encoding='UTF-8').readlines())
    template_rendered = string.Template(conf_template).safe_substitute(model_prefix=args['model_prefix'])
    print(template_rendered)

    conf_file.write(template_rendered)
    conf_file.close()


def views(args):
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create a simple CRUD Structure based contraslash django application structure")

    parser.add_argument('--django_application_folder', default=".")

    parser.add_argument('--model_name', type=str, help="Name of model for make the crud", required=True)

    parser.add_argument('--model_prefix', type=str, help="Prefix name for conf variable")

    args = vars(parser.parse_args())

    if args['model_prefix'] is None:
        args['model_prefix'] = args['model_name'].upper()

    pprint(args)

    sanity_check()

    conf(args)

    views(args)




