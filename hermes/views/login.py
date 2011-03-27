from pyramid.view import view_config
from wtforms import Form, PasswordField,TextField, validators
from pyramid.httpexceptions import HTTPFound
from hermes.model import DBSession
from hermes.model.db import User

import hashlib

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    
@view_config(route_name='login', renderer='/login.mako')
def login(context, request):
    if request.method == "POST":
        form = LoginForm(request.params)
        if form.validate():
            username = form.username.data
            password = form.password.data
            
            u = DBSession.query(User).filter_by(username = username).filter_by(password=hashlib.sha1(password).hexdigest()).first()
            if u:
                request.session['username'] = username
                request.session['principals'] = [a.principal_name for a in u.principals]
                request.session.save()
                return HTTPFound(location='/')
            else:
                return {'form': form, 'error': 'Username or password incorrect'}
            
        else:
            return {'form': form, 'error': None}
    else:
        return {'form': LoginForm(), 'error': None}
