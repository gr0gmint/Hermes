from pyramid.security import Allow, Authenticated, Deny, Everyone, ALL_PERMISSIONS, DENY_ALL

class Root(object):
    def __init__(self, request):
        self.request = request
        
class Protected(dict):
    __acl__ = [
        (Allow, Authenticated, 'view'),
        DENY_ALL
              ]
    def __init__(self, request):
        self.request = request
        
class Admin(dict):
    __acl__ = [
        (Allow, 'group:admin', 'view'),
        DENY_ALL
            ]
    def __init__(self, request):
        self.request = request
