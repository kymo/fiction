import sae
from xs7 import wsgi
from sae.ext.shell import ShellMiddleware
application = sae.create_wsgi_app(ShellMiddleware(wsgi.application))
