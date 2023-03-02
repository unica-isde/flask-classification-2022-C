from app import app
from flask import request
import json
import os
from config import Configuration

config = Configuration()


@app.route('/remove_image', methods=['POST'])
def remove_image():
    """Remove an image from the list of images"""
    image_id = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json_body = request.json
        image_id = json_body.get('image_id')
        # remove the image from the file system
        if image_id:
            os.remove(os.path.join(config.image_folder_path, image_id.replace('/', '')))
            return json.dumps({'success': True, 'image_id': str(image_id)}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False, 'image_id': str(image_id)}), 400, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False, 'image_id': str(image_id)}), 400, {'ContentType': 'application/json'}
