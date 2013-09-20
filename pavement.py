import os
import sys

from paver.easy import *
from paver.setuputils import setup

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

setup(
    name="geoq",
    packages=['geoq'],
    version='0.0.0.1',
    url="",
    author="Site Admin",
    author_email="admin@localhost"
)


@task
def install_dependencies():
    """ Installs dependencies."""
    sh('pip install --upgrade -r geoq/requirements.txt')


@cmdopts([
    ('fixture=', 'f', 'Fixture to install"'),
])
@task
def install_fixture(options):
    """ Loads the supplied fixture """
    fixture = options.get('fixture')
    sh("python manage.py loaddata {fixture}".format(fixture=fixture))


@task
def install_dev_fixtures():
    """ Installs development fixtures in the correct order """
    fixtures = [
        'geoq/fixtures/initial_data.json',  # Users and site-wide data
        'geoq/core/fixtures/initial_data.json',  # Core
        'geoq/maps/fixtures/initial_data.json',  # Maps
        ]

    for fixture in fixtures:
        sh("python manage.py loaddata {fixture}".format(fixture=fixture))


@task
def sync():
    """ Runs the syncdb process with migrations """
    sh("python manage.py syncdb --noinput")
    sh("python manage.py migrate --all")


@cmdopts([
    ('bind=', 'b', 'Bind server to provided IP address and port number.'),
])
@task
def start_django(options):
    """ Starts the Django application. """
    bind = options.get('bind', '')
    sh('python manage.py runserver %s &' % bind)


@needs(['sync',
        'start_django'])
def start():
    """ Syncs the database and then starts the development server. """
    info("GeoQ is now available.")


@cmdopts([
    ('template=', 'T', 'Database template to use when creating new database, defaults to "template_postgis"'),
])
@task
def createdb(options):
    """ Creates the database in postgres. """
    from geoq import settings
    template = options.get('template', 'template_postgis')
    database = settings.DATABASES.get('default').get('NAME')
    sh('createdb {database}'.format(database=database, template=template))
    sh('echo "CREATE EXTENSION postgis;CREATE EXTENSION postgis_topology" | psql -d  {database}'.format(database=database))


@task
def create_db_user():
    """ Creates the database in postgres. """
    from geoq import settings
    database = settings.DATABASES.get('default').get('NAME')
    user = settings.DATABASES.get('default').get('USER')
    password = settings.DATABASES.get('default').get('PASSWORD')

    sh('psql -d {database} -c {sql}'.format(database=database,
                                            sql='"CREATE USER {user} WITH PASSWORD \'{password}\';"'.format(user=user,
                                                                                                            password=password)))
