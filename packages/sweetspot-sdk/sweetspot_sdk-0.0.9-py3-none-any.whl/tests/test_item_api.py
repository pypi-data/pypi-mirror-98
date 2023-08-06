import pytest
import os 
import requests

from multiprocessing import Process
from flask import request, make_response
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from .endpoints import TestGeneralApiEndpoints, TestSpecificApiEndpoints
from sweetspot.client import Client

@pytest.fixture(scope='module')
def server(app):

    class ItemPictureUpload(MethodView):

        @jwt_required()
        def post(self, id):
            if not 'image' in request.files: 
                resp = make_response({'success':False}, 400)
            image = request.files.get('image')
            data = {'success':True}
            resp = make_response(data, 201)
            return resp

    app.add_url_rule('/api/item', view_func=TestGeneralApiEndpoints.as_view('general'))
    app.add_url_rule('/api/item/<uuid:id>', view_func=TestSpecificApiEndpoints.as_view('specific'))
    app.add_url_rule('/api/item/picture/<uuid:id>', view_func=ItemPictureUpload.as_view('upload'))

    server = Process(target=app.run)
    
    yield server.start()

    server.terminate()
    server.join()

def test_get_all_items(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.item.get_all_items()
    assert result.is_success() == True 

def test_add_item(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.item.add_item(payload)
    assert result.is_success() == True 

def test_get_item(server, sample_uuid):
    client = Client(environment='test')
    result = client.item.get_item(sample_uuid)
    assert result.is_success() == True 

def test_update_item(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.item.update_item(sample_uuid, payload)
    assert result.is_success() == True 

def test_replace_item(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.item.replace_item(sample_uuid, payload)
    assert result.is_success() == True 

def test_delete_item(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.item.delete_item(sample_uuid)
    assert result.is_success() == True

def test_upload_picture(server, sample_cookie_resp, sample_uuid):
    """
    headers = {
    'accept': 'application/json',
    'X-CSRF-TOKEN': sample_cookie_resp.get('csrf_access_token'),
    'Content-Type': 'multipart/form-data',
    }
    cookies = {'access_token_cookie': sample_cookie_resp.get('access_token_cookie')}
    files = {
        'image': ('no-photo-available.png', open(os.getcwd() + '/tests/static/no-photo-available.png', 'rb')),
    }

    response = requests.post('http://localhost:5000/api/item/picture/4c293a54-ff44-42d9-aca0-bc0e379af258', headers=headers, files=files, cookies=cookies)
    assert response.text == 'hello'
    """
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    image = open(os.getcwd() + '/tests/static/no-photo-available.png', 'rb')
    result = client.item.upload_picture(sample_uuid, ('no-photo-available.png', image))
    assert result.is_success() == True 
    


