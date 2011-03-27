from pyramid.httpexceptions import HTTPMovedPermanently
from wtforms import Form, TextField, PasswordField, validators
from pyramid.view import view_config
from hermes.model.db import User, Principal
from hermes.model import DBSession
from sqlalchemy.sql.expression import func
import random 
import string
from hermes.lib import get_principal
import re
import logging

log = logging.getLogger(__name__)

class SignupForm(Form):
    username = TextField('Username', [validators.Required(), validators.Length(min=3, max=30)])
    password = PasswordField('Password', [validators.Required()])
    confirm_password = PasswordField('Confirm password', [validators.EqualTo('password', message='Passwords must match')])
    
    def validate_username(form, field):
        log.error("validate_username")
        if not re.match('[a-zA-Z0-9-_]+', field.data):
            raise validators.ValidationError('Username may only contain alpha-numeric characters')
        if DBSession.query(User).filter(func.lower(User.username)==func.lower(field.data)).first():
            raise validators.ValidationError('Username already taken')
    
@view_config(route_name='signup', renderer='/signup.mako')
def signup(context, request):
    if request.method == "POST":
        form = SignupForm(request.params)
        if form.validate():
            u = User(form.username.data, form.password.data)
            u.passkey = "".join([random.choice(string.letters) for x in xrange(16)])
            p = get_principal('group:user')
            u.principals.append(p)
            log.error(form.username.data)
            DBSession.add(u)
            DBSession.commit()
            request.session['flashmessage'] = "Your user has been created! Passkey = "+u.passkey
            request.session.save()
            return HTTPMovedPermanently(location='/')
        else:
            return {'form': form}
    return {'form': SignupForm()}
