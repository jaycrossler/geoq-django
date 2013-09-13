

class UserPermsMiddleware(object):

    def process_request(self, request):
    	"""
    	Populates user permissions.
    	"""
        request.base_perms = request.user.get_all_permissions()
        return None
