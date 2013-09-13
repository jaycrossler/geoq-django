====
TODO
====

General improvements:

* Improve/Add CRUD views for: Maps, Layers, Features, FeatureTypes

Specific tasks:

* The "work AOI" view currently pulls in all geometry for a job.  The application should have a view that can receive the
  bounds of the map and only returns features in that bounds.
* Front-end is a buggy on batch create aois page.
	- Not sure if this is user error or if the page is buggy. I tried to randomly add features to the interface, and the features did not save when I hit 'save'.
	- Also, in the process of adding features, I added a piece of the national grid. I am not sure if this is supposed to be feature or not. I wasn't able to recreate. If this is a feature, then we need to make this more clear. If this isn't a feature, then we need remove whatever caused that to pop up in the front-end.
	Comments refer to this page type: /geoq/jobs/<pk>/batch-create-aois
	Sample url (after initial data load): http://localhost:8000/geoq/jobs/3/batch-create-aois


* Standardize JSON view responses (status, error, data) or move to a framework like Djangorest framework.

* The related inline form to add and edit layers on a map does not work.  I started working on view for the processing
  but haven't completed it. (maps.views.CreateMapView).

* Add permissions.
  - Users should be able to see all public projects and projects that they are members of.
  - Users should not be able to edit geometry on AOIs that they are not assigned to.
  - Users should only be able to edit geometry if they created the geometry, or if they are a reviewer of the job.

* FeatureType CRUD views should use javascript to help the user create valid JSON for the feature properties/style.


* Make django reversion accessible from the front-end.
	It is currently accessible in the django admin. I held off on exposing this until I understand the workflow better.

* On the dashboard, there is a list for "view all" AOIs. Currently there is no AOIs directory page. Should there be a AOIs directory page?

* Add Changelog for open source version. ... CHANGELOG.md? Automate w/ log?