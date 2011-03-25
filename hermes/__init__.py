from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from hermes.resources import Root
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from hermes.model import initialize_sql
from sqlalchemy import engine_from_config
import logging 

log = logging.getLogger(__name__)

def addslash(context, request):
    return HTTPMovedPermanently(location=request.path_info+'/')

class AuthenticationPolicy(object):
    def authenticated_userid(self,request):
        if  not 'username' in request.session:
            return None
        return request.session['username']
    def effective_principals(self, request):
        if not 'username' in request.session:
            return []
        return [request.session['username']]+request.session['principals']+[Everyone, Authenticated]
    def remember(self, request, principal, **kw):
        pass
    def forget(self, request):
        pass

authentication_policy = AuthenticationPolicy()
authorization_policy = ACLAuthorizationPolicy()

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings, authorization_policy=authorization_policy, authentication_policy=authentication_policy)
    config.set_session_factory(session_factory_from_settings(settings))
    config.add_route('announce', '/{passkey}/announce')
    config.add_route('addtorrent', '/addtorrent')
    config.add_route('signup', '/signup')
    config.add_static_view('static', 'hermes:static')
    config.scan('hermes.views')
    config.scan('hermes.model')
    engine = engine_from_config(settings, 'sqlalchemy.')
    log.error(engine)
    initialize_sql(engine)
    return config.make_wsgi_app()

