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

"""Json encoding and decoding"""

from flask import url_for, jsonify, json


def write_json(tags, path='/home/cern/.virtualenvs/it/src/invenio/invenio/modules/imagetagger/static/json/imagetagger/json.txt'):
	response = {}
	# for ind in range(len(tags)):
	# 	if first:
	# 		first = False
	# 	else:
	# 		json_str += ', '
	# 	tag = tags[ind]

	# 	new_tag = {}
	# 	new_tag["id"] = str(ind)
	# 	new_tag["title"] = tag[0]
	# 	new_tag["x"] = tag[1]
	# 	new_tag["y"] = tag[2]
	# 	new_tag["w"] = tag[3]
	# 	new_tag["h"] = tag[4]
	# 	new_tag["type"] = tag[5]
	# 	#new_tag = {"id":str(ind), "title":tag[0], "position_size":{"x":tag[1], "y":tag[2], "w":tag[2], "h":tag[3]}}
	# 	response.append([ind,new_tag])
	for tag in tags:
		#response.append([tag.id, tag.to_json()])
		response[str(tag.id)] = tag.to_json()
	print response
	response2 = {}
	response2['tags'] = response
	print response2
	result = jsonify([[0, response2]])
	# print response
	# result = jsonify(response)
	# print result
	json_file = open(path, "w")
	json_file.write(result.data)
	json_file.close()
	return result

def to_json(record_id, tags_array):
	for tag in tags:
		response.append(tag.to_json())
	json['record_id'] = record_id
	json['tags'] = response
	return jsonify(json)

def get_json(id_record):
	pass

def read_json(path='/home/cern/.virtualenvs/invenionext/src/invenio/invenio/modules/imagetagger/static/json.txt'):
	try:
		json_file = open(path, 'r')
	except IOError:
		print "oups"
	strj = json.loads(json_file.read())
	return strj

def json_exists(path='/home/cern/.virtualenvs/invenionext/src/invenio/invenio/modules/imagetagger/static/json.txt'):
	try:
		open(path)
	except IOError:
		return False
	return True


def json_to_array(tags, image_width=0):
	print '----------------tags-------------------'
	print tags
	result = []
	for ind in tags['tags'].keys():
		if image_width == 0:
			result.append([ind, tags['tags'][ind]['title'], tags['tags'][ind]['x'], tags['tags'][ind]['y'], tags['tags'][ind]['w'], tags['tags'][ind]['h'], int(tags['tags'][ind]['h'])+5, tags['tags'][ind]['type']])
		else:
			pass
	return result
