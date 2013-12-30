# GeoQ

#### Geographic Work Queueing and Tasking System ####

The aim of this project is to create an open-source Geographic tasking system that allows teams to collect geographic data across a large area, but manage the work in smaller geographic chunks. Large areas can be quickly broken up into small 1km square chunks and assigned to be worked by a team that has insight into what each other are doing.

GeoQ was originally developed in Ruby on Rails and is being converted to work with [Django](https://www.djangoproject.com/)/Python and a [PostgreSQL](http://www.postgresql.org/)/[PostGIS](http://postgis.net/). This project is for the Django build, which is intended to be fully opened and contributed to from all interested members of the geospatial community. It will be heavily influenced from existing lessons learned -- anyone who would like to change development priorities is welcome to Fork the library. Please submit any proposed fixes or improvements through a Github Pull Request.

### GeoQ Configuration ###

The ``geoq/settings.py`` file contains installation-specific settings. The Database name/pw and server URLs will need to be configured here.


### GeoQ Installation ###

Mac OSX Development Build Instructions::

1. Install PostGIS 2.0 using instructions at [https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#macosx](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#macosx). There are several options there, but for most, the easiest option is to follow the Homebrew instructions. If you don't have Homebrew installed, follow the (one line) instruction at [http://brew.sh](http://brew.sh).

	One exception: Instead of using brew to install postgres, it's usually easier to install Postgres.app from [postgresapp.com](http://postgresapp.com). After installing, add the app's bin directory (``/Applications/Postgres.app/Contents/MacOS/bin``) to your PATH.

2. (Optional) Install a Geoserver (we recommend the OGC Geoserver at [https://github.com/geoserver](https://github.com/geoserver))

3. Make sure Python, Virtualenv, and Git are installed

4. Install and setup geoq-django:

        % mkdir -p ~/pyenv
        % virtualenv --no-site-packages ~/pyenv/geoq
        % source ~/pyenv/geoq/bin/activate
        % git clone https://github.com/jaycrossler/geoq-django

5. Create the database and sync dependencies and data

        % cd geoq-django
        % pip install paver
        % paver install_dependencies
        % paver createdb
        % paver create_db_user
        % paver sync

6. (Optional) Load development fixtures:

        % paver install_dev_fixtures # creates an admin/admin superuser

7. Build user accounts:

        % python manage.py createsuperuser

8. Install less and add its folder ("type -p less") to your bash profile:

        % npm install -g less

9. Start it up!

        % paver start_django


### License ###
See LICENSE.txt


### TODOs ###
Current next development goals are tracked as Issues within GitHub, and high-level goals are in ```geoq/TODO.rst```.
