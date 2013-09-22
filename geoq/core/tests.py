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

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from geoq.core.models import Project

class CoreTest(TestCase):
    # TODO test requests to all views

    fixtures = ['core/initial_data.json']
    def setUp(self):

        self.get_views = [
                           'home',
                           'project-list',
                           'project-create',
                           'job-list',
                           'job-create',
                           'aoi-create',
                          ]

        self.admin, created = User.objects.get_or_create(username='admin', password='admin', is_superuser=True)

    def test_get_requests(self):
        """
        Makes a get request to views and ensures the view returns a 200.
        """
        c = Client()
        for view in self.get_views:
            response = c.get(reverse(view))
            self.assertEqual(200, response.status_code, "Problem with GET request to {0}".format(view))

    def test_usng_proxy(self):
        """
        Tests the USNG proxy.

        Given a comma seperated bbox (-77.6348876953125,37.81846319511331,-77.5360107421875,37.87051721701939) the
        service should USNG grids as GeoJSON.
        """

        pass


    def test_change_aoi_status(self):
        """
        Tests the ChangeAOIStatus View.

        Given an AOI id and a status, update the AOI's status attribute to the new status if user is allowed to update
        the AOI.  View should return JSON of the updated value.
        """

        pass

    def test_job_detailed_list_view(self):
        """
        Tests the JobDetailedList View.

        Given a job object return the job and related aois filtered by an optional status.  Error should return a
        human readable message with numeric response status both as JSON.

        Context data returned:
        object: The job, return a 404 if it does not exist.
        object_list: A list of aois related to the project.
        statuses: A list of all possible statuses (returned from the AOI model).
        active_status: The currently selected status, as received in a url parameter.
        """

        pass

    def test_detailed_list_view(self):
        """
        Tests the DetailedList View.

        Given a project object return the project and related jobs.  Errors should return a human readable message
        with numeric response status both as JSON.

        Context data returned:
        object: The project, return a 404 if it does not exist.
        object_list: A list of jobs related to the project.
        """

        pass

    def batch_create_views(self):
        """
        Tests the BatchCreateAOIS View.

        Given a job id received via the URL pattern return the job in the appropriate template on GET requests.  POST
        requests should contain the job (supplied via the URL route) and a GeoJSON representation of new AOIs.  The
        view will bulk create new AOIS from GeoJSON and relate them to the job.  Errors should return a human readable message
        with numeric response status both as JSON.

        Context data returned:

        GET:
        object: The job, return a 404 if it does not exist.
        """

        pass


    def dashboard(self):
        """
        Tests the Dashboard View.

        Returns the dashboard.

        Context data returned:

        GET:
        projects: List of projects.
        """

        pass

    def test_create_project_view(self):
        """
        Tests the create project view.
        """

        project = dict(name='Test project.', description="This is a test.", project_type='Fire')

        c = Client()
        c.login(username='admin', password='admin')
        response = c.post(reverse('project-create'), data=project)
        self.assertEqual(response.status_code, 201)

        # Make sure the user that creates the job becomes a supervisor
        proj = Project.objects.filter(name=project.get('name'))
        self.assertTrue(self.admin in proj.supervisors)


