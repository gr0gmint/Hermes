from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
@view_config(route_name='logout')
def logout(context, request):
    request.session.invalidate()
    return HTTPFound(location='/')
