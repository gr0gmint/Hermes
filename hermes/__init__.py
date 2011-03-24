from pyramid.config import Configurator
from hermes.resources import Root
from hermes.model import initialize_sql


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_route('announce', '/{passkey}/announce')
    config.add_route('scrape', '/{passkey}/scrape')
    config.add_route()
    config.scan('hermes:model')
    config.scan('hermes:views')
    initialize_sql(settings)
    config.add_static_view('static', 'hermes:static')
    return config.make_wsgi_app()

