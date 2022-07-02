import pytest
from website import website

def setup():
    print("HELLO")

def test_main_page():
    response = website.test_client().get('/')
    assert response.status_code == 200
    print("Main page is accessable!")
