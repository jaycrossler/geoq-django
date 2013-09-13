# GeoQ

#### Geographic Work Queueing and Tasking System ####

The aim of this project is to create an open-source Geographic tasking system that allows teams to collect geographic data across a large area, but manage the work in smaller geographic chunks. Large areas can be quickly broken up into small 1km square chunks and assigned to be worked by a team that has insight into what each other are doing.

GeoQ was originally developed in Ruby on Rails and is being converted to work with [Django](https://www.djangoproject.com/)/Python and a [PostgreSQL](http://www.postgresql.org/)/[PostGIS](http://postgis.net/). This project is for the Django build, which is intended to be fully opened and contributed to from all interested members of the geospatial community. It will be heavily influenced from existing lessons learned -- anyone who would like to change development priorities is welcome to Fork the library. Please submit any proposed fixes or improvements through a Github Pull Request.

### GeoQ Configuration ###

The ``geoq/settings.py`` file contains installation-specific settings. The Database name/pw and server URLs will need to be configured here.


### GeoQ Installation ###

Mac OSX Development Build Instructions::

1. Install PostGIS 2.0 using instructions at https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/
2. Install a Geoserver (we recommend the OGC Geoserver at https://github.com/geoserver)

        % mkdir -p ~/pyenv
        % virtualenv --no-site-packages ~/pyenv/geoq
        % source ~/pyenv/geoq/bin/activate
        % git clone [repo location]
        % cd geoq
        % pip install paver
        % paver install_dependencies
        % paver createdb
        % paver create_db_user
        % paver sync

3. If you would like to load development fixtures:
        % paver install_dev_fixtures # creates an admin/admin superuser

4. Build user accounts
        % python manage.py createsuperuser

5. Install less and add its folder ("type -p less") to your bash profile.
        % npm install -g less

6. Startup
        % paver start_django


### License ###
MIT License

### TODOs ###
Current next development goals are tracked in ```geoq/TODO.rst```.  Additionally, we maintain a non-publicly accessible work tracking site for bugs and feature requests. If there is enough community interest, this might be ported to Github.
