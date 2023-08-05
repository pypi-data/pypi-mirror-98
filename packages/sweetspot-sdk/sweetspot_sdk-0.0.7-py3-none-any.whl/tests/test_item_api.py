import pytest

from multiprocessing import Process
from flask import request
from .endpoints import TestGeneralApiEndpoints, TestSpecificApiEndpoints
from sweetspot.client import Client

@pytest.fixture(scope='module')
def server(app):
    app.add_url_rule('/api/item', view_func=TestGeneralApiEndpoints.as_view('general'))
    app.add_url_rule('/api/item/<uuid:id>', view_func=TestSpecificApiEndpoints.as_view('specific'))

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

