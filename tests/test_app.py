import falcon
from falcon import testing
import pytest
from uuid import uuid4
from os import mkdir
# internal imports
from easytasker import app
from db import db_users, query, get_hashed_password, cwd


# always (re)create test user in db_users with password test to ensure, that test will allways pass
test_cookie = str(uuid4())
db_users.upsert({'name': 'test',
                 'password':  get_hashed_password("test"),
                 'cookie_uuid': test_cookie,
                }, query.name == "test")
mkdir(cwd / "files/test")

@pytest.fixture
def client():
    return testing.TestClient(app)


def test_index_without_login(client):
    """Test that index have to redirect to login page withou proper authorization"""
    response = client.simulate_get('/')
    assert response.status == falcon.HTTP_303


def test_index_with_login(client):
    response = client.simulate_get('/', cookies={"user": "test", 'cookie_uuid': test_cookie})
    assert response.status == falcon.HTTP_OK
