# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
    invenio.modules.tags.blueprint
    ------------------------------

    Tagging interface.
"""

# Flask
from werkzeug import LocalProxy
from flask import render_template, request, flash, redirect, url_for, \
    jsonify, Blueprint
from invenio.base.i18n import _
from invenio.base.decorators import wash_arguments, templated
from flask.ext.login import current_user, login_required
from invenio.base.globals import cfg
from sqlalchemy.exc import SQLAlchemyError

# External imports
#from invenio.ext.menu import register_menu
#from invenio.ext.breadcrumb import default_breadcrumb_root, register_breadcrumb
#from invenio.ext.sqlalchemy import db

# Internal imports
#from .models import YourModel

blueprint = Blueprint('imagetagger', __name__, url_prefix='/imagetagger',
                      template_folder='templates', static_folder='static')

#default_breadcrumb_root(blueprint, '.imagetagger')

@blueprint.route('/')
def index():
    return 'Hello World'