# -*- coding: utf-8 -*-

class UserPermsMiddleware(object):

	def process_request(self, request):

		"""
		Populates user permissions.
		"""
		user = request.user
		perms = []

		perms = list(user.get_all_permissions()) + perms

		#print perms

		request.base_perms = set(perms)

		import logging
		logging.info(request.base_perms)

		return None
