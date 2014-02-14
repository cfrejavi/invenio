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
    invenio.modules.imagetagger.blueprint
    ------------------------------

    Tagging interface.
"""

import os
import numpy as np
import cv2

# Flask
from werkzeug import LocalProxy
from flask import render_template, request, flash, redirect, url_for, \
    jsonify, Blueprint, json, escape
from invenio.base.i18n import _
from invenio.base.decorators import wash_arguments, templated
from flask.ext.login import current_user, login_required
from invenio.base.globals import cfg
from invenio.ext.template import render_template_to_string
from sqlalchemy.exc import SQLAlchemyError
from invenio.ext.sqlalchemy import db
from invenio.modules.record_editor.models import Bibrec
#from invenio.legacy.search_engine import get_record
#from invenio.modules.websearch.lib.search_engine import get_record
# External imports
#from invenio.ext.menu import register_menu
#from invenio.ext.breadcrumb import default_breadcrumb_root, register_breadcrumb
#from invenio.ext.sqlalchemy import db

# Internal imports
from .json_utils import *
from .face_detection import find_faces
from .face_in_collection_similarity import find_faces_in_collection

blueprint = Blueprint('imagetagger', __name__, url_prefix='/imagetagger',
                      template_folder='templates', static_folder='static')
def get_record():
    pass

#default_breadcrumb_root(blueprint, '.imagetagger')

#image_path = '/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static/faces2.jpg'
image_path = 'img/imagetagger/faces2.jpg'
image_test_path2 = 'img/imagetagger/test_test.jpg'
image_model_path = '/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static/img/imagetagger/test_model.jpg'
image_test_path = '/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static/img/imagetagger/test_test.jpg'
json_path = '/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static/json/imagetagger/json.txt'
scaled_width = 800
mask = np.ones((235,165),np.uint8)
face_model_position = [0,'bidule',1280,219,72,83]
face_model_position2 = [0,'machin',434,258,73,78]
face_model_position3 = [0,'trucmuche',1047,248,62,77]
face_model_position4 = [0,'untel',258,264,74,91]
face_model_position5 = [0,'dudule',616,220,60,84]
face_model_position6 = [0,'tartempion',831,202,54,84]

face_model_position7 = [0,'1',112,309,58,66]
face_model_position8 = [0,'2',200,308,55,66]
face_model_position9 = [0,'3',310,300,62,63]
face_model_position10 = [0,'4',436,333,48,56]
face_model_position11 = [0,'5',552,303,48,66]
face_model_position12 = [0,'6',681,331,51,60]
face_model_position13 = [0,'7',792,346,42,60]
face_model_position14 = [0,'8',918,310,57,60]
face_model_position15 = [0,'9',1034,317,55,66]
collection = [face_model_position, face_model_position2, face_model_position3, face_model_position4, face_model_position5, face_model_position6]
collection2 = [face_model_position7, face_model_position8, face_model_position9, face_model_position10, face_model_position11, face_model_position12,face_model_position13,face_model_position14,face_model_position15]
#collection=[face_model_position]

@blueprint.route('/', methods=['GET', 'POST'])
def index():
    from .template_context_functions.tfn_imagetagger_overlay import template_context_function
    if request.method == 'POST':
        nb_tags = request.form["nb_tags"]
        tags = []
        for id_tag in range(int(nb_tags)):
            val = request.form['tag'+str(id_tag)].split(';')
            tags.append(val)
        res = write_json(tags)
        already_tagged = json_to_array(json.loads(res.data))
        potential_tags = find_faces("/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static"+url_for('imagetagger.static', filename=image_path), width=scaled_width, already_tagged=already_tagged)
        return template_context_function(2, image_path,tags=already_tagged, faces=potential_tags)
    else:
        if json_exists(json_path):
            result = read_json(json_path)
            potential_tags = find_faces("/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static"+url_for('imagetagger.static', filename=image_path), width=scaled_width, already_tagged=json_to_array(result))
            return template_context_function(1, image_path, tags=json_to_array(result), faces=potential_tags)
        else:
            potential_tags = find_faces("/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static"+url_for('imagetagger.static', filename=image_path), width=scaled_width)
            return template_context_function(1, image_path, faces=potential_tags)
    
@blueprint.route('/record/<int:id_bibrec>/<int:action>', methods=['GET', 'POST'])
def editor(id_bibrec):
    path = get_record(id_bibrec)['url'][0]['url']
    from .template_context_functions.tfn_imagetagger_overlay import template_context_function
    if request.method == 'POST':
        nb_tags = request.form["nb_tags"]
        tags = []
        for id_tag in range(int(nb_tags)):
            val = request.form['tag'+str(id_tag)].split(';')
            tags.append(val)
        res = write_json(tags,json_path)
        already_tagged = json_to_array(json.loads(res.data))
        potential_tags = find_faces("/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static"+url_for('imagetagger.static', filename=image_path), width=scaled_width, already_tagged=already_tagged)
        save_tags(id_bibrec, json.loads(res.data), action)
        return template_context_function(2, image_path,tags=already_tagged, faces=potential_tags)
    else:
        if json_exists(json_path):
            result = read_json(json_path)
            potential_tags = find_faces("/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static"+url_for('imagetagger.static', filename=image_path), width=scaled_width, already_tagged=json_to_array(result))
            return template_context_function(1, image_path, tags=json_to_array(result), faces=potential_tags)
        else:
            potential_tags = find_faces("/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static"+url_for('imagetagger.static', filename=image_path), width=scaled_width)
            return template_context_function(1, image_path, faces=potential_tags)

@blueprint.route('/record/<int:id_bibrec>/delete', methods=['GET', 'POST'])
def delete(id_bibrec):
    path = get_record(id_bibrec)['url'][0]['url']
    #to do: delete json in db
    os.remove(json_path)

@blueprint.route('/record/<int:id_bibrec>')
def get_tags_for_image(id_bibrec):
    #request the json from the db
    return read_json(json_path)

@blueprint.route('/testsuggestion')
def suggest(current_image=image_model_path, current_tags=collection, image_collection=[image_test_path]):
    from .template_context_functions.tfn_imagetagger_overlay import template_context_function
    proposed_tags = []
    #torso_path = '/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static/torso.jpg'
    torso_path = '/home/cern/Documents/torso1.jpg'
    #cv2.imwrite(torso_path, mask)
    suggested = find_faces_in_collection(current_image, current_tags, image_collection, torso_path, scaled_width)
    #return proposed_tags
    print suggested
    return template_context_function(1, image_test_path2, faces=[], suggested=suggested[image_test_path])

def save_tags(id_bibrec, json_tags, action):
    #record the json file associated to the record id
    pass
