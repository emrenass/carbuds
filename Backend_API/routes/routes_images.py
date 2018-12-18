import os
import sys

import jwt
from flask import request, make_response, render_template, Blueprint, jsonify, redirect
from flask import current_app as app
from werkzeug.utils import secure_filename

from Backend_API.utils.decorators import login_required
from Backend_API.database.database_interface import *

route_images = Blueprint('route_images', __name__)


@route_images.route('/get_user_image', methods=['GET'])
def get_user_image():
    user_id = request.args["user_image_id"]
    static = app.config['STATIC_FILE'] + "/"
    if (os.path.isdir(static + user_id)):
        image = os.listdir(static + user_id)
        return app.send_static_file("{0}/{1}".format(user_id, image[0]))
    else:
        return app.send_static_file("default/default_profile_image.jpg")


@route_images.route('/upload_user_image', methods=['POST'])
def upload_user_image():
    user_id = request.form["user_image_id"]
    file = request.files['pic']
    static = app.config['STATIC_FILE'] + "/"

    if (os.path.isdir(static + user_id)):
        image = os.listdir(static + user_id)
        try:
            if len(image)>0:
                os.remove(os.path.join(static + user_id, image[0]))
            filename = secure_filename(file.filename)
            file.save(os.path.join(static + user_id, filename))
            return jsonify(True)
        except Exception as e:
            return jsonify(False)
    else:
        try:
            os.makedirs(static+user_id)
            filename = secure_filename(file.filename)
            file.save(os.path.join(static + user_id, filename))
            return jsonify(True)
        except Exception as e:
            return jsonify(False)

