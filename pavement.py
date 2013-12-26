# -*- coding: utf-8 -*-

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, as long as
# any reuse or further development of the software attributes the
# National Geospatial-Intelligence Agency (NGA) auhtorship as follows:
# 'This software (GeoQ or Geographic Work Queueing and Tasking System)
# is provided to the public as a courtesy of the National
# Geospatial-Intelligence Agency.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
        'geoq/accounts/fixture/initial_data.json',
        'geoq/maps/fixtures/initial_data_types.json',  # Maps
        'geoq/core/fixture/initial_data.json',
        ]

    for fixture in fixtures:
        sh("python manage.py loaddata {fixture}".format(fixture=fixture))

    sh("python manage.py migrate --all")
    sh("python manage.py check_permissions")  # Check userena perms
    sh("python manage.py clean_expired")  # Clean our expired userena perms


@task
def sync():
    """ Runs the syncdb process with migrations """
    sh("python manage.py syncdb --noinput")
    sh("python manage.py migrate --all --no-initial-data")

@task
def reset_dev_env():
    """ Resets your dev environment from scratch in the current branch you are in. """
    from geoq import settings
    database = settings.DATABASES.get('default').get('NAME')
    sh('dropdb {database}'.format(database=database))
    createdb()
    sync()
    install_dev_fixtures()

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
# Order matters for the list of apps, otherwise migrations reset may fail.
_APPS = ['maps', 'accounts', 'badges', 'core']

@task
def reset_migrations():
    """
        Takes an existing environment and updates it after a full migration reset.
    """
    for app in _APPS:
        sh('python manage.py migrate %s 0001 --fake  --delete-ghost-migrations' % app)

@task
def reset_migrations_full():
    """
        Resets south to start with a clean setup.
        This task will process a default list: accounts, core, maps, badges
        To run a full reset which removes all migraitons in repo -- run paver reset_south full

    """
    for app in _APPS:
        sh('rm -rf geoq/%s/migrations/' % app)
        sh('python manage.py schemamigration %s --initial' % app)

    # Finally, we execute the last setup.
    reset_migrations()

