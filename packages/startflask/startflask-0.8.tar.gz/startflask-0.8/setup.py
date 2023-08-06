from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='startflask',
    author='Sashito Mizuki',
    author_email='sashito.mizuki@gmail.com',
    version='0.8',
    packages=['startflask'],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords=['Flask','startflask','flask start'],
    install_requires=[
        'Click',
        'Flask',
        'Flask-Migrate',
        'Flask-Login',
        'Flask-SQLAlchemy',
        'psycopg2-binary',
        'gunicorn'
    ],
    entry_points='''
        [console_scripts]
        startflask=startflask.startflask:create
    ''',
)
