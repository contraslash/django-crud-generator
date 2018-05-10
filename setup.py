import codecs
from setuptools import setup

def readme():
    with codecs.open('README.md') as f:
        return f.read()

setup(
    name='django_crud_generator',
    version='0.1',
    description='A simple scaffolding for django applications',
    long_description=readme(),
    url='http://github.com/contraslash/django-crud-generator',
    keywords='django scaffolding tool',
    author='contraslash S.A.S.',
    author_email='ma0@contraslash.com',
    license='MIT',
    packages=['django_crud_generator'],
    scripts=['django_crud_generator/bin/django-crud-generator.py'],
    zip_safe=False,
    include_package_data=True
)
 