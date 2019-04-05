import codecs
from setuptools import setup


def readme():
    with codecs.open('README.md') as f:
        return f.read()

setup(
    name='django_crud_generator',
    version='0.3.6',
    description='A simple scaffolding for django applications',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='http://github.com/contraslash/django-crud-generator',
    keywords='django scaffolding tool',
    author='contraslash S.A.S.',
    author_email='ma0@contraslash.com',
    classifiers=[ 
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    packages=['django_crud_generator'],
    scripts=['django_crud_generator/bin/django-crud-generator.py'],
    zip_safe=False,
    include_package_data=True,
    project_urls={  
        'Bug Reports': 'https://github.com/contraslash/django-crud-generator/issues',
        'Source': 'https://github.com/contraslash/django-crud-generator',
        'Contraslash': 'https://contraslash.com/'
    },
)
