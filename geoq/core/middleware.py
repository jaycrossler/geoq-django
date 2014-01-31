# -*- coding: utf-8 -*-

class UserPermsMiddleware(object):

	def process_request(self, request):

		"""
		Populates user permissions to use in the templates.
		"""
		user = request.user
		perms = []

		perms = list(user.get_all_permissions()) + perms
		request.base_perms = set(perms)
		logging.info(request.base_perms)

		return None
