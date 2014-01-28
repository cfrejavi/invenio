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
    invenio.modules.imagetagger.imagetag
    ------------------------------

    Tag class.
"""

class imagetag:
	def __init__(self, tag_id=0, tag_type=0, title=0, x=0, y=0, w=0, h=0, image_width=0, array=[]):
		if len(array) > 0:
			self.id = tag_id
			self.title = array[0]
			self.x = array[1]
			self.y = array[2]
			self.w = array[3]
			self.h = array[4]
			self.type = array[5]
			self.image_width = array[6]
		else:
			self.id = tag_id
			self.type = tag_type
			self.title = title
			self.x = x
			self.y = y
			self.w = w
			self.h = h
			self.image_width = image_width

	def to_array(self, image_width=0):
		factor =1
		if image_width != 0 and image_width != self.image_width:
			factor = float(image_width)/float(self.image_width)
		return [self.id, self.title, self.x, self.y, self.w, self.h, self.h+5, self.type]

	def to_json(self):
		return {'id':self.id, 'title':self.title, 'x':self.x, 'y':self.y, 'w':self.w, 'h':self.h, 'type':self.type, 'image_width':self.image_width}

