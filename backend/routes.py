from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        abort(404)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if not request.json or 'id' not in request.json or 'pic_url' not in request.json:
        abort(400)
    
    picture = {
        'id': request.json['id'],
        'pic_url': request.json['pic_url'],
        'event_country': request.json.get('event_country', ""),
        'event_state': request.json.get('event_state', ""),
        'event_city': request.json.get('event_city', ""),
        'event_date': request.json.get('event_date', "")
    }
    
    # Check if picture with the id already exists
    existing_pic = next((item for item in data if item["id"] == picture['id']), None)
    if existing_pic:
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302
    
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic = next((item for item in data if item["id"] == id), None)
    
    # If picture doesn't exist, return 404
    if pic is None:
        return jsonify({"message": "picture not found"}), 404

    # Ensure request has JSON data
    if not request.json:
        abort(400)

    # Update the picture data
    pic['pic_url'] = request.json.get('pic_url', pic['pic_url'])
    pic['event_country'] = request.json.get('event_country', pic['event_country'])
    pic['event_state'] = request.json.get('event_state', pic['event_state'])
    pic['event_city'] = request.json.get('event_city', pic['event_city'])
    pic['event_date'] = request.json.get('event_date', pic['event_date'])

    return jsonify(pic), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data  # Use the global variable if the data list is declared globally

    # Find the picture by id
    pic = next((item for item in data if item["id"] == id), None)

    # If picture doesn't exist, return 404
    if pic is None:
        return jsonify({"message": "picture not found"}), 404

    # Delete the picture from the data list
    data.remove(pic)

    # Return no content (204 status code)
    return '', 204
